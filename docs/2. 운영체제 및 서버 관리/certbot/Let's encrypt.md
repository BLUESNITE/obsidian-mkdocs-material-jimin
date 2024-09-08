![[Pasted image 20240703152646.png]]

#### **Let's Encrypt**

Let's Encrypt를 사용하여 와일드카드 SSL 인증서를 생성해서 여러 하위 도메인에 대해 하나의 인증서를 사용할 수 있는 방법을 알아보겠습니다. 와일드카드 인증서를 사용하면 도메인의 여러 서브도메인에 대해 인증을 제공하므로 관리가 용이하고 유연성을 얻을 수 있습니다. 아래는 와일드카드 SSL 인증서를 생성하는 데 필요한 과정에대한 설명 입니다.

#### **와일드 카드 인증서 및 DNS-01 챌린지 쉽게 이해하기**

- 와일드 카드 인증서
- DNS-01 챌린지
- Certbot

**1. 와일드 카드 인증서**

와일드카드 인증서는 하나의 인증서로 여러 서브도메인을 보호할 수 있는 SSL 인증서입니다. 예를 들어, blue.com 도메인의 와일드카드 인증서를 생성하면 다음과 같은 서브도메인에서 사용 할 수 있습니다.

- \*.blue.com (예: sub.blue.com, argocd.blue.com, api.blue.com 등)

즉, 와일드카드 인증서를 사용하면 각 서브도메인마다 별도의 인증서를 발급받을 필요 없이 하나의 인증서로 사용 할 수 있습니다.

**2. DNS-01 챌린지**

DNS-01 챌린지는 도메인 소유권을 증명하기 위한 방법 중 하나입니다. Let's Encrypt는 와일드카드 인증서를 발급하기 위해 DNS-01 챌린지를 요구합니다. 이 과정에서 특정 값을 가진 DNS TXT 레코드를 도메인 설정에 추가해야 합니다. DNS-01 챌린지 수행 방법은 아래에서 조금 더 상세하게 다루겠습니다.

**간략한 방법의 설명은 다음과 같습니다.**

1. Certbot이 제공하는 값을 DNS TXT 레코드로 추가합니다.
2. 이 레코드가 전파되면 Let's Encrypt가 이를 확인하여 도메인 소유권을 증명합니다.
3. Google Admin Toolbox 같은 사이트를 이용하여 전파 확인 가능합니다.

DNS-01 챌린지를 처음 접한다면 다소 어렵게 느껴질 수 있습니다. 특히, 여러 서브도메인을 설정해야 하는 경우 복잡할 수 있습니다. 그러나 기본적으로 제공된 지침을 따르고 DNS 관리 콘솔에서 정확히 설정하면 문제없이 인증서를 발급받을 수 있습니다.

**3. Certbot**

Certbot은 Let's Encrypt에서 SSL 인증서를 자동으로 발급받고 갱신해주는 도구입니다. 특히, Certbot을 사용하면 와일드카드 인증서도 쉽게 발급받을 수 있습니다.

#### **Quick Start (우분투환경)**

**- 설치**

```shell
sudo apt-get update
sudo apt-get install certbot
```

**- 생성**

```shell
sudo certbot certonly --manual --preferred-challenges=dns -d '*.example.com' -d 'example.com'
```

참고 위와 같이 생성을 수행한다면 DNS 챌린지를 두번 수행하게 됩니다.

**- 과정**
![[Pasted image 20240703152735.png]]

이 단계에서 DNS-01 챌린지를 수행해야합니다. 이때 Certbot이 와일드 카드 인증서 요청을 한 상태이고,

우리는 이 정보를 가지고 도메인 소유권을 증명하게 됩니다. 이하는 AWS Route 53을 통해서 DNS TXT 레코드를 설정하고 전파 확인하는 과정입니다.

**- 레코드 생성과 동기화 확인**

아래에 미리 등록해두었던 레코드 정보가 있습니다. 여기에서 설정하게 될 요소는 딱 3가지 입니다.

- 레코드 이름
- 레코드 유형
- 값

TXT 레코드 유형으로 설정 후 위 이미지에 Certbot이 와일드 카드 인증 요청한 내용에서의 도메인 정보를 레코드 이름에 value 값을 동일한 value(값)에 작성합니다.

![[Pasted image 20240703152816.png]]

**- Google Admin Toolbox로 전파 확인**

