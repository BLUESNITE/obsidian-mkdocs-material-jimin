#### 문제 상황

어느날 온프레미스 개발 서버의 성능이 급격히 느려졌다 ...
예상된 느려짐이라고 생각이 들었으나 담당자로써 정확한 원인과 해결 방법을 찾아 조치를 해야만 했습니다.

#### 원인 분석

> [!NOTE] 디스크 사용량 확인
> 먼저 아래의 명령어를 사용해서 가장 높은 디스크 사용량을 찾아보았습니다.

```shell
du -h --max-depth=1 /var/lib/docker/volumes
```

> 결과 중 높은 디스크 사용량 확인 `2.4T`

```script
root@abc:/home/tech# du -h --max-depth=1 /var/lib/docker/volumes
8.0K    /var/lib/docker/volumes/compose-files_postgresql_main_data
2.4T    /var/lib/docker/volumes/f5953ffa186e520aab1b983038336ca8e4840243387a65a418995bdfb9d6407c
12K     /var/lib/docker/volumes/test_postgresql
12K     /var/lib/docker/volumes/mysql2_mysql_data_master
12K     /var/lib/docker/volumes/ex-final_postgresql_main_data
12K     /var/lib/docker/volumes/compose-files_mysql_data_s
297M    /var/lib/docker/volumes/ed58db91b75986384845d422d5ee648f1e36d44ee26273b1f1480a3333014b8b
12K     /var/lib/docker/volumes/compose-files_mysql_data
12K     /var/lib/docker/volumes/mysql2_mysql_data_m
12K     /var/lib/docker/volumes/postgres-labs_postgresql_labs_data
72K     /var/lib/docker/volumes/test_sonarqube_logs
12K     /var/lib/docker/volumes/postgres-labs_postgresql_main_data
12K     /var/lib/docker/volumes/mysql2_mysql_data_s
32K     /var/lib/docker/volumes/test_sonarqube_extensions
12K     /var/lib/docker/volumes/compose-files_mysql_data_m
12K     /var/lib/docker/volumes/mysql_mysql_main_data
12K     /var/lib/docker/volumes/compose-files_mysql_data_v
250M    /var/lib/docker/volumes/sonarqube_sonarqube_data
12K     /var/lib/docker/volumes/compose-files_mysql-slave
12K     /var/lib/docker/volumes/mysql2_mysql_data_slave
150M    /var/lib/docker/volumes/test_sonarqube_data
12K     /var/lib/docker/volumes/compose-files_mysql-master
737M    /var/lib/docker/volumes/sonarqube_postgresql_data
2.4T    /var/lib/docker/volumes
```

> [!NOTE] 문제의 볼륨의 실제 컨테이너 식별
> 스크립트를 작성하여 확인해보았습니다.

```shell
#!/bin/bash
volume_id="f5953ffa186e520aab1b983038336ca8e4840243387a65a418995bdfb9d6407c"

for container in $(docker ps -aq); do
    if docker inspect -f '{{range .Mounts}}{{.Name}}{{end}}' $container | grep -q $volume_id; then
        echo "Container using the volume:"
        docker inspect -f '{{.Name}}' $container
    fi
done
```

실행결과 문제의 컨테이너는 _Nexus3_
![[Pasted image 20240823083641.png]]

#### Nexus Blob Stores

![[Pasted image 20240823083738.png]]

Total Size와 Available space를 확인해보면 이미 엄청나게 사용하고 있고, 얼마 남지 않았음을 알 수 있었습니다.

#### 해결방안

다행히 nexus에 Tasks > Scheduled tasks라는 메뉴가 있었습니다.

![[Pasted image 20240823083847.png]]

![[Pasted image 20240823083946.png]]

#### 설정한 정리작업

- Clean up docker repository (기본설정)
- Docker - Delete unused manifests and images
- Admin - Compact blob store
- Admin - Delete orphaned blobs

![[Pasted image 20240823094629.png]]

docker-hosted 위주로 관련된 파일 정기적으로 지워질수 있게 설정해주었습니다.

![[Pasted image 20240823085418.png]]
