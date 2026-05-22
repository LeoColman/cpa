# CPA · Identidade Visual

Referência viva da identidade visual do site institucional do Coletivo
Popular Autista. Compilado a partir do `index.html` (CSS embutido). Para
regras editoriais e de conteúdo, ver `CLAUDE.md`.

A identidade é uma só: **boletim de esquerda, sensorialmente acolhedor,
tipograficamente generoso, anticapacitista**. Toda decisão visual responde
a essas quatro coisas. Quando entrar em conflito com qualquer uma, parar e
perguntar antes de aplicar.

---

## 1 · Princípios

### 1.1 Sensorialmente cuidado
- Sem branco puro (`#FFFFFF`). Sem preto puro (`#000000`). Sem saturação.
- Contraste alto, mas sem agressão luminosa.
- Sem flashes, sem oscilação de cor, sem GIFs autoexecutáveis.
- Movimento curto, lento e desligável (sempre respeitar
  `prefers-reduced-motion: reduce`).
- Nenhum som inesperado: zero `autoplay`.

### 1.2 Boletim de esquerda
- Estética de jornal/zine: réguas finas, eyebrow mono em caixa-alta,
  numeração de seção com `§`, drop cap no primeiro parágrafo de bloco
  longo.
- Tipografia legível por padrão (Atkinson Hyperlegible no corpo, Lexend nos títulos), sem ornamento.
- Vermelho oxblood + dourado antigo como sinalizadores políticos, nunca
  decorativos.

### 1.3 Identidade política, não diagnóstica
- Símbolo: **estrela vermelha com contorno dourado** (leftist + autista).
- Proibido: quebra-cabeça (Autism Speaks) e azul como símbolo de autismo.
- Pessoa autista é sujeito político, não paciente.

### 1.4 Sem rastros de IA
- Sem em-dash (U+2014) em nenhum lugar do projeto.
- Sem ironia, hedging ou frases de encerramento de IA. Ver `CLAUDE.md`
  para a lista completa.

---

## 2 · Paleta

Todas as cores vivem em `:root` como custom properties. Não introduzir
cores fora dessa lista sem revisão.

### 2.1 Tema claro (padrão)

| Token             | HEX        | Uso                                          |
|-------------------|------------|----------------------------------------------|
| `--paper`         | `#EFE9DC`  | fundo principal (papel quente)               |
| `--paper-warm`    | `#E8E0CD`  | fundo de bloco (sensorial, hero notice)      |
| `--paper-deep`    | `#DDD3BC`  | fundo extra escuro (raro)                    |
| `--ink`           | `#1A1814`  | texto principal, fundos escuros (pullquote/contato/footer) |
| `--ink-soft`      | `#3A332A`  | corpo de texto secundário                    |
| `--ink-mute`      | `#6A5F50`  | metadados, eyebrows neutros                  |
| `--oxblood`       | `#8C2A2A`  | acento político (em italic, §, hover)        |
| `--oxblood-deep`  | `#6B1F1F`  | reserva (variação)                           |
| `--gold`          | `#A88341`  | réguas, contornos de detalhe                 |
| `--gold-soft`     | `#C9A968`  | acento sobre fundo escuro                    |

### 2.2 Tema escuro (`[data-theme="dark"]`)

Inverte papel/tinta sem trocar as funções dos tokens. Detecta
`prefers-color-scheme: dark` no primeiro load e persiste via
`localStorage.cpa-theme`.

| Token            | HEX        |
|------------------|------------|
| `--paper`        | `#1E1A15`  |
| `--paper-warm`   | `#241F18`  |
| `--paper-deep`   | `#141009`  |
| `--ink`          | `#E6DFD0`  |
| `--ink-soft`     | `#B5ADA0`  |
| `--ink-mute`     | `#786E5E`  |
| `--oxblood`      | `#B03535`  |
| `--oxblood-deep` | `#8C2A2A`  |
| `--gold`         | `#C9A968`  |
| `--gold-soft`    | `#A88341`  |

