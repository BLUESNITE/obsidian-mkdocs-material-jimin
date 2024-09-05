#### [도커를 이용하여 RO/RW PostgreSQL 설치하기]

> [!ㄷㄷㄷ] 속성 설명
> 
> - services
역할에 따라 슬래이브 기준으로 나누었다. 
postgresql-master와 postgresql-slave가 즉 컨테이너 이름
> - ports
>   마스터 서비스가 고유의 포트를 가지면 된다.  추가 된 슬래이브는 같은 네트워크를 가지기 때문에 마스터 포트 5432를 보게 한다.
> 
> - volumes
>   실 데이터 위치가 될 볼륨과 init sql 이 실행될 파일 세팅이 있다.
> - environment (가장 중요한)
>   POSTGRESQL_REPLICATION_MODE=master와 slave
>   POSTGRESQL_MASTER_PORT_NUMBER=5432 slave일 경우에 작성
>   

**docker-compose.yaml**
``` Shell
services:
  # master
  postgresql-master:
    container_name: postgresql-master
    image: 'bitnami/postgresql:latest'
    ports:
      - '5442:5432'
    restart: on-failure
    user: 'root'
    volumes:
      - postgresql_main_data:/bitnami/postgresql/data
    environment:
      - POSTGRESQL_REPLICATION_MODE=master
      - POSTGRESQL_REPLICATION_USER=abcde
      - POSTGRESQL_REPLICATION_PASSWORD=abcde_main1234%^
      - POSTGRESQL_USERNAME=abcde_main
      - POSTGRESQL_PASSWORD=abcde_main1234%^
      - POSTGRESQL_DATABASE=abcde_main
    networks:
      - net-postgresql

  # slave readonly
  postgresql-slave:
    container_name: postgresql-slave
    image: 'bitnami/postgresql:latest'
    ports:
      - '5443:5432'
    restart: on-failure
    user: 'root'
    depends_on:
      - postgresql-master
    environment:
      - POSTGRESQL_REPLICATION_MODE=slave
      - POSTGRESQL_REPLICATION_USER=abcde
      - POSTGRESQL_REPLICATION_PASSWORD=abcde_main1234%^
      - POSTGRESQL_MASTER_HOST=postgresql-master
      - POSTGRESQL_MASTER_PORT_NUMBER=5432
      - POSTGRESQL_USERNAME=abcde_main
      - POSTGRESQL_PASSWORD=abcde_main1234%^
    networks:
      - net-postgresql

volumes:
  postgresql_main_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/postgres-data-bit

networks:
  net-postgresql:
    driver: bridge
```

> replication-user-grant.sql
``` Shell
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO abcde;
ALTER USER abcde WITH SUPERUSER;
```
