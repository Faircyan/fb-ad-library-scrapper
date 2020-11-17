import os
import requests
import psycopg2
import hello.downloader as downloader
import logging

from django.shortcuts import render
from django.http import HttpResponse


from .models import Greeting

connection = None


def index(request):
    # return HttpResponse('Hello from Python!')
    # page = RenderPage(json)
    # todo handle here
    return render(request, "index.html")

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def GetData(link):
    return downloader.DownloadData(link)

def OpenPublisherPage(request, link):
    
    names, data, publisherName = GetData(link)

    return render(request, 'publisher.html',{'datas': data, "names":names, "publisherName":publisherName})

#    sql = """insert into public."Publisher" values(%s) """
"""   value = ('Blue Duck')
    result = None
    try:

        # connect to the PostgreSQL database
        conn = psycopg2.connect(user="postgres", password= "", host="127.0.0.1", port="5432", database="AdLibrary")
        # create a new cursor
        cur = conn.cursor()

        # execute the INSERT statement
        cur.execute(sql, [value])

        # get the generated id back

        # commit the changes to the database
        conn.commit()

        result = cur.fetchall();

        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()""" 