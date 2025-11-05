# Pods with YAML

YAML in Kubernetes

```rootlevelproperty
apiVersion: API versions (V1, )
kind:
metadata: information about the data, like name, labeles(app)

spec: additional information about specifications, spec is a dictionary
	containers: is a dictionary
	 - name:
	   image:
```

| **KIND**   | **VERSION** |
| ---------- | ----------- |
| Pod        | v1          |
| Service    | v1          |
| ReplicaSet | apps/v1     |
| Deployment | apps/v1     |

`kubectl create -f pod-definition.yml`

Commands
`kubectl get pods`
`kubectl describe pod myapp-pod`


## Demo
`kubectl apply -f demo-pod-deployment.yml`
