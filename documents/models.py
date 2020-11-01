from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
# Create your models here.

class DocumentType(models.Model):
    doc_type_id = models.AutoField(primary_key=True)
    doc_type = models.CharField(max_length=50)
    def __str__(self):
        return self.doc_type

    class Meta:
        db_table = 'document_type'

class Document(models.Model):
    id = models.AutoField(primary_key=True)
    doc_name = models.CharField(max_length=50)
    doc_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    preview_link = models.CharField(max_length=280)
    download_link = models.CharField(max_length=280)

    def __str__(self):
        return self.doc_name

    class Meta:
        db_table = 'documents'

