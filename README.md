# CPA · Coletivo Popular Autista

Site institucional do Coletivo Popular Autista. Construído por autistas,
para autistas e aliades.

Site: <https://coletivopopularautista.com.br> · Blog:
<https://coletivopopularautista.com.br/blog/> · Links:
<https://links.coletivopopularautista.com.br>

## Sobre

O CPA é um coletivo autista de base, de viés de esquerda. Organiza
comunidade, formação e apoio mútuo em torno de anticapacitismo, autonomia
neurodivergente, anticapitalismo, solidariedade de classe e
interseccionalidade.

Aqui, pessoa autista é sujeito político, não diagnóstico. A escrita evita
termos que patologizam ("portador de", "sofre de") e adota identidade
primeiro ("pessoa autista"), respeitando quem se nomeia diferente.

O símbolo do coletivo é o infinito arco-íris (neurodivergência) com a
bandeira vermelha e preta. O CPA não usa o quebra-cabeça nem o azul, pela
ligação com organizações rejeitadas por boa parte da comunidade autista.

## Cuidado sensorial

Acessibilidade sensorial vem antes de estética. O site segue regras
inegociáveis: paleta suave (sem branco ou preto puro, sem cor saturada),
movimento mínimo e desligável (respeita `prefers-reduced-motion`), sem
flashes ou estroboscopia, sem som automático, tipografia generosa (linha
curta, entrelinha alta, zoom até 200% sem quebrar) e texto completo antes
de qualquer imagem.

As regras completas estão em [`CLAUDE.md`](CLAUDE.md). A identidade visual
(paleta, tipografia, componentes, movimento, acessibilidade) está em
[`IDENTIDADE.md`](IDENTIDADE.md).

## Pilha técnica

Site estático: HTML, CSS externo em `shared/` e JavaScript mínimo. Sem
build step, sem framework. Servido por nginx em Docker Swarm. Fontes via
Google Fonts (Atkinson Hyperlegible, Lexend, JetBrains Mono).

A identidade visual em `shared/` (`cpa-base.css`, `cpa-home.css`, `cpa.js`)
é single source of truth: a home, a página de identidade e o blog
referenciam por URL absoluta, não copiam.

Três subprojetos têm stack própria e lifecycle independente:

| Subprojeto | Stack | Doc |
|---|---|---|
| `blog/` | Ghost 5 + MySQL 8, tema `cpa-theme` | [blog/README.md](blog/README.md) |
| `nextcloud/` | Nextcloud, Collabora e Forms, backup borgmatic | pasta `nextcloud/` |
| `links/` | LinkStack (link na bio) | [links/README.md](links/README.md) |

## Estrutura do repositório

| Caminho | O que é |
|---|---|
| `index.html` | Homepage (seções §00 a §09 e footer) |
| `identidade.html` | Página viva da identidade visual |
| `formulario.html` | Página de inscrição (embute o Nextcloud Forms) |
| `estatuto.html` | Estatuto em HTML acessível, servido em `/estatuto/` |
| `estatuto-cpa-2026.pdf` | Estatuto em PDF, para download e impressão |
| `favicon.svg` | Favicon: infinito arco-íris |
| `shared/` | CSS, JS, logo e og-image compartilhados |
| `blog/` | Blog Ghost (stack própria) |
| `nextcloud/` | Nextcloud (stack própria) |
| `links/` | LinkStack (stack própria) |
| `Dockerfile` | Imagem nginx com os arquivos estáticos |
| `docker-compose.yml` | Stack do site no Swarm |
| `deploy.sh` | Build e roll out no manager do Swarm |
| `deploy-server.js` | Webhook de deploy e watchdog |

A ordem e o propósito das seções da home estão documentados em
[`CLAUDE.md`](CLAUDE.md).

## Rodar localmente

O site é estático, sem build:

```bash
python3 -m http.server 8765
```

Abra <http://localhost:8765/>. A página de identidade fica em
`/identidade.html`.

Para o blog local (Ghost via Docker):

```bash
cd blog && docker compose up -d
```

## Deploy

O site sobe em Docker Swarm. No manager, `deploy.sh` faz o build da imagem
e o `docker stack deploy`. O deploy é automático: `deploy-server.js` recebe
o webhook de push do GitHub e, como rede de segurança, um watchdog compara
a cada 5 minutos o HEAD local com `origin/main` e reaplica se divergir.

Blog e Nextcloud são stacks separadas, com deploy manual próprio (ver os
READMEs de cada pasta).

## Como contribuir

Toda contribuição (código, conteúdo, design) respeita o cuidado sensorial.
As regras em [`CLAUDE.md`](CLAUDE.md) são inegociáveis: se uma mudança
conflita com qualquer uma, pare e pergunte antes.

Pontos de atenção:

- Escrita em pt-BR, linguagem direta, sem em-dash, sem emoji em texto
  institucional.
- A identidade visual em `shared/` é single source of truth. Não duplicar
  CSS: referenciar.
- Relato de barreira de acessibilidade é prioridade, não reclamação. Mande
  para <contato@coletivopopularautista.com.br> ou abra uma issue.

Issues e pull requests são bem-vindos.

## Contato

- Site: <https://coletivopopularautista.com.br>
- Blog: <https://coletivopopularautista.com.br/blog/>
- Links: <https://links.coletivopopularautista.com.br>
- Estatuto: <https://coletivopopularautista.com.br/estatuto/>
- Inscrição: <https://coletivopopularautista.com.br/formulario/>
- E-mail: <contato@coletivopopularautista.com.br>

## Licença

- Código: [AGPL-3.0-or-later](LICENSE).
- Conteúdo (textos e imagens do site): [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.pt-br).
