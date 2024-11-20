기본적으로 도커는 `/var/lib/docker` 디렉터리를 루트 디렉토리로 사용하지만 디스크 공간 문제를 해결하기 위해서 아래와 같은 작업을 해야 할 수 있습니다.

도커 기본경로 확인 CLI *docker info*
```
[root@localhost tech]# docker info
Client: Docker Engine - Community
 Version:    27.3.1
 Context:    default
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.17.1
    Path:     /usr/libexec/docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v2.29.7
    Path:     /usr/libexec/docker/cli-plugins/docker-compose

Server:
 Containers: 3
  Running: 1
  Paused: 0
  Stopped: 2
 Images: 2
 Server Version: 27.3.1
 Storage Driver: overlay2
  Backing Filesystem: xfs
  Supports d_type: true
  Using metacopy: false
  Native Overlay Diff: true
  userxattr: false
 Logging Driver: json-file
 Cgroup Driver: systemd
 Cgroup Version: 2
...
...
 CPUs: 4
 Total Memory: 5.525GiB
 Name: localhost.localdomain
 ID: bd269f32-f90f-4cf3-bfc7-38f3fb807862
 Docker Root Dir: /var/lib/docker
```

위와 같이 정보가 출력되고 끝자락에서 `Docker Root Dir` 경로를 확인 할 수 있습니다.
아래는 이 경로를 수정해주어서 궁극적으로 `overlay`의 경로까지 변경되는 것을 확인합니다.

**docker 서비스를 중지**
```
sudo systemctl stop docker
```

*마운트할 폴더 생성 및 권한 부여*
```
예시경로 /home/tech/data/docker-mnt

sudo mkdir -p /home/tech/data/docker-mnt
sudo chown -R root:docker /home/tech/data/docker-mnt
sudo chmod -R 700 /home/tech/data/docker-mnt
```

*기존 데이터 이관* (필요시)
```
sudo rsync -a /var/lib/docker/ /home/tech/data/docker-mnt
```

**Docker 데몬 설정 변경**
```
sudo systemctl cat docker

없으면 생성

sudo nano /etc/docker/daemon.json
```

*생성 내용*
```
{
  "data-root": "/home/tech/data/docker-mnt"
}
```

위 방법대로 하면 아래와 같이 경로가 바뀐것을 확인 할 수 있습니다

![[Pasted image 20241120112711.png]]

