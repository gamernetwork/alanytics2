curl -XPOST 'http://localhost:9200/_aliases' -d '
{
    "actions" : [
        { "add" : { "index" : "analytics-pageview-2016-07-18", "alias" : "analytics-pageview-today" } },
        { "add" : { "index" : "analytics-pageview-2016-07-17", "alias" : "analytics-pageview-minus-1-days" } },
        { "add" : { "index" : "analytics-pageview-2016-07-16", "alias" : "analytics-pageview-minus-2-days" } },
        { "add" : { "index" : "analytics-pageview-2016-07-15", "alias" : "analytics-pageview-minus-3-days" } },
        { "add" : { "index" : "analytics-pageview-2016-07-14", "alias" : "analytics-pageview-minus-4-days" } },
        { "add" : { "index" : "analytics-pageview-2016-07-13", "alias" : "analytics-pageview-minus-5-days" } },
        { "add" : { "index" : "analytics-pageview-2016-07-12", "alias" : "analytics-pageview-minus-6-days" } },
        { "add" : { "index" : "analytics-pageview-2016-07-11", "alias" : "analytics-pageview-minus-7-days" } }
    ]
}'
