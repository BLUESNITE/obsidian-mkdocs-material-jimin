**동작 구조**

- GitLab -> 웹 , 소스 , 파이프라인 실행 관리 -> .gitlab-ci.yml 로 Job이 정의됨
- Job -> GitLab Runner (Job이 전파되서 실행되는 에이전트/Docker, Shell 등) -> Executor 수행

```mermaid
flowchart TB
    subgraph GitLab Server
        A[사용자 Git Push]
        B[Pipeline Trigger]
        C[Job 요청 대기]
    end

    subgraph GitLab Runner
        D[gitlab-runner 등록됨]
        E[Job 받아옴]
        F[컨테이너에서 script 실행]
        G[로그/결과 반환]
    end

    A --> B --> C
    C --> D
    D --> E --> F --> G --> C
```

![[Pasted image 20250409082721.png]]

**1. 별도의 VM 서버에 작업시, 도커 설치**

```
deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update -y
sudo apt-get install docker-ce -y
```

**2. 도커 Runner 설치**

깃버전 체크하여 가능한 동일한 버전으로 진행 17.4

```
docker pull gitlab/gitlab-runner:17.4
```

```
version: "3.3"
services:
  gitlab-runner:
    container_name: gitlab-runner
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /srv/gitlab-runner/config:/etc/gitlab-runner
    image: gitlab/gitlab-runner:v17.4.0
networks: {}
```

*설치한 Docker 컨테이너에서의 CLI run*

```
gitlab-runner run

(사용 형식)
/etc/gitlab-runner/config.toml
```

> [!TIP] token 확인/발급
> 프로젝트 CD/CD > Set up a specific Runner manually

*Runner Agent에 세팅을 하게 될 Project Runner Tag 및 Token 발급 & 세팅 과정*

아래의 페이지에서 Project Runner 생성

![[Pasted image 20250407171709.png]]

![[Pasted image 20250407172015.png]]

Tags runners-opensearch-project
Description runners-opensearch-project

*Register Runner*

![[Pasted image 20250407172646.png]]

이 토큰 값이 Runner Agent에 register 입력할 내용 

*token* glrt-Lg-xxxxxxxxxxxxxxxxxZz

```
gitlab-runner register --name my-runner --url "http://gitlab.x2bee.com" --token my-authentication-token
```

(아래 CLI로 진행시 *ALL ENTER*)
```
sudo gitlab-runner register \
  --url https://gitlab.x2bee.com \
  --registration-token glrt-Lg-xxxxxxxxxxxxxxxxxZz \
  --name "runners-opensearch-project" \
  --executor docker \
  --docker-image gitlab/gitlab-runner:alpine-v17.4.2
```

![[Pasted image 20250407173203.png]]

![[Pasted image 20250407173338.png]]

![[Pasted image 20250407173442.png]]

*GPT가 Docker in Docker의 경우 아래 설정을 하라는데 나중에 보겠다*

```
[runners.docker]
  privileged = true  # docker-in-docker 사용할 경우
  volumes = ["/cache", "/var/run/docker.sock:/var/run/docker.sock"]
```

**파이프라인 내용이 필요하다**

Jenkins Jenkinsfile 구조의 groovy 스크립트를 실행하는 것과 비슷하게
Gitlab Runners cicd 구조의 yml 기반 Runner 소스 작성하는데

.gitlab-ci.yml 이 파일 내용 자체가 파이프라인 수행내용!

하단 내용은 간략하게 작성된것

```
stages:
  - test

check-runner:
  stage: test
  tags:
    - runners-opensearch-project   # → Runner에 등록한 태그
  script:
    - echo "Hello, GitLab CI/CD + Runner!"
```

*픽업 확인*

러너가 작업을 픽업할 수 있는지 수동으로 확인

```
gitlab-runner runners-opensearch-project

FATAL: Command runners-opensearch-project not found. 
```

