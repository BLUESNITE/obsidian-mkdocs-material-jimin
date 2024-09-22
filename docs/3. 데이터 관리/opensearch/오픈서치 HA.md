---
date: 2024-09-22
---

> [!INFO] 정리 
> 나름의 오픈서치 고가용성을 위한 설치 설정내용을 정리 작성

*Story*

오픈서치를 사용하기 시작한 초기부터 사용 용도나 의존도(?)가 높아지면서 더 효율적인 설정과 좋은 성능이 더더욱 필요로 해졌다.

하여 초기에는 `설치`에만 집중했다면 이제는 `다중 노드` 설치를 지나 `Role Base 노드` 설치로 높은 성능을 기대해보고자 한다.

찾아보고 알아본 기준은 대부분 Opensearch 홈페이지나 ChatGPT의 도움을 받았다. 작성해둔 내용이 부족하면... 하단에 링크들을 참고!

> [!CHECK] 기본설치 2 Node 구성
> [Opensearch 사이트 설치예시](https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/ "Opensearch 사이트 설치예시") 에서 Sample docker-compose.yml를 참고
> 
> 위 링크에서 정말 기본형의 좋은 예시를 제공하고 있다. (초기학습때 알았더라면...)

**environment (기본 옵션)**

- cluster.name=클러스터의 이름
- node.name=컨테이너에서 실행될 노드의 이름
- discovery.seed_hosts=클러스터를 탐색할때 찾을 노드들을 지정 (가능하면 모든 노드를 작성)
- cluster.initial_cluster_manager_nodes=클러스터 매니저 역할을 가진 노드를 지정
- node.roles=클러스터 룰 (클러스터매니저, 데이터, 수집, 비워두면 조정)
- bootstrap.memory_lock=JVM 힙메모리 스와핑을 비활성화
- OPENSEARCH_JAVA_OPTS=JVM 힙 크기의 최소 및 최대 값을 시스템 RAM의 최소 50%로 설정
- OPENSEARCH_INITIAL_ADMIN_PASSWORD=패스워드

> [!HINT] RAM, Memory 설정 힌트
> OPENSEARCH_JAVA_OPTS 설정과 Docker compose 작성시의 deploy.resources.limits.memory 설정은 매우 밀접한 관계이다.
> 
> 오픈서치에서 가이드 되고 있는 기준으로 살펴본다면, 구성시 최소 4G를 권장하고 있는데 이때의 JAVA_OPTS 설정은 `-Xms4g -Xmx4g`가 적절한 값이 된다. 이를 참고하여 노드 메모리 구성값을 계산하자.

#### Docker compose 작성공유

*요약*
```Shell
아래의 구성은 `node.roles`의 역할을 분산하여 작성한 내용이다.
기본적으로 4노드 구성이되며 단일역할은 `클러스터매니저1`, `조정1` 두개이고 
전체역할 `노드2`로 구성해두었다. 고가용성을 위해서 클러스터매니저 Role을 
기본 3개를 권장하는 내용을 보았는데 ... 
(자료의 위치를 까먹었다) 

아무튼 해당내용에 추가적인 노드가 필요하다면 
`Data`만 수행하는 노드를 추가하면 기대성능이 올라갈 것으로 추측된다.
```

