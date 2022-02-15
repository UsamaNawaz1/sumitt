from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
import logging
import csv
import io
import base64
from summarizerApp.utils import DgClass
from summarizerApp.summarize_util import SummarizeUtil
from django.http import HttpResponse

from documents.models import (Document, Usage)
from documents.forms import DocumentForm
from subscriptions.models import (Plan, Customer, Coupon, Setting)
import stripe
import datetime

from pprint import pprint
import time
from django.conf import settings


logger = logging.getLogger(__name__)


def home(request):
    plans = Plan.objects
    plan1 = get_object_or_404(Plan, pk=1)
    plan2 = get_object_or_404(Plan, pk=2)

    # print("price ", plan1.price)
    difference = (float(plan1.price) * 12) - float(plan2.price)
    return render(
        request,
        "documents/home.html",
        {"plans": plans, "plan1": plan1, "plan2": plan2, 'difference': difference},
    )


@login_required
def dashboard(request):
    upgrade = False
    setting = DgClass.getSettings()
    stripe.api_key = setting.stripe_api_key
    user_document_count = Document.objects.filter(
        user_id=request.user.id).count()
    document_count = Document.objects.count()
    user_count = User.objects.count()
    customer = Customer.objects.filter(user_id=request.user.id).first()
    if customer and customer.stripe_subscription_id:
        if not customer.current_period_end:
            subscription = stripe.Subscription.retrieve(
                customer.stripe_subscription_id)
            customer.current_period_end = subscription.current_period_end
            customer.save()
        elif time.time() > float(customer.current_period_end):
            messages.info(
                request, ("Your current subscription has expired. Please upgrade your account"))
            customer.membership = False
            customer.save()
            upgrade = True
    else:
        messages.info(
            request, ("You're currently on Basic Plan.. upgrade now to have more benefits!"))
        upgrade = True

    return render(
        request,
        "documents/dashboard.html", {
            'document_count': document_count,
            'user_document_count': user_document_count,
            'upgrade': upgrade,
            'user_count': user_count
        }
    )


@login_required
def summarize(request, document_id, sentences=''):
    customer = Customer.objects.filter(user_id=request.user.id).first()
    usage = Usage.objects.filter(user_id=request.user.id).first()
    if not usage:
        usage = Usage()
        usage.user = request.user        
        usage.count = 1
    if customer and customer.membership:
        pass
    elif request.user.is_superuser:
        usage.count = 1
    elif usage.count > 3:
        messages.info(
            request, ("You're have exceeededd your monthly limit. Upgrade now to have more benefits!"))
        return redirect('checkout', plan_id=1)

    usage.count = usage.count + 1
    d = datetime.datetime.now()
    if usage.current_month==d.strftime("%m"):
        pass
    else:
        usage.current_month = d.strftime("%m")
        usage.count = 1
    usage.save()
    document = get_object_or_404(Document, pk=document_id)
    if (document.user == request.user) or request.user.is_superuser:
        sentences = sentences if sentences else document.max_sentences
        info = SummarizeUtil.summarize(document, sentences)
        number_of_pages = info['pages']
        summary = info['summary']
    else:
        messages.error(request, "Can't access a document that isn't yours!")
        return redirect('documents')
    return render(
        request,
        "documents/summarize.html",
        {'document': document, "summary": summary, 'sentences': sentences,
            'number_of_pages': number_of_pages}
    )


@login_required
def documents(request):
    # document = get_object_or_404(Document, pk=4)
    # print(document.__dict__)
    documents = Document.objects.filter(user=request.user)
    return render(
        request,
        "documents/documents.html", {'documents': documents}
    )


@login_required
def document_add(request):
    uploaded_file_url = None
    document = DocumentForm()
    name = ""
    description = ""
    max_sentences = 10
    start_scan_page = 1
    end_scan_page = 200

    if request.method == "POST":
        document = DocumentForm(request.POST, request.FILES)
        file = request.FILES["file"]
        # print(file.__dict__)
        if not file.name.endswith(".pdf") and not file.name.endswith(".docx"):
            messages.error(request, "File must be word document or PDF")
            # print("File must be word document or PDF")
            temp = request.POST.dict()
            document.name = temp['name']
            document.description = temp['description']
            document.max_sentences = temp['max_sentences']
            document.start_scan_page = temp['start_scan_page']
            document.end_scan_page = temp['end_scan_page']
        else:
            if document.is_valid():
                document = document.save(commit=False)
                document.user = request.user
                document.save()
                messages.success(request, "Document saved")
                return redirect('documents')
            else:
                # pprint(document.errors)
                pass

    return render(
        request,
        "documents/document_add.html",
        {'uploaded_file_url': uploaded_file_url, 'document': document,
            'name': name, 'description': description, 'max_sentences': max_sentences, 'start_scan_page': start_scan_page, 'end_scan_page': end_scan_page}
    )


@login_required
def document_edit(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    name = document.name
    description = document.description
    max_sentences = document.max_sentences
    start_scan_page = document.start_scan_page
    end_scan_page = document.end_scan_page
    if request.method == "POST":
        temp = request.POST.dict()
        document.name = temp['name']
        document.description = temp['description']
        document.max_sentences = temp['max_sentences'] if temp['max_sentences'] else 10
        document.start_scan_page = temp['start_scan_page'] if temp['start_scan_page'] else 1
        document.end_scan_page = temp['end_scan_page'] if temp['end_scan_page'] else 200
        document.save()
        messages.success(request, "Document saved")
        return redirect('documents')

    return render(
        request,
        "documents/document_edit.html",
        {'document': document, 'name': name, 'description': description, 'max_sentences': max_sentences,
            'start_scan_page': start_scan_page, 'end_scan_page': end_scan_page}
    )


@login_required
@staff_member_required
def document_delete(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    if (document.user == request.user) or request.user.is_superuser:
        document.delete()
        messages.success(request, "Document deleted")
    else:
        messages.error(request, "Can't delete a document that isn't yours!")
    return redirect('documents')


@login_required
@staff_member_required
def users(request):
    # user = User.objects.all()
    users = User.objects.annotate(num_documents=Count('document'))
    # print("users ", users)
    return render(
        request,
        "documents/users.html", {'users': users}
    )


@login_required
@staff_member_required
def admin_documents(request):
    documents = Document.objects.all()
    return render(
        request,
        "documents/admin_documents.html",  {'documents': documents}
    )


def terms(request):
    return render(
        request,
        "documents/terms.html"
    )


def policy(request):
    return render(
        request,
        "documents/policy.html"
    )
