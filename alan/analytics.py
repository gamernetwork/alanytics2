import re
from pprint import pprint

from datetime import datetime
from collections import OrderedDict

from elasticsearch import Elasticsearch

class Analytics(object):
    
    def __init__(self):
        #TODO: make ES connection details configurable
        self.es = Elasticsearch()

    def register(self, site, path, section, referrer, published, platforms=None):
        pageview = {
            "site": site,
            "full_url": site + path,
            "section": section,
            "referrer": referrer,
            "timestamp": datetime.now(),
            "published": published,
        }
        if platforms:
            pageview['platforms'] = platforms
            pageview['platforms_raw'] = [platform.replace(' ', '').lower() for platform in platforms]
        self.es.index(index="alanytics-pageview", doc_type="pageview", 
            body=pageview)

    def _resolve_period(self, period):
        if period == 'last_hour':
            return ('now-1h', 60)
        if period == 'last_minute':
            return ('now-1m', 1)
        minutes_regex = "^last_([0-9]+)_minutes$"
        minutes_match = re.match(minutes_regex, period)
        if minutes_match:
            minutes = minutes_match.group(1)
            return ("now-%sm" % minutes, int(minutes))

    def _get_filters(self, period, section=None, site=None, referrer=None):
        filters = [
            {
              "range": {                                                             
                "timestamp": {                                                       
                    "gt": period
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

    def _build_aggregate_query(self, must_filters, aggregates, should_query=[]):
        query = {
          "size": 0,                                                                    
          "query": {
            "function_score": {
              "functions": [
                {
                  "gauss": {
                    "timestamp": {
                      "origin": "now",
                      "scale": "5m",
                      "decay": 0.9,
                    },
                  },
                },
                {
                  "gauss": {
                    "published": {
                      "origin": "now",
                      "scale": "3h",
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

    def get_top_articles(self, period, site=None, referrer=None, platforms=[], size=10):
        es_period, minutes = self._resolve_period(period)
        filters = self._get_filters(es_period, section="article", site=site, referrer=referrer)
        platform_query = self._get_platform_query(platforms=platforms)
        shard_size = size * 10
        aggregates = {                                                                     
          "group_by_url": {                                                   
            "terms": {                                                                
              "field": "full_url",                                                    
              "order" : { "article_score" : "desc" },
              "size": size,
              "shard_size": shard_size
            },
            "aggs": {
              "article_score": {"sum": {"script": "_score"}},
            }
          },
        }        
        query = self._build_aggregate_query(filters, aggregates, should_query=platform_query)
        result = self.es.search(index="alanytics-pageview", body=query)
        print("get_top_articles took %s" % result['took'])
        buckets = result['aggregations']['group_by_url']['buckets'][:10]
        all_counts = [(bucket['key'], bucket['article_score']['value']) for bucket in buckets]
        return OrderedDict(all_counts)

analytics = Analytics()