### 2.3 Réguas e divisores

| Token         | Definição                                                       |
|---------------|-----------------------------------------------------------------|
| `--rule`      | `1px solid color-mix(in srgb, var(--ink) 18%, transparent)`     |
| `--rule-gold` | `1px solid color-mix(in srgb, var(--gold) 45%, transparent)`    |

Padrão de borda de seção: `border-top: 2px solid var(--ink)`.
Quando a seção termina com pausa decorativa: `border-bottom: var(--rule-gold)`.

### 2.4 Grão de papel
`body::before` aplica ruído SVG fractal (240×240) com `mix-blend-mode:
multiply` e `opacity: 0.35` no tema claro; `screen` + `0.08` no escuro.
Estático, sem animação, `pointer-events: none`. Não remover: é parte da
textura.

---

## 3 · Tipografia

### 3.1 Famílias

| Token       | Família                                       | Função                          |
|-------------|-----------------------------------------------|---------------------------------|
| `--display` | Fraunces (variável: opsz, wght, SOFT, WONK)   | títulos, citações, ênfases      |
| `--body`    | Instrument Sans                               | texto corrido                   |
| `--mono`    | JetBrains Mono                                | eyebrows, créditos, metadados   |

Fontes via Google Fonts. **Fraunces é variável**: usar
`font-variation-settings` para controle fino, não pesos discretos.

### 3.2 Eixos variáveis da Fraunces (convenção)

| Contexto                          | opsz | SOFT | WONK | wght    |
|-----------------------------------|------|------|------|---------|
| Display gigante (hero, footer)    | 144  | 60-100 | 1  | 380-460 |
| Display grande (seção, contato)   | 72-96| 50-80| 0-1  | 360-380 |
| Display médio (nome de card)      | 36   | 70   | 0    | 460     |
| Lede e textos display em corpo    | 24   | 50-60| 0    | 400     |
| Ênfase em italic (acento)         | manter opsz | 100 | 1 | manter wght |
| Drop cap                          | 144  | 100  | 1    | 500     |

Regra: **italic = SOFT 100 + WONK 1 + cor oxblood**. É a marca de ênfase
do projeto. Sempre nessa combinação.

### 3.3 Escala tipográfica (clamp responsivo)

| Elemento                  | Tamanho                                  |
|---------------------------|------------------------------------------|
| Body                      | `clamp(15px, 1.05vw, 17px)` / `1.55`     |
| Corpo standfirst/intro    | `clamp(15.5px, 1.05vw, 17px)` / `1.65`   |
| Hero headline             | `clamp(48px, 8.5vw, 132px)` / `0.92`     |
| Hero lede                 | `clamp(18px, 1.5vw, 22px)` / `1.5`       |
| Hero quote                | `clamp(20px, 1.7vw, 26px)` / `1.3`       |
| Section title (padrão)    | `clamp(34px, 4.5vw, 64px)` / `0.98`      |
| Section title (participar)| `clamp(36px, 5vw, 72px)` / `0.95`        |
| Section title (sensorial) | `clamp(34px, 4vw, 56px)` / `1.0`         |
| Pullquote blockquote      | `clamp(40px, 6.5vw, 96px)` / `1.0`       |
| Footer cry shout          | `clamp(36px, 6.5vw, 96px)` / `0.96`      |
| Nome de card médio        | `clamp(20px, 1.7vw, 26px)` / `1.15`      |
| Nome de grupo (funciona)  | `clamp(19px, 1.5vw, 24px)` / `1.15`      |
| Numeral de regra/via      | `clamp(32-40px, 3.2-4.5vw, 44-56px)`     |
| Eyebrow                   | `12px` (mono, `letter-spacing: 0.16em`)  |
| Metadados/citação         | `11-11.5px` (mono)                       |

