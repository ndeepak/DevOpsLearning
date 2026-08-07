# Rolling Updates Lab

We have deployed a simple web application. Please inspect the Pods and Services within the default namespace.
**Note:** Please wait for the application to complete its deployment. Once the deployment is finished, access the application by clicking on the link labeled `Webapp Portal` located above your terminal.


```bash
controlplane ~ ➜  kubectl get pods
NAME                        READY   STATUS    RESTARTS   AGE
frontend-59dfbc6688-4pb4f   1/1     Running   0          70s
frontend-59dfbc6688-bnr2s   1/1     Running   0          70s
frontend-59dfbc6688-fqldb   1/1     Running   0          70s
frontend-59dfbc6688-zkmdq   1/1     Running   0          70s

controlplane ~ ➜  kubectl get services
NAME             TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
kubernetes       ClusterIP   10.43.0.1      <none>        443/TCP          11m
webapp-service   NodePort    10.43.53.244   <none>        8080:30080/TCP   86s
```

What is the current color of the web application?
Access the Webapp Portal.
`blue`



Execute the script named `curl-test.sh` to send multiple requests for testing the web application. Please make a note of the output produced.
Execute the script at `/root/curl-test.sh`.
```bash
controlplane ~ ✖ cat curl-test.sh 
for i in {1..35}; do
   kubectl exec --namespace=kube-public curl -- sh -c 'test=`wget -qO- -T 2  http://webapp-service.default.svc.cluster.local:8080/info 2>&1` && echo "$test OK" || echo "Failed"';
   echo ""
done


bash /root/curl-test.sh
```


Inspect the deployment in the `default` namespace to identify the number of Pods that have been deployed by it.
`4`

What container image is used to deploy the applications?
`kubectl describe pod pod-name`
`kodekloud/webapp-color:v1`


Inspect the deployment to determine the current strategy in use.
`RollingUpdate`
`kubectl get deployments`
`kubectl describe depolyments deployment-name`


What would occur if you were to upgrade the application at this moment?
`Pods are upgraded few at a time`

Let us try that. Upgrade the application by updating the image in the deployment to `kodekloud/webapp-color:v2`.
Please ensure that you do not delete and recreate the deployment. Instead, update the existing deployment by setting the new image name.
```bash
kubectl set image deployments/frontend simple-webapp=kodekloud/webapp-color:v2
```

Please execute the script `curl-test.sh` once more. Observe that the requests now target both the older and newer versions (if checked immediately). Importantly, none of the requests should fail.
Execute the script located at `/root/curl-test.sh` using the following command:
```bash
bash /root/curl-test.sh
```
Expected output:
```
Hello, Application Version: v1 ; Color: blue OK

Hello, Application Version: v2 ; Color: green OK
```

**Note:** The update may have already been applied, so you might only observe the updated response.


How many PODs can be down simultaneously for an upgrade?
existing strategy settings and note that the current number of PODs is 4.
`1 as 25% of 4`


Change the deployment strategy to `Recreate`.
Delete and re-create the deployment if necessary. Only update the strategy type for the existing deployment.

```bash
kubectl get deployments.apps frontend  -o yaml > depll.yaml
kubectl create -f depll.yaml 
```

`.spec.strategy.type==Recreate`


Upgrade the application by configuring the deployment to use the image `kodekloud/webapp-color:v3`.
Do not delete and re-create the deployment. Only set the new image name for the existing deployment.
 `kubectl set image deployments/frontend simple-webapp=kodekloud/webapp-color:v3`

Run the script `curl-test.sh` once more and observe the failures. Please wait for the new application to become fully operational. You should notice that the requests no longer reach both versions.
Execute the script located at `/root/curl-test.sh` using the following command:
```bash
bash /root/curl-test.sh
```
