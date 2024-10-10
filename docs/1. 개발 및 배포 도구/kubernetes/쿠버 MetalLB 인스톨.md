> [!NOTE] MetalLB 인스톨 과정 정리

**MetalLB 다운로드**
```
sudo curl -fsSLo metallb.yaml https://raw.githubusercontent.com/metallb/metallb/v0.14.3/config/manifests/metallb-native.yaml
```

**MetalLB 적용**
```
kubectl apply -f metallb.yaml
```

![[Pasted image 20241010173610.png]]

![[Pasted image 20241010173636.png]]

**ip-addr-pool.yaml 작성**
```
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: first-pool
  namespace: metallb-system
spec:
  addresses:
  - 192.168.180.140-192.168.180.160
---
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: second-pool
  namespace: metallb-system
spec:
  addresses:
  - 192.168.180.161-192.168.180.180
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: my-l2
  namespace: metallb-system
spec:
  ipAddressPools:
  - first-pool
  - second-pool
```

**ip-addr-pool.yaml 적용**

![[Pasted image 20241010173817.png]]

![[Pasted image 20241010174123.png]]

*테스트*



