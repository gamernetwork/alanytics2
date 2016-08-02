import re
from pprint import pprint

from datetime import datetime
from collections import OrderedDict

#from elasticsearch import Elasticsearch
from aioes import Elasticsearch

class Analytics(object):
    
    def __init__(self):
        #TODO: make ES connection details configurable
        self.es = Elasticsearch(['localhost:9200'])
        self.pageview_index = 'analytics-pageview-2016-07-27'
        #self.query_index = self.pageview_index
        self.query_index = []
        #for i in range(11, 19):
        #    self.query_index.append("analytics-pageview-v2-2016-07-%s" % i)
        for i in range(11, 19):
            self.query_index.append("analytics-pageview-filtered-2016-07-%s" % i)

    async def register(self, site, path, section, referrer, published, platforms=None, timestamp=None):
        if not timestamp:
            timestamp = datetime.now()
        pageview = {
            "site": site,
            "full_url": site + path,
            "section": section,
            "referrer": referrer,
            "timestamp": self._build_es_datetime(timestamp),
            "published": self._build_es_datetime(published),
        }
        if platforms:
            pageview['platforms'] = platforms
            pageview['platforms_raw'] = [platform.replace(' ', '').lower() for platform in platforms]
        await self.es.index(index=self.pageview_index, doc_type="pageview", 
            body=pageview)

    def _resolve_period(self, period, timestamp=None):
        origin = 'now'
        if timestamp:
            origin = self._build_es_datetime(timestamp) + '||'
        if period == 'last_hour':
            return ('%s-1h' % origin, 60)
        if period == 'last_minute':
            return ('%s-1m' % origin, 1)
        minutes_regex = "^last_([0-9]+)_minutes$"
        minutes_match = re.match(minutes_regex, period)
        if minutes_match:
            minutes = minutes_match.group(1)
            return ("%s-%sm" % (origin, minutes), int(minutes))

    def _get_filters(self, period, timestamp=None, section=None, site=None, referrer=None):
        if not timestamp:
            timestamp = "now"
        filters = [
            {
              "range": {                                                             
                "timestamp": {                                                       
                    "gt": period,
                    "lte": timestamp
                }
              }
            }
        ]
        if site:
            filters.append({"term": {"site": site}})
        if section:
            filters.append({"term": {"section": section}})
        if referrer:
            filters.append({"term": {"referrer": referrer}})
        return filters

    def _get_platform_query(self, platforms=[]):
        platform_filter = []
        for platform in platforms:
            platform_filter.append({'term': {'platforms_raw': platform}})
        return platform_filter

    def _build_es_datetime(self, timestamp):
        return datetime.strftime(timestamp, "%Y-%m-%dT%H:%M:%S")

    def _build_aggregate_query(self, must_filters, aggregates, should_query=[], timestamp=None):
        origin = 'now'
        if timestamp:
            origin = self._build_es_datetime(timestamp)
        query = {
          "size": 0,                                                                    
          "query": {
            "function_score": {
              "functions": [
                {
                  "exp": {
                    "timestamp": {
                      "origin": origin,
                      "scale": "5m",
                      "decay": 0.9,
                    },
                  },
                },
                {
                  "exp": {
                    "published": {
                      "origin": origin,
                      "scale": "0.25d",
                      "decay": 0.9,
                    },
                  },
                }
              ],
              "query": {
                "bool": {                                                               
                  "must": {"match_all": {}},
                  "should": should_query,
                  "minimum_should_match": 0,
                  "filter": {                                                               
                    "bool": {
                      "must": must_filters,
                    }
                  }
                }
              },                                                               
              "score_mode": "multiply"
            },
          },
          "aggs": aggregates,
        }
        return query

    async def get_top_articles(self, period, site=None, referrer=None, platforms=[], size=10, timestamp=None):
        es_period, minutes = self._resolve_period(period, timestamp)
        timestamp_str = self._build_es_datetime(timestamp)
        filters = self._get_filters(es_period, timestamp=timestamp_str, section="article", site=site, referrer=referrer)
        platform_query = self._get_platform_query(platforms=platforms)
        shard_size = size * 2
        aggregates = {                                                                     
          "group_by_url": {                                                   
            "terms": {                                                                
              "field": "full_url",                                                    
              "order" : { "article_score" : "desc" },
              "size": size,
              "shard_size": shard_size,
            },
            "aggs": {
              "article_score": {"sum": {"script": "_score", "lang": "expression"}},
              "published": {"terms": {"field": "published"}},
            }
          },
        }        
        #aggregates = {                                                                     
        #  "sample": {                                                   
        #    "sampler": {                                                                
        #      "field": "full_url",                                                    
        #      "max_docs_per_value": 100000,
        #      "shard_size": 1000,
        #    },
        #    "aggs": {
        #        "group_by_url": {                                                   
        #          "terms": {                                                                
        #            "field": "full_url",                                                    
        #            "order" : { "article_score" : "desc" },
        #          },
        #          "aggs": {
        #            "article_score": {"sum": {"script": "_score"}},
        #          }
        #        }
        #    }
        #  },
        #}        
        query = self._build_aggregate_query(filters, aggregates, should_query=platform_query, timestamp=timestamp)
        result = await self.es.search(index=self.query_index, body=query)
        print("get_top_articles took %s" % result['took'])
        buckets = result['aggregations']['group_by_url']['buckets'][:10]
        all_counts = [(("(%s) " + bucket['key']) % bucket['published']['buckets'][0]['key_as_string'], bucket['article_score']['value']) for bucket in buckets]
        #all_counts = [(bucket['key'], bucket['article_score']['value']) for bucket in buckets]
        return OrderedDict(all_counts)

analytics = Analytics()
