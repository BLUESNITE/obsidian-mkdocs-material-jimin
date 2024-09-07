### AWS EC2에 SSH 접속하기 위한 최소작업을 기록

*최소한의 생성 목록*
- VPC
- SUBNET
- SECURITY GROUP
- ROUTE TALBE
- INTERNET GW

___ 
![[Pasted image 20240725083232.png]]

이 구조가 나오도록. VPC <-> 서브넷 <-> 라우팅 테이블 <-> 네트워크 IGW연결이 필요합니다.
그리고 보안그룹에 SSH 접속을 위해 인바운드 규칙 22번 포트 추가합니다.

단순하지만 나중에 또 할때 빼먹을까봐 메모.