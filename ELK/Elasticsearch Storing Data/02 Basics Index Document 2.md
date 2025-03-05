# **Elasticsearch Indexes & Documents: A Practical Guide**
## **1. Understanding Indexes and Documents**
Elasticsearch is a **NoSQL distributed search engine** that stores and retrieves data using **indexes and documents** instead of tables and rows.
### **Relational Database vs Elasticsearch**

|Relational Database|Elasticsearch|
|---|---|
|Database|Index|
|Table|Type (Deprecated in ES 7.x)|
|Row|Document|
|Column|Field|
Each **document** in Elasticsearch is a JSON object stored inside an **index**.

---
## **2. Creating an Index**
An **index** in Elasticsearch is similar to a **database** in relational databases. It organizes and stores data for fast searching.
### **Create an index named `nba_players`**
```
curl -X PUT "localhost:9200/nba_players" -H "Content-Type: application/json" -d '
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  }
}'
```

✅ **What does this do?**
- `number_of_shards`: Defines how data is split across nodes.
- `number_of_replicas`: Defines redundancy (data backup).

### **Check if the index was created**
`curl -X GET "localhost:9200/_cat/indices?v"`

---
## **3. Inserting Documents**
A **document** in Elasticsearch is a single unit of data (like a row in a database table) and is stored in **JSON format**.
### **Add a document to `nba_players` index**
```
curl -X POST "localhost:9200/nba_players/_doc/1" -H "Content-Type: application/json" -d '
{
  "last_name": "James",
  "first_name": "LeBron",
  "position": "SF",
  "number": 23,
  "team": "Cleveland"
}'
```

### **Add more documents**
```
curl -X POST "localhost:9200/nba_players/_doc/2" -H "Content-Type: application/json" -d '
{
  "last_name": "Curry",
  "first_name": "Stephen",
  "position": "PG",
  "number": 30,
  "team": "Golden State"
}'
```

✅ **What does this do?**
- `nba_players/_doc/1` → Creates a document with ID `1`
- `_doc` → Default document type (since ES 7.x)

### **Check if a document exists**
`curl -X GET "localhost:9200/nba_players/_doc/1"`

You should get:
```
{
  "_index": "nba_players",
  "_id": "1",
  "_source": {
    "last_name": "James",
    "first_name": "LeBron",
    "position": "SF",
    "number": 23,
    "team": "Cleveland"
  }
}
```

---

## **4. Updating Documents**
### **Modify LeBron’s team from Cleveland to LA Lakers**
```
curl -X POST "localhost:9200/nba_players/_update/1" -H "Content-Type: application/json" -d '
{
  "doc": {
    "team": "LA Lakers"
  }
}'
```
### **Verify the update**
`curl -X GET "localhost:9200/nba_players/_doc/1"`

---
## **5. Deleting Documents**
### **Remove Curry’s document**
`curl -X DELETE "localhost:9200/nba_players/_doc/2"`

---

## **6. Searching Data in Elasticsearch**
### **Get all players**
`curl -X GET "localhost:9200/nba_players/_search?pretty"`

✅ **What does this do?**
- `_search` → Retrieves all documents from the `nba_players` index
- `pretty` → Formats the output in a readable JSON format

### **Find a player by team**
```
curl -X GET "localhost:9200/nba_players/_search" -H "Content-Type: application/json" -d '
{
  "query": {
    "match": {
      "team": "LA Lakers"
    }
  }
}'
```

---

## **7. Deleting an Index**
If you want to **delete an entire index** (equivalent to dropping a database):
`curl -X DELETE "localhost:9200/nba_players"`

---
## **8. Summary**

| Concept            | Description                                     |
| ------------------ | ----------------------------------------------- |
| **Index**          | Like a database, contains documents             |
| **Document**       | Like a row in a database, stored in JSON format |
| **Field**          | Like a column, holds values inside a document   |
| **Inverted Index** | Optimized search mechanism                      |

---
## **Next Steps**
- Try **bulk inserting** multiple documents at once.
- Learn **index mapping** for advanced data structures.
- Explore **aggregations** to analyze data patterns.