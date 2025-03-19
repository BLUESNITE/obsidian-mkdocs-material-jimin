> [!INFO] 완료된 설치 목록
>  - argocd
>  - istio
>  - kiali
>  - kubernetes dashboard
>  - metallb
>  - calico

이번 정리로 네트워크 설정에 대해 조금더 자세히 알아보고자 합니다.
기존에 온프레미스 환경에 주먹구구하듯이. 어플리케이션을 Loadbalancer로 무한정 세팅하여 앱서비스 연결을 하고있었는데, 개선해야지 개선해야지 하다가 이제야 재작업을 진행합니다.

> [!CHECK] 목표업무
> istio ingressgateway를 정확히 설정하고 dns 서버로 도메인 호스팅까지 유연하게 설정하기.

**Kiali 사용방법 및 활용가능여부 체크**

istio를 반복적으로 재설치 하다가 발견한 Kiali 공식 사이트의 가이드에 따라서 설치 연결은 성공하였는데. 이 툴의 도움을 받아 쉽게 설정할 수 있는지 확인. [Kiali Quick Start](https://kiali.io/docs/installation/quick-start/ "Kiali Quick Start")

> [!NOTE] 추가 설치 prometheus
> 설치하라고 해서 그냥 ...

```
kubectl apply -f /home/tech/data/k8s/istio-1.23.2/samples/addons/prometheus.yaml
```

![[Pasted image 20241023185017.png]]

**Create Gateway 설정 방법**

`Istio Gateway`는 외부 트래픽을 클러스터 내부 서비스로 라우팅하기 위한 중요한 구성 요소

- Namespace : Istio의 인그레스 게이트웨이를 설정하고 관리할 네임스페이스를 지정
- Name : 게이트웨이의 이름을 지정
- Workload Selector : 워크로드 선택기는 게이트웨이를 특정 워크로드에 연결할 수 있도록함. 만약 특정 레이블을 가진 워크로드에만 게이트웨이를 적용하고 싶다면 이 옵션을 사용하여 레이블을 설정
- Server List : 게이트웨이에서 처리할 트래픽의 포트와 프로토콜을 설정
- Labels : 게이트웨이 리소스에 레이블을 추가
- Annotations : 추가적인 메타데이터를 포함. 선택사항
- Preview : 미리확인

**예시 설정**

- Name: my-gateway
- Server List:
    - Port: 80
    - Protocol: HTTP
    - Name: http
- Labels: (필요 시 설정)
- Annotations: (필요 시 설정)

> [!NOTE] 연습해보기

*연습용 nginx pod*
```
apiVersion: v1
kind: Pod
metadata:
  name: nginx-test
  namespace: hello-world
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80
```

*연습용 nginx service*
```
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: hello-world
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80  # 서비스가 노출할 포트
      targetPort: 80  # Pod에서 노출된 포트
      nodePort: 30007  # 외부에서 접근할 수 있는 포트
  type: NodePort  # 외부에서 접근할 수 있는 방식
```

위 두개 파일 배포를 진행하면 Pod가 배포되고 http://192.168.2.172:30007 로 nginx 접속이 된다.

이제부터 istio gateway를 통해서 nginx로 들어올 수 있도록 작업을 해본다.

*연습용 Create Gateway 위 이미지처럼 GUI에서 진행*
```
namespace: hello-world
spec:
  selector:
    istio: ingressgateway  # Istio Ingress Gateway를 사용
```

![[Pasted image 20241024162200.png]]

생성한 게이트웨이

*gateway 내용*
```
kind: Gateway
apiVersion: networking.istio.io/v1
metadata:
  name: hello-world-gateway
  namespace: hello-world
  uid: ecb36983-a8c3-47cd-872b-36924954ac78
  resourceVersion: '179052'
  generation: 1
  creationTimestamp: '2024-10-24T07:22:52Z'
  managedFields:
  - manager: kiali
    operation: Update
    apiVersion: networking.istio.io/v1
    time: '2024-10-24T07:22:52Z'
    fieldsType: FieldsV1
    fieldsV1:
      f:spec:
        .: {}
        f:selector:
          .: {}
          f:istio: {}
        f:servers: {}
spec:
  servers:
  - port:
      number: 80
      protocol: HTTP
      name: http
    hosts:
    - '*'
    tls: {}
  selector:
    istio: ingressgateway
status: {}
```

*istio-ingressgateway priview*
```
apiVersion: v1
kind: Service
metadata:
  name: istio-ingressgateway
  namespace: istio-system
spec:
  type: NodePort
  selector:
    app: istio-ingressgateway
  ports:
    - name: http2
      port: 80
      targetPort: 8080
      nodePort: 30080  # 노드 포트 지정
    - name: https
      port: 443
      targetPort: 8443
      nodePort: 30443
```

*nginx-vs*
```
kind: VirtualService
metadata:
  name: nginx-vs
  namespace: hello-world
spec:
  hosts:
  - "*"  # 모든 호스트에 대해 허용
  gateways:
  - hello-world-gateway  # 방금 생성한 Gateway
  http:
  - match:
    - uri:
        prefix: "/"  # 모든 경로를 허용
    route:
    - destination:
        host: nginx-service  # NGINX 서비스 이름
        port:
          number: 80
```

> [!TIP] 흐름 설명
> Istio Gateway와 NGINX 서비스가 연동되는 흐름
>   
>   
> 1) **IngressGateway 서비스** 는 클러스터 외부에서 트래픽을 받아들이는 역할
>     (istio-ingressgateway의 nodeport 30080)
>   
>   
> 2) **kind: Gateway** 가 리소스를 어떤 트래픽으로 갈지 결정
>     (예를들어 * 도메인 에서 오는 트래픽을 허용하고 80포트 요청을 처리)
>     (Selector를 통해 istio ingressgateway가 Gateway와 연결 설정)
>     (Gateway는 필터링한 트래픽을 연결된 vs service로 전달)
>   
>   
>  3) **VirtualService** 리소스는 트래픽이 어디로 라우팅 될지 결정
>     (모든 트래픽에 대해서 nginx-service로 전달)


