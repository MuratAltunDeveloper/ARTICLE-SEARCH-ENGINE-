from elasticsearch import Elasticsearch
from fastapi import FastAPI, requests
import httpx
from pymongo import server_api

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

from pymongo.collection import Collection
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId

from typing import List, Optional, Dict
from dotenv import load_dotenv
import os

from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from pydantic import BaseModel

from datetime import datetime

load_dotenv()

MONGODB_PASSWORD = "Murat2024.."
ELASTIC_PASSWORD ="unFdtF0YSNepVr35v6y2jQ"

MONGODB_URI = uri = f"mongodb+srv://murataltun01937373737:{MONGODB_PASSWORD}@cluster0.cilqspn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
BASE_URL = "https://dergipark.org.tr/tr/search"

app = FastAPI()

class ArticleDetails(BaseModel):
    id: str

class Filters(BaseModel):
    query: str | None = None
    pubtypes: list[str] = []
    publishers: list[str] = []
    years: str | None = None
    citations: str | None = None
    authors: list[str] = []

class Sortings(BaseModel):
    query: str | None = None
    pubtypes: list[str] = []
    publishers: list[str] = []
    years: str | None = None
    citations: str | None = None
    authors: list[str] = []
    sort_param: str
    sort_order: int

MONTHS = {
    "Ocak": "01",
    "Şubat": "02",
    "Mart": "03",
    "Nisan": "04",
    "Mayıs": "05",
    "Haziran": "06",
    "Temmuz": "07",
    "Ağustos": "08",
    "Eylül": "09",
    "Ekim": "10",
    "Kasım": "11",
    "Aralık": "12"
}

async def get_articles(query: str):
    search_keywords = [keyword.lower() for keyword in query.split(" ")]
    results = search_in_mongodb(search_keywords)

    if len(results) > 0:
        print("girdi2")
        return results
    
    results = await search_in_dergipark(query)
    
    return results

async def search_in_dergipark(query: str):
    params = {
        "q": quote_plus(query),
        "section": "articles"
    }

    articles = []
    
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(BASE_URL, params=params)

        if response.status_code != 200:
            print(f"Failed to fetch data from {BASE_URL}")
            return []

        selector = BeautifulSoup(response.content, "html.parser")
        results = selector.select("div.card.article-card.dp-card-outline")

        for result in results:
            if len(articles) == 10:
                break

            pubtype = result.select_one("span.badge.badge-secondary")

            if pubtype is None:
                continue
            
            pubtype = pubtype.text

            url = result.select_one("h5.card-title a").attrs.get("href")

            details = await get_details(url, client)

            if details is None:
                continue

            details["pubtype"] = pubtype
            details["url"] = url
            details["search_keywords"] = [query.lower() for query in query.split(" ")]

            articles.append(details)

    if len(articles) == 0:
        return []

    client = MongoClient(MONGODB_URI)

    db = client.get_database("CampusDB")
    collection = db.get_collection("Articles")
    
    collection.insert_many(articles)

    client.close()
    
    for article in articles:
        article["_id"] = str(article["_id"])

    return articles
    
async def get_details(url: str, client: httpx.AsyncClient):
    response = await client.get(url)

    if response.status_code != 200:
        return None
    
    selector = BeautifulSoup(response.content, "html.parser")
    main_portlet = selector.select_one("div#article-main-portlet")

    pdf_url = main_portlet.select_one("div#article-toolbar a").attrs.get("href")
    title = main_portlet.select_one("div.tab-pane.active h3.article-title").text
    publisher = selector.select_one("h1#journal-title").text

    table_trs = selector.select("table.record_properties.table tr")
    pubdates = ""

    for tr in table_trs:
        if tr.select_one("th").text == "Yayımlanma Tarihi":
            pubdates = tr.select_one("td").text

            if pubdates == "":
                pubdates = "Henüz yayınlanmamıştır"

            break

    print(pubdates)

    authors = [author.text.strip() for author in main_portlet.select("div.tab-pane.active p.article-authors a")]
    doi = main_portlet.select_one("div.tab-pane.active div.article-doi.data-section a")
    abstract = main_portlet.select_one("div.tab-pane.active div.article-abstract.data-section").text
    keywords = [keyword.text for keyword in main_portlet.select("div.tab-pane.active div.article-keywords.data-section a")]
    references = [reference.text for reference in main_portlet.select("div.tab-pane.active div.article-citations.data-section li")]
    citations = [citation.text for citation in selector.select("div.media.cited_by_item h5 a")]

    parts = pubdates.split(" ")

    return {
        "pdf_url": f"https://dergipark.org.tr{pdf_url}" if pdf_url else "",
        "title": title.strip() if title else "",
        "publisher": publisher,
        "pubdates": pubdates,
        "pubdates_timestamp": datetime(int(parts[2]), int(MONTHS[parts[1]]), int(parts[0])) if pubdates != "Henüz yayınlanmamıştır" else datetime.now(),
        "authors": authors,
        "doi": doi.text if doi is not None else "",
        "abstract": "".join(abstract).replace("Öz", "").strip() if abstract else "",
        "keywords": keywords,
        "references": references,
        "citations": len(citations)
    }

def search_in_mongodb(query: List[str], sort_by: str = None, sort_order: int = None):
    client = MongoClient(MONGODB_URI)

    print(query, sort_by, sort_order)

    db = client.get_database("CampusDB")
    collection = db.get_collection("Articles")

    articles = collection.find(
        {
            "search_keywords": {
                "$size": len(query),
                "$all": query
            }
        },
        {
            "_id": { "$toString": "$_id" },
            "title": 1,
            "abstract": 1,
            "citations": 1,
            "pubdates": 1,
            "pubdates_timestamp": 1,
            "pubtype": 1,
            "authors": 1,
            "publisher": 1,
            "pdf_url": 1,
            "search_keywords": 1
        }
    )

    if sort_by is not None or sort_order is not None:
        articles = articles.sort(sort_by, sort_order)

    results = list(articles)

    client.close()

    return results

