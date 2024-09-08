> [!NOTE] Title
> 호기심 200%로 설치해봄 / 쿠버네티스 모니터링

```Shell
sudo wget https://github.com/sqshq/sampler/releases/download/v1.1.0/sampler-1.1.0-linux-amd64 -O /usr/local/bin/sampler
sudo chmod +x /usr/local/bin/sampler
sudo yum install alsa-lib-devel -y
-- sudo apt install libasound2-dev
```

```shell
sudo cd /usr/local/bin/sampler
sudo sampler -c example.yml
/usr/local/bin/sampler -c
sampler -c /home/tech/sampler/example.yml
/usr/local/bin/sampler -c /home/tech/sampler/k8s-dev.yml
```

> 쿠버 모니터링

```shell
textboxes:
  - title: Kubernetes Services
    position: [[0, 0], [75, 20]]
    rate-ms: 3000
    color: 211
    sample: kubectl get svc --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,TYPE:.spec.type,CLUSTER-IP:.spec.clusterIP,EXTERNAL-IP:.status.loadBalancer.ingress[*].ip,PORT:.spec.ports[*].port'
  - title: Kubernetes top pod
    position: [[25, 20], [50, 20]]
    rate-ms: 3000
    color: 178
    sample: kubectl top pod -A
  - title: Kubernetes top node
    position: [[0, 20], [25, 20]]
    rate-ms: 3000
    color: 255
    sample: kubectl top node | awk '{printf "%-20s %-10s %-10s\n", $1, $2, $4}'
```

> 쿠버 모니터링

```shell
runcharts:
  - title: K8S Node Ram Usage
    position: [[0, 20], [40, 20]]
    rate-ms: 5000
    triggers:
      - title: RAM usage exceeded
        condition: echo "$cur > 80" |bc -l
        actions:
            terminal-bell: true
            sound: true
            visual: true
            script: 'say alert: ${label} : RAM exceeded ${cur}% of usage'
    legend:
        enabled: true
        details: false
    scale: 0
    items:
      - label: node1
        color: 178
        sample: kubectl top nodes | awk 'NR==2 {printf "%d", $5}'
      - label: node2
        sample: kubectl top nodes | awk 'NR==3 {printf "%d", $5}'
      - label: node4
        sample: kubectl top nodes | awk 'NR==4 {printf "%d", $5}'
  - title: K8S Node CPU Usage
    position: [[40, 20], [40, 20]]
    rate-ms: 5000
    triggers:
      - title: CPU usage exceeded
        condition: echo "$cur > 80" |bc -l
        actions:
            terminal-bell: true
            sound: true
            visual: true
            script: 'say alert: ${label} : CPU exceeded ${cur}% of usage'
    legend:
        enabled: true
        details: false
    scale: 0
    items:
      - label: node1
        color: 178
        sample: kubectl top nodes | awk 'NR==2 {printf "%d", $3}'
      - label: node2
        sample: kubectl top nodes | awk 'NR==3 {printf "%d", $3}'
      - label: node4
        sample: kubectl top nodes | awk 'NR==4 {printf "%d", $3}'
textboxes:
  - title: Kubernetes events
    position: [[0, 0], [65, 20]]
    rate-ms: 3000
    color: 211
    sample: kubectl get events -A | grep -e "Failed" -e "NAMESPACE"
```
