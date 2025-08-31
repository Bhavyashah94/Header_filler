import streamlit as st
from docxtpl import DocxTemplate
import subprocess
import tempfile
import os
import io

st.title("Academic Header Page Filler - PDF Only")

with st.form("header_form"):
    year = st.text_input("Academic Year", "2025-26", max_chars=9)
    sem = st.text_input("Semester", max_chars=8)
    class_ = st.text_input("Class", max_chars=10)
    batch = st.text_input("Batch", max_chars=10)
    rollNo = st.text_input("Roll No.", max_chars=10)
    name = st.text_input("Name", max_chars=40)

    st.subheader("Subject")
    subject = st.text_input("Line 1 (max 58 chars)", max_chars=58, key="subject1")
    subject2 = st.text_input("Line 2 (optional, max 46 chars)", max_chars=46, key="subject2")

    number = st.text_input("Experiment / Assignment No.", max_chars=10)

    st.subheader("Title")
    title = st.text_input("Line 1 (max 60 chars)", max_chars=60, key="title1")
    title2 = st.text_input("Line 2 (optional, max 66 chars)", max_chars=66, key="title2")

    dop = st.date_input("Date of Performance")
    dos = st.date_input("Date of Submission")

    submitted = st.form_submit_button("Generate PDF")

if submitted:
    # --- Use temporary file for DOCX ---
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
        docx_file = tmp_docx.name

    # Create DOCX
    doc = DocxTemplate("Header.docx")
    context = {
        "year": year,
        "sem": sem,
        "class": class_,
        "batch": batch,
        "rollNo": rollNo,
        "name": name,
        "subject": subject,
        "subject2": subject2,
        "number": number,
        "title": title,
        "title2": title2,
        "dop": dop.strftime("%d-%m-%Y"),
        "dos": dos.strftime("%d-%m-%Y"),
    }
    doc.render(context)
    doc.save(docx_file)

    # --- Convert DOCX -> PDF ---
    output_dir = os.path.dirname(docx_file)
    subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_dir,
        docx_file
    ], check=True)

    # PDF path
    pdf_file = os.path.join(output_dir, os.path.splitext(os.path.basename(docx_file))[0] + ".pdf")

    # --- Provide PDF download ---
    with open(pdf_file, "rb") as f:
        pdf_bytes = io.BytesIO(f.read())

    friendly_name = f"{subject.replace(' ','_')}_{number}.pdf"
    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name=friendly_name,
        mime="application/pdf"
    )

    # Clean up temp files
    os.remove(docx_file)
    os.remove(pdf_file)
