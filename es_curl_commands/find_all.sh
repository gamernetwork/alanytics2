curl -XDELETE 'http://localhost:9200/analytics-pageview-2016-07-27/pageview/_search' -d '{
    "query" : { 
      "term": {
        "section": "article"
      }
    }
}'
