## 목차

- [1. 소개]
- [2. 설치]
  - [2.1. Terraform 디렉토리 구성]
  - [2.2. Docker 작성]
- [3. 사용법]
  - [3.1. 기본 사용법(hello world)]
  - [3.2. Datasets 작성 및 연결]
  - [3.3. Chart 그리기]
- [4. 결론]

---

## 1. 소개

> [!INFO] 글설명
> 최근에 Terraform 작업에 빠져있는 상황인데, Superset 설치를 요청받았습니다.
> 그냥 설치하면 재미없을게 뻔하기 때문에 Terraform으로 Docker 기반의 Superset을 설치해본 내용을 정리해보겠습니다.

> [!CHECK] 주저리
> 그라파나도 빡셌는데. 역시나 BI와 연관된 것들은 대부분 설치가 복잡하다 ... 특히 내부적으로 오픈소스임이 강조되는 아파치를 매우 좋아하는 분위기인데, 난 아파치가 싫다 ... 시작도 전부터 사실 험난한 길이 예고된 ....

---

## 2. 설치

### 2.1. Terraform 디렉토리 구성

> [!INFO]
> 이번에 작성한 기본적인 Terraform 구성이다.
> Main modul과 Sub modul로 구성하였고, 기본 변수 정의한 것을 기반으로 git clone 부터 시작하여 대상 게스트에 file 전송한다음 docker가 실행되는 형태이다.

```
|   default-variables.tf
|   main.tf
+---log
\---modules
    +---docker-compose
    |       docker-compose.tf
    +---file-transfer
    |       .env
    |       file-transfer.tf
    |       superset-compose.yaml
    \---git
            git.tf
```

### 2.2. Docker 작성

> [!INFO]
> Docker 작성이라고 타이틀을 달아두었지만 실제로 직접작성하지 않고, 아파치 깃에서 복사해온다. _git clone https://github.com/apache/superset.git_

> [!TIP] **.env**파일 작성 (가장중요)
> 안내되는 docker compose 파일을 읽어보면 *SECRET_KEY*를 설정하라고 나와있는데 함정이다. 실제로는 *SUPERSET_SECRET_KEY*로 작성해주어야한다.

> .env 파일

```env
# 데이터베이스 설정
DB_USER=superset
DB_PASS=superset
DB_HOST=db
DB_PORT=5432
DB_NAME=superset

# 데이터베이스 설정
DATABASE_DIALECT=superset
DATABASE_HOST=superset
DATABASE_PORT=5432
DATABASE_DB=superset
DATABASE_USER=superset
DATABASE_PASSWORD=superset

# Redis 설정docker
REDIS_HOST=redis
REDIS_PORT=6379

# Superset 설정
# docker/pythonpath_dev/superset_config.py에 SECRET_KEY = '명령어를 통해 발급받은 시크릿 키'

 # 이부분이 함정 변수
SUPERSET_SECRET_KEY=xpmTm7bmW2VvptczSk7FqAhITyKxWo3WhPRAJruo4R2rkJ1waC4aQTTL
# SECRET_KEY=xpmTm7bmW2VvptczSk7FqAhITyKxWo3WhPRAJruo4R2rkJ1waC4aQTTL

SUPERSET_ENV=production
SUPERSET_WEBSERVER_PORT=8088
SUPERSET_WEBSERVER_TIMEOUT=60

#postgres
POSTGRES_DB=superset
POSTGRES_USER=superset
POSTGRES_PASSWORD=superset
```

> docker/pythonpath_dev/superset_config.py 파일에 추가할 내용

```py
SUPERSET_SECRET_KEY=xpmTm7bmW2VvptczSk7FqAhITyKxWo3WhPRAJruo4R2rkJ1waC4aQTTL
```

> [!CHECK]

> docker-compose-non-dev.yml을 compose한 결과

_docker compose -f docker-compose-non-dev.yml up -d --build_
![[Pasted image 20240816090049.png]]

---

## 3. 사용법

### 3.1. 기본 사용법 (hello world)

> [!INFO]
> 위와 같이 진행이 잘되었다면 기본계정 admin/admin으로 접속이 가능합니다.
> localhost:8088

### 3.2. Datasets 작성 및 연결

![[Pasted image 20240816090639.png]]
기본적으로 Datasets을 생성하기 위해서는 _우상단 Settings 메뉴의 > Database Connerctions_ 통해서 데이터베이스 연결이 필요합니다.

![[Pasted image 20240816090807.png]]
Datasets 메뉴에서는 *Database > Schema > Table*을 선택하면 쉽게 대상 테이블을 설정할 수 있고,

_SQL > SQL Lab_ 메뉴에서 대상 테이블의 쿼리를 작성하여 Dataset을 생성할 수도 있습니다.

### 3.3. Chart 그리기

![[Pasted image 20240816091134.png]]

*Chart*를 그릴때는 이전에 생성해둔 Dataset을 기반으로 다양한 Chart를 선택하여 그려볼 수 있습니다.

---

## 4. 결론

_나름의 (?) 정성 가득한_ hello world
![[Pasted image 20240816090444.png]]

> [!INFO]
> 간략한 후기로는 ... 비개발자 or 간단한 SQL 작성가능한 사용자라면 Superset이 좋을 수도 있겠다 싶었지만, BI 솔루션들에 비해 경쟁력이 있을지는 모르겠습니다.
