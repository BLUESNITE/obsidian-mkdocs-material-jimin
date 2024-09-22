> [!NOTE] 젠킨스 에이전트
> 젠킨스 slave 추가 구성 (젠킨스에서의 용어는 agent)

![[Pasted image 20240703153741.png]]

**도커로 키 생성 CLI**
``` Shell
docker exec -it jenkins ssh-keygen -t rsa
```

**생성 경로**
``` Shell
/root/.ssh/

(확인 내용 예시)
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDeaz5BH6FlRQnDrGYOr9N................FqNT0BXSVoV9QnPYAZRBflKqJ3P+pLKYeBzYn7hevHoMZUwZlxd0wIbqAFUCfZPM= root@a2b34500533e
```

**docker compose file**
``` Shell
services:
  node:
    container_name: jenkins-slave01
    image: jenkins/ssh-agent
    restart: unless-stopped
    environment:
      - JENKINS_AGENT_SSH_PUBKEY=ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDeaz5BH6FlRQnDrGYOr9Np7MP3heDQS/TIi605y8RzcsVkt1LVxhIvMjzMrrvwmDGTiTMhSAgp6.......................................Pz5KtTx4DchlyoZDr9TU056NeS2R446fLhYikc/07sG79yJoPD+1qiGEfx9q0FhQL6QT6UpQgi/rfWQylwzBgLBcalN8hK8pdN1It7VRFnFLIHq3ELxLz0mMU6RHEsYFqNT0BXSVoV9QnPYAZRBflKqJ3P+pLKYeBzYn7hevHoMZUwZlxd0wIbqAFUCfZPM= root@a2b34500533e
    volumes:
      - "/data/jenkins/jenkins_slave_home:/var/jenkins_home"
```

> [!CHECK] 설치확인 절차

```Shell
docker exec -it <컨테이너명> which java

출력문 : /opt/java/openjdk/bin/java
```

> [!NOTE] Jenkins에서 Slave Agent node 추가

*노드 추가 (Slave-In Node)*

- Permanent Agent (선택)

*다음 페이지*

- Remote root directory : /var/jenkins_home
- Lables : slave
- Launch method : Launch agents via SSH
- Host : slave
- Credentials : <여기서 잠깐. 인증값 작업이 필요하다. 하단에 추가>
- Host Key Verification Strategy : Non verifying Verification Strategy

*잔여 작업으로 Java 경로를 지정해주어야 한다.*

- Node Properties에서 Tool Locations

근대 뭐가 없을 수 있다. 잠시 다른 메뉴로 넘어가야한다.

- Jenkins 관리 -> Tools -> JDK install (JAVA_HOME 설정)

정상 추가 되었다면 다시. Configure에서 Tool Locations에 보면 JDK가 추가되어있다.  

> [!TIP] Jenkins master Credentials

New credentials

- Kind : SSH Username with pricate key
- Id and Username : jenkins
- Private Key : 직접입력 (시작 때 생성한 키)

> [!NOTE] 설정 적용
> 내가 추가한 Agent Slave-In Node에 가서 Relaunch agent를 눌러보자.

![[Pasted image 20240703093959.png]]

![[Pasted image 20240703094100.png]]

> [!NOTE] 노드 실행의 로그
> 노드에도 실행 로그를 확인 할 수 있다. 잘 못 한게 있다면 여기서 오류를 확인하고 해결하자,

```shell
slave: Temporary failure in name resolution SSH Connection failed with IOException: 
"slave: Temporary failure in name resolution", retrying in 15 seconds. 
There are 5 more retries left.
```

너무 단순하게 따라만 했나보다. 로그를 참고하여 개선.
docker compose 파일의 host 개선과 인증키 세팅을 다시 한번씩.
컨테이너 재생성 때문에 아무래도 키값이 달라졌나보다.

> 이후 발생한 추가 오류

```shell
파일에 대한 액세스 문제
```