Regras:
- Texto corrido nunca em `px` rígido. Sempre `clamp()` ou `rem`.
- Linha curta: máximo `~70ch` em parágrafos longos (`max-width: 70ch`).
- Entrelinha mínima `1.5` em corpo. `1.6-1.7` em descrições compactas.
- Hierarquia clara: display gigante → display médio → mono → body.

### 3.4 Letter-spacing
- Display: negativo (`-0.015em` a `-0.03em`). Fraunces respira sozinha.
- Mono eyebrow/nav: `0.06em` a `0.16em`. Caixa-alta precisa de ar.

---

## 4 · Layout

### 4.1 Container

```css
.shell {
  max-width: var(--max);   /* 1340px */
  margin: 0 auto;
  padding: 0 var(--gutter); /* clamp(20px, 4vw, 56px) */
  position: relative;
  z-index: 2;
}
```

Toda seção envolve seu conteúdo em `.shell`. Nada vai borda a borda do
viewport (exceto fundos coloridos da própria `<section>`).

### 4.2 Padding vertical de seção

| Densidade          | Padding                                |
|--------------------|----------------------------------------|
| Compacto           | `clamp(40px, 6vw, 88px) 0`             |
| Padrão             | `clamp(56px, 8vw, 120px) 0`            |
| Pullquote (drama)  | `clamp(64px, 9vw, 128px) 0`            |
| Footer             | `clamp(56px, 7vw, 100px) 0 clamp(28px, 3vw, 48px)` |

### 4.3 Grids de cabeçalho de seção
Padrão `1fr 2fr` (eyebrow esquerda, h2 direita) com `align-items:
baseline`. Colapsa para `1fr` em `max-width: 720px-860px`.

```css
.section__head {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 2fr);
  gap: clamp(20px, 4vw, 56px);
  align-items: baseline;
  margin-bottom: clamp(24px, 4vw, 56px);
}
```

### 4.4 Grids de conteúdo

| Padrão            | Uso                              | Breakpoints                              |
|-------------------|----------------------------------|------------------------------------------|
| 3 colunas         | grupos (funciona), vias          | `1000px → 2col`, `640px → 1col`          |
| 2 colunas         | ingresso, regras                 | `860px → 1col`                           |
| 2 colunas mosaico | sensorial, contato (`gap: 2px`)  | `860px → 1col`                           |

### 4.5 Mosaico de cartelas (sensorial / contato)
Truque de borda interna: container com `gap: 2px` + `background:
color-mix(... 14-15%)` que aparece pelos espaços. Cada `<li>` tem
background sólido (`var(--paper-warm)` ou `var(--ink)`). Produz grid de
células com divisórias finas sem borda explícita.

---

## 5 · Componentes

### 5.1 Anatomia de seção

```html
<section class="X" id="x">
  <div class="shell">
    <header class="X__head">
      <p class="eyebrow">
        <a class="section-link" href="#x">
          NN · <b>Nome da seção</b>
        </a>
      </p>
      <h2 class="X__title">
        Título <em>com ênfase</em>.
      </h2>
    </header>

    <!-- conteúdo: intro opcional + grid ou body -->
  </div>
</section>
```

Cada seção:
- Tem `id` único em kebab-case curto (`#inicio`, `#manifesto`, `#posicao`,
  `#funciona`, `#regras`, `#participar`, `#ingresso`, `#contato`,
  `#sensorial`).
- Eyebrow numerado em sequência (`§ 00`, `§ 01`, ...). Ao adicionar
  seção: renumerar todas a partir daquela posição.
- Eyebrow envolvido em `.section-link` para virar permalink compartilhável.

### 5.2 Eyebrow

```css
.eyebrow {
  font-family: var(--mono);
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--ink-mute);
  display: flex; align-items: center; gap: 10px;
}
.eyebrow::before {
  content: "§";
  color: var(--oxblood);
  font-family: var(--display);
  font-size: 16px;
  font-style: italic;
}
.eyebrow b { color: var(--oxblood); font-weight: 500; }
```

