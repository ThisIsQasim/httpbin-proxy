from flask import Flask, request, Response
from flask_limiter import Limiter
import requests, os

def static_limiter_key():
    return os.environ['UPSTREAM_URL']

app = Flask(__name__)
limiter = Limiter(app, key_func=static_limiter_key)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@limiter.limit(os.environ['LIMIT_RATE'])
def _proxy(*args, **kwargs):
    # https://stackoverflow.com/a/36601467
    resp = requests.request(
        method=request.method,
        url=request.url.replace(request.host_url, os.environ['UPSTREAM_URL']),
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response