#### 최종 컴포즈 파일
```shell
services:
  jenkins:
    image: jenkins/jenkins:jdk17
    depends_on:
      - node
    restart: always
    user: root
    container_name: jenkins
    environment:
      - TZ=Asia/Seoul
    volumes:
      - "/data/jenkins/jenkins_home:/var/jenkins_home"
      - "/usr/local/bin/helm:/usr/local/bin/helm"
      - "/usr/bin/argocd:/usr/bin/argocd"
      - "/usr/bin/docker:/usr/bin/docker"
      - "/var/run/docker.sock:/var/run/docker.sock"
    ports:
      - "8081:8080"
      - "50000:50000"
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: '4g'
        reservations:
          cpus: '1.0'
          memory: '2g'
  node:
    container_name: jenkins-slave01
    image: jenkins/ssh-agent:latest-jdk17
    restart: unless-stopped
    user: root
    environment:
    - JENKINS_AGENT_SSH_PUBKEY=ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC5g/BF8AR9sOlv5VurbMduq1WDSmwwaaDGF34HQeb7gBVjqKU+CEARsTFWXp6+f+G2dU3q46YCN0yKk5WFBIJHQDyCE76mhAAljLNKBAKy4tj8njBJWek12SMT5UIWt48jSEpiOzUG3tuO6fsX.............................qa3nDzOmgeaEUL3MDfT1ZVpsSaVQVw3I8UGOx/hCIGyVeVgqLhLc1G+Y0sBoiq4dyT/KeBvfY8xcLub8Jg/u/Lj/04M5ntQOm1mhYmvHk01F3AMabISyrutO9QsXA+Q27rqMWXSl9LZVEEsYojNwuvGZbKFuy1yWlYrfQbBTtiCDS1eIGLupjQInbXn//ywBMjBQON0= root@b2871f60ac57
    volumes:
      - "/data/jenkins/jenkins_slave_home:/var/jenkins_home"
    entrypoint: >
      sh -c "
      chown -R jenkins:jenkins /var/jenkins_home &&
      chmod -R 755 /var/jenkins_home &&
      setup-sshd"
```
___

> [!TIP] 재작업 history
> 지난번 작업했던 내용중 아쉬운 부분이 있어 다시 추가 작업을 진행하였다.
> 
> 1. 다른 host 에서의 agent 연결을 원함
> 2. docker agent 컨테이너를 이용하여 해결하려고 여러 방면 작업을 해보았으나 ...
>    결론적으로 docker, argocd, git을 설치하고 수행시키는데 어려움을 겪음
> 3. (최종작업) VM ubuntu 서버를 별도로 띄워서 진행
>    
> 하여 아래는 VM ubuntu 서버 설치 이후 부터 모든 패키지를 설치하고 agent 세팅하는데까지 자동화를 목표로 작성해보았음.   

#### Rock

> VM 설정 정보

```
ubuntu24.04-Jenkins-agent
vCPU 4
Memory 12288 / 24576
Disk 50G
```

> VM에서의 작업

```
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install openssh-server curl vim -y
reboot
```

> SSH로 작업

```
sudo adduser jenkins #(비번입력,  올 엔터)
cd /home/jenkins
echo <(직접입력) Key 2f53342f289d6cf71fd2291535a74b6e> > secret-file
curl -sO http://192.168.2.246:8081/jnlpJars/agent.jar
cd /root/.ssh
(파일생성) id_rsa  id_rsa.pub
```

> JAVA와 MAVEN ( agent )( rockey linux )

```
sudo dnf install java-17-openjdk-devel
java -version
wget https://archive.apache.org/dist/maven/maven-3/3.5.4/binaries/apache-maven-3.5.4-bin.tar.gz
tar -xvzf apache-maven-3.5.4-bin.tar.gz
sudo mv apache-maven-3.5.4 /opt/maven
export M2_HOME=/opt/maven
export MAVEN_HOME=/opt/maven
export PATH=${M2_HOME}/bin:${PATH}
source ~/.bashrc
```

> JAVA 버전 변경

```
sudo alternatives --config java
```

> Jenkins 사용자에 Docker 그룹 권한 부여

```
sudo usermod -aG docker jenkins
```

> Docker 데몬 소켓 권한 수정

