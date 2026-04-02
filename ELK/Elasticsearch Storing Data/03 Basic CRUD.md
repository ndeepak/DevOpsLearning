# Basics CRUD - Create, Read, Update and Delete
## Interacting with Elasticsearch
HTTP Client --> GET / --> Elasticsearch
Elasticsearch --> 200OK --< HTTP Client

Used in HTTP Client:
cURL 
Chrome
Kibana


In Elasticsearch machine:
`netstat -antp`
:9200 for elasticsearch, 5601 for kibana

In Kibana dashboard,
Go to various modules to see Elastic data.

GET /

/index/type/id
{
DOCUMENT
}

PUT /athletes/basketball/1
{
	"last_name":"Curry",
	"first_name":"Steph",
	"position":"PG",
	"number":"30",
	"team":"Golden State"
}
