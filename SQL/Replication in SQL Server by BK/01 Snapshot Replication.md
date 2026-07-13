# 01 Snapshot Replication

Snapshot replication distributes data exactly as it appears at a specific moment in time and does not monitor for updates to the data. When synchronization occurs, the entire snapshot is generated and sent to Subscribers.
It replicates a snapshot of the data.


When to use snapshot replication?
* Data do not change frequently
* A large volume of changes occurs at a specific time.
* When it is acceptable to have copies of data that are out of data with respect to the publisher for a period of time.
* Replicating small volumes of data.
* The database is used for reporting purposes.