```
sudo chmod 666 /var/run/docker.sock
```
___
#### 수동연결
*에이전트 컨테이너에서 수행하는 CLI 절차*
```
apt update -y
apt install curl

cd /home/jenkins

echo b576b9649a67ab3a5ef83671c74aee0f2f53342f289d6cf71fd2291535a74b6e > secret-file

curl -sO http://192.168.2.246:8081/jnlpJars/agent.jar

apt install openjdk-17-jre-headless -y

(테스트)
java -jar agent.jar -url http://192.168.2.246:8081/ -secret @secret-file -name "Slave-In Node 3" -workDir "/var/jenkins_home"

sudo chown -R jenkins:jenkins /var/jenkins_home
sudo chmod -R 755 /var/jenkins_home

(서비스 등록진행)
sudo nano /etc/systemd/system/jenkins-agent.service

[Unit]
Description=Jenkins Agent Service
After=network.target

[Service]
User=jenkins
WorkingDirectory=/var/jenkins_home
ExecStart=/usr/bin/java -jar /home/jenkins/agent.jar -url http://192.168.2.246:8081/ -secret 0c74040a361cfe227d0ee8fd39cd1c7ab43b1f144a96017a70fa2cfe2f881f83 -name "VM Slave-In Node 1-159" -workDir "/var/jenkins_home"
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

*Compose 파일로 작성*
```
services:
  node:
    container_name: jenkins-slave04
    image: jenkins/ssh-agent:latest-jdk17
    restart: unless-stopped
    user: root
    ports:
      - "50000:50000"
      - "8822:22"
    environment:
      - ENV_SECRET_FILE=bdbbc7e2954a36a916fa68ae3728ee28b129da15b20691c0623c421859ba61af
      - ENV_SLAVE_NAME=Slave-In Node 4
      - ENV_HOST_SEVER=192.168.2.246:8081
      - JENKINS_AGENT_SSH_PUBKEY=ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDGZU1maHQXSR5jmbDLNdY/fze6Ebw3SBt2u8+T5r8vxPpYXiHwphulhYCf7nUOAH8bVK0aUq0JWwqE5LoPrrSOe4K+etbJjhe+0dWZyyQW51s/aRplMCpNDMDsEF+pQm3jLDRKSMHE2JPvQXxyUG7xCjYda9N7jTrDamlGvvPXuv/XI9y58XnCBtLpnypJWuSNdBrOXt23eNoJKRse8dPmcOYa44QSxeGO+7dPpzE4hjtx6TwWPwr2IO4DQWG/0Ex6S8OpBpMPvWPzDfcv5Jihez2R0Ql+qGfS8vAFU8VbtJATVobI0/iAUE6AStI3ay5gwpUeeba7lu0LKor9Q1KbNGnDlBrEkfxQVkwZGXiqV8uVdmpgSC4RvaD3LWPCI9mOOtz17t4LZvyH/2NVMGBEOU7szNuAx917qpfGMQ2I2+aqzL1YWU2cmZh75NL2OR9S0NYfzqLO/g/J1K6FAeGDR5ipEJS+GALqI78C58NV8a8SOzEMzv97LHr+SvjuGLU= root@8bfb4b4cb0b1
    volumes:
      - "./jenkins/node.sh:/node.sh"
      - "/data/jenkins/jenkins_slave_home:/var/jenkins_home"
    entrypoint: >
      sh -c "
      chown -R jenkins:jenkins /var/jenkins_home &&
      chmod -R 755 /var/jenkins_home &&
      sh /node.sh &&
      setup-sshd &&
      echo 'Running node.sh'"
```

*실행 sh스크립트*
```
#!/bin/sh

echo "Starting node.sh script"

echo "ENV_SECRET_FILE: ${ENV_SECRET_FILE}"
echo "ENV_SLAVE_NAME: ${ENV_SLAVE_NAME}"
echo "ENV_HOST_SEVER: ${ENV_HOST_SEVER}"

# curl 설치 여부 확인 및 설치
if ! command -v curl &> /dev/null; then
  apt-get update -y && apt-get install curl -y
fi

# secret 파일 생성
echo ${ENV_SECRET_FILE} > /var/jenkins_home/secret-file

# agent.jar 다운로드
curl -sO http://${ENV_HOST_SEVER}/jnlpJars/agent.jar
chown -R /home/jenkins/agent.jar
chmod -R 755 /home/jenkins/agent.jar

sudo chown -R jenkins:jenkins /var/jenkins_home
sudo chmod -R 755 /var/jenkins_home

echo "down end agent"

# Jenkins 홈 디렉토리 권한 설정
chown -R jenkins:jenkins /var/jenkins_home
chmod -R 755 /var/jenkins_home

# Jenkins 에이전트 실행
# ENV_SLAVE_NAME
java -jar /home/jenkins/agent.jar -url http://${ENV_HOST_SEVER}/ -secret @/var/jenkins_home/secret-file -name "${ENV_SLAVE_NAME}" -workDir /var/jenkins_home

# SSH 데몬 설정
echo "Finished node.sh script"
```

> free swap

```
sudo swapoff -a 

sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
```

> 에이전트 분할

```
에이전트 1
next pub
next
nest

에이전트 2
(남는거)
common-api
display-api
event-api
goods-api
member-api
order-api