링크 정보 ([https://toolbox.googleapps.com/apps/dig/#TXT](https://toolbox.googleapps.com/apps/dig/#TXT))

일반적으로 레코드 정보를 수정 또는 생성한 후에 레코드의 상태만 INSYNC 확인 하면 되지만 반복적으로 실패한다면 전파 확인이 필수 적입니다.

![](https://blog.kakaocdn.net/dn/UKGWo/btsH7Ac6Fpy/MxWyNFzhsgTmhvQC32Jjw1/img.png)

구글 툴박스에서의 확인

![[Pasted image 20240703152845.png]]

위와 같이 TXT VALUE가 내가 설정한 값으로 보인다면 전파확인이 완료 된 것입니다.

이제 다시 CLI 창으로 가서 Enter를 눌러줄 준비가 완료 되었습니다.

**- Certbot에서 Enter 후 생성**

인증서가 생기면 사실상 원하는 목표지점까지 완료가 된 것입니다.

하지만 오류가 있거나 자동화 까지 목적이 추가작성하였습니다.

**- 이중 와일드 카드 서브도메인에 적용하기**

단순하게 와일드 카드에 서브 프리픽스에 도메인으로 작성된 경우에는 아래 이미지와 같이 전파확인이 안될 수 있습니다.

이때 Certbot도 인증서를 생성해 내지 못합니다.

CNAME 전파를 위해 대기중

![](https://blog.kakaocdn.net/dn/c0RC4B/btsH703E2h0/FSvvGPlA3dsNdUmR9u9dhK/img.png)

**- 도커를 사용하여 자동화 하기**

도커를 사용하면 호스트 시스템을 깨끗하게 유지할 수 있고, 이미 운영 중인 Nginx의 80 포트와의 충돌을 피할 수 있습니다. 일반적으로 Certbot 자동화가 필요한 환경에서는 Nginx와 같은 80 포트를 점유하는 어플리케이션이 있을 가능성이 매우 높습니다. 이러한 문제를 해결하기 위해 도커를 사용하여 인증서를 생성하도록 하고 볼륨 설정을 통해 원하는 위치의 Nginx에서 사용하는 인증서를 자동으로 갱신하는 계획을 세워보겠습니다.

**도커로 인증서 생성 동작**

```
docker run -it --rm --name certbot -p 7979:80 -v '/etc/nginx/volume-file/letsencrypt:/etc/letsencrypt' -v '/etc/nginx/volume-file/lib/letsencrypt:/var/lib/letsencrypt' -v '/etc/nginx/volume-file/letsencrypt/archive/blue.com:/etc/nginx/blue.com' certbot/certbot certonly -d '*.blue.com' --manual --preferred-challenges dns
```

아래는 /etc/nginx에 볼륨을 연결하고 생성된 파일인 인증서 파일을 /etc/nginx/blue.com에 배치 시켰습니다.

```
docker run -it --rm --name certbot -p 7979:80 -v '/etc/nginx/volume-file/letsencrypt:/etc/letsencrypt' -v '/etc/nginx/volume-file/lib/letsencrypt:/var/lib/letsencrypt' -v '/etc/nginx/volume-file/letsencrypt/archive/blue.com:/etc/nginx/blue.com' certbot/certbot certonly -d '*.blue.com' --manual --preferred-challenges dns
```

그 다음 작업으로 갱신 작업을 작성해 보겠습니다.

**- 사전 작업 expect 설치**

```
sudo apt-get update -y
sudo apt-get install expect -y
##(권한부여)
chmod +x /etc/nginx/renew_cert.exp
##(실행)
/etc/nginx/renew_cert.exp
```

**- renew_cert.exp  작성**

```
#!/usr/bin/expect -f
set timeout -1

spawn docker run -it --rm --name certbot \
   -p 7979:80 \
   -v "/etc/nginx/volume-file/letsencrypt:/etc/letsencrypt" \
   -v "/etc/nginx/volume-file/lib/letsencrypt:/var/lib/letsencrypt" \
   -v "/etc/nginx/volume-file/letsencrypt/archive/blue.com:/etc/nginx/blue.com" \
   certbot/certbot certonly --manual --preferred-challenges dns -d "*.blue.com"

expect "What would you like to do?"
send "2\r"
expect eof
```

- **renew_cert.exp 파일 실행 스케줄링**

이건 아직 고민중입니다.

내장형이 아닌 관리를 하고 싶은데. 유력한 후보는 jenkins를 통해서 스케줄링하고 ssh 실행.
