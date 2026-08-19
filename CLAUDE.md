# CPA · Coletivo Popular Autista

Site institucional do CPA. Construído por autistas, para autistas e aliades.
Coletivo de viés de esquerda: anticapacitismo, autonomia neurodivergente,
anticapitalismo, solidariedade de classe, interseccionalidade.

Idioma do conteúdo: **pt-BR**.

---

## Cuidado sensorial · regras obrigatórias

Estas regras são inegociáveis. Toda contribuição (código, conteúdo, design)
deve respeitar todas elas. Se uma alteração entrar em conflito com qualquer
item, **pare e pergunte** antes de aplicar.

### 1. Paleta suave
Sem branco puro (`#FFFFFF`), sem preto puro (`#000000`), sem cores saturadas.
Contraste alto, mas sem agressão luminosa. Usar as variáveis CSS definidas
em `:root`. Não introduzir cores novas sem revisão. Palette atual:
papel `#EFE9DC`, tinta `#1A1814`, oxblood `#8C2A2A`, ouro antigo `#A88341`.

Exceção única e registrada: o logo da marca (`/shared/cpa-logo.png`) usa
anel quase-preto e infinito arco-íris saturado. A exceção vale só pro
logo; o corpo do site segue a paleta suave. No modo escuro o logo recebe
um chip claro atrás pra não sumir no fundo.

### 2. Movimento mínimo
Animações são curtas, lentas e desligáveis. Sempre respeitar
`prefers-reduced-motion: reduce`. A media query no CSS já desativa toda
animação e transição. Nada de parallax, autoplay de vídeo, carrosséis
automáticos, scroll hijacking, contadores animados ou números que pulam.

### 3. Sem flashes
Nenhum elemento pode piscar, cintilar, mudar de cor abruptamente nem
oscilar em luminosidade. Sem GIFs autoexecutáveis. Sem efeitos estroboscópicos.
Sem alertas de cor que latejam.

### 4. Sem som inesperado
Nada toca automaticamente. Vídeos e áudios sempre exigem clique consciente
do usuário. Não usar `autoplay` nem `<audio>` em background.

### 5. Tipografia generosa
Linha curta (máx. ~70 caracteres), entrelinha alta (≥ 1.5 em corpo),
hierarquia clara. O layout deve permitir leitura em zoom até 200% sem
quebrar. Não usar `font-size` em `px` rígido para texto corrido. Preferir
`clamp()` ou `rem`.

### 6. Texto antes de imagem
O conteúdo informativo deve ser completo só com texto. Imagens decorativas
recebem `aria-hidden="true"` e `alt=""`. Imagens informativas têm `alt`
descritivo. SVGs decorativos: `aria-hidden`.

### 7. Linguagem direta
Evitar ironia, metáfora ambígua e jargão político sem definição. Falar
claro. Termos técnicos (capacitismo, masking, ABA, neurodivergência) devem
poder ser explicados em uma linha caso o leitor não conheça.

### 8. Crítica é bem-vinda
Acessibilidade é processo, nunca está pronta. Manter o canal de retorno
visível e tratar relato de barreira como prioridade, não como reclamação.

---

## Regras de escrita

### NUNCA usar em-dash (U+2014)

Em-dash é marca registrada de texto gerado por IA. Não usar **em hipótese
alguma**, em nenhum lugar do projeto: prosa, títulos, eyebrows, comentários,
meta-tags, CSS, commits, README, mensagens de PR. Vale para o caractere
direto (U+2014) e para a entidade HTML `&mdash;`.

Substitutos preferidos, em ordem:

1. **Vírgula**: para apostos e incisos curtos.
2. **Ponto**: quando dá pra quebrar a frase em duas. Geralmente fica melhor.
3. **Dois-pontos**: quando o que vem depois explica ou lista o que veio antes.
4. **Parênteses**: para aparte de fato secundário.
5. **Ponto e vírgula**: para enumerações longas ou clausulas independentes.
6. **Middot** (`·`): só em separadores estilísticos curtos (mastheads,
   eyebrows, créditos), nunca em prosa.

En-dash (U+2013) também não. Hífen comum (`-`) só onde for hífen mesmo
(palavras compostas, intervalos numéricos curtos como `01-06`).

### Outras pegadinhas de IA, evitar
- Não começar parágrafo com "É importante destacar que".
- Não fechar com "Em suma" ou "Por fim".
- Não usar "elevar a outro patamar", "trazendo à tona", "tecer considerações".
- Não usar emoji em texto institucional.
- Aspas tipográficas (`"` `"` `'` `'`) sim. Aspas retas (`"`) só em código.

---

## Decisões editoriais

- **Pessoa autista é sujeito político**, não diagnóstico. Evitar termos que
  patologizem ("portador de", "sofre de", "vítima do autismo").
- **Identity-first** quando o contexto pedir ("pessoa autista", não
  "pessoa com autismo"). Segue preferência majoritária da comunidade
  autista brasileira. Mas respeitar pessoa que se nomeia diferente.
- **Não usar** "azul" como símbolo do autismo (ligação com Autism Speaks,
  organização rejeitada por boa parte da comunidade). Símbolo do CPA é
  o logo (`/shared/cpa-logo.png`): bandeira vermelha/preta (esquerda) e
  infinito arco-íris (neurodivergência) com "CPA" num círculo de
  pincelada. O favicon (`favicon.svg`) é o infinito arco-íris sozinho.
- **Não usar** o símbolo do quebra-cabeça pela mesma razão.

---

## Pilha técnica

Site estático. HTML + CSS externo em `shared/` + JS mínimo. Sem build
step. Sem framework. Páginas servidas por nginx via Docker Swarm.
Fontes via Google Fonts (Atkinson Hyperlegible, Lexend, JetBrains Mono).

Identidade visual compartilhada (`/shared/cpa-base.css`, `cpa-home.css`,
`cpa.js`) é **single source of truth**: homepage, identidade, estatuto,
formulário e blog referenciam por URL absoluta, não copiam. Ver
`IDENTIDADE.md` §11-12.

Blog em `coletivopopularautista.com.br/blog` (subpath). Stack
independente em `blog/` (Ghost 5 + MySQL 8). Caddy roteia `/blog*` via
matcher de path sem strip-ar prefixo. Tema `cpa-theme` reusa
`/shared/cpa-base.css`. Ver `blog/README.md`.

Para preview local:
```
python3 -m http.server 8765
```

## Estrutura da homepage

Ordem das seções (numeradas em `§`):
- `§ 00` Hero / Manifesto inicial
- `§ 01` Quem somos (standfirst)
- `§ 02` Posição política (pull-quote)
- `§ 03` Como funciona o coletivo
- `§ 04` Regras do coletivo
- `§ 05` Estatuto (link pra `/estatuto/` e download do PDF)
- `§ 06` Como participar
- `§ 07` Ingresso e desvinculação
- `§ 08` Contato
- `§ 09` Cuidado sensorial
- Footer (brado de fechamento)

Ao adicionar nova seção, renumerar os `§` em ordem.
