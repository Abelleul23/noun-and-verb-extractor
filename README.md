PDF Upload and Text Extraction
This Django application allows users to upload PDF files and extract text from them. The extracted text is then processed to identify nouns and verbs using natural language processing techniques.

Installation
Clone the repository:

Copy
git clone <repository-url>
Create a virtual environment and activate it:

Copy
python3 -m venv myenv
source myenv/bin/activate
Install the required dependencies:

basic
Copy
pip install -r requirements.txt
Set up a MongoDB database and update the connection URI in the code:

Copy
client = MongoClient('mongodb://localhost:27017')  # Replace with your connection URI
Run the Django development server:

Copy
python manage.py runserver
Access the application in your web browser at http://localhost:8000.

Usage
Upload a PDF file by navigating to the PDF upload page.

The uploaded file will be processed, and the text will be extracted using PyMuPDF library.

The extracted text will be divided into paragraphs, and nouns and verbs will be identified using NLTK (Natural Language Toolkit).

The identified nouns and verbs will be stored in a MongoDB database.

The processed data will be displayed on the web page, showing the extracted nouns and verbs.
