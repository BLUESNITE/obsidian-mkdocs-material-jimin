>사용하는 캘린더가 여러 개로 나뉘어 있는 경우, 일정 중복 확인이나 반복적인 등록/수정 작업으로 인하여 개인 일정 관리가 불편하다고 느낄때가 있습니다. 이번 게시글에서 JIRA 일정을 Apple 캘린더 (Mac 캘린더)에 통합하는 과정을 작성했습니다.

**JIRA에 등록된 이슈 일정을 .ics 형식으로 가져와 Mac에서 직접 구독하는 방식**

#### 1. 결과물 확인

아래 이미지와 같이 JIRA 정지민 이라는 별도의 항목으로 캘린더 일정이 추가 된 것을 확인!

![[Pasted image 20250701180803.png]]
#### 2. 캘린더 구독 구조

Mac 캘린더에서는 .ics 확장자의 URL을 통해 외부 캘린더를 구독 가능

1. 상단 메뉴 > 파일 > 새로운 캘린더 구독... 선택
2. 팝업창이 뜨면, JIRA에서 생성한 **.ics URL**을 입력

(참조 이미지)

![[Pasted image 20250701180824.png]]

![[Pasted image 20250701180836.png]]

#### 3. JIRA에서 Issue Calendar 설정하기

JIRA에 Issue Calendar App을 추가하면 커스텀 뷰 없이도 화면의 우측 끝의 Share 버튼을 통해서 외부 구독 URL을 생성 가능

![[Pasted image 20250701180847.png]]

![[Pasted image 20250701180858.png]]

위 이미지 우측끝에 Share 버튼 클릭

![[Pasted image 20250701180907.png]]

**여기서부터 담당자 기준으로 iCal 생성**

- Projects : 대상 프로젝트 선택
- Name : JIRA 정지민
- Start date field : (필수값인) Target start
- Due date field : (필수값인) Target end
- Issue filters : ***** 보고 싶은 담당자 지정**

![[Pasted image 20250701180920.png]]

마지막으로 생성한 URL을 복사하여 아래와 같이 적용 진행

![[Pasted image 20250701180940.png]]

구독을 클릭 후 캘린더 모두 새로고침 수행.