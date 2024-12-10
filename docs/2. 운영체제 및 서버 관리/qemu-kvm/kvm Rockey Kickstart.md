> [!INFO] Kickstart
> Kickstart는 Red Hat 계열의 Linux 배포판에서 무인 설치를 자동화 하는데 사용되는 파일 기반의 설치 방식입니다. Kickstart를 정의하여 일관성 있는 시스템 설치가 가능합니다.

**주요 구성 요소**
- 기본 시스템 설정
- 설치 소스
- 디스크 파티션
- 패키지 설치
- 설치 후 작업

*kickstart.cfg.j2*

> [!TIP] kickstart.cfg.j2 확장자 파일을 사용하는 이유
> Ansible을 통하여 Jinja2 문법으로 값을 동적으로 설정

```
# 언어 및 키보드 설정
lang ko_KR.UTF-8
keyboard --vckeymap=kr --xlayouts='kr'

# 네트워크 설정 (DHCP)
network --bootproto=dhcp --device=ens3 --onboot=on

# 시간대 설정
timezone Asia/Seoul --utc

# 사용자 계정 설정
rootpw --plaintext {{ vm_user }}
user --name={{ vm_user }} --password={{ vm_password }} --plaintext --gecos="{{ vm_user }}" --groups=wheel

# 설치 원천 (로컬 미디어)
# cdrom

# 설치 원천 설정 (네트워크 URL 사용)
url --url={{ vm_inst_base_repo }}

# 저장소 설정
repo --name="AppStream" --baseurl={{ vm_inst_app_repo }}
repo --name="BaseOS" --baseurl={{ vm_inst_base_repo }}

# 부트로더 설정
bootloader --location=mbr --boot-drive=vda

# 디스크 파티션 설정 (자동 설정)
zerombr                      # 모든 디스크 초기화
clearpart --all --initlabel  # 모든 기존 파티션 제거
autopart --type=lvm          # LVM으로 자동 파티션 구성

# 패키지 설치
%packages
@^minimal-environment        # 최소 설치 환경
chrony                       # 시간 동기화
vim                          # 텍스트 편집기
bash-completion              # 명령어 자동 완성
%end

# 설치 후 스크립트
%post
# 설치 완료 로그 작성
echo "Installation complete on $(date)" > /root/install.log

# NTP 설정
systemctl enable chronyd
systemctl start chronyd

# SELinux 활성화
setenforce 1

# 방화벽 설정
firewall-cmd --permanent --add-service=ssh
firewall-cmd --reload

umount /mnt/source

echo "Post-install tasks completed" >> /root/install.log
%end

```

*주의 사항 1*
아래 설정이 적용되지 않을시 인스톨 불가
`vm_inst_base_repo: https://download.rockylinux.org/pub/rocky/9/BaseOS/x86_64/os/`
`vm_inst_app_repo: https://download.rockylinux.org/pub/rocky/9/AppStream/x86_64/os/`
```
# 설치 원천 설정 (네트워크 URL 사용)
url --url={{ vm_inst_base_repo }}

# 저장소 설정
repo --name="AppStream" --baseurl={{ vm_inst_app_repo }}
repo --name="BaseOS" --baseurl={{ vm_inst_base_repo }}
```

*주의 사항 2*
아래 설정으로 자동 설정 구성 ( but, 목적에 맞게 파티션 구성도 할 수 있어야함 )
```
# 디스크 파티션 설정 (자동 설정)
zerombr                      # 모든 디스크 초기화
clearpart --all --initlabel  # 모든 기존 파티션 제거
autopart --type=lvm          # LVM으로 자동 파티션 구성
```

*주의 사항 3*
umount를 진행하지 않으면 계속해서 CDROM boot 가 되기에 설치 & 리붓 무한반복
```
umount /mnt/source
```