from aiohttp import web
from random import randint
import json
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def quote(request):
    response_obj = fetch_quote()
    return web.Response(text=json.dumps(response_obj))

async def quote_tags(request):
    tags = request.query["tags"].split(',')
    try:
        response_obj = fetch_quote(tags)
        return web.Response(text=json.dumps(response_obj))
    except Exception as e:
        response_obj = { "status" : "failed", "reason": str(e) }
        return web.Response(text=json.dumps(response_obj), status=500)

def fetch_quote(tags=None):
    logger.info(f"Fetching quote with tags: {tags}")
    all_tags = []
    quotes = load_quotes()
    for quote in quotes:
        all_tags.extend(quote["tags"])
    tags = set(tags).intersection(set(all_tags)) if tags else all_tags
    quotes = [quote for quote in quotes if common_elements(quote["tags"], tags)]
    if len(quotes) < 1:
        raise Exception("You've filtered everything out with your dumb tags")
    quote = quotes[randint(0,len(quotes)-1)]
    response_obj = {**{ "status" : "success" }, **quote}
    return response_obj

def common_elements(list_one, list_two):
    return set(list_one).intersection(set(list_two))

def load_quotes():
    with open("src/quotes.json") as json_file:
        quotes = json.load(json_file)
    return quotes

if __name__ == '__main__':
    app = web.Application()
    app.router.add_get("", quote)
    app.router.add_get("/", quote)
    app.router.add_get("/tags", quote_tags)
    web.run_app(app)
