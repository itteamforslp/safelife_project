from django.contrib import admin
from .models import Document, DocumentType
# Register your models here.

class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('doc_type', 'doc_type_id')
    exclude = ['doc_type_id',]

class DocumentAdmin(admin.ModelAdmin):
    model = Document
    exlude =['id',]

admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentType, DocumentTypeAdmin)