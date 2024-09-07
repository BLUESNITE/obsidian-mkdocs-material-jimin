> [!ㄷㄷㄷ] docker compose file
> 아래는 도커 컴포즈 파일이며, 
> 
> web은 8081이 중복되어 8082로 변경 설정
> docker-hosted는 5000번
> (8085는 모름 … )
```
services:
  nexus3:
    image: sonatype/nexus3
    container_name: nexus3
    volumes:
      - "/data/nexus:/sonatype-work"
    ports:
      - "8082:8081"
      - "8085:8085"
      - "5000:5000"
```

> 패스워드 확인
```
user admin
pwd admin.password (file)
```

> 설치 후 설정
```
Server Administration and Repository에 들어가서
> Blob Stores 진입
```

> Create Blob Store
```
1)
Type File
Name docker-hosted

2)
Type File
Name docker-hub
```

> Create repository
```
1) docker (hosted)
Name docker-hosted
HTTP (체크) 5000
Enable Docker V1 API (체크)
Blob store (선택) docker-hosted (생성해둔것-Blob Store)

2) docker (proxy)
Name docker-hub
Enable Docker V1 API (체크)
Remote storage (? URL...)(ex http://registry.x2commerce.com)
Docker Index Use Docker-Hub
Blob store (선택) docker-hub (생성해둔것-Blob Store)
```

> Realms
```
docker bearer Token Realm (추가)
```

> docker login
```
docker login <nexus-registry-ip>:5000
(아마 안될거다 아래에 조치사항)
```

> http 가능케하기 ★★★
```
vi /etc/docker/daemon.json

{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "features": {
    "buildkit": true
  },
  "insecure-registries": [
    "<nexus-registry-ip>:5000"
  ]
}

sudo systemctl restart docker
```

> [!ㄷㄷㄷ] 임의 테스트 진행
> docker login을 진행한 후 ...
> docker images를 통해서 가진 이미지 확인 > 확인 된 이미지를 Nexus nexus-repo-ip에 맞춘다
> docker image tag <가진 이미지> <넥서스 레포 아이피>:<포트>/path
> docker push <넥서스 레포 아이피>:<포트>/path

> 태그명 맞추기
```
docker image tag docker.x2bee.com/onpremise/lotte-x2bee-api-common_stg:latest 192.168.2.246:5000/onpremise/lotte-x2bee-api-common_stg:1.0
```

> 이미지 넥서스에 올리기
```
docker push 192.168.2.246:5000/onpremise/lotte-x2bee-api-common_stg:1.0
```
___
## 테스트 완료
___
