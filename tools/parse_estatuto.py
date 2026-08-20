"""Extrai a estrutura do Estatuto a partir do PDF original (texto + posicoes)."""
import re
import subprocess
import sys

X_MARGEM = 85.15      # inicio da area de texto
X_INCISO = 102.15     # primeira linha de inciso
X_RECUO = 120.60      # recuo de 1,25 cm (1a linha de paragrafo ou continuacao de inciso)
X_CABECALHO = 396.70
X_NUM_PAGINA = 532.10


def linhas_do_pdf(caminho):
    xml = subprocess.run(
        ["pdftotext", "-bbox-layout", caminho, "-"],
        capture_output=True, text=True, check=True).stdout
    paginas = re.split(r"<page ", xml)[1:]
    for pagina in paginas:
        linhas = []
        for m in re.finditer(r'<line xMin="([\d.]+)"[^>]*>(.*?)</line>', pagina, re.S):
            x = float(m.group(1))
            texto = " ".join(re.findall(r">([^<]*)</word>", m.group(2)))
            texto = texto.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
            linhas.append((x, texto.strip()))
        yield linhas


def perto(a, b, tol=1.0):
    return abs(a - b) <= tol


def blocos(caminho):
    """Devolve lista de (tipo, texto). Tipos: capa, centro, capitulo, artigo,
    corpo (1a linha recuada), rente (sem recuo, ex. paragrafos §), inciso."""
    saida = []
    for n_pagina, linhas in enumerate(linhas_do_pdf(caminho), start=1):
        for x, texto in linhas:
            if not texto:
                continue
            if perto(x, X_CABECALHO, 40) and texto.startswith("CPA - Estatuto"):
                continue
            if perto(x, X_NUM_PAGINA, 8) and texto.isdigit():
                continue
            if n_pagina == 1:
                saida.append(["capa", texto])
                continue
            if perto(x, X_INCISO):
                saida.append(["inciso", texto])
            elif perto(x, X_RECUO):
                if saida and saida[-1][0] == "inciso":
                    saida[-1][1] += " " + texto
                else:
                    saida.append(["corpo", texto])
            elif perto(x, X_MARGEM):
                if re.match(r"^Art\. ", texto):
                    saida.append(["artigo", texto])
                elif re.match(r"^\d+ [A-ZÁÂÃÉÊÍÓÔÕÚÇ]", texto) or texto.startswith("ANEXO "):
                    saida.append(["capitulo", texto])
                elif texto.startswith("§") or texto.startswith("Parágrafo único"):
                    saida.append(["rente", texto])
                elif saida:
                    saida[-1][1] += " " + texto
                else:
                    saida.append(["rente", texto])
            else:
                saida.append(["centro", texto])
    return [(t, re.sub(r"\s+", " ", c).strip()) for t, c in saida]


if __name__ == "__main__":
    for tipo, texto in blocos(sys.argv[1]):
        print(f"{tipo:9} | {texto}")
