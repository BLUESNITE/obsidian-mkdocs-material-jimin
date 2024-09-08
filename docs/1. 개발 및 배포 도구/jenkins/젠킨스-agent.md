> [!NOTE] 젠킨스 에이전트
> 젠킨스 slave 추가 구성 (젠킨스 전용용어 agent)
>
> ![[Pasted image 20240703153741.png]]

> 도커로 키 생성 CLI

```Shell
docker exec -it jenkins ssh-keygen -t rsa
```

> 생성된 경로

```Shell
/root/.ssh/

(확인 내용 예시)
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDeaz5BH6FlRQnDrGYOr9N................FqNT0BXSVoV9QnPYAZRBflKqJ3P+pLKYeBzYn7hevHoMZUwZlxd0wIbqAFUCfZPM= root@a2b34500533e
```

> docker compose file

```Shell
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
```

> 출력문 : /opt/java/openjdk/bin/java

> [!NOTE] Jenkins에서 Slave Agent node 추가
>
> 노드 추가 (Slave-In Node)
>
> - Permanent Agent (선택)
>
> 다음 페이지
>
> - Remote root directory : /var/jenkins_home
> - Lables : slave
> - Launch method : Launch agents via SSH
> - Host : slave
> - Credentials : <여기서 잠깐. 인증값 작업이 필요하다. 하단에 추가>
> - Host Key Verification Strategy : Non verifying Verification Strategy
>
> ##### Save
>
> 잔여 작업으로 Java 경로를 지정해주어야 한다.
>
> - Node Properties에서 Tool Locations
>
> 근대 뭐가 없을 수 있다. 잠시 다른 메뉴로 넘어가야한다.
>
> - Jenkins 관리 -> Tools -> JDK install (JAVA_HOME 설정)
>
> 정상 추가 되었다면 다시. Configure에서 Tool Locations에 보면 JDK가 추가되어있다.  
>

> [!TIP] Jenkins master Credentials
>
> #### New credentials
>
> - Kind : SSH Username with pricate key
> - Id and Username : jenkins
> - Private Key : 직접입력 (시작 때 생성한 키)

#### [이제 마지막일까 (?)]

> [!NOTE] 설정 적용
> 내가 추가한 Agent Slave-In Node에 가서 Relaunch agent를 눌러보자.
>
> ![[Pasted image 20240703093959.png]]
> ![[Pasted image 20240703094100.png]]

> [!NOTE] 노드 실행의 로그
> 노드에도 실행 로그를 확인 할 수 있다. 잘 못 한게 있다면 여기서 오류를 확인하고 해결하자,

```shell
slave: Temporary failure in name resolution SSH Connection failed with IOException: "slave: Temporary failure in name resolution", retrying in 15 seconds. There are 5 more retries left.
```

너무 단순하게 따라만 했나보다. 로그를 참고하여 개선.
docker compose 파일의 host 개선과 인증키 세팅을 다시 한번씩.
컨테이너 재생성 때문에 아무래도 키값이 달라졌나보다.

> 이후 발생한 추가 오류

```shell
파일에 대한 액세스 문제
```

#### [최종 컴포즈 파일]

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

#### [수동연결]

_에이전트 컨테이너에서 수행하는 CLI 절차_

```
apt update -y
apt install curl

echo b576b9649a67ab3a5ef83671c74aee0f2f53342f289d6cf71fd2291535a74b6e > secret-file

curl -sO http://192.168.2.246:8081/jnlpJars/agent.jar

java -jar agent.jar -url http://192.168.2.246:8081/ -secret @secret-file -name "Slave-In Node 3" -workDir "/var/jenkins_home"
```

_Compose 파일로 작성_

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

_실행 sh스크립트_

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

---

- 참고 사이트
  [[docker] docker 환경에서 젠킨스(jenkins) master-slave 컨테이너 설정해서 ... (xmlangel.kr)](https://xmlangel.kr/posts/2022-09-04-docker-jenkins-salve)
