#### 온프레미스 및 EC2 기반 VM, Docker, Kubernetes 모니터링 구축

> [!NOTE] 본격적인 이유
> 생각보다 깔끔한 공학도적인 대시보드, 구성하기 쉬운 모니터링 차트
> 직관적이고 누구나 쉽게 재구성가능한 UI 끝으로 프로메테우스 데이터 수집

*Zabbix 설치는 Docker 모니터링편에서 다루었습니다.*

#### Zabbix로 온프레미스 + VM 직접 모니터링 구성하기

온프레미스 호스트 (PC) + 각 특징적인 VM (K8S + Jenkins-slave)에 대한 모니터링 대시보드를 구성

![[Pasted image 20250331154302.png]]

#### Zabbix로 K8S Pod 직접 모니터링 구성하기

여기에 추가적으로 프로메테우스 연동을 통한 K8S 모니터링 구성까지.

*(수행 CLI)*

```
wget https://get.helm.sh/helm-v3.9.3-linux-amd64.tar.gz
```

```
tar xvf helm-v3.9.3-linux-amd64.tar.gz
```

```
sudo mv linux-amd64/helm /usr/local/bin
```

*cleanup*

```
rm helm-v3.9.3-linux-amd64.tar.gz && rm -rf linux-amd64
```

```
helm version
```

> [!CHECK] check helm CLI
> bash: helm: command not found...

```
curl -LO https://get.helm.sh/helm-v3.14.4-linux-amd64.tar.gz
```

```
tar -zxvf helm-v3.14.4-linux-amd64.tar.gz
```

```
sudo mv linux-amd64/helm /usr/local/bin/helm
```

```
sudo chmod +x /usr/local/bin/helm
```

```
echo 'export PATH=$PATH:/usr/local/bin' >> /root/.bashrc
source /root/.bashrc
```

*url check*

나중에 안 사실. k8s에 설치시 버전을 일치시켜서 설치해주자. 7.2.4

![[Pasted image 20250401144616.png]]

```
(버전 ...)
helm repo add zabbix-chart-6.0  https://cdn.zabbix.com/zabbix/integrations/kubernetes-helm/6.0

(확인하자 ...)
helm repo add zabbix-chart-7.2 https://cdn.zabbix.com/zabbix/integrations/kubernetes-helm/7.2
```

```
(버전 ...)
helm show values zabbix-chart-6.0/zabbix-helm-chrt > $HOME/zabbix_values.yaml

(확인하자 ...)
helm show values zabbix-chart-7.2/zabbix-helm-chrt > $HOME/zabbix_values.yaml
```

*sudo vim zabbix_values.yaml*

zabbix proxy

```
## Note that since version 6.0 the variable ZBX_SERVER_PORT is not supported anymore. Instead, add a colon (:) followed by the port number to the end of ZBX_SERVER_HOST value.  

- name: ZBX_SERVER_HOST  
	value: 192.168.0.4:10051 or domain name + port number
	(ex: 192.168.2.249:10051)

## Zabbix proxy data Persistent Volume mount root path
##
mountPath: /data/zabbix
```

zabbix agent

```
- name: ZBX_SERVER_HOST  
   value: 192.168.2.249
   
- name: ZBX_PASSIVESERVERS  
   value: 0.0.0.0/0
```

```
kubectl create namespace zabbix-monitoring
```

```
(설치 마다 다름 우선 $KUBECONFIG로 설치 경로를 확인 구태여 변경필요없음)
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
```

```
(버전 ...)
helm install zabbix zabbix-chart-6.0/zabbix-helm-chrt --dependency-update -f $HOME/zabbix_values.yaml -n zabbix-monitoring

(확인하자 ...)
helm install zabbix zabbix-chart-7.2/zabbix-helm-chrt --dependency-update -f $HOME/zabbix_values.yaml -n zabbix-monitoring
```

*설치결과*

```
[root@k8s-master tech]# helm install zabbix zabbix-chart-6.0/zabbix-helm-chrt --dependency-update -f $HOME/zabbix_values.yaml -n zabbix-monitoring
NAME: zabbix
LAST DEPLOYED: Mon Mar 31 17:20:38 2025
NAMESPACE: zabbix-monitoring
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Thank you for installing zabbix-helm-chrt.

Your release is named zabbix.
Zabbix agent installed:  "zabbix/zabbix-agent2:alpine-6.0.33"
Zabbix proxy installed:  "zabbix/zabbix-proxy-sqlite3:alpine-6.0.33"

Annotations:
app.kubernetes.io/name: zabbix-zabbix-helm-chrt
helm.sh/chart: zabbix-helm-chrt-1.4.7
app.kubernetes.io/version: "6.0.33"
app.kubernetes.io/managed-by: Helm


Service account created:
    zabbix-service-account

To learn more about the release, try:

  $ helm status zabbix -n zabbix-monitoring
  $ helm get all zabbix -n zabbix-monitoring
```

*설치된 내용 확인*

```
kubectl get ns | grep zabbix-monitoring

kubectl get all -n zabbix-monitoring

helm status zabbix -n zabbix-monitoring

kubectl get secret zabbix-service-account -n zabbix-monitoring -o jsonpath={.data.token} | base64 -d
```

*접근은 위한 서비스 타입 수정*

ClusterIP를 **NodePort** 또는 **LoadBalancer** 유형으로 변경

zabbix-zabbix-helm-chrt-agent

```
kubectl get svc zabbix-zabbix-helm-chrt-agent -n zabbix-monitoring -o yaml > zabbix-agent-service.yaml
```

zabbix-zabbix-helm-chrt-proxy

```
kubectl get svc zabbix-zabbix-helm-chrt-proxy -n zabbix-monitoring -o yaml > zabbix-agent-proxy.yaml
```
