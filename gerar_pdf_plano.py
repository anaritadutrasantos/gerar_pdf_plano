from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
import textwrap, datetime, os

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
    """Detecta títulos do plano de aula."""
    s = linha.strip()
    if s.startswith("■ "):
        rotulo = s[2:].strip()
        if rotulo in TITULOS_OFICIAIS:
            return rotulo
        return None
    if s in TITULOS_OFICIAIS:
        return s
    return None

def gerar_pdf_plano(conteudo_textual: str, nome_arquivo="Plano_de_Aula.pdf"):
    """Gera um plano de aula formatado com layout institucional."""
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    W, H = A4
    M = 2.5 * cm
    MAX_COL = 86
    y_min = 120
    y_top_texto = H - 100

    # Cabeçalho
    def cabecalho():
        c.setFillColor(colors.HexColor("#155FA0"))
        c.rect(0, H - 40, W, 40, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.white)
        c.drawCentredString(W / 2, H - 26, "Escola X — Plano de Aula")
        c.setFont("Helvetica", 10)
        c.drawRightString(W - M, H - 55, f"Data: {datetime.datetime.now().strftime('%d/%m/%Y')}")

    cabecalho()

    # Bloco de identificação
    y = H - 95
    c.setFillColor(colors.HexColor("#E9F0FA"))
    c.roundRect(M - 5, y - 90, W - 2 * M + 10, 100, 8, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#1F2D3D"))
    c.setFont("Helvetica", 11)
    for linha in [
        "Escola X — Curso Técnico em Informática",
        "Componente Curricular: Linguagem de Programação – Web",
        "Tema: ___________________________",
        "Duração: ________________________",
        "Professor(a): ____________________",
        "Data: ___________________________",
    ]:
        c.drawString(M + 5, y, linha)
        y -= 16
    y -= 12

    # Helpers
    def nova_pagina():
        c.showPage()
        cabecalho()
        return H - 100

    def desenhar_titulo(rotulo, y):
        if y < y_min:
            y = nova_pagina()
        if rotulo == "Referências":
            c.setFont("Helvetica-Bold", 12)
            c.setFillColor(colors.HexColor("#155FA0"))
            c.drawString(M + 5, y, f"■ {rotulo}")
            return y - 22
        largura_texto = W - 2 * M - 0.5 * cm
        c.setFillColor(colors.HexColor("#E9F0FA"))
        c.roundRect(M - 5, y - 8, largura_texto + 10, 20, 5, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.HexColor("#155FA0"))
        c.drawString(M + 5, y, f"■ {rotulo}")
        return y - 26

    # Corpo do texto
    texto = c.beginText(M + 5, y)
    texto.setFont("Helvetica", 12)
    texto.setLeading(17)

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
            texto.setFont("Helvetica", 12)
            texto.setLeading(17)
            continue

        if texto.getY() < y_min:
            c.drawText(texto)
            texto = c.beginText(M + 5, y_top_texto)
            texto.setFont("Helvetica", 12)
            texto.setLeading(17)

        for sub in textwrap.wrap(raw, MAX_COL):
            texto.textLine(sub)

    c.drawText(texto)
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.HexColor("#6B7785"))
    c.drawString(M, 1.8 * cm, "📘 Documento gerado automaticamente — Escola X")
    c.drawString(M, 1.2 * cm, "Assinatura do(a) Professor(a): ___________________________")

    c.save()
    caminho = os.path.abspath(nome_arquivo)
    print(f"✅ Plano de aula gerado com sucesso!\n👉 [Abrir ou baixar {nome_arquivo}]({caminho})")
    return caminho
