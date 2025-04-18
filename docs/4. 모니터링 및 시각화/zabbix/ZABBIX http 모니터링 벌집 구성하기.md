> [!NOTE] 벌집
> 모니터링 대시보드를 구성하는데 이용하는 위젯별 내용을 작성. 이번 챕터에서는 벌집 위젯

ZABBIX는 *호스트*, *호스트그룹* 을 기반으로 모니터링 위젯을 생성 관리하게 된다.

이번에는 벌집 위젯을 사용하여 http health 상태를 표현하고자 한다.

[ZABBIX 벌집](https://www.zabbix.com/documentation/current/en/manual/web_interface/frontend_sections/dashboards/widgets/honeycomb "ZABBIX 벌집")

![[Pasted image 20250402140223.png]]

내가 작성하는 방법이 100% 정답이 아닐 것이다.

하지만 자료나 그리는 방법이 어렵기때문에 실습을 하며 정리 & 표현하고자 작성하는 글이다.

지금 하려는 절차는 아래와 같다.

`호스트` -> `웹 시나리오` -> `호스트 아이템` -> `의존아이템 기준으로 신규 Key 생성` -> `벌집 위젯`

호스트 생성은 생략

*웹 시나리오 작성하기*

작성에 앞서서 웹 시나리오 작성은 한 페이지에서 끝나지 않고

스텝에 따라 `시나리오` > `스탭` 최소 두 화면을 작성해주어야한다.

시나리오탭에서는 간단하게 구분을 할 수 있는 이름으로 시나리오 이름을 작성하여 준다.

![[Pasted image 20250402141421.png]]

두번째 스탭에서 실제 웹 시나리오의 동작을 작성하게 된다. 스탭에서 추가버튼을 통해서 팝업을 띄울수 있다.

![[Pasted image 20250402141559.png]]

웹 시나리오의 새로운 단계 > 팝업에서 항목이 많아보이지만 최소한만 작성해도 된다면 이름과 URL 정도면 되겠다.

![[Pasted image 20250402141640.png]]

해당 패턴으로 웹 시나리오를 작성하고 호스트 아이템을 작성해야한다.

웹 시나리오와 동일 위치의 탭 앞쪽에 아이템이 있다.

![[Pasted image 20250402141817.png]]

위와 같은 이미지에서 사용할 의존 아이템의 키를 작성해야하니 우측 상단 아이템 생성을 눌러준다.

![[Pasted image 20250402141930.png]]

아이템의 새 항목을 입력하는 창이다.

중요한건 이번 벌집표현에서는 의존 아이템을 사용한다는 것이다.

이름 <- 이 항목이 실제 벌집에서의 기본 라벨이 될 것이니 그에 맞추어서 이름을 작성해준다

키 <- 이 항목은 최종 벌집 위젯에서 선택하게 되는 항목 패턴이 된다

마스터 아이템 <- 이 항목이 앞서 작성한 웹 시나리오에서 생선된 키 패턴이 있는 곳이다. 아래와 같이 설정할 도메인의 패턴 값을 찾아서 선택하자.

![[Pasted image 20250402142155.png]]

기타 값들은 크게 중요하지 않으니 이대로 추가 생성을 종료한다.

이와 같은 작업으로 벌집에 표현할 도메인 별 호스트 아이템을 모두 생성한다.

반복해서 작업을 완료해주면 호스트 아이템에 아래와 같이 키 패턴들이 등록 된 것을 확인 할 수 있다.

![[Pasted image 20250402142552.png]]

이제 준비가 다 되었으니 벌집 위젯을 생성하러 넘어간다.

벌집 위젯 생성 팝업을 띄우면 아래와 같이 확인 할 수 있는데 직전에 확인한 패턴이 들어가는 곳이 항목 패턴이다.

![[Pasted image 20250402142745.png]]

*고급 구성*

![[Pasted image 20250402145314.png]]

*텍스트 값으로 사용할 것들*

- {ITEM.ID} : 아이템의 내부 ID (숫자)
- {ITEM.KEY} : 아이템의 key 값
- {ITEM.LASTVALUE} : 아이템의 마지막 값
- {ITEM.VALUE} : 아이템의 트리거 현재 값
- {ITEM.NAME} : 아이템의 이름
- {ITEM.DESCRIPTION} : 아이템의 설명

적용의 예시

![[Pasted image 20250402151409.png]]