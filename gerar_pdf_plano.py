
---

## 💻 2️⃣ CÓDIGO PYTHON (cole isso no GitHub, substituindo o conteúdo do arquivo `gerar_pdf_plano.py`)

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import textwrap, datetime, os

# ---------- Fonte Unicode ----------
# É importante que o arquivo DejaVuSans.ttf esteja no mesmo diretório do script no GitHub
pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", "DejaVuSans-Bold.ttf"))

# ---------- Títulos oficiais ----------
TITULOS_OFICIAIS = [
    "Objetivos de Aprendizagem",
    "Conteúdo Programático",
    "Metodologia e Desenvolvimento",
    "Recursos Didáticos",
    "Avaliação",
    "Dicas para o Professor",
    "Referências",
]

def _eh_titulo(linha: str) -> str | None:
    """Detecta se a linha é um título oficial."""
    s = linha.strip()
    if s.startswith("■ "):
        rotulo = s[2:].strip()
        if rotulo in TITULOS_OFICIAIS:
            return rotulo
    if s in TITULOS_OFICIAIS:
        return s
    return None

def gerar_pdf_plano(conteudo_textual: str, nome_arquivo="Plano_de_Aula.pdf"):
    """Gera o PDF com layout institucional e formatação automática."""
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    W, H = A4
    M = 2.5*cm
    MAX_COL = 90
    y_min = 100
    y_top_texto = H - 150

    # ---------- Cabeçalho ----------
    def cabecalho():
        c.setFillColor(colors.HexColor("#155FA0"))
        c.rect(0, H - 60, W, 60, stroke=0, fill=1)
        c.setFont("DejaVuSans-Bold", 16)
        c.setFillColor(colors.white)
        c.drawCentredString(W/2, H - 38, "Escola Céu Azul — Plano de Aula")
        c.setFont("DejaVuSans", 10)
        c.drawRightString(W - M, H - 75, f"Data: {datetime.datetime.now().strftime('%d/%m/%Y')}")

    cabecalho()

    # ---------- Bloco de identificação ----------
    y = H - 130
    c.setFillColor(colors.HexColor("#E9F0FA"))
    c.roundRect(M - 5, y - 90, W - 2*M + 10, 100, 8, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#1F2D3D"))
    c.setFont("DejaVuSans", 11)
    for linha in [
        "Curso: Técnico em Desenvolvimento de Sistemas",
        "Componente Curricular: Linguagem de Programação – Web",
        "Tema: ___________________________",
        "Duração: ________________________",
        "Professor(a): ____________________",
        "Data: ___________________________",
    ]:
        c.drawString(M + 5, y, linha)
        y -= 16
    y -= 10

    # ---------- Helpers ----------
    def nova_pagina():
        c.showPage()
        cabecalho()
        return H - 150

    def desenhar_titulo(rotulo, y):
        if y < y_min:
            y = nova_pagina()
        c.setFillColor(colors.HexColor("#E9F0FA"))
        c.roundRect(M - 5, y - 8, W - 2*M + 10, 22, 5, stroke=0, fill=1)
        c.setFont("DejaVuSans-Bold", 12)
        c.setFillColor(colors.HexColor("#155FA0"))
        c.drawString(M + 5, y, f"■ {rotulo}")
        return y - 26

    # ---------- Corpo do texto ----------
    texto = c.beginText(M + 5, y)
    texto.setFont("DejaVuSans", 11)
    texto.setLeading(17)
    texto.setFillColor(colors.HexColor("#1F2D3D"))

    for linha in conteudo_textual.split("\n"):
        raw = linha.rstrip()
        if not raw:
            if texto.getY() > y_min:
                texto.textLine("")
            continue

        rotulo = _eh_titulo(raw)
        if rotulo:
            c.drawText(texto)
            y = texto.getY()
            y = desenhar_titulo(rotulo, y)
            texto = c.beginText(M + 5, y)
            texto.setFont("DejaVuSans", 11)
            texto.setLeading(17)
            texto.setFillColor(colors.HexColor("#1F2D3D"))
            continue

        if texto.getY() < y_min:
            c.drawText(texto)
            texto = c.beginText(M + 5, y_top_texto)
            texto.setFont("DejaVuSans", 11)
            texto.setLeading(17)
            texto.setFillColor(colors.HexColor("#1F2D3D"))

        for sub in textwrap.wrap(raw, MAX_COL):
            texto.textLine(sub)

    c.drawText(texto)

    # ---------- Rodapé ----------
    c.setFont("DejaVuSans-Oblique", 9)
    c.setFillColor(colors.HexColor("#6B7785"))
    c.drawString(M, 1.8*cm, "📘 Documento gerado automaticamente — Escola Céu Azul")
    c.drawString(M, 1.2*cm, "Assinatura do(a) Professor(a): ___________________________")

    c.save()
    print(f"✅ PDF gerado com sucesso! → {os.path.abspath(nome_arquivo)}")
