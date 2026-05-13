#!/usr/bin/env node
// Deploy server do CPA.
//
//   POST /github   X-Hub-Signature-256  → webhook do repo GitHub
//   POST /deploy   Bearer AGENT_TOKEN   → trigger manual (streaming)
//   GET  /healthz                       → liveness check
//   GET  /status                        → últimos 10 deploys + estado
//
// Watchdog: a cada 5 min compara HEAD local com origin/main e deploya
// automaticamente se divergir (defesa contra webhook perdido).

const http    = require("http");
const https   = require("https");
const crypto  = require("crypto");
const fs      = require("fs");
const { spawn, execSync } = require("child_process");
const path    = require("path");

const PORT           = parseInt(process.env.PORT || "4243", 10);
const TOKEN          = process.env.AGENT_TOKEN || "";
const WEBHOOK_SECRET = process.env.GITHUB_WEBHOOK_SECRET || "";
const ALERT_URL      = process.env.ALERT_WEBHOOK_URL || "";
const SCRIPT_DIR     = __dirname;
const STATE_FILE     = "/tmp/deploy-state-cpa.json";

if (!TOKEN) { console.error("AGENT_TOKEN não definido."); process.exit(1); }

// ── Estado ────────────────────────────────────────────────────────────────
function loadState() {
  try { return JSON.parse(fs.readFileSync(STATE_FILE, "utf8")); }
  catch { return { lastDeploys: [] }; }
}
function saveState() {
  try { fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2)); }
  catch (e) { console.error("[state]", e.message); }
}
const state = loadState();
function recordDeploy(entry) {
  state.lastDeploys = [entry, ...state.lastDeploys].slice(0, 10);
  saveState();
}

// ── Alerta (Discord/Slack/qualquer webhook JSON) ──────────────────────────
function sendAlert({ code, tail }) {
  if (!ALERT_URL) return;
  try {
    const url  = new URL(ALERT_URL);
    const body = JSON.stringify({
      content: `🚨 CPA deploy falhou (exit ${code})\n\`\`\`\n${(tail || "").slice(-1500)}\n\`\`\``,
    });
    const req = (url.protocol === "https:" ? https : http).request({
      method: "POST", hostname: url.hostname,
      port: url.port || (url.protocol === "https:" ? 443 : 80),
      path: url.pathname + url.search,
      headers: { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(body) },
    }, (r) => r.resume());
    req.on("error", (e) => console.error("[alert]", e.message));
    req.write(body); req.end();
  } catch (e) { console.error("[alert]", e.message); }
}

// ── Fila de deploy ────────────────────────────────────────────────────────
let busy = false;
const queue = [];

function runDeploy(source = "manual") {
  const startedAt = new Date().toISOString();
  console.log(`[${startedAt}] deploy start (source=${source})`);
  const proc = spawn("bash", ["-c",
    `cd ${SCRIPT_DIR} && \
     git fetch origin main && git reset --hard origin/main && \
     git log -1 --oneline && \
     bash ${path.join(SCRIPT_DIR, "deploy.sh")}`
  ], { cwd: SCRIPT_DIR, env: { ...process.env, HOME: process.env.HOME || "/root" } });

  let tail = "";
  const append = (d) => { tail = (tail + d.toString()).slice(-8192); };
  proc.stdout.on("data", (d) => { append(d); process.stdout.write(d); });
  proc.stderr.on("data", (d) => { append(d); process.stderr.write(d); });
  proc.on("close", (code) => {
    let head = null;
    try { head = execSync("git rev-parse HEAD", { cwd: SCRIPT_DIR }).toString().trim(); } catch {}
    recordDeploy({ startedAt, finishedAt: new Date().toISOString(), code, source, head, tail: tail.slice(-4000) });
    console.log(`[${new Date().toISOString()}] deploy exit ${code}`);
    if (code !== 0) sendAlert({ code, tail });
    busy = false;
    const next = queue.shift();
    if (next) { busy = true; runDeploy(next); }
  });
  proc.on("error", (e) => { console.error("[deploy]", e.message); busy = false; });
}

function enqueue(res, source) {
  res.writeHead(202, { "Content-Type": "text/plain" });
  res.end("deploy queued\n");
  if (busy) { queue.push(source); return; }
  busy = true; runDeploy(source);
}

