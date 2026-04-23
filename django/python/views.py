from django.shortcuts import render, redirect, get_object_or_404
from .models import ESGReport
from prism_esg.modules.pipeline import run_full_pipeline


from prism_esg.modules.pdf_loader import extract_pages
from prism_esg.modules.chunking import chunk_page
from prism_esg.modules.embeddings import build_embeddings
from prism_esg.modules.retrieval import semantic_search

def search_view(request):

    results = None

    if request.method == "POST":

        query = request.POST.get("query")

        pdf_path = "media/reports/HUL_2023-2024_BRSR_zHbKIW2.pdf"

        chunks = []

        # Extract pages and chunk them
        for page_number, text in extract_pages(pdf_path):

            page_chunks = chunk_page(
                document_id="TEST_DOC",
                page_number=page_number,
                raw_text=text
            )

            chunks.extend(page_chunks)

        # Create embeddings
        embeddings = build_embeddings(chunks)

        # Run semantic search
        results = semantic_search(query, embeddings, chunks)

    return render(request, "dashboard/search.html", {"results": results})


# HOME PAGE
def home(request):
    return render(request, 'dashboard/home.html')


def contact(request):
    return render(request, "dashboard/contact.html")


def about(request):
    return render(request, "dashboard/about.html")


# UPLOAD REPORT
def upload_report(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        pdf = request.FILES.get('pdf_file')

        # Save initial report
        report = ESGReport.objects.create(
            title=title,
            pdf_file=pdf,
            status='pending'
        )

        pdf_path = report.pdf_file.path

        # -----------------------
        # 🔥 RUN ML PIPELINE
        # -----------------------
        result = run_full_pipeline(pdf_path, str(report.id))

        scores = result["scores"]
        full_text = result["full_text"]

        # -----------------------
        # SAVE RESULTS TO DB
        # -----------------------
        report.environmental_score = scores.get("E", 0)
        report.social_score = scores.get("S", 0)
        report.governance_score = scores.get("G", 0)
        report.extracted_text = full_text
        report.status = "processed"
        report.save()

        return redirect('report_list')

    return render(request, 'dashboard/upload.html')


# REPORT LIST PAGE
def report_list(request):
    reports = ESGReport.objects.all().order_by('-uploaded_at')
    return render(request, 'dashboard/reports.html', {'reports': reports})


# DELETE REPORT
def delete_report(request, report_id):
    report = get_object_or_404(ESGReport, id=report_id)
    report.delete()
    return redirect('report_list')


# EDIT REPORT
def edit_report(request, report_id):
    report = get_object_or_404(ESGReport, id=report_id)

    if request.method == "POST":
        new_title = request.POST.get("title")
        new_file = request.FILES.get("pdf_file")  # ✅ SAFE

        # ✅ Update title if provided
        if new_title and new_title.strip():
            report.title = new_title

        # ✅ Update file only if uploaded
        if new_file:
            report.pdf_file = new_file

            # OPTIONAL: re-run pipeline if file changed
            pdf_path = report.pdf_file.path
            result = run_full_pipeline(pdf_path, str(report.id))

            scores = result["scores"]
            report.environmental_score = scores.get("E", 0)
            report.social_score = scores.get("S", 0)
            report.governance_score = scores.get("G", 0)
            report.extracted_text = result["full_text"]
            report.status = "processed"

        report.save()
        return redirect('report_list')

    return render(request, 'dashboard/edit_report.html', {'report': report})


# DASHBOARD VIEW
def dashboard(request):
    reports = ESGReport.objects.all()

    esg_data = {
        "environmental": 72,
        "social": 65,
        "governance": 80
    }

    return render(request, 'dashboard/dashboard.html', {
        'reports': reports,
        'esg_data': esg_data
    })


# ANALYTICS PAGE
def analytics(request):
    reports = ESGReport.objects.all()

    total_reports = reports.count()
    processed_reports = reports.filter(status='processed').count()
    pending_reports = reports.filter(status='pending').count()

    context = {
        "reports": reports,
        "total_reports": total_reports,
        "processed_reports": processed_reports,
        "pending_reports": pending_reports,
    }

    return render(request, "dashboard/analytics.html", context)


# PROFILE
def profile(request):
    return render(request, 'dashboard/profile.html')


def report_detail(request):
    return render(request, "dashboard/report_detail.html")


def gap_analysis(request):
    return render(request, "dashboard/gap_analysis.html")