![[napkin-selection.png]]

한번더

1) 외부 클라이언트가 `http://<노드 IP>:30080`으로 요청을 보냅니다.

2) istio-ingressgateway가 NodePort로 트래픽을 받아, Istio Gateway에서 트래픽을 필터링

3) hello-world-gateway는 80번 포트로 오는 모든 트래픽 허용하고 nginx-vs라는 VirtualService로 전달

4) nginx-vs는 모든 경로(`"/"`)의 트래픽을 nginx-service의 80번 포트로 라우팅

5) NGINX 서비스가 트래픽을 받아 처리

> [!WARNING] 추가고려사항

NodePort 말고 LoadBalancer로 설정하여 아이피를 설정할 수 있다.

```
apiVersion: v1
kind: Service
metadata:
  name: istio-ingressgateway-loadBalancer
  namespace: istio-system
spec:
  type: LoadBalancer
  externalIPs:
    - 192.168.2.172  # 외부 IP 설정
  selector:
    app: istio-ingressgateway
  ports:
    - name: http2
      port: 80
      targetPort: 8080
    - name: https
      port: 443
      targetPort: 8443
```

> [!CHECK] 이제부터 dns 설정에 따른 gateway 테스트 점검

**Nginx 설정**

아래와 같이 `labs-nginx.x2bee.com`와 `labs-argocd.x2bee.com`를 동일한 Nginx conf에 정의하고,
Tplink를 통해서 동일하게 k8s Istio gateway로 요청이 넘어가게 작업을 하였다.
하면, 지금까지 작성했던 내용 기반으로 같은 Pod Nginx까지 도달하게 된다.
```
root@ip-10-0-1-86:/etc/nginx/conf.d/labs-pc# cat labs-istio.conf
server {
        listen 80;
        server_name labs-nginx.x2bee.com labs-argocd.x2bee.com;
        return 301 https://$host$request_uri;
}
server {
         listen 443 ssl;
         server_name labs-nginx.x2bee.com labs-argocd.x2bee.com;

         location / {
                 proxy_redirect off;
                 proxy_http_version 1.1;
                 proxy_pass_header Server;
                 proxy_connect_timeout 600;
                 proxy_send_timeout 600;
                 proxy_read_timeout 600;
                 send_timeout 600;
                 proxy_set_header X-Scheme $scheme;
                 proxy_set_header Host $host;
                 proxy_set_header X-Real-IP $remote_addr;
                 proxy_set_header X-Forwarded-Proto $scheme;
                 proxy_pass http://118.223.251.22:10055;
        }
}
```

*여기까지 점검이 되었다면*

Nginx VirtualService를 수정하여 서로 다른 Service Nginx까지 도달하도록 작업을 진행해본다.

*연습용 nginx pod 2*
```
apiVersion: v1
kind: Pod
metadata:
  name: nginx-test-2
  namespace: hello-world
  labels:
    app: nginx-2
spec:
  containers:
  - name: nginx-2
    image: nginx:latest
    ports:
    - containerPort: 80
```

*연습용 nginx service 2*
```
apiVersion: v1
kind: Service
metadata:
  name: nginx-service-2
  namespace: hello-world
spec:
  selector:
    app: nginx-2
  ports:
    - protocol: TCP
      port: 80  # 서비스가 노출할 포트
      targetPort: 80  # Pod에서 노출된 포트
      nodePort: 30008  # 외부에서 접근할 수 있는 포트
  type: NodePort  # 외부에서 접근할 수 있는 방식
```

위 두가지 설정을 배포 한 뒤 확인.
필요시 Pod의 `/usr/share/nginx/html/index.html` 로 가면 index.html 파일이 있으니 타이틀 정도만 수정하여 구분이 가도록 합니다.

![[Pasted image 20241025082432.png]]
![[Pasted image 20241025082446.png]]

도메인 준비
https://labs-nginx.x2bee.com
https://labs-nginx2.x2bee.com

```
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: nginx-vs
  namespace: hello-world
spec:
  hosts:
  - "labs-nginx.x2bee.com"  # 첫 번째 도메인
  - "labs-nginx2.x2bee.com"  # 두 번째 도메인
  gateways:
  - hello-world-gateway  # 사용 중인 Gateway
  http:
  - match:
    - uri:
        prefix: "/"  # 모든 경로 허용
      headers:
        host:
          exact: "labs-nginx.x2bee.com"  # 첫 번째 도메인 매칭
    route:
    - destination:
        host: nginx-service  # 첫 번째 NGINX 서비스
        port:
          number: 80
  - match:
    - uri:
        prefix: "/"  # 모든 경로 허용
      headers:
        host:
          exact: "labs-nginx2.x2bee.com"  # 두 번째 도메인 매칭
    route:
    - destination:
        host: nginx-service-2  # 두 번째 NGINX 서비스
        port:
          number: 80
```

접속 테스트하면 끝.