function stream(res) {
  res.writeHead(200, { "Content-Type": "text/plain; charset=utf-8", "Transfer-Encoding": "chunked" });
  const proc = spawn("bash", ["-c",
    `cd ${SCRIPT_DIR} && \
     git fetch origin main && git reset --hard origin/main && \
     git log -1 --oneline && \
     bash ${path.join(SCRIPT_DIR, "deploy.sh")}`
  ], { cwd: SCRIPT_DIR, env: { ...process.env, HOME: process.env.HOME || "/root" } });
  proc.stdout.on("data", (d) => { res.write(d); process.stdout.write(d); });
  proc.stderr.on("data", (d) => { res.write(d); process.stderr.write(d); });
  proc.on("close", (code) => res.end(`\nexit ${code}\n`));
  proc.on("error", (e) => res.end(`spawn error: ${e.message}\n`));
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end",  () => resolve(Buffer.concat(chunks)));
    req.on("error", reject);
  });
}

function timingSafeEqual(a, b) {
  const ab = Buffer.from(a), bb = Buffer.from(b);
  return ab.length === bb.length && crypto.timingSafeEqual(ab, bb);
}

// ── HTTP server ───────────────────────────────────────────────────────────
const server = http.createServer(async (req, res) => {

  // POST /github — webhook HMAC-assinado do repo
  if (req.method === "POST" && req.url === "/github") {
    if (!WEBHOOK_SECRET) { res.writeHead(500); return res.end("GITHUB_WEBHOOK_SECRET não configurado\n"); }
    const body = await readBody(req);
    const sig  = req.headers["x-hub-signature-256"] || "";
    const exp  = "sha256=" + crypto.createHmac("sha256", WEBHOOK_SECRET).update(body).digest("hex");
    if (!sig || !timingSafeEqual(sig, exp)) { res.writeHead(401); return res.end("Bad signature\n"); }
    const event = req.headers["x-github-event"];
    if (event === "ping") { res.writeHead(200); return res.end("pong\n"); }
    if (event !== "push") { res.writeHead(202); return res.end(`ignored: ${event}\n`); }
    let payload;
    try { payload = JSON.parse(body.toString()); } catch { res.writeHead(400); return res.end("Bad JSON\n"); }
    if (payload.ref !== "refs/heads/main") { res.writeHead(202); return res.end(`ignored ref: ${payload.ref}\n`); }
    console.log(`[${new Date().toISOString()}] github push by ${payload.pusher?.name}`);
    return enqueue(res, "github");
  }

  // POST /deploy — trigger manual com output em stream
  if (req.method === "POST" && req.url === "/deploy") {
    if ((req.headers["authorization"] || "") !== `Bearer ${TOKEN}`) {
      res.writeHead(401); return res.end("Unauthorized\n");
    }
    return stream(res);
  }

  // GET /healthz
  if (req.method === "GET" && req.url === "/healthz") {
    res.writeHead(200); return res.end("ok\n");
  }

  // GET /status
  if (req.method === "GET" && req.url === "/status") {
    let head = null;
    try { head = execSync("git rev-parse HEAD", { cwd: SCRIPT_DIR }).toString().trim(); } catch {}
    res.writeHead(200, { "Content-Type": "application/json" });
    return res.end(JSON.stringify({ head, busy, queueLen: queue.length, lastDeploys: state.lastDeploys }, null, 2));
  }

  res.writeHead(404); res.end("not found\n");
});

// ── Watchdog ─────────────────────────────────────────────────────────────
setInterval(() => {
  if (busy || queue.length) return;
  try {
    const local  = execSync("git rev-parse HEAD", { cwd: SCRIPT_DIR }).toString().trim();
    const remote = execSync("git ls-remote origin main", { cwd: SCRIPT_DIR }).toString().split(/\s+/)[0];
    if (!remote || local === remote) return;
    console.log(`[${new Date().toISOString()}] [watchdog] drift ${local.slice(0,7)} → ${remote.slice(0,7)}, deploying`);
    busy = true; runDeploy("watchdog");
  } catch (e) { console.error("[watchdog]", e.message); }
}, 5 * 60 * 1000);

server.listen(PORT, "0.0.0.0", () => {
  console.log(`[${new Date().toISOString()}] CPA deploy server :${PORT}`);
});
