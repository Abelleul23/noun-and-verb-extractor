from django.db import models
from pymongo import MongoClient

class PDF(models.Model):
    file = models.CharField(max_length=255)
    nouns = models.TextField()
    verbs = models.TextField()

    def save(self, *args, **kwargs):
        client = MongoClient('mongodb://localhost:27017')
        db = client['pdf_db']
        collection = db['pdf_coll']
        
        document = {
            'file': self.file,
            'nouns': self.nouns,
            'verbs': self.verbs
        }
        
        collection.insert_one(document)
        
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'pdf_db'