import os
from urllib.parse import urlparse

if not os.path.exists('serverquest/database'):
    os.mkdir('serverquest/database')

from . app import app

url = urlparse('http://0.0.0.0:8080')
host, port = url.hostname, url.port
app.run(host=host, port=port, debug=True)
