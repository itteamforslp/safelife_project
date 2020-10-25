from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.db import connection
from django.http import HttpResponseRedirect
import datetime
from django.http import JsonResponse
from django.db.models import Count
from documents.models import Document, DocumentType
from django.core.exceptions import PermissionDenied
# Create your views here.

@login_required(login_url = '/users')
def home(request, doc_id):
        super = request.user.is_superuser
        with connection.cursor() as cursor:
                cursor.execute('SELECT D.id, D.doc_name, DT.doc_type_id '
                                'FROM documents AS D, document_type as DT '
                                'WHERE D.doc_type_id = DT.doc_type_id '
                                'ORDER BY DT.doc_type_id ')
                doc_list = cursor.fetchall()

        
        categories = DocumentType.objects.select_related().raw('SELECT * '
                                                          'FROM document_type AS DT '
                                                          'ORDER BY DT.doc_type ')
        
        current_doc = Document.objects.filter(id=doc_id)
                                                        
        if super is True:
            template = loader.get_template('documents/admindocs.html')
        else:
            template = loader.get_template('documents/teacherdocs.html')
        context = {
                'doc_list': doc_list,
                'categories': categories,
                'current_doc': current_doc
        }

    # Render the template to the user
        return HttpResponse(template.render(context, request))

@login_required(login_url = '/users')
def default(request):
        super = request.user.is_superuser
        with connection.cursor() as cursor:
                cursor.execute('SELECT D.id, D.doc_name, DT.doc_type_id '
                                'FROM documents AS D, document_type as DT '
                                'WHERE D.doc_type_id = DT.doc_type_id '
                                'ORDER BY DT.doc_type_id ')
                doc_list = cursor.fetchall()

        
        categories = DocumentType.objects.select_related().raw('SELECT * '
                                                          'FROM document_type AS DT '
                                                          'ORDER BY DT.doc_type ')
        
                                                        
        if super is True:
            template = loader.get_template('documents/admindocsdefault.html')
        else:
            template = loader.get_template('documents/teacherdocsdefault.html')
        context = {
                'doc_list': doc_list,
                'categories': categories
        }

    # Render the template to the user
        return HttpResponse(template.render(context, request))

@login_required
def redirect(request):
    if user.is_superuser:
        return redirect('/administrator')
    else:
        return redirect('/teacher')