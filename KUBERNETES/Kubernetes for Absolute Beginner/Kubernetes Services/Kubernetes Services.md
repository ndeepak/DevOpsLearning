# Kubernetes Services



Services Types

NodePort
ClusterIP
Loadbalancer


Service NodePort
	TargetPort
	ServicePort
Range: 30000-32767


```service-definition.yml
apiVersion: v1
kind: Service
metadata:
	name: myapp-service
spec:
	type: NodePort
	ports:
	- targetPort: 80
	  port: 80
	  nodePort: 3008
	selector:
		app: myapp
		type: frontend
```

`kubectl create -f service-definiton.yml`
`kubectl get serivices`
`curl http://192.168.1.2:3008`

Algorithm: Random
SessionAffinity: Yes

In multiple nodes environment pods,
Services expands in all across the cluster

`kubectl get svc`

`minikube service myapp-service --url`
