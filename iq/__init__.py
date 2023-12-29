
from elasticsearch import Elasticsearch

#
# CONFIG
#

from dotenv import load_dotenv
import os

load_dotenv()

es = Elasticsearch(
    hosts=[os.getenv('ES_HOST', "https://localhost:9200")],
    http_auth=(os.getenv('ES_USER', "admin"), os.getenv('ES_PASSWORD', "admin")),
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
)
