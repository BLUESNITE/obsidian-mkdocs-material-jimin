---
date:
  created: 2025-03-26
status: new
---
https://minikube.sigs.k8s.io/docs/start/?arch=/macos/arm64/stable/homebrew

#### 설치 (mac)
```
brew install minikube
brew install --cask docker
```

/opt/homebrew/Cellar/minikube/1.35.0
/opt/homebrew/Cellar/docker-completion/28.0.4

![[Pasted image 20250326152735.png]]

*실행테스트*
```
minikube start --driver=docker
```

> [!NOTE] Docker Desktop Kubernetes
> minikube 설치를 수행 중이지만, Docker Desktop에 내장 Kubernetes를 발견하여 메모 ...

*설치 완료 후*

minikube에는 자동내장설치된 kubernetes dashboard가 있다

```
minikube dashboard
```

해당 커맨드로 실행시

![[Pasted image 20250326155239.png]]

#### 실행 연습

*서비스*
```

kubectl create deployment hello-minikube --image=kicbase/echo-server:1.0

kubectl expose deployment hello-minikube --type=NodePort --port=8080

(일시적 선언)
kubectl port-forward service/hello-minikube 7080:8080
```

*사용종료*
```
minikube pause (일시중지)
minikube stop
```

*메모리한도 수정*
```
minikube config set memory 9001
```