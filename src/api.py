from aiohttp import web
from random import randint
import json
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def quote_from_anyone(request):
    response_obj = fetch_quote()
    return web.Response(text=json.dumps(response_obj))

async def quote_from_character(request):
    cast_member = request.query["name"]
    try:
        response_obj = fetch_quote(cast_member)
        return web.Response(text=json.dumps(response_obj))
    except Exception as e:
        response_obj = { "status" : "failed", "reason": str(e) }
        return web.Response(text=json.dumps(response_obj), status=500)

def fetch_quote(character=None):
    character = character or 'anyone'
    logger.info(f"Fetching quote from {character}")
    all_characters = [d['character'] for d in quotes]
    valid_characters = all_characters if character == 'anyone' else [character]
    quote_list = [d for d in quotes if d['character'] in valid_characters]
    if len(quote_list) < 1:
        raise Exception("Invalid character selection, fucking idiot")
    quote = quote_list[randint(0,len(quote_list)-1)]
    response_obj = {**{ "status" : "success" }, **quote}
    return response_obj

if __name__ == '__main__':
    with open("quotes.json") as json_file:
        quotes = json.load(json_file)

    app = web.Application()
    app.router.add_get("", quote_from_anyone)
    app.router.add_get("/", quote_from_anyone)
    app.router.add_get("/who", quote_from_character)

    web.run_app(app)