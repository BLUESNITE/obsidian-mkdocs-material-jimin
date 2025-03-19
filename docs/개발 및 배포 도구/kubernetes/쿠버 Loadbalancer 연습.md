**작업 전 상태**
![[Pasted image 20241011085951.png]]

**loadbalancer-argocd.yaml**
```
apiVersion: v1
kind: Service
metadata:
  name: argocd-server
  namespace: argocd
spec:
  selector:
    app: argocd-server
  ports:
    - protocol: TCP
      port: 31190
      targetPort: 8080
  type: LoadBalancer
```

**작업 후 상태**
![[Pasted image 20241011090337.png]]

**최종 서비스 업데이트**

아래 원본 서비스 내용에서 selector app을 변경 적용해주자.
```
selector:
    app: argocd-server

selector:
    app.kubernetes.io/name: argocd-server
```

```
apiVersion: v1
kind: Service
spec:
  allocateLoadBalancerNodePorts: true
  clusterIP: 10.103.9.77
  clusterIPs:
  - 10.103.9.77
  externalTrafficPolicy: Cluster
  internalTrafficPolicy: Cluster
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack
  ports:
  - nodePort: 30379
    port: 31190
    protocol: TCP
    targetPort: 8080
  selector:
    app: argocd-server
  sessionAffinity: None
  type: LoadBalancer
status:
  loadBalancer:
    ingress:
    - ip: 192.168.180.141
      ipMode: VIP
```
