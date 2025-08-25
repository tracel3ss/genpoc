import os
import random
import string
import argparse
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import pikepdf

WORDS = (
    "lorem ipsum dolor sit amet consectetur adipiscing elit "
    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua "
    "ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi "
    "ut aliquip ex ea commodo consequat"
).split()

def random_sentence():
    return " ".join(random.choices(WORDS, k=random.randint(6, 12)))

def draw_page(c, width, height, poc=False, collaborator_url=None):
    """Dibuja una página con contenido aleatorio"""
    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Título de prueba para File Upload PoC - TraceL3ss")
    y -= 30

    c.setFont("Helvetica", 12)
    for _ in range(20):
        line = random_sentence()
        c.drawString(50, y, line)
        y -= 15
        if y < 150:
            break

    if poc and collaborator_url:
        y -= 20
        c.setFont("Helvetica-Oblique", 12)
        c.drawString(50, y, f"[PoC collaborator link inserted]")
        # También puedes crear un link clickeable si quieres:
        c.linkURL(collaborator_url, (50, y-2, 400, y+12))

def generate_pdf(filename, target_size_mb, verbose=False, endpoint_url=None, poc=False):
    target_size_bytes = target_size_mb * 1024 * 1024
    width, height = letter

    # Calcular tamaño promedio de página dinámicamente
    test_buffer = io.BytesIO()
    test_canvas = canvas.Canvas(test_buffer, pagesize=letter)
    draw_page(test_canvas, width, height)
    test_canvas.showPage()
    test_canvas.save()
    avg_page_bytes = len(test_buffer.getvalue())
    if verbose:
        print(f"[i] Tamaño estimado por página: {avg_page_bytes} bytes")

    # Crear PDF real en memoria
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    estimated_size = 0

    # Generar páginas normales hasta acercarse al tamaño objetivo
    while estimated_size < target_size_bytes * 0.9:
        draw_page(c, width, height)
        c.showPage()
        estimated_size += avg_page_bytes

    # Última página PoC si corresponde
    if poc and endpoint_url:
        draw_page(c, width, height, poc=True, collaborator_url=endpoint_url)
        c.showPage()

    # Guardar canvas solo UNA vez
    c.save()
    pdf_data = buffer.getvalue()

    # Guardar PDF temporal
    temp_file = filename + ".tmp"
    with open(temp_file, "wb") as f:
        f.write(pdf_data)

    # Agregar OpenAction PoC si corresponde
    if poc and endpoint_url:
        with pikepdf.Pdf.open(temp_file, allow_overwriting_input=True) as pdf:
            pdf.Root.OpenAction = pdf.make_indirect(
                pikepdf.Dictionary({
                    "/S": pikepdf.Name("/URI"),
                    "/URI": endpoint_url
                })
            )
            pdf.save(temp_file)

    # Rellenar hasta tamaño deseado
    with open(temp_file, "rb") as f:
        final_data = f.read()

    current_size = len(final_data)
    if current_size < target_size_bytes:
        padding = b"% filler " * ((target_size_bytes - current_size) // 9)
        final_data += padding

    # Guardar PDF final y eliminar temporal
    with open(filename, "wb") as f:
        f.write(final_data)
    os.remove(temp_file)

    if verbose:
        final_size_mb = os.path.getsize(filename) / (1024 * 1024)
        print(f"[✓] PDF generado: {filename} ({final_size_mb:.2f} MB)")



def main():
    parser = argparse.ArgumentParser(description="Generador de PDFs de prueba con PoC OpenAction")
    parser.add_argument("-s", "--size", required=True, help="Tamaños en MB, separados por coma (ej: 1,5,10)")
    parser.add_argument("-px", "--prefix", default="test", help="Prefijo del nombre de archivo")
    parser.add_argument("-sx", "--suffix", default="", help="Sufijo del nombre de archivo")
    parser.add_argument("-i", "--iterator", choices=["d", "a"], default="d", help="Iterador: d=dígitos, a=letras")
    parser.add_argument("-v", "--verbose", action="store_true", help="Modo verbose")
    parser.add_argument("--eu", "--endpoint-url", dest="endpoint_url", help="Endpoint URL para PoC OpenAction")
    parser.add_argument("--poc", action="store_true", help="Habilitar PoC OpenAction en el PDF")

    args = parser.parse_args()

    sizes = [int(x) for x in args.size.split(",")]

    if args.iterator == "d":
        iterator_values = [str(i+1) for i in range(len(sizes))]
    else:
        iterator_values = list(string.ascii_lowercase[:len(sizes)])

    for size, it in zip(sizes, iterator_values):
        filename = f"{args.prefix}{args.suffix}{it}.pdf"
        if args.verbose:
            print(f"[+] Generando {filename} de ~{size} MB ...")
        generate_pdf(
            filename,
            size,
            verbose=args.verbose,
            endpoint_url=args.endpoint_url,
            poc=args.poc
        )

if __name__ == "__main__":
    main()