def filter(filters: Filters, sort_param: str = None, sort_order: int = None):
    es = Elasticsearch(
        "https://localhost:9200",
     #   ssl_assert_fingerprint="69:a1:1b:85:c0:52:03:74:75:1a:f9:04:10:5a:ef:9f:f4:66:a1:1c:d0:3f:21:67:52:86:34:be:36:b0:5d:df",
        basic_auth=("elastic", ELASTIC_PASSWORD)
    )

    if es.indices.exists(index="articles"):
        es.indices.delete(index="articles")

    search_keywords = [keyword.lower() for keyword in filters.query.split(" ")]

    results = []

    if sort_param and sort_order:
        results = search_in_mongodb(search_keywords)
    else:
        results = search_in_mongodb(search_keywords, sort_param, sort_order)

    es.bulk(operations=generate_actions(results), refresh=True)

    must_array = []

    if len(filters.pubtypes) > 0:
        must_array.append({
            "bool": {
                "should": [
                    {
                        "match": {
                            "pubtype": pubtype
                        }
                    } for pubtype in filters.pubtypes
                ]
            }
        })

    if len(filters.publishers) > 0:
        must_array.append({
            "bool": {
                "should": [
                    {
                        "match": {
                            "publisher": publisher
                        }
                    } for publisher in filters.publishers
                ]
            }
        })

    if len(filters.authors) > 0:
        must_array.append({
            "bool": {
                "should": [
                    { "match": { "authors": author } } for author in filters.authors
                ]
            }
        })

    if filters.years:
        years = filters.years.split("-")

        must_array.append({
            "range": {
                "pubdates_timestamp": {
                    "gte": datetime(int(years[0]), 1, 1),
                    "lte": datetime(int(years[1]), 12, 31)
                }
            }
        })
        
    if filters.citations:
        citations = filters.citations.split("-")

        must_array.append({
            "range": {
                "citations": {
                    "gte": int(citations[0]),
                    "lte": int(citations[1])
                }
            }
        })

    print(must_array)

    body = {
        "query": {
            "bool": {
                "must": must_array
            }
        }
    }

    if sort_param and sort_order:
        order = "asc" if sort_order == 1 else "desc"
        body["sort"] = [{sort_param : {"order" : order}}]

    results = es.search(index="articles", body=body)

    return results

@app.get("/search")
async def index(query: str = None, sort_by: str = None, sort_order: int = None):
    if query == None:
        return {
            "error": True,
            "message": "No query was provided",
            "articles": []
        }
    
    results = []
    
    if sort_by == None or sort_order == None:
        results = await get_articles(query)
    else:
        search_keywords = [keyword.lower() for keyword in query.split(" ")]
        
        results = search_in_mongodb(search_keywords, sort_by, sort_order)

    return {
        "error": False,
        "message": "Articles found",
        "articles": results
    }

@app.post("/sorting")
async def sorting(sortings: Sortings):
    filters = Filters(query=sortings.query, pubtypes=sortings.pubtypes, authors=sortings.authors, publishers=sortings.publishers, pubdates=sortings.pubdates, citations=sortings.citations)
    results = filter(filters, sortings.sort_param, sortings.sort_order)

    return {
        "error": False,
        "message": "Articles found",
        "articles": recover_documents([hit["_source"] for hit in results["hits"]["hits"]])
    }

@app.post("/details")
async def details(id: ArticleDetails):
    client = MongoClient(MONGODB_URI)

    db = client.get_database("CampusDB")
    collection = db.get_collection("Articles")

    article = collection.find_one(
        {
            "_id": ObjectId(id.id)
        },
        {
            "_id": 0,
            "title": 1,
            "authors": 1,
            "publisher": 1,
            "pubtype": 1,
            "pubdates": 1,
            "citations": 1,
            "pdf_url": 1,
            "url": 1,
            "abstract": 1,
            "references": 1,
            "doi": 1,
            "keywords": 1,
            "search_keywords": 1
        }
    )

    client.close()

    return {
        "error": False,
        "message": "Article found",
        "article": article
    }
    
@app.get("/articles")
async def get_all_articles(sort_by: str = None, sort_order: int = None):
    client = MongoClient(MONGODB_URI)

    db = client.get_database("CampusDB")
    collection = db.get_collection("Articles")

    articles = collection.find(
        {},
        {
            "_id": { "$toString": "$_id" },
            "title": 1,
            "citations": 1,
            "pubdates": 1,
            "pubtype": 1,
            "publisher": 1,
            "pdf_url": 1,
            "search_keywords": 1
        }
    )

    if sort_by is not None or sort_order is not None:
        articles = articles.sort(sort_by, sort_order)

    results = list(articles)

    client.close()

    return {
        "error": False,
        "message": "Articles found",
        "articles": results
    }

@app.post("/filter")
async def filter_articles(filters: Filters):
    if filters.query is None:
        return {
            "error": True,
            "message": "No query was provided",
            "articles": []
        }
    
    results = filter(filters)

    return {
        "error": False,
        "message": "Articles found",
        "articles": recover_documents([hit["_source"] for hit in results["hits"]["hits"]])
    }

def generate_actions(data):
    for document in data:
        document["id"] = document.pop("_id")

        for value in [{ "index": { "_index": "articles" } }, document]:
            yield value

def recover_documents(data):
    for document in data:
        document["_id"] = document.pop("id")

    return data