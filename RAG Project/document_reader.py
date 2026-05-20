from docx import Document

def read_docx(file_path):

    doc = Document(file_path)

    text = []

    for para in doc.paragraphs:

        if para.text.strip():

            text.append(para.text)

    return "\n".join(text)