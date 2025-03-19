> [!NOTE] Install
> Harbor는 기본적으로 [Docker Compose](https://docs.docker.com/compose/) 기반에서 운영됩니다

#### 선호되는 하드웨어 기준치

**CPU** 최소 2vcpu 선호 4vcpu
**MEM** 최소 4GB 선호 8GB
**디스크** 최소 40GB 선호 160GB
#### 설치

https://github.com/goharbor/harbor/releases 에서 releases를 확인하여 진행합니다.

latest 가 2.12.2 버전 일 경우

```
wget https://github.com/goharbor/harbor/releases/download/v2.12.2/harbor-online-installer-v2.12.2.tgz

tar xvf harbor-online-installer-v2.12.2.tgz

cd harbor
```

구성 파일

![[Pasted image 20250319151534.png]]

이어서 설치 내용을 *harbor.yml에 구성*

아이디 패스워드 도메인 정도

설치 CLI는 위 구성파일에 포함된 *install.sh*을 실행으로 

```
sh install.sh
```

....

놀랍게도 설치 끝

![[Pasted image 20250319160550.png]]

![[Pasted image 20250319161822.png]]