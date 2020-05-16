from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from scrapyd_api import ScrapydAPI

import pymysql
from time import sleep
import datetime

# Create your views here.
def home(request):
    return render(request, "index.html")

def handle_request(request):
    # get keyword from input
    keyword = request.GET.get('keyword')

    # create an object of scrapyd API
    scrapyd = ScrapydAPI("http://localhost:6800")
    request_time = datetime.datetime.now()

    # create a job id
    job_id = scrapyd.schedule(project='quotes_scrape', spider='quotes_crawler', keyword=keyword,
                              request_time=request_time)
    qry = f"select * from quotes where job_id = '{job_id}'"

    job_status = "running"

    values = []

    # check for job status
    while job_status != "finished":
        job_status = scrapyd.job_status(project='quotes_scrape', job_id=job_id)
        if job_status == 'finished':

            # database connection
            con = pymysql.connect(host="localhost", user="root", passwd="", db="quotes_scrape",
                                  cursorclass=pymysql.cursors.DictCursor)
            cursor = con.cursor()
            # get records from database of particular database
            cursor.execute(qry)

            values = cursor.fetchall()
            print(values)
        else:
            sleep(1)

    return JsonResponse(data=values, safe=False)


