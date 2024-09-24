기존 팀블로그 내 작성글 이관 

[Spring Boot Batch 설명 - 플래티어 연구소 테크 블로그 (tistory.com)](https://x2bee.tistory.com/22)
___
vscode로 플러그인 설치하고, Hello Scala 출력하기

### **vscode extention 설치**

플러그인명 : **Scala Syntax (offical)**

설명 : 공식적으로 지원되는 스칼라 문법 강조 확장입니다. 기본적인 문법 강조와 코드 가독성을 높여줍니다  
  

![](https://blog.kakaocdn.net/dn/bDWc9t/btsCKrFu36f/PEmLD2KWKLnGk6V3RnTuDK/img.png)

---

플러그인명 : **Metals**

설명 : Scala 및 sbt 프로젝트용 풍부한 기능을 제공하는 확장입니다. 코드 내비게이션, 리팩터링, 자동완성, 코드 액션 등 다양한 기능을 제공합니다.  
  

Metals = Meta (from Scalameta) + LS (from Language Server)

![](https://blog.kakaocdn.net/dn/s1j2Z/btsCAjWhutG/U1VFzQjyKoceFm9wAbKSyk/img.png)

---

플러그인명 : **Scala Language Server**

설명 : 스칼라 언어 서버를 활용한 확장으로, 코드 분석, 자동완성, 코드 작성 지원 등 다양한 기능을 제공합니다.  
  

![](https://blog.kakaocdn.net/dn/bMQalb/btsCzJubvFH/cwvpFuvmycSueY3hwdJJ1K/img.png)

---

플러그인을 검색을 해보면 Scala Syntax (offical)가 오피셜이 붙어있어서 대세의 플러그인이구나 할 수 있지만,

해외의 경험을 비교해 보면 vscode에서는 **Scala Metals**가 주류로 사용됨을 알 수 있습니다.

하여 Metals만 먼저 알아보기로 하겠습니다.

[https://scalameta.org/metals/docs/editors/vscode/](https://scalameta.org/metals/docs/editors/vscode/)에서 상단의 주요 인용을 가져오면,

> 확장 Scala Language Server 및 Scala(sbt)가 설치되어 있는 경우 비활성화해야 합니다. Dotty Language Server는 Metals 및 Dotty 확장이 비활성화되지 않기 때문에 비활성화할 필요가 없습니다 서로 충돌합니다. 그러나 Scala 3 코드에서 작업하려는 경우 이전에 열었던 작업 공간은 다음을 수행해야 합니다. Metals로 작업 공간을 열기 전에 먼저 제거하십시오.

Scala Language Server와 Scala(sbt)가 둘 다 설치돼 있으면 이 둘을 비활성화하는 것을 권장하고 있습니다.

하여 저는 Metals만 설치하여 사용하였습니다.

### **Metals 설정**

**Custom sbt launcher**

기본적으로 Metals는 내장된 SBT 런처를 사용하며, 환경 변수 및 **'.sbtopts' '.jvmopts' 'SBT_OPTS' 'JAVA_OPTS'**와 같은 설정들을 무시합니다. 이를 해결하기 위해서는 Metals 설정들 중에서 **'Sbt 스크립트'**를 업데이트하여 사용자 지정 스크립트를 사용할 수 있습니다. 추가적인 사용자 설정은 **'.sbt'** 파일 같은 환경과 유사한 사용자 정의를 적용할 수 있습니다.

**Speeding up import**

처음에 빌드를 실행할 때 시간이 많이 소요될 수 있습니다. 빌드의 복잡성에 따라 다양한 라이브러리 종속성을 다운로드해야 합니다. 

**Metals Commands**

- metals.run-current-file : 현재 파일의 주 클래스 실행
- metals.test-current-file : 현재 파일의 테스트 클래스 실행
- metals.test-current-target : 현재 프로젝트의 모든 테스트 실행

이제 대충 설치는 끝이 났습니다. Hello Scala 출력으로의 진행을 확인해보겠습니다.

### **Hello Scala 출력하기**

extention metals를 설치를 하고,

![](https://blog.kakaocdn.net/dn/c6zpXD/btsCzSdBwiX/zUuJ1iY5l5iUTVF4dP6d4k/img.png)

누른 채로 잠시 내버려두니 마치 해킹당한 듯이 vscode에 이것저것 대량으로 설치되기 시작했습니다.

주르륵주르륵 아래는 설치 후 로그창입니다.

![](https://blog.kakaocdn.net/dn/EfD3g/btsCJiPAfE6/0KbCLpKI5hpG15256KrDeK/img.png)

마찬가지로 설치 후 디렉토리

![](https://blog.kakaocdn.net/dn/vkaDf/btsCEKsjEFv/Fe7grbkrOGMIOoiP5oNkQ1/img.png)

추가된 extention을 통해 New Scala project를 클릭하여 hello world를 위한 프로젝트를 생성합니다.

이번에도 조금 걸립니다.

![](https://blog.kakaocdn.net/dn/beRogB/btsCzQ7Ws1E/mZItQUAWzFnQk4uXXXMJc1/img.png)

아래에는 생성된 hellow world 프로젝트 구조입니다.

![](https://blog.kakaocdn.net/dn/O2440/btsCy7CcNqu/H34kL7WBuGcH5W6gIMPKq0/img.png)

실행 테스트는 왠지 파이썬과 비슷할 것 같아 Main.scala 파일을 열어서 살짝(?) 기다리니

아래와 같이 run | debug가 나타납니다. 클릭하여 실행

![](https://blog.kakaocdn.net/dn/cT66H6/btsCKREedBz/ycV3JvTA0gCjkPwpJVwV1K/img.png)

아래는 확인된 로그창 문구는 ( Hello Scala!로 수정)

![](https://blog.kakaocdn.net/dn/bmXzxz/btsCEIOQdkx/12ulo7RqpxgQU2nlgHyUdK/img.png)

이상으로 아무것도 모르지만 Hello Scala까지 출력완료!

+ Scala3를 사용하기 위해서 습관처럼 버전업도 해줍시다.

build.sbt 파일을 열어봅니다.

이때 기본버전이 **"2.13.12"**으로 설치되어 있다면 가장 최신버전( **"3.3.1"** )으로 변경해줍니다.

변경 후 우측 끝에서 Libraries이하 **scala3-library_3-3.3.1-sources.jar**를 확인 할 수 있습니다.

![](https://blog.kakaocdn.net/dn/bYV4e3/btsCLohA7vh/KjovNDhjomEmqkWyTLTqW1/img.png)