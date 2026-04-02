## Log Management
* Security investigations require logs that are:
	* Centralized
	* Normalized
	* Filtered
	* Indexed
	* Searchable
---
## ELK / Elastic Stack Components
"Reliably and securely take data from any source, in any format, and search, analyze and visualize it in real time."
### ElasticSearch
* Where do I store my data?
	* A database for storing json documents
	* based on Lucene (inverted index)
	* designed for fast full-text search
	* data statistics, aggregations and transformations
	* designed for distributed computing and scale
	* uses RESTFUL APIs
---
### Logstash
* How do I get my data into storage?
	* A data processing pipeline
	* Input takes data from a variety of sources
	* parsing and filtering allows data normalizing
	* output sends data to a variety of destinations
---
### Kibana
* How do I interact with my data?
	* Web-based GUI designed to work with ElasticSearch
	* Flexible search language
	* search result output with pivots
	* visualization and graph wizards (charts and all)
	* real-time dashboard output
---
## ELK Interaction
![[ELK Interactions.png]]Order:
1. Logstash reads Evidence data from various sources.
2. Logstash then sends data to ElasticSearch where it is stored in index
3. We are querying in Kibana, reading from elastic search and back to us.