Variantes para fundos escuros:
- `.pullquote__eyebrow`: `color: gold-soft`, `§` em `oxblood`.
- `.contato__eyebrow`: `color: gold-soft`, `b` em `paper`.

### 5.3 Section-link (permalink)

```css
.section-link { border-bottom: 0; }
.section-link::after {
  content: " #";
  color: var(--oxblood);
  opacity: 0;
  margin-left: 0.4em;
  transition: opacity 200ms ease;
}
.section-link:hover::after,
.section-link:focus-visible::after { opacity: 1; }
```

`#` aparece no hover/focus, em oxblood. Cor herdada do eyebrow (sem
override).

### 5.4 Hero
Grid `7fr 4fr` (titular esquerda, lateral direita com quote + notice
sensorial). Lateral tem borda esquerda dourada
(`border-left: var(--rule)`). Hero é a única seção com `reveal`
escalonado (delays 80-640ms).

### 5.5 Standfirst (manifesto, quem somos)
Header eyebrow + título. Corpo em **duas colunas** (`columns: 2`) com
`column-rule: var(--rule)`. **Drop cap** na primeira letra do primeiro
parágrafo: Fraunces 144 SOFT 100 WONK 1, oxblood, `5.2em`, float
esquerda. Colapsa para 1 coluna em `720px`.

### 5.6 Pullquote
Fundo `var(--ink)` (sempre escuro, independente do tema). Gradiente
radial sutil oxblood + gold como atmosfera. Citação enorme em italic
Fraunces 144, palavra-chave envolta em `<span>` ganha `gold-soft +
font-style: normal` (contra-italic). Não animar. Não introduzir
estroboscópio mesmo em estado decorativo.

### 5.7 Cartelas

Há quatro tipos com estrutura comum (borda topo + título + descrição).
Diferenças resumidas:

| Classe              | Topo                           | Numeração       | Largura típica  |
|---------------------|--------------------------------|-----------------|-----------------|
| `.via` (participar) | `2px solid ink` + numeral i/ii grande oxblood | romano | 3 colunas |
| `.grupo` (funciona) | `2px solid ink`                | sem número      | 3 colunas |
| `.regra` (regras)   | `2px solid ink`, grid `auto 1fr` | numeral display oxblood grande | 2 colunas |
| `.ingresso__block`  | `2px solid ink`                | sem número      | 2 colunas |

Texto descritivo das cartelas: `14.5px`, `line-height: 1.6`,
`color: var(--ink-soft)`.

Nomes (`__name`) em Fraunces 36, weight 460, `clamp(19-20px, 1.5-1.7vw,
24-26px)`. Em `.grupo` o nome ganha cor oxblood (diferenciação visual de
grid mais denso).

### 5.8 Sensorial
Fundo `var(--paper-warm)` + linha dourada fina no topo
(`::before height: 1px`). Grid `5fr 7fr` (título esquerda, lista direita).
Lista em mosaico 2×N com divisórias `gap: 2px`. Cada item: rótulo mono
oxblood caixa-alta + descrição.

### 5.9 Contato (fundo escuro)
Mesmo padrão da pullquote: `background: var(--ink)`, sempre escuro.
Grid `5fr 7fr`. Lista de canais em mosaico 2×N com `gap: 2px` e divisor
papel/transparente. Aviso de cuidado com `border-left: 2px solid
var(--oxblood)`.

### 5.10 Masthead
Linha grossa + linha fina douradas em cima. Grid `auto 1fr auto`
(marca, nav, meta). Nav em mono caixa-alta com underline animado
oxblood (`scaleX 0 → 1` em `260ms`).

Marca:
```html
<svg class="brand__mark" viewBox="0 0 24 24">
  <path class="star-outline"
        d="M12 0.6 L14.9 8.5 ..." />
</svg>
```
Estrela 10 pontas **ligeiramente assimétrica** (gesto de
neurodivergência). Fill oxblood, stroke gold `0.6`. Não simetrizar.

