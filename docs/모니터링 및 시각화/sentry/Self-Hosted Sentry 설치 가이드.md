### Sentry Self-Hosted 설치 가이드

> [!NOTE] 최소 사양 권장
> - 4 CPU Cores
> - 16 GB RAM
> - 20 GB Free Disk Space
>    
>    
> *8GB RAM에서 설치 시 `install.sh`에서 오류가 발생함. 요구 사양을 준수하자.*

#### 설치 과정

- 최신 버전 정보 가져오기
- Sentry 소스 클론
- 최신 버전으로 체크 아웃
- 설치 수행

```
VERSION=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/getsentry/self-hosted/releases/latest)

VERSION=${VERSION##*/}

git clone https://github.com/getsentry/self-hosted.git

cd self-hosted

git checkout ${VERSION}

./install.sh
```

>After installation, run the following to start Sentry:

*docker compose up --wait*

**설치 과정에서 ~**

*관리자 생성*

>Would you like to create a user account now? [Y/n]:

```
y
Email: jeongzmin@plateer.com
Password: Xxxxxxxxxxx1
```

브라우저 확인 -> http://<서버_IP>:9000

**트러블 슈팅**

*로그인 세션 이슈 발생시 아래의 내용을 재수행*

```
docker compose down

docker compose up -d
```

*.env 설정 추가*
```
SENTRY_USE_SSL=true
SENTRY_SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
```

*127.0.0.1:9000 으로 로그인 시도*

아래의 Sentry 설정 진행 입력값
- Root URL : https://sentry-dev.x2bee.com

![[Pasted image 20250418085550.png]]

![[Pasted image 20250418085602.png]]

![[Pasted image 20250418085616.png]]

*SMTP 서버 설정*

sentry/config.yml (핵심파일)

```
###############
# Mail Server #
###############

mail.backend: 'smtp'  # Use dummy if you want to disable email entirely
mail.host: 'email-smtp.ap-northeast-2.amazonaws.com'
mail.port: 587
mail.username: 'AKIAUUQIW2OL3LXNQ6MY'
mail.password: 'xXxxxxxxxxxxxxxx'
# NOTE: `mail.use-tls` and `mail.use-ssl` are mutually exclusive and should not
#        appear at the same time. Only uncomment one of them.
mail.use-tls: true
mail.use-ssl: false
mail.from: 'plateer_adm@plateer.com'
```

*서비스 도메인 설정*
```
system.url-prefix: 'https://sentry-dev.x2bee.com'
```

서비스 도메인까지 설정하면 왠만해서는 호스팅 및 로그인이 성공 될것이다.

#### 설정 과정

**계정 세부 정보**

사이트 메뉴에서 -> 설정을 찾아서 아래와 같은 이미지 화면에서 계정 세부 정보를 갱신하자.

![[Pasted image 20250418094057.png]]

이름, 테마, 언어, 시간대 등이 있는데 특히 *서울* 설정은 꼭 진행하자.

**이메일**

![[Pasted image 20250418094428.png]]

메일 전송이 안된다면 ... 어떻게 해서든 트러블 슈팅을 통해서 전송되도록 고쳐놓도록 하자

*설정을 바꾸면 빠른 재적용*

```
docker compose restart web
```

```
docker compose run --rm web sentry django sendtestemail jeongzmin@plateer.com
```

