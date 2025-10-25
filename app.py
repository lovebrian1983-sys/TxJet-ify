import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from PIL import Image

st.title("PDF Banner Adder")

# Upload PDF
uploaded_pdf = st.file_uploader("Upload your PDF", type="pdf")

# Banner image
banner_path = "banner.jpg"

if uploaded_pdf is not None:
    original_pdf = PdfReader(uploaded_pdf)
    output_pdf = PdfWriter()

    # First page with banner
    first_page = original_pdf.pages[0]
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    banner = Image.open(banner_path)
    banner_width, banner_height = banner.size

    page_width = first_page.mediabox.width
    page_height = first_page.mediabox.height
    scale = page_width / banner_width
    banner_width_scaled = banner_width * scale
    banner_height_scaled = banner_height * scale

    can.drawImage(banner_path, 0, page_height - banner_height_scaled,
                  width=banner_width_scaled, height=banner_height_scaled)
    can.save()
    packet.seek(0)

    banner_pdf = PdfReader(packet)
    first_page.merge_page(banner_pdf.pages[0])
    output_pdf.add_page(first_page)

    # Add remaining pages
    for i in range(1, len(original_pdf.pages)):
        output_pdf.add_page(original_pdf.pages[i])

    # Prepare for download
    pdf_bytes = BytesIO()
    output_pdf.write(pdf_bytes)
    pdf_bytes.seek(0)

    st.download_button(
        label="Download PDF with Banner",
        data=pdf_bytes,
        file_name="banner_added.pdf",
        mime="application/pdf"
    )
