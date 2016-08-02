curl -XPUT 'http://localhost:9200/alanytics-pageview-meaty/' -d '
{
	"settings" : {
        "number_of_shards" : 50,
        "number_of_replicas" : 1
    }
}'

curl -XPUT 'http://localhost:9200/alanytics-pageview-meaty/_mapping/pageview' -d '
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

