> [!NOTE] Argocd 쿠버네티스에 설치과정
> 1. 네임스페이 생성
> 2. install.yaml 로 설치 (하지만 난 yaml 파일을 보관하기 원하기에 파일다운로드로 진행)
> - 필요시 로드밸런서 연결

> 네임 스페이스 생성

```Shell
kubectl create namespace argocd
```

> 설치 파일 다운로드

```Shell
curl -O https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

> 쿠버에 apply

```Shell
kubectl apply -f 파일명
```

> 임의 패스워드 확인

```Shell
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath=``"{.data.password}" | base64 -d; echo

-- taf4BgdPn7hNRDWj
```

> 신규 패스워드 등록

```Shell
로그인 > Left [User Info] > Center [UPDATE PASSWORD]
```

> Settings Repositories 에서 아래와 같이 작성 (VIA HTTPS)

![[Pasted image 20240704122936.png]]

> Settings Projects 에서 아래와 같이 작성

```Shell
Project Name [생성]
Description [프로젝트명과 동일하게]
```

> 프로젝트 생성 후 1. Summary

```Shell
SOURCE REPOSITORIES
> https://gitlab.dev.x2bee-tech.com/onpremise/sandbox/x2bee-pipeline.git

SCOPED REPOSITORIES
> https://gitlab.dev.x2bee-tech.com/onpremise/sandbox/x2bee-pipeline.git

DESTINATIONS
> (Server) https://kubernetes.default.svc
> (Name) in-cluster
> (Namespace) 신규작성
```

> 프로젝트 생성 후 2. Roles

> [!NOTE] 주의
> role name은 파이프라인소스와 젠킨스 Credentials에 동일한 명칭으로 작성해야한다.

```Shell
(Role Name) sandbox-role
(Role Description) sandbox-role
(POLICY RULES)
> get application allow
> update application allow
> sync application allow
> * application allow
```

> 룰 작성 후 3. 다시열기 (CREATE 진행)

> [!NOTE] Title
> 다시 한번 열고 제일 하단으로 내려보면 JWT Tokens가 나오며
> 시크릿 값을 확인 할 수 있다. 이 값을 가지고 젠킨스 role에 값을 넣어준다.

```Shell
argocd-role-abcde-dev
> Kind Secret text
> Secret <argocd NEW TOKEN>
> ID argocd-role-abcde-dev
> Des argocd-role-abcde-dev
```

> 파이프라인 4. role 명칭 맞추기

> [!NOTE] Title
> 파일 검색으로 role 찾으면 많은 동일 값을 찾을 수 있다 이 것들을 전부 신규 작성하는
> role명칭으로 바꾸어 준다 ex) sandbox-role

> 젠킨스에 설치

아무튼 젠킨스에는 할게 졸라게 많다

```Shell
+ argocd app set -p application.build_number=91
/var/jenkins_home/workspace/onprem-abcde-dev/abcde-api-common@tmp/durable-8537bfbf/script.sh.copy: 2: argocd: Permission denied
```

> [!NOTE] Argocd cli 설치
> 젠킨스 실행이 되는 위치에 가서 Argocd cli를 설치해주어야한다.

```Shell
curl -LO https://github.com/argoproj/argo-cd/releases/download/v2.8.3/argocd-linux-amd64
curl -LO https://github.com/argoproj/argo-cd

나는 최신 버전이 좋으니까 깃헙에 버전업된 것이 있는지도 확인해보았다.

curl -LO https://github.com/argoproj/argo-cd/releases/download/v2.11.2/argocd-linux-amd64
```

아래는 한방에 실행 (이것도 도커 컴포즈시 자동 추가 항목이네)

```Shell
cd /usr/local/bin/
curl -LO https://github.com/argoproj/argo-cd/releases/download/v2.11.2/argocd-linux-amd64
mv argocd-linux-amd64 argocd
chmod 755 /usr/local/bin/argocd
argocd version
```

> 기타 CLI

```Shell
argocd login [argocd url] --grpc-web --insecure
username
password

argocd login 192.168.1.254:10031 --grpc-web --insecure
argocd login argocd-stg.abcde.com --grpc-web --insecure

docker login docker-stg.abcde.com
Username:
Password:
```
