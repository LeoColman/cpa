"""Regenera o PDF do Estatuto a partir da estrutura do PDF original.

O PDF original veio de um .docx que nao existe mais. Este script le o PDF
antigo, extrai a estrutura (capitulos, artigos, paragrafos, incisos), aplica
as correcoes de texto e escreve um ODT plano que o LibreOffice converte em
PDF com a mesma diagramacao: A4, Liberation Sans 12, entrelinha 1,5,
cabecalho e numero de pagina.

As medidas de pagina sao calibradas automaticamente contra o PDF original
(ver ALVOS): cada rodada mede o PDF gerado e corrige as margens ate bater.
"""
import base64
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse_estatuto import blocos  # noqa: E402

PT_POR_CM = 28.3465
DATA_APROVACAO = "16 de maio de 2026"

# Posicoes do PDF original, em pontos a partir do topo da pagina.
ALVOS = {
    "cabecalho": 36.31,      # linha "CPA - Estatuto politico-organizativo"
    "corpo": 85.44,          # primeira linha de texto da pagina
    "rodape": 792.49,        # numero da pagina
    "capa_imagem": 84.97,    # topo do logo
    "capa_1": 286.18,        # COLETIVO POPULAR AUTISTA (14 pt, negrito)
    "capa_2": 334.42,        # ESTATUTO POLITICO-ORGANIZATIVO (16 pt, negrito)
    "capa_3": 362.07,        # E NORMAS GERAIS DE CONVIVENCIA (16 pt, negrito)
    "capa_4": 425.54,        # linha de situacao (12 pt)
    "capa_5": 556.24,        # ano (12 pt)
}

ANTERIOR = {"capa_1": "capa_imagem", "capa_2": "capa_1", "capa_3": "capa_2",
            "capa_4": "capa_3", "capa_5": "capa_4"}

CABECALHO = "CPA - Estatuto político-organizativo"
PAGINAS_ALVO = 14


