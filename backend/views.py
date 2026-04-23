# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json

from ingestion.pipeline import process_pdf
from chatbot import answer_query
from llm import HybridLLM
from model_loader import load_embedding_model

from storage.document_store import save_document, load_document
from storage.metadata_db import create_user, add_document, list_documents

# -------- INIT --------
embedding_model = load_embedding_model()


# ---------------------------
# CREATE USER
# ---------------------------
@csrf_exempt
def create_user_view(request):
    user_id = create_user()
    return JsonResponse({"user_id": user_id})


# ---------------------------
# UPLOAD PDF
# ---------------------------
@csrf_exempt
def upload_pdf(request):
    if request.method == "POST":

        user_id = request.POST.get("user_id")
        pdf_file = request.FILES.get("file")

        if not user_id or not pdf_file:
            return JsonResponse({"error": "Missing user_id or file"}, status=400)

        # -------- SAVE TEMP FILE --------
        os.makedirs("temp", exist_ok=True)
        file_path = os.path.join("temp", pdf_file.name)

        with open(file_path, "wb+") as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)

        # -------- CREATE DOC ID --------
        doc_id = add_document(user_id, pdf_file.name)

        # -------- PROCESS PDF --------
        result = process_pdf(file_path, doc_id)

        # -------- SAVE DOCUMENT --------
        save_document(
            doc_id,
            {"chunks": result["chunks"]},
            result["faiss_index"]
        )

        return JsonResponse({
            "message": "PDF uploaded and processed",
            "doc_id": doc_id
        })


# ---------------------------
# LIST DOCS
# ---------------------------
@csrf_exempt
def list_docs(request):
    user_id = request.GET.get("user_id")

    if not user_id:
        return JsonResponse({"error": "Missing user_id"}, status=400)

    docs = list_documents(user_id)
    return JsonResponse(docs, safe=False)


# ---------------------------
# ASK QUESTION
# ---------------------------
@csrf_exempt
def ask_question(request):
    if request.method == "POST":

        try:
            body = json.loads(request.body)
        except:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        doc_id = body.get("doc_id")
        query = body.get("query")

        if not doc_id or not query:
            return JsonResponse({"error": "Missing doc_id or query"}, status=400)

        llm = HybridLLM(mode="gemini")

        # ✅ NEW CORRECT CALL
        result = answer_query(
            query,
            doc_id,
            embedding_model,
            llm
        )

        return JsonResponse(result)