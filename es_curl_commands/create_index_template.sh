#curl -XPUT 'http://localhost:9200/_template/pageview_index' -d '
#{
#    "template": "analytics-pageview-*",
#	"settings" : {
#        "number_of_shards" : 5,
#        "number_of_replicas" : 1
#    },
#    "mappings": {
#      "pageview": {
#        "properties": {
#          "section": {
#              "type":     "string",
#              "index":    "not_analyzed"
#          },
#          "platforms": {
#              "type":     "string",
#              "index":    "not_analyzed"
#          },
#          "platforms_raw": {
#              "type":     "string",
#              "index":    "not_analyzed"
#          },
#          "referrer": {
#              "type":     "string",
#              "index":    "not_analyzed"
#          },
#          "full_url": {
#              "type":     "string",
#              "index":    "not_analyzed"
#          },
#          "site": {
#              "type":     "string",
#              "index":    "not_analyzed"
#          },
#          "timestamp": {
#              "type":     "date"
#          },
#          "published": {
#              "type":     "date"
#          }
#        }
#      }
#    }
#}'

curl -XPUT 'http://localhost:9200/_template/pageview_index' -d '
{
    "template": "analytics-pageview-filtered-*",
	"settings" : {
        "number_of_shards" : 2,
        "number_of_replicas" : 1
    },
    "mappings": {
      "pageview": {
        "properties": {
          "section": {
              "type":     "string",
              "index":    "not_analyzed"
          },
          "platforms": {
              "type":     "string",
              "index":    "not_analyzed"
          },
          "platforms_raw": {
              "type":     "string",
              "index":    "not_analyzed"
          },
          "referrer": {
              "type":     "string",
              "index":    "not_analyzed"
          },
          "full_url": {
              "type":     "string",
              "index":    "not_analyzed",
              "doc_values": false,
              "fielddata": {
                "filter": {
                    "frequency": {
                        "min": 0.01,
                        "min_segment_size": 500
                    }
                }
              }
          },
          "site": {
              "type":     "string",
              "index":    "not_analyzed"
          },
          "timestamp": {
              "type":     "date"
          },
          "published": {
              "type":     "date"
          }
        }
      }
    }
}'
