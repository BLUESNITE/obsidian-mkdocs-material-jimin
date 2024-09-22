**현재 아이피 확인**
```shell
ip addr show
```

**라우트 확인**
```shell
ip route
```

**netplan 파일 찾기**
```shell
ls /etc/netplan/
```

**고정 IP 작성하기**
```shell
network:
  version: 2
  ethernets:
    enp0s3:
      dhcp4: no
      addresses:
        - 192.168.2.148/24  # 고정 IP 주소
      gateway4: 192.168.2.235  # 게이트웨이 주소
      nameservers:
        addresses:
          - 8.8.8.8  # 구글 DNS 서버
          - 8.8.4.4
```

**설정 적용**
```shell
sudo netplan apply
```