# 01 Lab - Monitoring Cluster Components

We have deployed a few PODs running workloads. Inspect them.
Wait for the pods to be ready before proceeding to the next question.


Let us deploy the Metrics Server to enable monitoring of the PODs and Nodes in the cluster.

Deploy the Metrics Server in your Kubernetes cluster by applying the latest release `components.yaml` manifest using the following command:
Run the `kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml`

It takes a few minutes for the metrics server to start gathering data.

Run the `kubectl top node` command and wait for a valid output.
```bash
controlplane ~ ➜  kubectl top node
NAME           CPU(cores)   CPU(%)   MEMORY(bytes)   MEMORY(%)   
controlplane   330m         2%       914Mi           1%          
node01         47m          0%       170Mi           0%          

```

Identify the node that consumes the `most` CPU(cores).
```bas
 kubectl top pod
NAME       CPU(cores)   MEMORY(bytes)   
elephant   24m          30Mi            
lion       1m           16Mi            
rabbit     153m         250Mi  
```

Identify the node that consumes the `most` Memory(bytes).
`controlplane`

Identify the POD that consumes the `most` Memory(bytes) in default namespace.
`rabbit`

Identify the POD that consumes the `least` CPU(cores) in default namespace.
`lion`

