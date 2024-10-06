기존 팀블로그 내 작성글 이관 

[Spring Boot Batch 설명 - 플래티어 연구소 테크 블로그 (tistory.com)](https://x2bee.tistory.com/22)
___
**Introduction**

이번 글에서는 Mongodb를 처음 사용해보는 초초짜 개발자가 기초 명령어를 수행하는 과정을 기록합니다.

![](https://blog.kakaocdn.net/dn/ZvQoQ/btsAIH6a8vw/WgpQXWkc5UmoEiykRuaH80/img.png)

실행시 화면

### 1. dbtabase 생성과 _MONGOSH  명령어 입력

![](https://blog.kakaocdn.net/dn/QQ6Py/btsAMrAxvF9/6SHo00kikzFBfheuasCoIk/img.png)

위 이미지는 'mongosh' 명령어를 사용하여 컬렉션을 생성하는 과정입니다.

use jeongzmin에서 'jeongzmin'은 데이터베이스 이름이며,

db.createCollection('myCollection')에서 'myCollection'은 컬렉션을 생성합니다.

### 2. 데이터 INSERT

![](https://blog.kakaocdn.net/dn/cBGQKn/btsALK8tdSj/Q2IuxwhCsqkJHJSQ1meN01/img.png)

위 이미지는 명령어를 사용하여 컬렉션에 데이터를 입력하는 과정입니다.

  
db.myCollection.insertOne({myname:'Jeong Ji Min', nickname:'Tech정또해방'});

명령어를 통해서 데이터를 추가하였습니다. 몽고DB는 Json 객체를 저장합니다.

### 3. 데이터 조회

![](https://blog.kakaocdn.net/dn/wZvW1/btsALUb9tZV/z2cfElIuRmibI31Yt3k2lk/img.png)

리스트 조회

![](https://blog.kakaocdn.net/dn/JhJZB/btsAJBR1SzB/3F4ijVVqfsBbV4rNHkl3I0/img.png)

단건 조회

### 4. 데이터 수정 및 신규 추가

![](https://blog.kakaocdn.net/dn/qxhSA/btsAIdjLtPM/EJ9nBfTVRBVk07kjA93wUk/img.png)

데이터 수정과 신규 추가

db.myCollection.updateOne({'nickname':'Tech정또해방'},  {$set : {'addr':'서울', 'nickname':'Tech정또해방2'}})

addr이 추가되었고, nickname이 업데이트 되었습니다.

### 5. 데이터 삭제

deleteOne을 사용하여 동일한 방법으로 삭제진행해봅시다.

이상으로 Mongodb를 처음 사용해보면서 CRUD 작업을 진행해보았습니다.