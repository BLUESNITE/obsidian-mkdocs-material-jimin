## 1. 소개

> [!INFO] 이 사이트를 호스팅하기까지의 내용 작성입니다.
> 사실 이 전부터 개인 호스팅블로그에 대한 욕심은 많았었던 것 같다.
> 네이버 블로그, 티스토리, 팀블로그, 노션 등 ... 그러나 왠지 모를 이유로 늘 부족했고 아쉬웠다.
> 그래서 일까 각이 보이자마자 이것저것 다 쑤셔가며 만들어냈다. 아래는 그 과정이다.

> [!CHECK] 주저리
> 먼저, 짚고 넘어 갈 것 포인트. 나는 `개인용 외부아이피`를 가지는데 어려움을 겪고있다.
> 팀장님은 `라즈베리파이`와 `duckdns`를 활용하라며 이야기를 하시는데. 둘다 기본적으로 마음에 들지 않는다. 결국 내가 블로그를 운영하기 위해서 가지고 싶은건 안정적으로 `24시간 호스팅` 할 수 있는 `외부 아이피를 보유한 컨테이너`이다.

---

## 2. 작업

첫번째로 `가비아`에서 도메인을 아주 저렴하게 사고 산김에 확인해보니 `컨테이너 호스팅`이 있어 Node기반의 가장 싼 `라이트 컨테이너`를 구매해보았다. 아래는 기본사양이다

### 2.2. 가비아 컨테이너 호스팅

**가비아의 컨테이너 호스팅 Nodejs 라이트**

- 월비용 2500원
- 메모리 256MB
- 트래픽 월 24GB
- 웹 500MB
- DB 500MB
- Redis 미제공
- 메일 2개/2GB
- 설치비 만원 (타사도메인 3만원)

여기에서 한번 멈칫하였다. 마지막 한줄을 읽지 않고 들어갔더니 `예상 결제비용이 32500원` ...
결국에는 `자사도메인` 이었기에 `결제는 12500원 진행`하였다.

여기서 한가지 의문부호가 들긴하다.
`호스팅으로 컨테이너 서비스`를 이용하는데 왜 `설치비용`이 별도로 들지?
선택지가 없어서 일단 진행은 했었다.

신청하고 두어시간이 흐른뒤. 접속할 수 있는 정보가 생성되었고 `SSH` 접속을 해보았다가.
접속 10분도 되지않아 환불신청을 하게 되었다.

이유인 즉슨 `root`에 대한 권한. `가비아` 측 답변을 짧게 요약하면 `다수의 고객들이 이용하는 공용서버 환경에서 제공되며 root 권한 및 슈퍼유저 권한이 제공되지 않습니다.`라고 답변을 받았다. 다소 아쉬움 ... 나같은 이상한놈들은 무조건 `root`권한이어야 한다. 기본목적 말고도 이거저거 다 할 것이기 때문에.

---

### 2.3. Vultr 컨테이너 호스팅

**그래서 넘어간, Vultr**
국내에는 내 성격에 맞는 업체를 찾을 수가 없었다. 그래서 GPT에 물어서 알게 된 사이트이다.
해당 사이트에서는 여러가지를 선택 할 수가 있었고, 마찬가지로 최소 비용으로 서비스를 요청했다.

- 월비용 약6900원
- 1 vCPU
- 메모리 1024MB
- Storage 25GB
- OS Ubuntu 22.04

무엇보다 처음부터 `root` 계정을 부여해준다.

---

## 1. 서버에 작업

**서버에서의 세팅**

이 부분은 사실별거 없다. 내 Github Clone 해다가 주기적으로 Pull 받게하고. 서비스 등록하는 정도.

> git clone

```Shell
git clone https://<개인토큰>@github.com/<개인깃헙>/project-obsidian-quartz4.git
```

> git pull 전략 (이미지로 말지 않을 계획이라 종종 pull 받을때 쫑나는 걸 방지)

아래 내용은 crontab에서 사용할 git-pull.sh로 저장

```Shell
git reset --hard HEAD
git fetch origin
git reset --hard origin/main
```

> 서비스 등록관리

```Shell
[Unit]
Description=Quartz Build and Serve
After=network.target

[Service]
ExecStart=/usr/bin/npx quartz build --serve -d /project/<깃프로젝트>/content
WorkingDirectory=/project/<깃프로젝트명>
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root

[Install]
WantedBy=multi-user.target
```

> crontab을 활용한 자동배포

```Shell
crontab -e

*/10 * * * * /bin/bash /blog/git-pull.sh
```

---

**늦은 소개 Obsidian Quartz4**

Quartz4에 대한 소개는 내 블로그 최하단 `footer`를 확인해도 된다.

*초기버전*

![[Pasted image 20240922135125.png]]