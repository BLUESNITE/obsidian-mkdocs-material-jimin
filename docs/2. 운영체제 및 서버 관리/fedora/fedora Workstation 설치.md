> [!NOTE] Linux Workstation에 사실 관심이 없지만 해본다 설치
> sudo dnf update -y
   sudo dnf upgrade -y

**Install to Hard Drive** / 이 사실 부분이 선행되어야 한다.
![[Pasted image 20241011131836.png]]

**오류**
해당 폴더 파일 제거 sudo rm -f /var/run/anaconda.pid

![[Pasted image 20241011132040.png]]

**GUI 진행**
이후 진행은 간단하여 생략
![[Pasted image 20241011132215.png]]

> [!CHECK] OPENSSL SEVER 설치
> sudo dnf install openssl
> sudo dnf install openssh-server

```
# SSH 서비스 시작
sudo systemctl start sshd

# 부팅 시 자동 시작 설정
sudo systemctl enable sshd
```

**패스워드 설정**
```
sudo passwd liveuser
```

**사용자 생성 및 권한부여**
```
sudo useradd -m -G $(id -Gn liveuser | tr ' ' ',') tech
sudo passwd tech
sudo usermod -aG wheel tech
```

**네트워크 설정 저장**
```
sudo nmcli connection modify "Wired connection 1" connection.autoconnect yes
sudo chmod 600 filename
sudo systemctl restart NetworkManager
```

```
[ipv4]
address1=192.168.2.174/24,192.168.2.235
dns=8.8.8.8;168.126.63.1;
method=manual
```

**xrdp 설치**
```
sudo dnf install xrdp -y
```

```
# xrdp 서비스 시작 
sudo systemctl start xrdp 

# 부팅 시 자동으로 xrdp가 시작되도록 설정 
sudo systemctl enable xrdp
```

**방화벽 해제**
```
sudo systemctl stop firewalld
sudo systemctl disable firewalld
```

