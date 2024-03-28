from django.urls import path
from pdfprocessor.views import pdf_upload


urlpatterns = [
    # ...
    path('pdf-upload/', pdf_upload, name='pdf-upload'),
    # ...
]