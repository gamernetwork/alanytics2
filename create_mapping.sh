curl -XPUT 'http://localhost:9200/alanytics-pageview/' -d '{}'

curl -XPUT 'http://localhost:9200/alanytics-pageview/_mapping/pageview' -d '
{
  "properties": {
    "section": {
        "type":     "string",
        "index":    "not_analyzed"
    },
    "url": {
        "type":     "string",
        "index":    "not_analyzed"
    },
    "full_url": {
        "type":     "string",
        "index":    "not_analyzed"
    },
    "site": {
        "type":     "string"
    },
    "timestamp": {
        "type":     "date"
    }
  }
}'

