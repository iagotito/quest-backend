from urllib.parse import urlparse

from . app import app

url = urlparse('http://0.0.0.0:8080')
host, port = url.hostname, url.port
app.run(host=host, port=port, debug=True)
