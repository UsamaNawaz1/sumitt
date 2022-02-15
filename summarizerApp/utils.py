"""
    Custom utility class to hold custom functions, by degee
"""
import calendar
import datetime
# from Crypto.Cipher import AES 
import base64
from django.core.files.storage import FileSystemStorage
from django.core import serializers
from collections.abc import Iterable
from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from subscriptions.models import (Plan, Customer, Coupon, Setting)

class DgClass:
    
    today = datetime.date.today()

    # month = 2
    # print("last day of month is " + str(calendar.monthrange(year, month)[1]))

    start_week = today - datetime.timedelta(today.weekday())
    end_week = start_week + datetime.timedelta(7)
    month = today.month
    year = today.year
    if today.day > 25:
        today += datetime.timedelta(7)
    first_day_of_month = today.replace(day=1)
    last_day_of_month = today.replace(day=calendar.monthrange(year, month)[1])

    MASTER_KEY="Some-long-base-key-to-use-as-encryption-key"

    def getSettings():
        if settings.LIVE_MODE:
            setting = get_object_or_404(Setting, pk=1)
        else:
            setting = get_object_or_404(Setting, pk=2)
        return setting

    def dd(request, data=''):
        try:
            scheme      = request.scheme
            server_name = request.META['SERVER_NAME']
            server_port = request.META['SERVER_PORT']
            remote_addr = request.META['REMOTE_ADDR']
            user_agent  = request.META['HTTP_USER_AGENT']
            path        = request.path
            method      = request.method
            session     = request.session
            cookies     = request.COOKIES

            get_data = {}
            for key, value in request.GET.lists():
                get_data[key] = value

            post_data = {}
            for key, value in request.POST.lists():
                post_data[key] = value

            files = {}
            for key, value in request.FILES.lists():
                files['name'] = request.FILES[key].name
                files['content_type'] = request.FILES[key].content_type
                files['size'] = request.FILES[key].size

            dump_data = ''
            query_data = ''
            executed_query = ''
            if data:
                if isinstance(data, Iterable):
                    if isinstance(data, QuerySet):
                        executed_query = data.query
                        query_data = serializers.serialize('json', data)
                    else:
                        dump_data = dict(data)
                else:
                    query_data = serializers.serialize('json', [data])


            msg = f'''
                <html>
                    <span style="color: red;"><b>Scheme</b></span>        : <span style="color: blue;">{scheme}</span><br>
                    <span style="color: red;"><b>Server Name</b></span>   : <span style="color: blue;">{server_name}</span><br>
                    <span style="color: red;"><b>Server Port</b></span>   : <span style="color: blue;">{server_port}</span><br>
                    <span style="color: red;"><b>Remote Address</b></span>: <span style="color: blue;">{remote_addr}</span><br>
                    <span style="color: red;"><b>User Agent</b></span>    : <span style="color: blue;">{user_agent}</span><br>
                    <span style="color: red;"><b>Path</b></span>          : <span style="color: blue;">{path}</span><br>
                    <span style="color: red;"><b>Method</b></span>        : <span style="color: blue;">{method}</span><br>
                    <span style="color: red;"><b>Session</b></span>       : <span style="color: blue;">{session}</span><br>
                    <span style="color: red;"><b>Cookies</b></span>       : <span style="color: blue;">{cookies}</span><br>
                    <span style="color: red;"><b>Get Data</b></span>      : <span style="color: blue;">{get_data}</span><br>
                    <span style="color: red;"><b>Post Data</b></span>     : <span style="color: blue;">{post_data}</span><br>
                    <span style="color: red;"><b>Files</b></span>         : <span style="color: blue;">{files}</span><br>
                    <span style="color: red;"><b>Executed Query</b></span>: <span style="color: blue;"><br>{executed_query}</span><br>
                    <span style="color: red;"><b>Query Data</b></span>    : <span style="color: blue;"><br>{query_data}</span><br>
                    <span style="color: red;"><b>Dump Data</b></span>     : <span style="color: blue;"><br>{dump_data}</span><br>
                </html>
            '''

            return msg
        except ObjectDoesNotExist:
            return False

    def uploadFile(file):
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        return uploaded_file_url

    def dg_b64encode(text):
        return base64.urlsafe_b64encode(text.encode('UTF-8')).decode('ascii')

    def dg_b64decode(text):
        pw_bytes = text.encode('utf-8')
        # return pw_bytes.decode("utf-8")
        return base64.b64decode(pw_bytes).decode("utf-8")

    # def encrypt_val(clear_text):
    #     enc_secret = AES.new(MASTER_KEY[:32])
    #     tag_string = (str(clear_text) +
    #                 (AES.block_size -
    #                 len(str(clear_text)) % AES.block_size) * "\0")
    #     cipher_text = base64.b64encode(enc_secret.encrypt(tag_string))

    #     return cipher_text

    # def decrypt_val(cipher_text):
    #     dec_secret = AES.new(MASTER_KEY[:32])
    #     raw_decrypted = dec_secret.decrypt(base64.b64decode(cipher_text))
    #     clear_val = raw_decrypted.decode().rstrip("\0")
    #     return clear_val