Meta no canto: ano · edição · botão de tema. Botão de tema em mono caixa
baixa com borda fininha; troca de label `◑ tema escuro` / `◐ tema
claro`.

### 5.11 Footer (cry)
Fundo `var(--ink)`. Brado de fechamento em Fraunces 144 com `em` em
`gold-soft` e `<u>` com `text-decoration-color: oxblood`,
`text-decoration-thickness: 4px`, `text-underline-offset: 8px`. Régua
oxblood `2px` no topo (`::before`).

Colunas (`grid-template-columns: repeat(4, 1fr)`):
1. Coletivo (Manifesto, Participar, Regras)
2. Acesso (Cuidado sensorial, Relatar barreira)
3. Contato (e-mail)
4. Princípio editorial (parágrafo)

Base inferior: ano · CC BY-SA 4.0 · "Feito com cuidado, sem pressa".

---

## 6 · Movimento

### 6.1 Reveal único, suave

```css
.reveal {
  opacity: 0;
  transform: translateY(8px);
  animation: gentleRise 900ms cubic-bezier(.2, .6, .2, 1) forwards;
}
.reveal-1 { animation-delay: 80ms; }
.reveal-2 { animation-delay: 220ms; }
.reveal-3 { animation-delay: 360ms; }
.reveal-4 { animation-delay: 500ms; }
.reveal-5 { animation-delay: 640ms; }
```

Usado apenas no hero/masthead. Não aplicar a seções de baixo da página
(não usar scroll-triggered: ambígua para usuários sensoriais).

### 6.2 Transições padrão
- Hover de link: `border-color, color` em `240ms ease`.
- Underline animado: `transform 260ms ease`.
- Section-link "#": `opacity 200ms ease`.
- Botão tema: `220ms ease`.

### 6.3 Reduced motion
Já implementado globalmente:

```css
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001ms !important;
  }
}
```

Toda animação/transition adicionada precisa respeitar esse override
(usar variáveis de animação, não hardcode burlando o `!important`).

### 6.4 Proibido sempre
Mesmo com motion habilitado:
- Parallax.
- Autoplay de vídeo ou áudio.
- Carrossel automático.
- Scroll hijacking.
- Contadores animados, números que pulam.
- Qualquer pulso, piscar, oscilação de luminosidade.

---

## 7 · Acessibilidade

### 7.1 Skip link

```html
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
```
Escondido fora do viewport, aparece em foco. Outline gold `2px`.

### 7.2 Focus ring

```css
*:focus-visible {
  outline: 2px solid var(--oxblood);
  outline-offset: 3px;
  border-radius: 1px;
}
```
Sempre visível. Não remover. Não substituir por `outline: none`.

### 7.3 Imagens
- Decorativas: `aria-hidden="true"` + `alt=""`.
- Informativas: `alt` descritivo em pt-BR.
- SVGs decorativos (`brand__mark`, ícones): `aria-hidden="true"`.

### 7.4 Tema escuro
Detecção automática via `prefers-color-scheme`, persistência via
`localStorage.cpa-theme`. Inline script no `<head>` para evitar flash
de tema errado.

### 7.5 Zoom
Layout permite leitura em zoom até 200% sem quebra (todos os tamanhos
em `clamp()` ou `rem`, sem `px` rígido em texto corrido).

---

## 8 · Estrutura semântica

### 8.1 HTML
- `<header class="masthead">` no topo.
- `<main id="conteudo">` envolve todas as seções.
- Cada `<section>` tem `id` + classe própria.
- Cabeçalho de seção em `<header class="X__head">` com `<p class="eyebrow">`
  e `<h2 class="X__title">`.
- Cartelas em `<article class="X">`.
- `<footer class="cry">` no fim.

### 8.2 Ordem das seções
Ver `CLAUDE.md` (única fonte da verdade).

