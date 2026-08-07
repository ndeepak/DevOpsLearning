
# Env Variables Lab
How many PODs exist on the system?\
in the current(default) namespace
1

What is the environment variable name set on the container in the pod?
APP_COLOR


What is the value set on the environment variable `APP_COLOR` on the container in the pod?
pink

View the web application UI by clicking on the `Webapp Color` Tab above your terminal.


Update the environment variable on the POD to display a `green` background.
Note: Delete and recreate the POD. Only make the necessary changes. Do not modify the name of the Pod.


View the changes to the web application UI by clicking on the `Webapp Color` Tab above your terminal.
If you already have it open, simply refresh the browser


How many `ConfigMaps` exists in the `default` namespace?
```bash
 kubectl get configmaps 
NAME               DATA   AGE
db-config          3      40s
kube-root-ca.crt   1      11m
```
`2`


Identify the database host from the config map `db-config`.
```bash
 kubectl describe cm db-config 
Name:         db-config
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
DB_HOST:
----
**SQL01.example.com**

DB_NAME:
----
SQL01

DB_PORT:
----
3306


BinaryData
====

Events:  <none>
```


Create a new ConfigMap for the `webapp-color` POD. Use the spec given below.
ConfigMap Name: webapp-config-map
Data: APP_COLOR=darkblue
Data: APP_OTHER=disregard
```bash
kubectl create configmap webapp-config-map --from-literal=APP_COLOR=darkblue --from-literal=APP_OTHER=disregard
```

