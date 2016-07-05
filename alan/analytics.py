from datetime import datetime

from elasticsearch import Elasticsearch

class Analytics(object):
    
    def __init__(self):
        #TODO: make ES connection details configurable
        self.es = Elasticsearch()

    def register(self, section, slug):
        pageview = {
            "site": "pudding.bn.gntech.systems",
            "section": section,
            "url": slug,
            "full_url": section + ':' + slug,
            "timestamp": datetime.now(),
        }
        self.es.index(index="alanytics-pageview", doc_type="pageview", 
            body=pageview)

analytics = Analytics()