에이전트 3
bo
bo-api
batch-gddp
batch-mbod
```

```
docker exec -it jenkins-slave01 sh /install.sh
docker exec -it jenkins-slave01 sh /login.sh
```

> 위와 같이 작업을 하였더니 argocd와 docker 명령어에서 말썽을 일으켰다 하여 수정.

```Shell
services:
  node:
    container_name: jenkins-slave01
    image: jenkins/ssh-agent:latest-jdk17
    restart: unless-stopped
    user: root
    ports:
      - "50000:50000"
      - "8822:22"
    environment:
      - ENV_SECRET_FILE=0a278a088584e3dc1c3eefd952bde7e91d5f25b641191955e059d8a1ab2aea68
      - ENV_SLAVE_NAME=Slave-In Node 1
      - ENV_HOST_SEVER=192.168.2.246:8081
      - JENKINS_AGENT_SSH_PUBKEY=ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDGZU1maHQXSR5jmbDLNdY/fze6Ebw3SBt2u8+T5r8vxPpYXiHwphulhYCf7nUOAH8bVK0aUq0JWwqE5LoPrrSOe4K+etbJjhe+0dWZyyQW51s/aRplMCpNDMDsEF+pQm3jLDRKSMHE2JPvQXxyUG7xCjYda9N7jTrDamlGvvPXuv/XI9y58XnCBtLpnypJWuSNdBrOXt23eNoJKRse8dPmcOYa44QSxeGO+7dPpzE4hjtx6TwWPwr2IO4DQWG/0Ex6S8OpBpMPvWPzDfcv5Jihez2R0Ql+qGfS8vAFU8VbtJATVobI0/iAUE6AStI3ay5gwpUeeba7lu0LKor9Q1KbNGnDlBrEkfxQVkwZGXiqV8uVdmpgSC4RvaD3LWPCI9mOOtz17t4LZvyH/2NVMGBEOU7szNuAx917qpfGMQ2I2+aqzL1YWU2cmZh75NL2OR9S0NYfzqLO/g/J1K6FAeGDR5ipEJS+GALqI78C58NV8a8SOzEMzv97LHr+SvjuGLU= root@8bfb4b4cb0b1
    volumes:
      - "./jenkins/node.sh:/node.sh"
      - "./jenkins/install.sh:/install.sh"
      - "./jenkins/login.sh:/login.sh"
      - "/data/jenkins/jenkins_slave_home:/var/jenkins_home"
    entrypoint: >
      sh -c "
      chown -R jenkins:jenkins /var/jenkins_home &&
      chmod -R 755 /var/jenkins_home &&
      sh /node.sh &&
      setup-sshd &&
      echo 'Running node.sh'"
```

> 스크립트 파일 세개 

*node.sh*
```shell
#!/bin/sh

echo "Starting node.sh script"

echo "ENV_SECRET_FILE: ${ENV_SECRET_FILE}"
echo "ENV_SLAVE_NAME: ${ENV_SLAVE_NAME}"
echo "ENV_HOST_SEVER: ${ENV_HOST_SEVER}"

# curl 설치 여부 확인 및 설치
if ! command -v curl &> /dev/null; then
  apt-get update -y && apt-get install curl -y
fi

# secret 파일 생성
echo ${ENV_SECRET_FILE} > /var/jenkins_home/secret-file

# agent.jar 다운로드
curl -sO http://${ENV_HOST_SEVER}/jnlpJars/agent.jar
chown -R /home/jenkins/agent.jar
chmod -R 755 /home/jenkins/agent.jar

echo "down end agent"

# Jenkins 홈 디렉토리 권한 설정
chown -R jenkins:jenkins /var/jenkins_home
chmod -R 755 /var/jenkins_home

# Jenkins 에이전트 실행
# ENV_SLAVE_NAME
java -jar /home/jenkins/agent.jar -url http://${ENV_HOST_SEVER}/ -secret @/var/jenkins_home/secret-file -name "${ENV_SLAVE_NAME}" -workDir /var/jenkins_home

# SSH 데몬 설정
echo "Finished node.sh script"

```

*install.sh*
```
echo "argocd 1"
cd /usr/local/bin/
curl -LO https://github.com/argoproj/argo-cd/releases/download/v2.11.2/argocd-linux-amd64
mv argocd-linux-amd64 argocd
chmod 755 /usr/local/bin/argocd
argocd version
echo "argocd end"

echo "docker 1"
apt-get update
apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
echo "docker 2"
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io
echo "docker 3"
docker --version
echo "docker end"
```

*login.sh*
```
argocd login 192.168.1.254:10031 --grpc-web --insecure

docker login docker-dev.x2bee.com
```

___ 
- 참고 사이트
[[docker] docker 환경에서 젠킨스(jenkins) master-slave 컨테이너 설정해서 ... (xmlangel.kr)](https://xmlangel.kr/posts/2022-09-04-docker-jenkins-salve)

