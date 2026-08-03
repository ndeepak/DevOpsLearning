# 02 Managing Application Logs

Logs - Docker
```
docker run kodekloud/event-simulator

VS

docker run -d kodekloud/event-simulator
docker logs -f ecf
```

Logs - Kubernetes
```yaml
apiVersion: v1
kind: pod
metadata: 
	name: event-simulator-pod
spec:
	containers:
	- name: event-simulator
	  image: kodekloud/event-simulator
```

```bash
kuebctl create -f event-simulator.yaml

kubectl logs -f event-simulator-pod
```

lets add other image:
```yaml
apiVersion: v1
kind: pod
metadata: 
	name: event-simulator-pod
spec:
	containers:
	- name: event-simulator
	  image: kodekloud/event-simulator
	- name: image-processor
	  image: some-image-processor
```

```bash
kubectl logs -f event-simulator-pod event-simulator
kubectl logs -f event-simulator-pod some-image-processor
```


