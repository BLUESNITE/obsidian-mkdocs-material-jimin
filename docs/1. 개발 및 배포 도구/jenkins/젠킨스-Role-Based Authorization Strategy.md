> [!NOTE] 메모
> Jenkins에 로그인한 사용자 계정별로 볼 수 있는 item 목록을 구성하기 위한 플로그인
> Role-Based Authorization Strategy (RBAC)

### 플러그인 설치
Role-Based Authorization Strategy
___
### 설정
**[Manage Jenkins] -> [Configure Global Security]**

![[Pasted image 20240912095559.png]]

**Authorization** 섹션에서 **Role-Based Strategy** 를 선택

![[Pasted image 20240912104752.png]]

다시 **[Manage Jenkins] -> [Manage and Assign Roles]**

![[Pasted image 20240912104845.png]]

**역할(Role)** 생성 후 **Item roles** 적용

![[Pasted image 20240912105252.png]]

![[Pasted image 20240912122911.png]]

다음과 같이 적용 후 develop 계정으로 로그인한 브라우져에서 확인.

> [!TIP] 
> 다른 브라우저에서 미리 develop 으로 로그인 후 새로고침해도 즉시 반영되는 것 확인 가능
