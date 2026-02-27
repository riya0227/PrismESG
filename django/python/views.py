from django.shortcuts import render, redirect, get_object_or_404
from .models import ESGReport

from prism_esg.modules.pipeline import run_full_pipeline

# HOME PAGE
def home(request):
    return render(request, 'dashboard/home.html')


# UPLOAD REPORT
def upload_report(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        pdf = request.FILES.get('pdf_file')

        # Step 1: Save report initially
        report = ESGReport.objects.create(
            title=title,
            pdf_file=pdf,
            status='pending'
        )

        try:
            # Step 2: Extract text from saved PDF
            pdf_path = report.pdf_file.path
            full_text = ""

            for page_number, text in extract_pages(pdf_path):
                full_text += text + " "

            # Step 3: Save extracted text
            report.extracted_text = full_text
            report.status = 'processed'

        except Exception as e:
            print("Extraction Error:", e)
            report.status = 'incomplete'

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
        report.pdf_file = request.FILES['pdf_file']
        report.save()
        return redirect('report_list')

    return render(request, 'dashboard/edit_report.html', {'report': report})


def dashboard(request):
    reports = ESGReport.objects.all()

    # Temporary ESG scores (later from NLP)
    esg_data = {
        "environmental": 72,
        "social": 65,
        "governance": 80
    }

    return render(request, 'dashboard/dashboard.html', {
        'reports': reports,
        'esg_data': esg_data
    })


def analytics(request):
    reports = ESGReport.objects.all()

    # Temporary ESG data (later from NLP)
    esg_data = {
        "environmental": 70,
        "social": 60,
        "governance": 75
    }

    total_reports = reports.count()
    processed_reports = reports.filter(status='processed').count()
    pending_reports = reports.filter(status='pending').count()

    context = {
        "reports": reports,
        "esg_data": esg_data,
        "total_reports": total_reports,
        "processed_reports": processed_reports,
        "pending_reports": pending_reports,
    }

    return render(request, "dashboard/analytics.html", context)


from django.contrib.auth.decorators import login_required

def profile(request):
    return render(request, 'dashboard/profile.html')

def report_detail(request):
    return render(request, "dashboard/report_detail.html")

def gap_analysis(request):
    return render(request, "dashboard/gap_analysis.html")


