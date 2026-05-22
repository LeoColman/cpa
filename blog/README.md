# Blog do CPA

Mini-plataforma de blogs do Coletivo Popular Autista. Roda em
`https://coletivopopularautista.com.br/blog`, como subpath do site
principal. Sem subdomínio.

## Stack

- **Ghost 5** (Node.js, MIT) — gerencia autoria, posts, painel admin.
- **MySQL 8** — banco do Ghost.
- **Caddy** (externo, compartilhado com o site) — roteia `/blog*` para o
  Ghost via matcher de path. Não strip-a o prefixo (Ghost precisa
  receber `/blog/...` inteiro).
- **Tema custom `cpa-theme`** — Handlebars fino que herda a identidade
  visual de `/shared/cpa-base.css` (mesmo arquivo servido pelo site
  principal, via nginx). Single source of truth.

## Roles

| Role do Ghost | Capacidade | Atende |
|---|---|---|
| Owner | Tudo. Único. | Admin supremo (primeira pessoa) |
| Admin | Gerencia users, posts, settings | Admin supremo (multi) |
| Author | Cria/edita/exclui apenas próprios posts | Autora do coletivo |

Suspender autora: painel → *Settings → Staff → \[autora\] → Suspend*.
Login bloqueado, posts continuam públicos.

## Deploy

1. Copiar `.env.example` → `.env`, preencher senhas de MySQL.
2. Rodar `bash deploy.sh` no manager do Swarm.
3. Abrir `https://coletivopopularautista.com.br/blog/ghost` — primeira
   visita roda o wizard de bootstrap (cria Owner com email+senha).
4. Ativar tema: painel → *Design → Change theme → Activate cpa-theme*.

## URLs

| Caminho | Servido por |
|---|---|
| `/` | nginx (site institucional) |
| `/identidade` | nginx |
| `/shared/*` | nginx (assets de identidade compartilhados) |
| `/favicon.svg` | nginx |
| `/blog` | Ghost (lista de posts) |
| `/blog/<slug>` | Ghost (post inteiro) |
| `/blog/ghost` | Ghost (painel admin) |
| `/blog/author/<slug>` | Ghost (página de autora) |

## Reuso de identidade

O tema `cpa-theme` **não duplica** CSS. Todos os templates referenciam
`<link rel="stylesheet" href="/shared/cpa-base.css">` por URL absoluta.
Caddy roteia `/shared/*` para o nginx (porque não está dentro do
matcher `/blog*`), nginx devolve o mesmo arquivo que serve a homepage.

Mudar paleta? Edita `shared/cpa-base.css` no repo, rebuilda imagem do
site, e o blog reflete na mesma hora (próximo refresh).

Estilos exclusivos do blog (grid de cards, post body) ficam em
`themes/cpa-theme/assets/css/blog.css`, servidos pelo próprio Ghost.

## Pontos abertos

- **SMTP**: convite de autora exige email; sem SMTP configurado, o
  Owner precisa copiar o link de convite manualmente do painel.
- **Backup**: ainda sem Borgmatic. Padrão futuro = `nextcloud/`.
- **Alias `/admin`**: hoje o admin é `/blog/ghost`. Se quiser
  `/admin → /blog/ghost`, adicionar redirect no Caddy do site.
- **Members/newsletter**: feature do Ghost ligada por padrão. Decidir
  se ligar ou desligar conforme postura editorial do coletivo.
