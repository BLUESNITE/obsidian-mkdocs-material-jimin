![[Pasted image 20250220185508.png]]

오랜만에 접속한 Superset 설치 Quickstart 내용이 많이 간결해져서 새로 작성

**1. Get Superset**

기존과 동일
```
git clone https://github.com/apache/superset
```


**2. latest Update**

```
cd superset
git checkout tags/4.1.1
docker compose -f docker-compose-image-tag.yml up
```

**3. login**

```
username: admin
password: admin
```

이전에는 SUPERSET_SECRET_KEY 설정하고 기타등등 확인하고 해야했는데
이제는 위 과정으로 설치가 정말 잘 된다.
진작 이렇게 만들지. 다시봤다 슈퍼샤이(set)