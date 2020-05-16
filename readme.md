Hello Guys,


In this tutorial We are going to learn **How To integrate crawler developed in scrapy with django**.

- Crawler (backend) : scrapy
- Frontend : django
- database : MySQl

We are going to make an app which takes keyword from user and extract the quotes related to that keyword from  [this site](http://quotes.toscrape.com/).

First We are going to make a crawer in scrapy. That will extract data and store it in database. The database used is MySQL.  If you don't have idea about scrapy crawler please visit here https://docs.scrapy.org/en/latest/intro/tutorial.html

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
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'request_handler'
]
```

go to views.py file in directory named 'request_handler'. Create one view for inserting keyword. For that we will create an html file (template) and render the same

```
def home(request):
    return render(request, "index.html")
```
Now we will create second view for handling the request and getting data and send json response.
We pass keyword from django to scrapy. We set job_id , use the same job_id in scrapy for identify request and  use the same job_id in django for getting data from database.

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
for installation you can refer [https://scrapyd.readthedocs.io/en/stable/install.html#installing-scrapyd-generic-way](https://scrapyd.readthedocs.io/en/stable/install.html#installing-scrapyd-generic-way)

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
You can check in browser by going to :  _http://localhost:6800/_

deploy spider, you need write the name whatever in config file with deploy for e.g [deploy:local]

```
scrapyd-deply local
```

go to home page and enter keyword

![home page](https://github.com/ad54/integrate_crawler_django/blob/master/screenshot/home_page.png)

after crawling complete you will get result in json format
![result page](https://github.com/ad54/integrate_crawler_django/blob/master/screenshot/result_page.png)


Thank you,

Happy Coding