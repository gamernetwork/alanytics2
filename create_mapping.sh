curl -XPUT 'http://localhost:9200/alanytics-pageview/' -d '{}'

curl -XPUT 'http://localhost:9200/alanytics-pageview/_mapping/pageview' -d '
{
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
        "index":    "not_analyzed"
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
}'

