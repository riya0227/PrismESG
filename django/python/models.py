from django.db import models

class ESGReport(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('incomplete', 'Incomplete'),
    ]

    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    extracted_text = models.TextField(blank=True, null=True)

    environmental_score = models.FloatField(default=0)
    social_score = models.FloatField(default=0)
    governance_score = models.FloatField(default=0)

    def __str__(self):
        return self.title
