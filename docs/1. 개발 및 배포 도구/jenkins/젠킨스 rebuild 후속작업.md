#### install cli

```
cd /usr/local/bin/
curl -LO https://github.com/argoproj/argo-cd/releases/download/v2.11.2/argocd-linux-amd64
mv argocd-linux-amd64 argocd
chmod 755 /usr/local/bin/argocd
argocd version
```

> [!NOTE] 자동화가 필요해보임. 쉘스크립트 심어서 해결(?)
> 방법은 귀찮아서 나중에 찾고 기록기록

```
argocd login argocd-dev.abcde.com --grpc-web --insecure
username
password

docker login docker-dev.abcde.com
Username:
Password:
```
