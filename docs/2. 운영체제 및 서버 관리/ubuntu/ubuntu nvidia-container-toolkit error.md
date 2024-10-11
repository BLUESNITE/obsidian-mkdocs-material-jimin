> [!DANGER] Error Case

```shell
docker compose -f postgresql-compose.yaml up -d --build

[+] Running 1/2
 ⠙ Container postgresql-master  Starting                                                                                                              0.2s
 ✔ Container postgresq-slave   Created                                                                                                               0.0s

Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: unable to retrieve OCI runtime error (open /run/containerd/io.containerd.runtime.v2.task/moby/931d766bc477e1572e50d994bb59d63290de8c4fa0e1e07bca8a8c42557b16fa/log.json: no such file or directory): exec: "nvidia-container-runtime": executable file not found in $PATH: unknown
```

> [!CHECK] Re Install nvidia-container-runtime

```shell
user> sudo dpkg -l | grep nvidia-container-runtime
user> sudo apt-get update

....
...
Reading package lists... Done
W: https://download.docker.com/linux/ubuntu/dists/noble/InRelease: Key is stored in legacy trusted.gpg keyring (/etc/apt/trusted.gpg), see the DEPRECATION section in apt-key(8) for details.
W: https://nvidia.github.io/nvidia-docker/ubuntu22.04/amd64/InRelease: Key is stored in legacy trusted.gpg keyring (/etc/apt/trusted.gpg), see the DEPRECATION section in apt-key(8) for details.
W: https://nvidia.github.io/nvidia-container-runtime/ubuntu22.04/amd64/InRelease: Key is stored in legacy trusted.gpg keyring (/etc/apt/trusted.gpg), see the DEPRECATION section in apt-key(8) for details.
root@user:/data/docker/postgresql-for-codeassistant# sudo apt-get install nvidia-container-runtime
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 nvidia-container-toolkit : Depends: libnvidia-container-tools (>= 1.4.0) but it is not installable
                            Depends: libnvidia-container-tools (< 2.0.0) but it is not installable
E: Unable to correct problems, you have held broken packages.

```

#### 문제해결과정

**문제 분석**
`nvidia-container-toolkit` 설치 시 의존성 문제 발생.
NVIDIA 리포지토리 적용 후 설치

```shell
# 필요시 sudo rm /etc/apt/sources.list.d/nvidia-container-toolkit.list

distribution=ubuntu22.04
curl -s -L https://nvidia.github.io/libnvidia-container/stable/$distribution/libnvidia-container.list | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update

sudo apt-get install nvidia-container-runtime
```

