import streamlit as st
from docxtpl import DocxTemplate

st.title("Academic Header Page Filler")

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

    submitted = st.form_submit_button("Generate DOCX")

if submitted:
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
    safe_subject = subject.replace(" ", "_")
    safe_number = number.replace(" ", "_")
    output_file = f"{safe_subject}_{safe_number}.docx"

    doc.save(output_file)

    with open(output_file, "rb") as f:
        st.download_button("Download Filled Header", f, file_name=output_file)
