# LinkStack do CPA

Substituto self-hosted do linktr.ee/colpopautista. Roda em
`https://links.coletivopopularautista.com.br`.

## Stack

- **LinkStack** (PHP, MIT) — link-in-bio FOSS. Painel admin nativo,
  editor visual de links, temas customizáveis, exporta vCard, QR code.
- Imagem oficial `linkstackorg/linkstack:latest` (Apache + PHP + SQLite
  embutidos).
- **Caddy** (externo, compartilhado) — roteia subdomínio
  `links.coletivopopularautista.com.br` via label.

## Persistência

Volume nomeado `cpa-links_linkstack_data` em `/htdocs` — contém banco
SQLite, uploads de avatar/imagens, customizações de tema. Backup
futuro via Borgmatic (padrão Nextcloud).

## Deploy

1. **DNS**: apontar `links.coletivopopularautista.com.br` (A ou CNAME)
   pro IP do ritalee. Caddy busca cert ACME automático.
2. Copiar `.env.example` → `.env`, ajustar `LINKS_HOST` e `TZ` se
   necessário.
3. Rodar `bash deploy.sh` no manager do Swarm.
4. Abrir `https://links.coletivopopularautista.com.br` — wizard de
   install do LinkStack (cria conta admin com email+senha, escolhe
   tema inicial).
5. Painel → *Customize* → trocar paleta pra cores CPA
   (`#EFE9DC`/`#1A1814`/`#8C2A2A`/`#A88341`).

## Identidade visual

LinkStack tem editor de tema próprio (cores + fontes via painel).
Não reusa `/shared/cpa-base.css` automaticamente. Caminhos pra
alinhar visual:

- **Mínimo**: configurar cores no editor de tema do LinkStack.
- **Melhor**: criar tema custom em `/htdocs/themes/cpa/` (via
  bind-mount adicional) com CSS apontando pra `/shared/cpa-base.css`
  servido pelo nginx do site. Requer Caddy roteando `/shared/*` no
  host `links.*` também (label adicional) ou copiar o CSS pro tema.

Decidir depois conforme apetite de manutenção.

## Pontos abertos

- Backup do volume via Borgmatic.
- Tema custom alinhado com identidade (vs só tweak de cores no painel).
