> [!INFO] 사전 설치

```shell
sudo dnf update -y
sudo dnf install net-tools -y
```

> [!NOTE] 편의 세팅에 필요한 설치진행

```shell
sudo dnf update -y
sudo dnf upgrade -y
sudo dnf install vim -y
sudo dnf install net-tools -y
sudo yum install yum-utils -y

sudo systemctl stop firewalld
sudo systemctl disable firewalld
sudo systemctl status firewalld

dnf group list --installed -y
dnf group list --available -y

sudo dnf group install "Workstation" -y
sudo dnf group install "Server with GUI" -y
sudo systemctl set-default graphical
sudo reboot
```

> [!TIP] 네트워크 설정
> 수정 할 부분은 [ipv4] 이하 항목들

```shell
/etc/NetworkManager/system-connections$ cat enp1s0.nmconnection

cd /etc/NetworkManager/system-connections

[ipv4]
address1=192.168.2.172/24,192.168.2.235
dns=8.8.8.8;168.126.63.1;
method=manual

sudo systemctl restart NetworkManager
```

> [!NOTE] 도커 설치

```shell
sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo

sudo dnf update -y
sudo dnf upgrade -y

sudo dnf install docker-ce docker-ce-cli containerd.io -y
sudo systemctl start docker
sudo systemctl enable docker

sudo docker version
```
