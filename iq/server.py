from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader


from iq import es
from iq.language import pluralize, decimal, humanize

app = FastAPI()
env = Environment(loader=FileSystemLoader('templates'))
env.filters['pluralize'] = pluralize
env.filters['decimal'] = decimal
env.filters['humanize'] = humanize

templates = Jinja2Templates(directory="templates")
templates.env = env 

app.mount("/static", StaticFiles(directory="static"), name="static")


def pluralize(count, singular, plural=None):
    if count == 1:
        return singular
    else:
        return plural if plural else singular + 's'



@app.get("/", response_class=HTMLResponse)
async def start(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/q", response_class=HTMLResponse)
async def search(request: Request, query: str = Query(None)):
    es_query = {
        "query": {
            "query_string": {
                "query": query
            }
        },
        "_source": ["title", "url", "last_seen"],
        "highlight": {
            "fields": {
                "paragraphs": {}
            }
        }
    }
    response = es.search(index='webdocuments', body=es_query)

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "query": query, 
        "hits": response.get('hits'), 
        "es_time": response.get('took')
    })
