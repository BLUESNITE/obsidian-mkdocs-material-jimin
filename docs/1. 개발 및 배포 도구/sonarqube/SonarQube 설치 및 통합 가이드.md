## 목차
- [1. 소개]
- [2. 설치]
  - [2.1. Docker compose 파일]
  - [2.2. max_map_count 설정]
- [3. 젠킨스 파이프라인 통합]
  - [3.1. 소나큐브 웹에서 토큰 생성]
  - [3.2. 젠킨스 웹에서 설정]
- [4. 결론]
___
## 1. 소개
> [!INFO] 글설명
> **SonarQube는 코드 품질 및 보안 분석 도구**로서, **Jenkins와의 통합**을 통해 코드의 지속적인 검사를 자동화할 수 있습니다. 이 가이드는 SonarQube를 Docker 컨테이너로 설치하고, Jenkins 파이프라인에 통합하는 방법까지 다룹니다.

> [!CHECK] 주저리
> 소나큐브를 설치하고 파이프라인에 통합하는 과정은 생각보다 복잡했다.
> 도커 허브에서 소나큐브 이미지를 찾아 설치했고, 젠킨스 파이프라인에 통합까지 한땀한땀 검색해보면서 설정했다.
> 
> 특히 설치를 진행하면서 PostgreSQL 및 Elasticsearch와 같은 종속 항목 설정으로 인하여 다양한 오류가 발생 하였다. 아래에는 이러한 이슈들을 해결하고 개선하는 진행 과정이다.

___
## 2. 설치
> [!INFO] bitnami SonarQube 이미지를 이용하여 설치했습니다.
> 아래는 도커 compose 파일
```shell
services:
  sonarqube-postgresql:
    container_name: sonarqube-postgresql
    image: docker.io/bitnami/postgresql:16.3.0
    ports:
      - '5432'
    volumes:
      - 'postgresql_data:/bitnami/postgresql'
    environment:
      - ALLOW_EMPTY_PASSWORD=yes
      - POSTGRESQL_USERNAME=sonarqube
      - POSTGRESQL_DATABASE=sonarqube
    networks:
      - net-sonarqube

  sonarqube:
    container_name: sonarqube
    user: "root"
    image: docker.io/bitnami/sonarqube:10.5.1
    ports:
      - '8087:9000'
      - '8443'
    volumes:
      - 'sonarqube_data:/bitnami/sonarqube'
    depends_on:
      - sonarqube-postgresql
    environment:
      - ALLOW_EMPTY_PASSWORD=yes
      - SONARQUBE_DATABASE_HOST=sonarqube-postgresql
      - SONARQUBE_DATABASE_PORT_NUMBER=5432
      - SONARQUBE_DATABASE_USER=sonarqube
      - SONARQUBE_DATABASE_NAME=sonarqube
      - SONARQUBE_MAX_HEAP_SIZE=512m
      - SONARQUBE_MIN_HEAP_SIZE=512m
      - SONARQUBE_USERNAME=admin #초기값
      - SONARQUBE_PASSWORD=bitnami #초기값
    networks:
      - net-sonarqube

volumes:
  postgresql_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/sonarqube-data/postgres
  sonarqube_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/sonarqube-data/sonar

networks:
  net-sonarqube:
    driver: bridge
```

> [!TIP] max_map_count
> 소나큐브를 설치하면서 시행착오를 겪으면서 삽질을 통해서 알게 된 사실입니다. 생각보다 중요.
> 
> 이 설정은 소나큐브 보다 Elasticsearch를 위해 필요합니다.
> 자세하게 왜 필요한지 먼지 잘 몰라도 일단 아래를 보고 설정합니다.

> 호스트 서버에서의 설정
```shell
sudo sysctl -w vm.max_map_count=262144

or

sudo vim /etc/sysctl.conf 
vm.max_map_count=262144
sudo sysctl -p
```
___
## 3.젠킨스 파이프라인 통합
> [!NOTE] 소나큐브 웹에서 설정
> 1) Administrator > Security > Generate Tokens 으로 이동합니다.
>    (또는 우측 상단 프로필 My Account)
>    
> 2) Type User Token으로 젠킨스에서 사용할 Tokens을 생성합니다.
>   이때 생성한 토큰값은 잘 기록!
>   
> 아래는 예시    

*(생성했으나 안씀)*
```shell
jenkins-sonar User Token
squ_77747b1b5377277fdd5f7fbad2b33ac33125ea7d
```

*(이것만 사용)*
```shell
global-token Global Analysis Token
sqa_da78fbbae2e3a5570489beb59a034e88fd6888bc
```

>[!NOTE] 젠킨스 웹에서 웹 설정
> 3. 플러그인 설치 > Jenkins 로 이동 > Jenkins 관리 > sonarqube 검색 > SonarQube Scanner 설치
> 4. 스캐너 추가 > Jenkins 관리 > Tools > SonarQube Scanner installations
>    Name sonarqube
>    Version SonarQube Scanner 5.0.1.3006
> 5. 시스템 설정 > Jenkins 관리 > System > SonarQube servers > Add SonarQube
>    Name SonarServer
>    ServerUrl http://<소나큐브 URL>
>    Server authentication token <설정한 jenkins-sonar>
> 6. Global Credentials 생성 (먼저해야댐)
>    ID jenkins-sonar
>    Descriptions jenkins-sonar
>    Secret sqa_da78fbbae2e3a5570489beb59a034e88fd6888bc

> [!CODE] 파이프라인 소스에서의 작성내용
> ex) build.groovy
> 
> 
> 
```shell
/**
* Sonarqube Scanner in Jenkins
*/
def sonarqube() {
    stage('SonarQube analysis') {
        dir("project") {
            script {
                withSonarQubeEnv(installationName: 'SonarQube') {
                   sh "${MVN_COMMAND} sonar:sonar -Dsonar.projectKey=${프로젝트명} -Dsonar.host.url=<http://소나큐브 URL> -Dsonar.login=<생성했던 Secret Key>"
                }
            }
        }
    }
}
```

___
## 4.결론

> 젠킨스에서 빌드 캡쳐

![[Pasted image 20240718125743.png]]
