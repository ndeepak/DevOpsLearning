# 02 Lab - Managing Application Logs

We have deployed a POD hosting an application. Inspect it. Wait for it to start.


A user - `USER5` - has expressed concerns accessing the application. Identify the cause of the issue.
Inspect the logs of the `webapp-1` POD
`kubectl logs -f `
- Account does not exist
- Application Crashed
- Item Out of Stock
- **Account Locked due to Many Failed Attempts**


We have deployed a new POD - `webapp-2` - hosting an application. Inspect it. Wait for it to start.

A user is reporting issues while trying to purchase an item. Identify the user and the cause of the issue.
Inspect the logs of the web application running in the `webapp-2` pod.
- USER - Account does not exist
- USER - Item Out of Stock
- USER2 - Application Crashed
- **USER30 - Item Out of Stock**




