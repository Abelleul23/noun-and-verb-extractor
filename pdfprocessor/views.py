from django.shortcuts import render
from .forms import UploadFileForm
from pymongo import MongoClient
import nltk
import tempfile

from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from .models import PDF
from .serializers import PDFSerializer
import fitz  # PyMuPDF library

@api_view(['GET', 'POST'])
def pdf_upload(request):
    if request.method == 'GET':
        # Create an empty form instance for consistency (optional)
        form = UploadFileForm()
        return render(request, 'pdf_upload.html', {'form': form})

    else:
        parser_classes = [FileUploadParser]
        data = request.data
        file = request.FILES.get('file')

        if not file:
            return Response({'error': 'No file uploaded.'}, status=400)

        if not file.name.lower().endswith(".pdf"):
            return Response({'error': 'Invalid file format. Only PDF files are allowed.'}, status=400)

        # Process the uploaded file
        try:
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)

                # Use PyMuPDF for text extraction
                doc = fitz.open(temp_file.name)
                text = ""
                for page in doc:
                    text += page.get_text("text")  # Extract text using "text" argument

                # Process the extracted text
                paragraphs = text.strip().split('\n\n')
                nouns, verbs = [], []
                for paragraph in paragraphs:
                    tokens = nltk.word_tokenize(paragraph.lower())
                    tagged_tokens = nltk.pos_tag(tokens)
                    nouns.extend([word for word, pos in tagged_tokens if pos[:1] == 'N'])
                    verbs.extend([word for word, pos in tagged_tokens if pos[:1] == 'V'])

                # Prepare context data
                nouns_str = ','.join(set(nouns))  # Join and remove duplicates
                verbs_str = ','.join(set(verbs))
                #print(nouns_str)

                # Save data (optional, uncomment if needed)
                client = MongoClient('mongodb://localhost:27017')  # Replace with your connection URI
                db = client['pdf_db']
                collection = db['pdf_coll']

                document = {
                    'file': file.name,
                    'nouns': ','.join(set(nouns)),  # Remove duplicates
                    'verbs': ','.join(set(verbs))
                }

                collection.insert_one(document)
                pdf = PDF(file=file.name, nouns=','.join(set(nouns)), verbs=','.join(set(verbs)))
                serializer = PDFSerializer(pdf)
                return render(request, 'pdf_upload.html', {'nouns': nouns_str, 'verbs': verbs_str})
        except Exception as e:
            return Response({'error': f'Error processing PDF: {str(e)}'}, status=400)

    return Response({'error': 'Invalid request method. Only POST allowed.'}, status=400)


