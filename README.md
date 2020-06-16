# Anchorman Quote API

> Simple API to fetch quotes from The Anchorman franchise.

### Setup

> Running directly

```shell
$ git clone https://github.com/srussell91/anchorman-quote-api.git
$ cd anchorman-quote-api
$ pip install src/requirements.txt
$ python src/api.py
```

> Running with docker

```shell
$ git clone https://github.com/srussell91/anchorman-quote-api.git
$ cd anchorman-quote-api
$ docker build -t anchorman-api .
$ docker run --rm -it -p 8080:8080 anchorman-api
```

The service will be accessible at http://localhost:8080

---

## Usage (Optional)

- Get a random quote at: http://localhost:8080/
- You can specify a character to limit you're query at: http://localhost:8080/who?name=Veronica