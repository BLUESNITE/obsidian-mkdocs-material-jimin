#### 도커를 이용하여 RO/RW Mysql 설치하기

> [!NOTE] 컴포즈 파일에 다 담지 못한 내용이 있기 때문에 아래와 같이 실행한다.
> 
> 컨테이너 스케일 작성 할 수 있다. 이를 통해 스케일이 자동 조정된다.
> master 1
> slave 3
> 
> 아래의 경우 1마스터 3슬래이브(복제레플리카)가 생성되며 값을 수정하여 배포하면 그대로 컨테이너가 늘거나 줄어든다

```Shell
docker compose -f mysql-compose.yml up --detach --scale mysql-master=1 --scale mysql-slave=3

docker compose -f mysql-compose2.yml up --detach --scale mysql-master=1 --scale mysql-slave=2
```

> [!NOTE] 슬래이브 포트에 대해서
> slave의 컨테이너 갯수가 자동으로 생성 배포 됨으로. 지정하여 둘 수 없다

**docker-compose.yaml**
```Shell
services:
  mysql-master:
    container_name: mysql-master
    image: 'bitnami/mysql:latest'
    ports:
      - '3306'
      - '3316:3306'
    volumes:
      - mysql_main_data:/bitnami/mysql/data
    environment:
      - MYSQL_REPLICATION_MODE=master
      - MYSQL_REPLICATION_USER=abcde
      - MYSQL_REPLICATION_PASSWORD=abcde
      - MYSQL_ROOT_PASSWORD=abcde
      - MYSQL_USER=abc_main
      - MYSQL_PASSWORD=abc_main12345
      - MYSQL_DATABASE=abcde_main12345
    networks:
      - net-mysql

  mysql-slave:
    #container_name: mysql-slave
    image: 'bitnami/mysql:latest'
    ports:
      - '3306'
    depends_on:
      - mysql-master
    environment:
      - MYSQL_REPLICATION_MODE=slave
      - MYSQL_REPLICATION_USER=abcde
      - MYSQL_REPLICATION_PASSWORD=abcde
      - MYSQL_MASTER_HOST=mysql-master
      - MYSQL_MASTER_PORT_NUMBER=3306
      - MYSQL_MASTER_ROOT_PASSWORD=abcde
    networks:
      - net-mysql

volumes:
  mysql_main_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/mysql-data-bit

networks:
  net-mysql:
    driver: bridge
```
