curl -XPOST 'http://localhost:9200/_reindex' -d '
{
  "source": {
    "index": "alanytics-pageview",
    "query": {
      "range": {
        "timestamp": {
          "gt": "2016-07-11T00:00:00.000",
          "lt": "2016-07-12T00:00:00.000"
        }
      }
    }
  },
  "dest": {
    "index": "analytics-pageview-filtered-2016-07-11"
  }
}'


curl -XPOST 'http://localhost:9200/_reindex' -d '
{
  "source": {
    "index": "alanytics-pageview",
    "query": {
      "range": {
        "timestamp": {
          "gt": "2016-07-12T00:00:00.000",
          "lt": "2016-07-13T00:00:00.000"
        }
      }
    }
  },
  "dest": {
    "index": "analytics-pageview-filtered-2016-07-12"
  }
}'

curl -XPOST 'http://localhost:9200/_reindex' -d '
{
  "source": {
    "index": "alanytics-pageview",
    "query": {
      "range": {
        "timestamp": {
          "gt": "2016-07-13T00:00:00.000",
          "lt": "2016-07-14T00:00:00.000"
        }
      }
    }
  },
  "dest": {
    "index": "analytics-pageview-filtered-2016-07-13"
  }
}'

curl -XPOST 'http://localhost:9200/_reindex' -d '
{
  "source": {
    "index": "alanytics-pageview",
    "query": {
      "range": {
        "timestamp": {
          "gt": "2016-07-14T00:00:00.000",
          "lt": "2016-07-15T00:00:00.000"
        }
      }
    }
  },
  "dest": {
    "index": "analytics-pageview-filtered-2016-07-14"
  }
}'

curl -XPOST 'http://localhost:9200/_reindex' -d '
{
  "source": {
    "index": "alanytics-pageview",
    "query": {
      "range": {
        "timestamp": {
          "gt": "2016-07-15T00:00:00.000",
          "lt": "2016-07-16T00:00:00.000"
        }
      }
    }
  },
  "dest": {
    "index": "analytics-pageview-filtered-2016-07-15"
  }
}'

curl -XPOST 'http://localhost:9200/_reindex' -d '
{
  "source": {
    "index": "alanytics-pageview",
    "query": {
      "range": {
        "timestamp": {
          "gt": "2016-07-16T00:00:00.000",
          "lt": "2016-07-17T00:00:00.000"
        }
      }
    }
  },
  "dest": {
    "index": "analytics-pageview-filtered-2016-07-16"
  }
}'

curl -XPOST 'http://localhost:9200/_reindex' -d '
{
  "source": {
    "index": "alanytics-pageview",
    "query": {
      "range": {
        "timestamp": {
          "gt": "2016-07-17T00:00:00.000",
          "lt": "2016-07-18T00:00:00.000"
        }
      }
    }
  },
  "dest": {
    "index": "analytics-pageview-filtered-2016-07-17"
  }
}'

curl -XPOST 'http://localhost:9200/_reindex' -d '
{
  "source": {
    "index": "alanytics-pageview",
    "query": {
      "range": {
        "timestamp": {
          "gt": "2016-07-18T00:00:00.000",
          "lt": "2016-07-19T00:00:00.000"
        }
      }
    }
  },
  "dest": {
    "index": "analytics-pageview-filtered-2016-07-18"
  }
}'
