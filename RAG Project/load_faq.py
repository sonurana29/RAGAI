from document_reader import read_docx

from workflow import graph

from qdrant_service import create_collection


create_collection("faq_documents")

text = read_docx("wealth_management_faq.docx")

graph.invoke({
    "document_text": text
})

print("Document stored successfully")