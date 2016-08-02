curl -XPOST 'http://localhost:9200/_reindex' -d '
{
  "source": {
    "index": "analytics-pageview-2016-07-18"
  },
  "dest": {
    "index": "analytics-pageview-2016-07-27"
  }
}'

