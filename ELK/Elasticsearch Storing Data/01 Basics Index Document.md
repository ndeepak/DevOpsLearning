## Basics Concepts, indexes and documents
Documents, Types and Indexes

Here below is the table for relational database:
NBA Players Database
Players Table

| PID | Last_name | First_name | Position | Number | Team         |
| --- | --------- | ---------- | -------- | ------ | ------------ |
| 101 | James     | LeBron     | SF       | 23     | Cleveland    |
| 102 | Curry     | Steph      | PG       | 30     | Golden State |
| 103 | Davis     | Anthony    | C        | 23     | New Orleans  |
| 104 | Karl      | Towns      | C        | 32     | Minnesota    |
Teams Table

| Team_ID | Team_name    |
| ------- | ------------ |
| 1       | Minnesota    |
| 2       | Cleveland    |
| 3       | Golden State |
| 4       | New Orleans  |
| 5       | Chicago      |
Position table

| Pos_ID | Position |
| ------ | -------- |
| 1      | PG       |
| 2      | SG       |
| 3      | SF       |
| 4      | PF       |
| 5      | C        |

Hierarchy of Relational DB vs ElasticSearch
* Relational DB
	* Database
		* Table
			* Row
				* Column
* Elasticsearch
	* Index
		* Type
			* Document
				* Field

Indexes:
* Designed for SEARCH
* Inverted Index
	* Imagine it as book index
		* The quick brown fox jumped over the lazy dog
		* Quick brown foxes leap over lazy dogs in summer
		* relate the relevancy on above two statement in table with inverted index.

Documents:
* Database record in terms of database
* JSON(Javascript Object Notation)
	* Name value pair
	* separated by commas
	* { } brace holds objects
	* [] square holds arrays
	* Awesome example from above table, players and all.
```
{
	"last_name":"james",
	"firs_name":"Lebron",
	"position":"SF",
	"number":23,
	"team":"Cleveland"
}
{
	"last_name":"O'neil",
	"firs_name":"Shaquille",
	"position":"C",
	"number":30,
	"current_team":"Retired",
	"past_teams":[
		{
			"team1":"orlando",
			"team2":"LA",
			"team3":"Miami"
		}
	]
}
```


The Whole Picture:
Index > Type > Document > Field/Value from a sample JSON data file.
* Index: Athletes
	* TYPE: Basketball
		* Document 1: Athlete
		* Document 2: Athlete
	* TYPE: Football
		* Document 1: Athlete
		* Document 2: Athlete
	* TYPE: Hockey
	* TYPE: Soccer

Summary
* Elasticsearch is built for fast search and relies on indexes
* The ES data model is very different from relational database, and uses an inverted index.
* The main components of the ES data structure are indexes, types, documents, and names/values.
* Documents in ES rely on JSON structured data.