*opensearch-compose.yml*
```Shell
# opensearch.yml
# index.number_of_replicas: 1 # 로운 인덱스가 생성될 때 기본적으로 복제본 수가 1로 설정하면 데이터의 가용성이 향상

# 공통 환경 변수 설정 (YAML 앵커 사용)
x-opensearch-environment: &opensearch-environment
  cluster.name: opensearch-cluster
  bootstrap.memory_lock: "true"
  OPENSEARCH_JAVA_OPTS: "-Xms4g -Xmx4g"
  OPENSEARCH_INITIAL_ADMIN_PASSWORD: "X2commerce!1"

services:
  opensearch-m1:
    image: opensearchproject/opensearch:2.17.0
    container_name: opensearch-m1
    environment:
      <<: *opensearch-environment
      node.name: opensearch-m1
      node.roles: '[cluster_manager]'
      discovery.seed_hosts: opensearch-m1,opensearch-d1,opensearch-d2
      cluster.initial_cluster_manager_nodes: opensearch-m1,opensearch-d1,opensearch-d2
    deploy:
      resources:
        limits:
          memory: 8g
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    volumes:
      - opensearch-data-m1:/usr/share/opensearch/data
      - ./conf/opensearch-plugins-install.sh:/usr/share/opensearch/opensearch-plugins-install.sh
    ports:
      - 9200:9200
      - 9600:9600
    networks:
      - opensearch-net
    entrypoint:
      - /bin/sh
      - -c
      - |
        /usr/share/opensearch/opensearch-plugins-install.sh
        /usr/share/opensearch/opensearch-docker-entrypoint.sh

  opensearch-d1:
    image: opensearchproject/opensearch:2.17.0
    container_name: opensearch-d1
    environment:
      <<: *opensearch-environment
      node.name: opensearch-d1
        #node.roles: '[cluster_manager,data]'
      discovery.seed_hosts: opensearch-m1,opensearch-d1,opensearch-d2
      cluster.initial_cluster_manager_nodes: opensearch-m1,opensearch-d1,opensearch-d2
    deploy:
      resources:
        limits:
          memory: 8g
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    volumes:
      - opensearch-data1:/usr/share/opensearch/data
      - ./conf/opensearch-plugins-install.sh:/usr/share/opensearch/opensearch-plugins-install.sh
    networks:
      - opensearch-net
    entrypoint:
      - /bin/sh
      - -c
      - |
        /usr/share/opensearch/opensearch-plugins-install.sh
        /usr/share/opensearch/opensearch-docker-entrypoint.sh

  opensearch-d2:
    image: opensearchproject/opensearch:2.17.0
    container_name: opensearch-d2
    environment:
      <<: *opensearch-environment
      node.name: opensearch-d2
        #node.roles: '[cluster_manager,data]'
      discovery.seed_hosts: opensearch-m1,opensearch-d1,opensearch-d2
      cluster.initial_cluster_manager_nodes: opensearch-m1,opensearch-d1,opensearch-d2
    deploy:
      resources:
        limits:
          memory: 8g
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    volumes:
      - opensearch-data2:/usr/share/opensearch/data
      - ./conf/opensearch-plugins-install.sh:/usr/share/opensearch/opensearch-plugins-install.sh
    networks:
      - opensearch-net
    entrypoint:
      - /bin/sh
      - -c
      - |
        /usr/share/opensearch/opensearch-plugins-install.sh
        /usr/share/opensearch/opensearch-docker-entrypoint.sh

  opensearch-c1:
    image: opensearchproject/opensearch:2.17.0
    container_name: opensearch-c1
    environment:
      <<: *opensearch-environment
      node.name: opensearch-c1
      node.roles: '[]'
      discovery.seed_hosts: opensearch-m1,opensearch-d1,opensearch-d2
      cluster.initial_cluster_manager_nodes: opensearch-m1,opensearch-d1,opensearch-d2
    deploy:
      resources:
        limits:
          memory: 8g
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    volumes:
      - opensearch-data-c1:/usr/share/opensearch/data
      - ./conf/opensearch-plugins-install.sh:/usr/share/opensearch/opensearch-plugins-install.sh
    networks:
      - opensearch-net
    entrypoint:
      - /bin/sh
      - -c
      - |
        /usr/share/opensearch/opensearch-plugins-install.sh
        /usr/share/opensearch/opensearch-docker-entrypoint.sh

  opensearch-dashboards:
    image: opensearchproject/opensearch-dashboards:latest
    container_name: opensearch-dashboards
    ports:
      - 5601:5601
    expose:
      - "5601"
    environment:
      OPENSEARCH_HOSTS: '["https://opensearch-c1:9200"]'
    networks:
      - opensearch-net

# 볼륨 설정
volumes:
  opensearch-data1:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/opensearch-dir/data-d1
  opensearch-data2:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/opensearch-dir/data-d2
  opensearch-data-c1:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/opensearch-dir/data-c1
  opensearch-data-m1:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/opensearch-dir/data-m1

# 네트워크 설정
networks:
  opensearch-net:
```