잘안되었는데. 처음부터 delivery 부터 runner까지 다시 체크

*1. 프로젝트에서 Project runners 활성화 확인*

![[Pasted image 20250408093913.png]]

*2. 프로젝트에 .gitlab-ci.yml 작성*

![[Pasted image 20250408094043.png]]

.gitlab-ci.yml 재작성 (실행 성공본)

```
stages:
  - test
image: alpine:latest
check-runner:
  stage: test
  tags:
    - runners-runners-project   # → Runner에 등록한 태그
  variables:
    GIT_STRATEGY: none
    CI_REPOSITORY_URL: "http://jeongzmin:xxxxxxxxxxxxxxxxxZz@gitlab.x2bee.com/tech-team/x2bee-ait/x2bee-runners.git"
  script:
    - echo "✅ 러너가 정상 작동 중입니다."
```

*3. Gitlab 프로젝트에서 파이프라인 편집기 내용 확인*

![[Pasted image 20250408094133.png]]

*4. Gitlab 프로젝트에서 파이프라인 시뮬레이션 검증*

![[Pasted image 20250408094242.png]]

*5. Gitlab 프로젝트 파이프라인 확인*

![[Pasted image 20250408094530.png]]

실패 트러블 슈팅 1

```
Preparing environmentRunning on runner-5ztasdskx-project-589-concurrent-0 via 33ef79219599...Getting source from Git repositoryFetching changes with git depth set to 20...Reinitialized existing Git repository in /builds/tech-team/x2bee-ait/x2bee-runners/.git/remote: HTTP Basic: Access denied. The provided password or token is incorrect or your account has 2FA enabled and you must use a personal access token instead of a password. See http://gitlab.x2bee.com/help/topics/git/troubleshooting_git#error-on-git-fetch-http-basic-access-deniedfatal: Authentication failed for 'http://gitlab.x2bee.com/tech-team/x2bee-ait/x2bee-runners.git/'Cleaning up project directory and file based variablesERROR: Job failed: exit code 1
```

프로젝트 CI_REPOSITORY_URL 변수 설정 해보기
GitLab 웹 → 해당 프로젝트 → Settings → CI / CD → Variables 에서

Key `CI_REPOSITORY_URL`
Value `http://<username>:<your_token>@gitlab.x2bee.com/tech-team/x2bee-ait/x2bee-runners.git`

(X)
http://jeongzmin@plateer.com:<your_token>@gitlab.x2bee.com/tech-team/x2bee-ait/x2bee-runners.git

(O) - Value
http://jeongzmin:xxxxxxxxxxxxxxxxxZz@gitlab.x2bee.com/tech-team/x2bee-ait/x2bee-runners.git

> [!CHECK] PAT
> Personal Access Token (개인 엑세스 토큰)

개인토큰 runer `xxxxxxxxxxxxxxxxxZz` and feed token `tBEU_847J4npi_5598xS`

밑도끝도없이 설정하면 되는지 모르지만 일단 수행

![[Pasted image 20250408095628.png]]

*Shell 실행에 대한 이슈가 발생하여 아래와 같이 runner의 이미지를 교체*

```
version: "3.3"
services:
  gitlab-runner:
    container_name: gitlab-runner
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /srv/gitlab-runner/config:/etc/gitlab-runner
    image: gitlab/gitlab-runner:alpine-v17.4.2
networks: {}
```

```
gitlab-runner register \
  --url https://gitlab.x2bee.com \
  --registration-token glrt-5zTaSdSkxp5TsoKAamei \
  --name "runners-runners-project" \
  --executor docker \
  --docker-image gitlab/gitlab-runner:alpine-v17.4.2
```

수행 성공시

![[Pasted image 20250408184944.png]]

![[Pasted image 20250408184953.png]]

**위까지는 간단 동작까지 end 이고, gitlab-ci.yml로 파이프라인을 본격적 작성 필요**

