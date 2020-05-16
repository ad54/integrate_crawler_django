Hello Geeks,

In this tutorial We are going to learn **'To integrate crawler developed in scrapy with django'**.

We are going to make an app which take keyword from user and extract the quote related to that keyword from  [this site] (http://quotes.toscrape.com/).

First We are going to make a crawer in scrapy. That will extract data and store it in database. The database used is MySQL.  If you don't have idea about scrapy crawler please visit here ('http://')

Now We will make a django project using command. 
```
djangoadmin startproject quotes_scrape
```
Then we will create an app named 'request_handler'
```
cd quotes_scrape
python manage.py startapp request_handler
```

add name of the app  'request_handler' in list 'INSTALLED_APPS' in settings.py.

go to views.py file in directory named 'request_handler'. Create one view for inserting keyword. For that we will create an html file (template) and render the same

```
def home(request):
    return render(request, "index.html")
```
Now we will create second view for handling the request and getting data and send json response

```
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
            con = pymysql.connect(host="localhost", user="root", passwd="Arihant", db="quotes_scrape",
                                  cursorclass=pymysql.cursors.DictCursor)
            cursor = con.cursor()
            # get records from database of particular database
            cursor.execute(qry)

            values = cursor.fetchall()
            print(values)
        else:
            sleep(1)
    
    return JsonResponse(data=values, safe=False)

```

So for deploying our crawler we will use 'scrapyd'
for installation you can refer [https://scrapyd.readthedocs.io/en/stable/install.html#installing-scrapyd-generic-way] (https://scrapyd.readthedocs.io/en/stable/install.html#installing-scrapyd-generic-way)

```
pip install scrapyd

```
if you get any error like 'windows scrapyd-deploy is not recognized' then can install

```
pip install git+https://github.com/scrapy/scrapyd-client
```

Now edit conf file of crawler : scrapy.cfg
uncomment the line below 
[deploy:local]

start scrapyd using command

```
start scrapyd
```
You can check in browser by going to :  http://localhost:6800/

deploy spider, you need write the name whatever in config file with deploy for e.g [deploy:local]

```
scrapyd-deply local
```

go to home page and enter keyword

![home page]()

after crawling complete you will get result in json format
![result page]()


Thank you,

Happy Coding