*파일 및 폴더 4개 준비하기*

```
compose.yaml
Dockerfile
nvidia.conf
nvidia-gpu (DIR)
```

*1) nvidia-gpu* > git clone https://git.zabbix.com/scm/ap/nvidia-gpu.git

*2) nvidia.conf* > 
```
### Option:Plugins.NVIDIA.System.Path
#	Path to loadable plugin executable.
#
# Mandatory: yes
# Default:
# Plugins.NVIDIA.System.Path=

### Option: Plugins.NVIDIA.Timeout
#	Amount of time to wait for a server to respond when first connecting and on
#   follow up operations in the session.
#   Global item-type timeout (or individual item timeout) will override this value if it is greater.
#
# Mandatory: no
# Range: 1-30
# Default:
# Plugins.NVIDIA.Timeout=<Global timeout>
Plugins.NVIDIA.System.Path=/usr/sbin/zabbix-agent2-plugin/nvidia-gpu
Plugins.NVIDIA.Timeout=15
```

*3) compose.yaml*
```
version: "3.8"
services:
  zabbix-agent-nvidia:
    build:
      context: /home/tech/data/zabbix
    container_name: zabbix-agent-nvidia
    environment:
      - ZBX_HOSTNAME=192.168.2.242
      - ZBX_SERVER_HOST=192.168.2.249
    init: true
    runtime: nvidia
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    volumes:
      - ./nvidia-gpu:/nvidia-gpu
      - ./nvidia.conf:/etc/zabbix/zabbix_agent2.d/plugins.d/nvidia.conf
      - /usr/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:ro
networks: {}
```

*4) Dockerfile*
```
# ./Dockerfile
FROM zabbix/zabbix-agent2:7.2-ubuntu-latest

USER root

RUN apt-get update && apt-get install -y wget bash build-essential golang-go

RUN mkdir -p /usr/sbin/zabbix-agent2-plugin
COPY ./nvidia-gpu /nvidia-gpu

WORKDIR /nvidia-gpu
RUN CGO_ENABLED=1 go build -o nvidia-plugin .

COPY ./nvidia.conf /etc/zabbix/zabbix_agent2.d/plugins.d/nvidia.conf

RUN mkdir -p /usr/lib/zabbix/agent2/plugins \
    && cp ./nvidia-plugin /usr/lib/zabbix/agent2/plugins/zabbix_agent2_plugin_nvidia \
    && chmod +x /usr/lib/zabbix/agent2/plugins/zabbix_agent2_plugin_nvidia

USER zabbix
```

*컨테이너에서 확인*
```
zabbix_agent2 -t nvml.system.driver.version
```

**기타 오류**

*Error response from daemon: unknown or invalid runtime name: nvidia*

![[Pasted image 20250403094925.png]]

![[Pasted image 20250403094937.png]]

아래처럼 적용하기 위해서 데몬 수정

```
sudo mkdir -p /etc/docker
sudo nano /etc/docker/daemon.json

{
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  }
  ,"default-runtime": "nvidia"
}
```

sudo systemctl restart docker

*확인*

```
docker info | grep -i runtime
```



