기존 팀블로그 내 작성글 이관 

[Spring Boot Batch 설명 - 플래티어 연구소 테크 블로그 (tistory.com)](https://x2bee.tistory.com/22)
___
Hello Scala를 찍어보았지만 아는 게 너무 없어서 최신 릴리즈 정보부터 학습해 보겠습니다.

#### **New in Scala 3**

가장 중요한 변화들에 대한 간단한 개요를 제공해 드리겠습니다.

더 자세한 정보를 원하신다면 공식 홈페이지의 자료를 확인해 주세요!

- **스칼라 3 북** : 스칼라 언어를 처음 접하는 개발자 용
- **구문 요약 (Syntax Summary)** : 새 구문들에 대한 공식적인 설명 제공
- **언어 참조 (Language Reference)** : Scala2에서 Scala3으로의 변경 사항에 대한 자세한 설명
- **마이그레이션 가이드** : Scala2에서 Scala3로 이동하는데 필요한 정보
- **스칼라 3 Contributing 가이드** : 문제 해결 가이드 및 컴파일러

[https://docs.scala-lang.org/scala3/new-in-scala3.html](https://docs.scala-lang.org/scala3/new-in-scala3.html)의 내용을 기초로 하고 있습니다.

 [New in Scala 3

Info: JavaScript is currently disabled, code tabs will still work, but preferences will not be remembered. The exciting new version of Scala 3 brings many improvements and new features. Here we provide you with a quick overview of the most important change

docs.scala-lang.org](https://docs.scala-lang.org/scala3/new-in-scala3.html)

내용을 보자면 마치. nextjs의 대규모 패치 때와 같은 느낌의 소개로 시작되고 있습니다.

> Scala 3 is a complete overhaul of the Scala language. At its core, many aspects of the type-system have been changed to be more principled. While this also brings exciting new features along (like union types), first and foremost, it means that the type-system gets (even) less in your way and for instance type-inference and overload resolution are much improved.  
>   
> Scala 3는 Scala 언어의 완전한 개편입니다. 핵심적으로 타입 시스템의 많은 측면이 더 원칙적으로 변경되었어요. 이는 유니언 타입과 같은 흥미로운 새로운 기능을 가져오긴 하지만, 무엇보다도 타입 시스템이 사용자의 방해를 (더) 적게 하게 되었다는 것을 의미해요. 예를 들어, 타입 추론과 오버로드 해결이 크게 개선되었습니다.

new-in-scala3 페이지에서 소개되는 주요 다섯 가지 사항은 아래와 같습니다.

- 새롭고 반짝거리는: 문법 (New & Shiny: The Syntax)
- 주관적인: 맥락적 추상화 (Opinionated: Contextual Abstractions)
- 의미하는 대로 말하기: 타입 시스템 개선 (Say What You Mean: Type System Improvements)
- 새롭게 바라보는: 객체 지향 프로그래밍 (Re-envisioned: Object-Oriented Programming)
- 전부 포함된: 메타프로그래밍 (Batteries Included: Metaprogramming)

항목들의 상세한 내용을 하나씩 살펴보겠습니다.

먼저 ,

#### **새롭고 반짝거리는: 문법 (New & Shiny: The Syntax)**

크고 작은 사소한 정리 작업 이외도, Scala 3 문법은 다음과 같은 개선 사항을 제공합니다.

- if, while, for와 같은 제어 구조를 위한 새로운 "quiet (조용한)" 문법 (새로운 제어 구조 문법)
- new 키워드의 선택 사항화 (크리에이터 애플리케이션)
- 들여 쓰기에 민감한 방해 없는 스타일의 프로그래밍을 지원하는 선택적 중괄호
- 타입 레벨 와일드카드의 _를 ?로 변경
- 임플리시트(그리고 그들의 문법)가 크게 개정

#### **주관적인: 맥락적 추상화 (Opinionated: Contextual Abstractions)**

Scala의 기본 핵심 개념 중 하나는 사용자에게 강력한 소수의 기능을 제공하여 그것들을 조합해 크고 때로는 예상치 못한 표현력을 낼 수 있게 하는 것입니다.

예를 들어, 임플리시트 기능은 맥락적 추상화 모델링, 타입 수준의 계산 표현, 타입 클래스 모델링, 암시적 강제 변환, 확장 메서드 인코딩 등 여러 용도로 활용되었습니다.

이러한 사용 사례를 통해 배운 점을 바탕으로 Scala3는 약간 다른 접근 방식을 취하며 메커니즘보다 의도에 중점을 두고 있습니다. 매우 강력한 하나의 기능을 제공하는 대신에 Scala3는 프로그래머가 직접 자신의 의도를 표현할 수 있도록 여러 맞춤형 언어 기능을 제공합니다.

- **문맥 정보 추상화**  
    Using 절을 통해 프로그래머는 호출된 문맥에서 사용 가능하고 암시적으로 전달되어야 하는 정보를 추상화할 수 있습니다. Scala2의 implicits보다 개선된 using 절은 타입으로 명시할 수 있어 함수 서명에서 명시적으로 참조되지 않은 용어 변수이름을 해방시킵니다.  
      
    (*** Scala2의 implicits**는 컴파일러에 의해 자동으로 삽입되는 암시적 값이나 암시적 매개변수를 나타냅니다.)  
      
    
- **Type 클래스 인스턴스 제공  
    **Given 인스턴스를 통해 프로그래머는 특정 타입의 규범적인 값을 정의할 수 있습니다. 이는 구현 세부사항을 노출시키지 않고 타입 클래스를 사용한 프로그래밍을 더 직관적으로 만듭니다.  
      
    
- **클래스 후속적 확장  
    **Scala2에서는 확장 메서드를 암시적 변환이나 암시적 클래스를 사용하여 인코딩해야 했습니다. 그러나 Scala3에서는 확장 메서드가 언어 자체에 내장되어 더 나은 오류 메시지와 개선된 타입 추론을 제공합니다.  
      
    
- **유형 간 전환  
    **암시적 변환은 타입 클래스 Conversion의 인스턴스로 완전히 새롭게 재설계되었습니다.   
      
    
- **고차 문맥적 추상화  
    **컨텍스트 함수의 새로운 기능은 문맥적 추상화를 주요한 요소로 만들어냅니다. 이는 라이브러리 작성자들에게 중요한 도구로, 간결한 도메인 특화 언어를 표현할 수 있게 해 줍니다.  
      
    
- **컴파일러가 행동 가능한 피드백  
    **컴파일러가 암시적 매개변수를 해결할 수 없는 경우, 문제를 해결할 수 있는 import 제안을 제공합니다.

#### **의미하는 대로 말하기: 타입 시스템 개선 (Say What You Mean: Type System Improvements)**

Scala3의 타입 시스템은 크게 개선된 타입 추론뿐만 아니라, 타입에서 불변성을 정적으로 표현하는 강력한 도구들을 제공합니다.

- **열거형**  
    Enum은 case 클래스와 잘 어우러지도록 재설계되어 대수적 데이터 유형을 표현하는 새로운 표준을 형성합니다.  
      
    
- **불투명 형식  
    **Opaque types 성능에 부담을 주지 않으면서도 불투명한 타입 별칭 뒤에 구현 세부 사항을 숨깁니다. Opaque types은 값 클래스를 대체하고 추가적인 박싱 오버헤드를 유발하지 않고 추상화 장벽을 설정할 수 있게 해 줍니다  
      
    
- **교집합 및 합집합 유형  
    **새로운 기반 위에 타입 시스템을 구축함으로써 교집합 유형의 인스턴스(A & B와 같은) A와 B의 인스턴스입니다. 합집합 유형의 인스턴스(A | B와 같은)는 A 또는 B의 인스턴스입니다. 두 구조는 상속 계층 외부에서 타입 제약을 유연하게 표현할 수 있게 해 줍니다.  
      
    
- **의존 함수 유형  
    **Scala2에서 이미 반환 유형을 (값) 인수에 따라 달라지게 할 수 있었습니다. Scala3에서는 이 패턴을 추상화하고 의존 함수 유형을 표현할 수 있게 되었습니다. (예 type F = (e: Entry) => e.Key)  
      
    
- **다형적 함수 유형**  
    종속 함수 유형과 마찬가지로 Scala2는 유형 매개변수를 허용하는 메서드를 지원했지만 프로그래머가 이러한 메서드를 추상화하는 것은 허용되지 않았습니다. Scala3에서 다형성 함수 유형은 값 인수 외에 유형 인수를 취하는 함수를 추상화할 수 있습니다. (예 [A] => List[A] => List[A] )  
      
    
- **타입 람다  
    **Scala2에서 컴파일러 플러그인을 사용하여 표현해야 했던 것이 이제 Scala3의 일류 기능입니다. 유형 람다는 보조 유형 정의 없이 유형 인수로 전달될 수 있는 유형 수준함수입니다.  
      
    
- **매치 유형  
    **타입 수준의 계산을 암시적 해결을 통해 인코딩하는 대신 Scala3에서는 타입에 대한 직접적인 매칭 지원을 제공합니다. 타입 수준 계산을 타입 검사기에 통합함으로써 개선된 오류 메시지를 가능하게 하고 복잡한 인코딩이 필요하지 않게 합니다. 

#### **재 구성된: 객체 지향 프로그래밍 (Re-envisioned: Object-Oriented Programming)**

Scala는 항상 함수형 프로그래밍과 객체 지향 프로그래밍 사이의 전선에 있었는데, Scala3는 이 두 방향으로의 경계를 더욱 넓혀 나가고 있습니다. 위에서 언급된 타입 시스템 변경과 컨텍스트 추상화의 재설계는 이전보다 함수형 프로그래밍을 더 쉽게 만들어주고 있습니다. 동시에 아래의 새로운 기능들은 구조화된 객체 지향 디자인을 가능케 하며 최상의 방법론을 지원합니다.

- **통과  
    **트레이트는 클래스에 더 가까워졌으며 이제 파라미터를 받을 수 있어서 모듈화 된 소프트웨어 분해에 더 강력한 도구로 작용합니다.  
      
    
- **확장 계획  
    **의도하지 않은 클래스의 확장은 객체 지향 디자인에서 오래된 문제였습니다. 이 문제를 해결하기 위해서 오픈 클래스는 라이브러리 디자이너가 클래스를 명시적으로 열어두도록 요구합니다.  
      
    
- **구현 세부 사항 숨기기  
    **동작을 구현하는 유틸리티 트레이트가 때로는 유추된 타입의 일부가 되면 안 될 때가 있습니다. Scala3에서는 해당 트레이트를 투명하게 표시하여 사용자로부터 상속을 숨길 수 있습니다. (유추된 타입에서)  
      
    
- **상속보다 구성  
    **이 문구는 자주 인용되지만 구현하기는 번거로웠습니다. 그러나 Scala3의 익스포트 절로 이제 그렇지 않습니다. 임포트와 대칭되는 익스포트 절은 사용자가 객체의 선택된 멤버에 대한 별칭을 정의할 수 있습니다.  
      
    
- **NPE가 더 이상 없음 (실험적)**  
    Scala3는 이전보다 더 안전해졌습니다. 명시적 null은 null을 타입 계층에서 제거하여 에러를 정적으로 잡을 수 있게 도와줍니다. 완전한 초기화를 위한 추가적인 검사로 초기화되지 않은 객체에 대한 액세스를 감지할 수 있습니다.  
      
    

#### **전부 포함된: 메타프로그래밍 (Batteries Included: Metaprogramming)**

Scala2에서의 매크로는 실험적 기능이었지만 Scala3에서는 메타프로그래밍을 위한 강력한 도구들이 함께 제공됩니다. 매크로 튜토리얼에는 다양한 기능에 대한 상세한 정보가 담겨있습니다. Scala3는 메타프로그래밍을 위해 다음과 같이 제공합니다.

- **인라인**  
    기본 출발점으로 인라인 기능은 값과 메서드를 컴파일 시간에 축소할 수 있게 합니다. 이 간단한 기능은 이미 많은 사용 사례를 다루고 있으며 동시에 더 고급 기능에 대한 진입점을 제공합니다.  
      
    
- **컴파일 시간 연산  
    **scala.compiletime 패키지에는 인라인 메서드를 구현하는 데 사용할 수 있는 추가 기능이 포함되어 있습니다.  
      
    
- **쿼트된 코드 블록  
    **Scala3에서는 코드의 준인용 기능을 추가하여 코드를 생성하고 분석하기 위한 편리한 고수준 인터페이스를 제공합니다. 1과 1을 더하는 코드를 생성하는 것은 '{1+1}' 처럼 매우 간단합니다.  
      
    
- **리플렉션 API  
    **더 고급 사용 사례를 위해 quotes.reflect는 프로그램 트리를 검사하고 생성하는 데 더 자세한 제어를 제공합니다.

#### **Scala3의 패키지 구조**

scla 패키지에는 명시적인 한정이나 가져오기없이 모든 Scala 컴파일 단위에서 엑세스할 수 있는 **"Int" "Float" "Array"** 또는 **"Option"**과 같은 핵심 유형이 포함되어 있습니다.

주목할만한 패키지는 다음과 같습니다.

- **"scala.collection"** 의 이하에는 Scala의 컬렉션 프레임워크가 포함되어 있습니다.
    - **"scala.collection.immutable"** Vector, List, Range, HashMap, HashSet 등의 불변한 순차적 데이터 구조
    - **"scala.collection.mutable"** ArrayBuffer, StringBuilder, HashMap, HashSet 등의 가변한 순차적 데이터 구조
    - **"scala.collection.concurrent"** Future 및 Promise와 같은 동시성 프로그래밍을 위한 기본 요소들  
          
        
- **"scala.concurrent"** TrieMap과 같은 가변적인 동시성 데이터 구조
- **"scala.io"** 입출력 작업
- **"scala.math"** 기본적인 수학 함수 및 BigInt, BigDecimal과 같은 추가적인 숫자 타입
- **"scala.sys"** 다른 프로세스 및 운영체제와 상호작용
- **"scala.util.matching"** 정규 표현식
- **"scala.reflect"** Scala의 리플렉션 API (scala-reflect.jar)
- **"scala.xml"** XML 파싱, 조작 및 직렬화 (scala-xml.jar)
- **"scala.collection.parallel"** 병렬 컬렉션 (scala-parallel-collections.jar)
- **"scala.util.parsing"** 파서 컴비네이터 (scala-parser-combinators.jar)
- **"scala.swing"** swing이라고 불리는 java의 gui프레임워크를 편리하게 래핑한것 (scala-swing.jar)

위 프로젝트 구조는 [https://www.scala-lang.org/api/3.3.1/](https://www.scala-lang.org/api/3.3.1/)를 참고하여 작성하였습니다.

여기까지 Scala 3에서 변화된 중점들을 확인해 보았습니다.