def escapar(texto):
    return (texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def corrigir(blocos_lidos):
    """Tira as marcas de minuta e registra a data de aprovacao."""
    saida = []
    for tipo, texto in blocos_lidos:
        if tipo == "capa" and texto.startswith("Minuta para aprovação"):
            texto = f"Aprovado em assembleia em {DATA_APROVACAO}"
        elif texto.startswith("Este Estatuto entra em vigor após aprovação em assembleia"):
            texto = ("Este Estatuto está em vigor desde a aprovação em assembleia, "
                     f"em {DATA_APROVACAO}, e substitui as normas anteriores que "
                     "forem incompatíveis com seu conteúdo.")
        saida.append((tipo, texto))

    # A pagina final de aprovacao e reescrita: sai o formulario em branco,
    # entra o registro da assembleia que aprovou o texto.
    fim = next(i for i, (t, c) in enumerate(saida) if t == "centro" and c == "APROVAÇÃO")
    saida = saida[:fim] + [
        ("centro", "APROVAÇÃO"),
        ("corpo", "Este Estatuto foi aprovado em assembleia do Coletivo Popular "
                  f"Autista em {DATA_APROVACAO}."),
    ]
    return saida


ESTILOS_PARAGRAFO = """
  <style:style style:name="Corpo" style:family="paragraph">
   <style:paragraph-properties fo:text-align="justify" fo:text-indent="1.25cm"
    fo:line-height="150%" fo:margin-top="0cm" fo:margin-bottom="0cm"
    fo:widows="2" fo:orphans="2"/>
  </style:style>
  <style:style style:name="Rente" style:family="paragraph">
   <style:paragraph-properties fo:text-align="justify" fo:text-indent="0cm"
    fo:line-height="150%" fo:margin-top="0cm" fo:margin-bottom="0cm"
    fo:widows="2" fo:orphans="2"/>
  </style:style>
  <style:style style:name="Inciso" style:family="paragraph">
   <style:paragraph-properties fo:text-align="justify" fo:margin-left="1.25cm"
    fo:text-indent="-0.65cm" fo:line-height="150%" fo:margin-top="0cm"
    fo:margin-bottom="0cm" fo:widows="2" fo:orphans="2"/>
  </style:style>
  <style:style style:name="Artigo" style:family="paragraph">
   <style:paragraph-properties fo:text-align="start" fo:text-indent="0cm"
    fo:line-height="150%" fo:margin-top="0.212cm" fo:margin-bottom="0cm"
    fo:widows="2" fo:orphans="2"/>
   <style:text-properties fo:font-weight="bold" style:font-weight-asian="bold"/>
  </style:style>
  <style:style style:name="Capitulo" style:family="paragraph">
   <style:paragraph-properties fo:text-align="start" fo:text-indent="0cm"
    fo:line-height="150%" fo:margin-top="0.423cm" fo:margin-bottom="0cm"
    fo:widows="2" fo:orphans="2"/>
   <style:text-properties fo:font-weight="bold" style:font-weight-asian="bold"/>
  </style:style>
  <style:style style:name="Centro" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:text-indent="0cm"
    fo:line-height="150%" fo:margin-top="0cm" fo:margin-bottom="0.212cm"
    fo:widows="2" fo:orphans="2"/>
   <style:text-properties fo:font-weight="bold" style:font-weight-asian="bold"/>
  </style:style>
  <style:style style:name="Cabecalho" style:family="paragraph">
   <style:paragraph-properties fo:text-align="end" fo:line-height="100%"/>
   <style:text-properties fo:font-size="9pt" fo:color="#505050"/>
  </style:style>
  <style:style style:name="Rodape" style:family="paragraph">
   <style:paragraph-properties fo:text-align="end" fo:line-height="100%"/>
  </style:style>
"""


def estilos_capa(p):
    """Estilos da capa. p traz os espacamentos calibrados, em cm."""
    return f"""
  <style:style style:name="CapaImagem" style:family="paragraph"
   style:master-page-name="Capa">
   <style:paragraph-properties fo:text-align="center" fo:text-indent="0cm"
    fo:line-height="100%" fo:margin-top="{p['capa_imagem']:.3f}cm" fo:margin-bottom="0cm"/>
  </style:style>
  <style:style style:name="Capa1" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:text-indent="0cm"
    fo:line-height="100%" fo:margin-top="{p['capa_1']:.3f}cm" fo:margin-bottom="0cm"/>
   <style:text-properties fo:font-size="14pt" fo:font-weight="bold"
    style:font-weight-asian="bold"/>
  </style:style>
  <style:style style:name="Capa2" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:text-indent="0cm"
    fo:line-height="100%" fo:margin-top="{p['capa_2']:.3f}cm" fo:margin-bottom="0cm"/>
   <style:text-properties fo:font-size="16pt" fo:font-weight="bold"
    style:font-weight-asian="bold"/>
  </style:style>
  <style:style style:name="Capa3" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:text-indent="0cm"
    fo:line-height="100%" fo:margin-top="{p['capa_3']:.3f}cm" fo:margin-bottom="0cm"/>
   <style:text-properties fo:font-size="16pt" fo:font-weight="bold"
    style:font-weight-asian="bold"/>
  </style:style>
  <style:style style:name="Capa4" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:text-indent="0cm"
    fo:line-height="100%" fo:margin-top="{p['capa_4']:.3f}cm" fo:margin-bottom="0cm"/>
  </style:style>
  <style:style style:name="Capa5" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:text-indent="0cm"
    fo:line-height="100%" fo:margin-top="{p['capa_5']:.3f}cm" fo:margin-bottom="0cm"/>
  </style:style>
"""


def montar_fodt(itens, imagem_b64, p):
    corpo = []
    capa = [c for t, c in itens if t == "capa"]
    corpo.append(
        '<text:p text:style-name="CapaImagem">'
        '<draw:frame draw:style-name="Moldura" text:anchor-type="as-char" '
        'svg:width="6.2cm" svg:height="6.2cm">'
        f'<draw:image><office:binary-data>{imagem_b64}</office:binary-data></draw:image>'
        '</draw:frame></text:p>')
    for estilo, texto in zip(["Capa1", "Capa2", "Capa3", "Capa4", "Capa5"], capa):
        corpo.append(f'<text:p text:style-name="{estilo}">{escapar(texto)}</text:p>')

    primeiro_centro = True
    for tipo, texto in itens:
        if tipo == "capa":
            continue
        if tipo == "centro":
            # APRESENTACAO sai da capa; APROVACAO abre a ultima pagina
            estilo = "CentroInicio" if primeiro_centro else "CentroQuebra"
            primeiro_centro = False
        else:
            estilo = {"corpo": "Corpo", "rente": "Rente", "inciso": "Inciso",
                      "artigo": "Artigo", "capitulo": "Capitulo"}[tipo]
        corpo.append(f'<text:p text:style-name="{estilo}">{escapar(texto)}</text:p>')

    largura_texto = 21.0 - p["margem_esq"] - p["margem_dir"]
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<office:document xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
 xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
 xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
 xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
 xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
 xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
 office:version="1.3" office:mimetype="application/vnd.oasis.opendocument.text">
 <office:font-face-decls>
  <style:font-face style:name="Liberation Sans" svg:font-family="'Liberation Sans'"
   style:font-family-generic="swiss" style:font-pitch="variable"/>
 </office:font-face-decls>
 <office:styles>
  <style:default-style style:family="paragraph">
   <style:paragraph-properties fo:hyphenate="false" style:writing-mode="lr-tb"/>
   <style:text-properties style:font-name="Liberation Sans" fo:font-size="12pt"
    fo:language="pt" fo:country="BR"/>
  </style:default-style>
  <style:style style:name="Standard" style:family="paragraph">
   <style:text-properties style:font-name="Liberation Sans" fo:font-size="12pt"/>
  </style:style>
  <style:style style:name="Moldura" style:family="graphic">
   <style:graphic-properties style:vertical-pos="middle" style:vertical-rel="text"
    fo:margin="0cm" fo:padding="0cm" fo:border="none"/>
  </style:style>
{ESTILOS_PARAGRAFO}
  <style:style style:name="CentroInicio" style:family="paragraph"
   style:parent-style-name="Centro" style:master-page-name="Standard"/>
  <style:style style:name="CentroQuebra" style:family="paragraph"
   style:parent-style-name="Centro">
   <style:paragraph-properties fo:break-before="page"/>
  </style:style>
{estilos_capa(p)}
 </office:styles>
 <office:automatic-styles>
  <style:page-layout style:name="pm2">
   <style:page-layout-properties fo:page-width="21cm" fo:page-height="29.7cm"
    style:print-orientation="portrait" fo:margin-top="{p['margem_topo']:.3f}cm"
    fo:margin-bottom="{p['margem_base']:.3f}cm" fo:margin-left="{p['margem_esq']:.3f}cm"
    fo:margin-right="{p['margem_dir']:.3f}cm" style:writing-mode="lr-tb"/>
  </style:page-layout>
  <style:page-layout style:name="pm1">
   <style:page-layout-properties fo:page-width="21cm" fo:page-height="29.7cm"
    style:print-orientation="portrait" fo:margin-top="{p['margem_topo']:.3f}cm"
    fo:margin-bottom="{p['margem_base']:.3f}cm" fo:margin-left="{p['margem_esq']:.3f}cm"
    fo:margin-right="{p['margem_dir']:.3f}cm" style:writing-mode="lr-tb"/>
   <style:header-style>
    <style:header-footer-properties fo:min-height="{p['alt_cabecalho']:.3f}cm"
     fo:margin-bottom="{p['esp_cabecalho']:.3f}cm" style:dynamic-spacing="false"/>
   </style:header-style>
   <style:footer-style>
    <style:header-footer-properties fo:min-height="{p['alt_rodape']:.3f}cm"
     fo:margin-top="{p['esp_rodape']:.3f}cm" style:dynamic-spacing="false"/>
   </style:footer-style>
  </style:page-layout>
  <style:style style:name="Capa" style:family="text"/>
 </office:automatic-styles>
 <office:master-styles>
  <style:master-page style:name="Capa" style:page-layout-name="pm2"
   style:next-style-name="Standard"/>
  <style:master-page style:name="Standard" style:page-layout-name="pm1">
   <style:header>
    <text:p text:style-name="Cabecalho">{escapar(CABECALHO)}</text:p>
   </style:header>
   <style:footer>
    <text:p text:style-name="Rodape"><text:page-number text:select-page="current"
     >1</text:page-number></text:p>
   </style:footer>
  </style:master-page>
 </office:master-styles>
 <office:body>
  <office:text>
   {chr(10).join(corpo)}
  </office:text>
 </office:body>
</office:document>
"""


# PDF marcado (leitor de tela) e sem embutir o ODT de origem, que dobraria o
# tamanho do arquivo.
FILTRO_PDF = ('pdf:writer_pdf_Export:{"IsAddStream":{"type":"boolean","value":"false"},'
              '"UseTaggedPDF":{"type":"boolean","value":"true"}}')


def converter(fodt, destino_dir):
    subprocess.run(["soffice", "--headless", "--norestore", "--convert-to", FILTRO_PDF,
                    "--outdir", destino_dir, fodt],
                   capture_output=True, check=True, timeout=300)
    return os.path.join(destino_dir, os.path.splitext(os.path.basename(fodt))[0] + ".pdf")


def topo_da_imagem(pdf, altura):
    """Le a matriz de posicionamento da imagem da capa no fluxo de conteudo."""
    import zlib
    dados = open(pdf, "rb").read()
    for bruto in re.findall(rb"stream\r?\n(.*?)endstream", dados, re.S):
        try:
            fluxo = zlib.decompress(bruto)
        except Exception:
            continue
        m = re.search(rb"([\d.]+) 0 0 ([\d.]+) ([\d.]+) ([\d.]+) cm\s*/\w+ Do", fluxo)
        if m:
            alt = float(m.group(2))
            base = float(m.group(4))
            return altura - (base + alt)
    return None


def medir(pdf):
    """Mede as posicoes-chave do PDF gerado, em pontos a partir do topo."""
    xml = subprocess.run(["pdftotext", "-bbox-layout", pdf, "-"],
                         capture_output=True, text=True, check=True).stdout
    paginas = re.split(r"<page ", xml)[1:]
    altura = float(re.search(r'height="([\d.]+)"', paginas[0]).group(1))

    def linhas(pagina):
        return [(float(m.group(1)), float(m.group(2)), float(m.group(3)),
                 " ".join(re.findall(r">([^<]*)</word>", m.group(4))))
                for m in re.finditer(
                    r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)"[^>]*>(.*?)</line>',
                    pagina, re.S)]

    capa = linhas(paginas[0])
    p2 = linhas(paginas[1])
    m = {"paginas": len(paginas), "altura": altura}
    for chave, indice in (("capa_1", 0), ("capa_2", 1), ("capa_3", 2),
                          ("capa_4", 3), ("capa_5", 4)):
        if len(capa) > indice:
            m[chave] = capa[indice][1]
    m["capa_imagem"] = topo_da_imagem(pdf, altura)
    m["capa_textos"] = [c[3] for c in capa]
    cab = [l for l in p2 if l[3].startswith("CPA - Estatuto")]
    m["cabecalho"] = cab[0][1] if cab else None
    corpo = [l for l in p2 if not l[3].startswith("CPA - Estatuto") and not l[3].isdigit()]
    m["corpo"] = corpo[0][1] if corpo else None
    num = [l for l in p2 if l[3].isdigit()]
    m["rodape"] = num[0][1] if num else None
    m["inicio_paginas"] = []
    for pagina in paginas:
        ls = [l for l in linhas(pagina)
              if not l[3].startswith("CPA - Estatuto") and not l[3].isdigit()]
        m["inicio_paginas"].append(ls[0][3][:55] if ls else "")
    return m


def calibrar(itens, imagem_b64, dir_trabalho, rodadas=8):
    """Ajusta margens e espacamentos ate o PDF gerado bater com o original.

    Duas fases: primeiro a geometria da pagina (cabecalho, primeira linha do
    corpo, numero de pagina), depois os espacamentos da capa.
    """
    p = {
        "margem_topo": 1.25, "margem_base": 2.00, "margem_esq": 3.00, "margem_dir": 2.00,
        "alt_cabecalho": 0.40, "esp_cabecalho": 1.15,
        "alt_rodape": 0.45, "esp_rodape": 0.30,
        "capa_imagem": 1.20, "capa_1": 4.60, "capa_2": 1.20, "capa_3": 0.32,
        "capa_4": 1.60, "capa_5": 4.00,
    }
    fodt = os.path.join(dir_trabalho, "estatuto.fodt")

    def gerar():
        with open(fodt, "w", encoding="utf-8") as f:
            f.write(montar_fodt(itens, imagem_b64, p))
        return medir(converter(fodt, dir_trabalho))

    def erros_de(m, chaves):
        return {k: m[k] - ALVOS[k] for k in chaves if m.get(k) is not None}

    geometria = ("cabecalho", "corpo", "rodape")
    for rodada in range(rodadas):
        m = gerar()
        e = erros_de(m, geometria)
        print(f"geometria {rodada}: paginas={m['paginas']} "
              + " ".join(f"{k}={v:+.2f}" for k, v in e.items()))
        if len(e) == len(geometria) and all(abs(v) < 0.6 for v in e.values()):
            break
        p["margem_topo"] = max(0.2, p["margem_topo"] - e.get("cabecalho", 0) / PT_POR_CM)
        p["esp_cabecalho"] = max(0.0, p["esp_cabecalho"]
                                 - (e.get("corpo", 0) - e.get("cabecalho", 0)) / PT_POR_CM)
        p["margem_base"] = min(4.0, max(0.5, p["margem_base"]
                                        + e.get("rodape", 0) / PT_POR_CM))

    capa = ("capa_imagem", "capa_1", "capa_2", "capa_3", "capa_4", "capa_5")
    for rodada in range(rodadas):
        m = gerar()
        if len(m["capa_textos"]) != 5:
            raise SystemExit(f"capa com {len(m['capa_textos'])} linhas: {m['capa_textos']}")
        e = erros_de(m, capa)
        print(f"capa {rodada}: paginas={m['paginas']} "
              + " ".join(f"{k}={v:+.2f}" for k, v in e.items()))
        if all(abs(v) < 0.6 for v in e.values()):
            break
        for chave in capa:
            if chave not in e:
                continue
            anterior = ANTERIOR.get(chave)
            delta = e[chave] - (e.get(anterior, 0) if anterior else 0)
            p[chave] = max(0.0, p[chave] - delta / PT_POR_CM)

    # Fase 3: altura util da mancha. O espaco entre corpo e rodape decide
    # quantas linhas cabem na pagina; ajusta ate fechar em 14 paginas.
    for rodada in range(rodadas):
        m = gerar()
        print(f"mancha {rodada}: paginas={m['paginas']} esp_rodape={p['esp_rodape']:.2f}cm")
        if m["paginas"] == PAGINAS_ALVO:
            break
        if m["paginas"] > PAGINAS_ALVO and p["esp_rodape"] > 0.05:
            p["esp_rodape"] = max(0.0, p["esp_rodape"] - 0.05)
        elif m["paginas"] < PAGINAS_ALVO:
            p["esp_rodape"] += 0.05
        else:
            break

    m = gerar()
    return os.path.join(dir_trabalho, "estatuto.pdf"), p, m


def main():
    origem = sys.argv[1] if len(sys.argv) > 1 else "/home/leonardo/Downloads/Estatuto 2026.pdf"
    destino = sys.argv[2] if len(sys.argv) > 2 else "/home/leonardo/Workspace/cpa/estatuto-cpa-2026.pdf"
    dir_trabalho = sys.argv[3] if len(sys.argv) > 3 else "/tmp/estatuto-build"
    os.makedirs(dir_trabalho, exist_ok=True)

    itens = corrigir(blocos(origem))
    subprocess.run(["mutool", "extract", origem], cwd=dir_trabalho,
                   capture_output=True, check=True)
    jpg = next(f for f in sorted(os.listdir(dir_trabalho)) if f.endswith(".jpg"))
    imagem_b64 = base64.b64encode(open(os.path.join(dir_trabalho, jpg), "rb").read()).decode()

    original = medir(origem)
    pdf, p, m = calibrar(itens, imagem_b64, dir_trabalho)
    print("paginacao (original -> gerado):")
    iguais = 0
    for i in range(max(len(original["inicio_paginas"]), len(m["inicio_paginas"]))):
        a = original["inicio_paginas"][i] if i < len(original["inicio_paginas"]) else "-"
        b = m["inicio_paginas"][i] if i < len(m["inicio_paginas"]) else "-"
        marca = "ok " if a == b else "DIF"
        iguais += a == b
        print(f"  {marca} p{i + 1:02d}: {a[:45]:45} | {b[:45]}")
    print(f"paginas iguais: {iguais}/{len(original['inicio_paginas'])}")
    print("parametros:", {k: round(v, 3) for k, v in p.items()})
    print("paginas:", m["paginas"])
    for i, inicio in enumerate(m["inicio_paginas"], 1):
        print(f"  p{i:02d}: {inicio}")
    shutil.copy(pdf, destino)
    print("gerado:", destino)


if __name__ == "__main__":
    main()