### 8.3 Nomenclatura BEM
`bloco__elemento` (duas underscores). Sem `--modificador` no projeto
atual (paleta simples). Manter consistência ao criar componente novo.

---

## 9 · Escrita

Regras detalhadas no `CLAUDE.md`. Resumo visual:
- **Idioma**: pt-BR.
- **Pessoa autista é sujeito político**, identity-first.
- **Sem em-dash** (U+2014) em hipótese alguma.
- **Sem en-dash** (U+2013) tampouco.
- **Sem emoji** em texto institucional.
- **Sem aspas retas** (`"`) em prosa: usar `"" '`.
- **Sem "É importante destacar", "Em suma", "Por fim"**.
- **`·` (middot)** apenas em separadores curtos (mastheads, créditos,
  eyebrows), nunca em prosa.
- **Linguagem inclusiva**: "todas as pessoas", "participantes",
  "pessoas autistas", "aliades".

---

## 10 · Anti-patterns

Coisas que **não fazer**, listadas para não esquecer:

- ❌ Branco puro `#FFFFFF`, preto puro `#000000`, cor saturada.
- ❌ Cor nova fora dos tokens em `:root`.
- ❌ Em-dash, en-dash, emoji em texto.
- ❌ `font-size` em `px` rígido para texto corrido.
- ❌ Animação que pulse, pisque ou oscile em luminosidade.
- ❌ Autoplay (vídeo, áudio).
- ❌ Símbolo do quebra-cabeça, azul como símbolo do autismo.
- ❌ Remoção de `outline` em foco.
- ❌ Termos patologizantes: "portador de", "sofre de", "vítima".
- ❌ Carrossel, parallax, scroll hijacking, contador animado.
- ❌ Footer/header diferente entre páginas (no momento só `index.html`).

---

## 11 · Assets compartilhados (`/shared/`)

A identidade visual mora em `shared/`, servida pelo nginx em
`/shared/*`. Todas as superfícies (homepage, identidade, blog) usam o
mesmo arquivo, não cópia.

| Arquivo | O que tem | Quem referencia |
|---|---|---|
| `shared/cpa-base.css` | Tokens (`:root`), tema escuro, body, masthead, eyebrow, footer cry, reveal, focus | `index.html`, `identidade.html`, tema `cpa-theme` do blog |
| `shared/cpa-home.css` | Layouts da home (`.hero*`, `.standfirst`, `.pullquote`, `.participar`, `.ingresso`, `.funciona`, `.regras`, `.sensorial`, `.contato`) | só `index.html` |
| `shared/cpa.js` | Toggle de tema (claro/escuro) | todas |

Mudar paleta = mudar `cpa-base.css`. Reflete em todo lugar simultaneamente.

Tokens em `:root` continuam vindo primeiro. Comentários de seção em
banner ASCII (`/* === NOME === */`) para facilitar navegação.

## 12 · Blog (`/blog`)

Subpath em `coletivopopularautista.com.br/blog`. Framework: **Ghost 5**
com tema custom `cpa-theme` (Handlebars). Mesma identidade do site.

- Stack separada em `blog/` (docker-compose próprio, Caddy roteia
  `/blog*` para Ghost via matcher, sem strip-ar prefixo).
- Tema `cpa-theme` referencia `/shared/cpa-base.css` por URL absoluta:
  navegador busca no nginx, não duplica.
- CSS exclusivo do blog (cards, post body, autora) fica em
  `blog/themes/cpa-theme/assets/css/blog.css`.
- Painel admin: `/blog/ghost`.

Ver `blog/README.md` para deploy e bootstrap.

## 13 · Preview local

```
python3 -m http.server 8765
```

Site abre em `http://localhost:8765/`. Identidade em `/identidade.html`.
Para preview do blog, rodar a stack `blog/` localmente:

```
cd blog && docker compose up -d
```

Ghost wizard em `http://localhost:2368/ghost` (mapear porta em dev).
