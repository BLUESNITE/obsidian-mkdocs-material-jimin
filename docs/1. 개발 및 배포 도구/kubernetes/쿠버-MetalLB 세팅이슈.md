> [!CHECK] MetalLB 설치 세팅

> kubectl edit configmap -n kube-system kube-proxy
```shell
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: "ipvs"
ipvs:
  strictARP: true
```

> 파일 다운 및 설치, 적용
```shell
sudo curl -fsSLo /mnt/loadbalancer-yaml/metallb.yaml https://raw.githubusercontent.com/metallb/metallb/v0.14.3/config/manifests/metallb-native.yaml

kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl 
rand -base64 128)"
```

> calico가 설치되어 있다면
```shell
vi calico.yaml에서 CALICO_IPV4POOL_CIDR 찾아서 10.100.0.0/16 
```

> [!TIP] calico
> https://docs.projectcalico.org/manifests/calico.yaml
> https://calico-v3-25.netlify.app/archive/v3.25/manifests/calico.yaml

> [!CHECK] 내용정리
> YAML 파일로 MetalLB를 사용하여 Kubernetes 클러스터에 IP 주소 풀을 설정하고 L2 광고를 구성하는 내용을 진행

일전에 Metal LB를 사용할 때 추가 작성 적용만하고
대충 넘어갔던 부분이다. 그런데 이번에 추가된 어플리케이션 서비스가 많아지다보니. pool이 다 찾다. svc가 적용을 못하는 모양을 보자니 감이와서 정리부터 해보고 재적용하려한다.

> [!NOTE] 적용한 ip-addr-pool.yaml
> 
> kind : `IPAddressPool` 리소스에서 IP 주소 풀을 정의
> metadata : `name` IP 주소 풀의 이름과 `namespace` 네임스페이스
> spec.addresseds : `ip pool`의 할당 가능한 범의
> 
> and
> 
> kind : `L2Advertisement` 리소스에서 L2 광고를 정의. (정확인 먼 뜻인지 모르겠다)
> metadata : 전개는 위와 같다. 하지만 `my-l2` 라고 정의하는데 의도를 아직 파악해내지 못했다.
> spec.ipAddressPools : 이 L2 광고가 적용될 IP 주소 풀의 이름

```shell hl:4,8,13,17
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
kind: L2Advertisement
metadata:
  name: my-l2
  namespace: metallb-system
spec:
  ipAddressPools:
  - first-pool
```

> [!NOTE] 확장한 ip-addr-pool.yaml
```shell hl:4,8,13,17,26,27
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

> [!TIP] 성능적인 관점의 pool 사용 용이성
> 
> (1안) 첫번째에 range를 192.168.180.140-192.168.180.160에서 +20
> (2안) 정의하는 IPAddressPool을 2개로 관리 적용

*(정리)*
```shell
(1안)은 로드 분산과 문제 격리 측면에서 더 나은 성능을 제공할 수 있습니다. 
특히, 대규모 클러스터나 고가용성이 중요한 환경에서는 (1안)이 더 적합할 수 있습니다. 

그러나 관리의 단순성과 일관성이 중요하고, 비교적 작은 클러스터에서는 (2안)이 더 효율적일 수 있습니다.
```
 ___
 
 미정리 코드
 ```shell
 istio

curl -L https://istio.io/downloadIstio | sh -

export PATH="$PATH:/home/tech/yaml/istio-1.21.2/bin"

istioctl x precheck
istioctl install --set profile=demo -y

kubectl label namespace default istio-injection=enabled

kubectl apply -f samples/bookinfo/platform/kube/bookinfo.yaml
istioctl dashboard kiali

kubectl edit svc istio-ingressgateway -n istio-system
```