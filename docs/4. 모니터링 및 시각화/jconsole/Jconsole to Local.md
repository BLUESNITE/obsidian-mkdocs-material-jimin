**※ 주저리 주저리...**
갑지기 또 왜 `Jconsole` 이냐 ... ?
그라파나를 할려니 `JVM`을 봐야했고, `JMX`를 쓰려니 `JVM`을 모니터링해야하고,
`JVM`을 쓰려하니 `Jconsole`을 이용하라고 한다. 첩첩산중이다. 이래서 **모니터링은** **골치가 아프다**
그래도 일단 해본다.

> [!TIP] Local host 환경에서의 JVM, Jconsole로 모니터링하기
> 여기서부터는 대부분 처음 보게 된 내용이고 잘 알지도 못한다.
> 그래도 기록을 남겨두어야 난중에 이해를해서 편집이라도 할 것 아닌가 ...

> [!CHECK] 1단계. JAVA_HOME 확인
> 내 경우엔 아래와 같이 자바 경로가 잡혀있다.
> 
> (JAVA_HOME)
...\java\java-17-openjdk-17.0.3.0.6-1.win.x86_64

> [!CODE] 2단계. Jconsole 사용을 위한 설정
> Jconsole을 이용하기 위해서는 java option을 수정하여 사용하는데 나는 JAVA_HOME의 설정을 이용할거다. 왜냐면 이게 쉬운거 같으니까.
> 
> 예상되는 단점은 모든 JAVA_HOME 실행에 적용될 텐데. 확인해보고 원복 시키면 되겠지.

**그래서 JAVA_HOME을 공통으로 사용하고 JVM에다가 java option을 추가하는 경우**
Open JDK 17 기준으로 JAVA_HOME 설정한 곳에 들어가면 다음과 같다.
![[Pasted image 20240701112059.png]]

감으로 이 폴더 저 폴더 열어보면 다음과 같은 management 폴더의 구성을 찾을 수 있다.
![[Pasted image 20240701112202.png]]

여기서 **management.properties에 다음을 추가하겠다.**
```shell
com.sun.management.jmxremote
com.sun.management.jmxremote.port=<Applicaion Sever Port 8091>;
```

아 하여간 마음에 안든다.
MSA라서 어플리케이션 서버도 여러개를 운영하는데. 단일이라니.
그래서 GPT 한테 이것도 물어보고 진행한다.
```shell
물어봐도 GPT도 햇소리만 한다.
이해를 못한게 정확하다.
그래도 난 이해했으니 다음 질문으로 넘어갔다.
```

`java -Dcom.sun.management.jmxremote=true \ -Dcom.sun.management.jmxremote.port=8093 \ -Dcom.sun.management.jmxremote.authenticate=false \ -Dcom.sun.management.jmxremote.ssl=false \ -jar your-application.jar`

> [!CODE] 위 코드를 mvnw에 적용 하는 방법을 찾아보자.
```shell
MAVEN_OPTS="$(concat_lines "$MAVEN_PROJECTBASEDIR/.mvn/jvm.config") $MAVEN_OPTS"
이하에 다음을 추가

JMX_JAVA_OPTS="$JAVA_OPTS -Dcom.sun.management.jmxremote=true"
JMX_JAVA_OPTS="$JAVA_OPTS -Dcom.sun.management.jmxremote.port=8093"
JMX_JAVA_OPTS="$JAVA_OPTS -Dcom.sun.management.jmxremote.authenticate=false"
JMX_JAVA_OPTS="$JAVA_OPTS -Dcom.sun.management.jmxremote.ssl=false"

MAVEN_OPTS="$MAVEN_OPTS $JMX_JAVA_OPTS"
```

> [!CHECK] 음... 안되네...? 실행 로그 분석
> VSCODE에서는 mvnw 직접실행임에도 의도한대로 실행이 잘되지않았다.
```shell
Copyright (C) Microsoft Corporation. All rights reserved.

새로운 기능 및 개선 사항에 대 한 최신 PowerShell을 설치 하세요! https://aka.ms/PSWindows

PS C:\project\aws-moon\moon-x2bee-api-member-vanilla>  & 'C:\tool\java\java-17-openjdk-17.0.3.0.6-1.win.x86_64\bin\java.exe' '@C:\Users\USER\AppData\Local\Temp\cp_an4yazjlx40tgrue8924ju9ex.argfile' 'com.x2bee.api.member.X2beeApiMemberApplication' 
SLF4J(W): Class path contains multiple SLF4J providers.
SLF4J(W): Found provider [ch.qos.logback.classic.spi.LogbackServiceProvider@5ffead27]
SLF4J(W): Found provider [org.apache.logging.slf4j.SLF4JServiceProvider@6356695f]
SLF4J(W): See https://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J(I): Actual provider is of type [ch.qos.logback.classic.spi.LogbackServiceProvider@5ffead27]
12:40:11,138 |-INFO in ch.qos.logback.classic.LoggerContext[default] - This is logback-classic version 1.5.6
```

> [!CODE] 그럼 방법을 전환하여 실행 CLI를 직접 수정하자
```shell hl:7-8
cd C:\project\aws-moon\moon-x2bee-api-member-vanilla

(수정전)
& 'C:\tool\java\java-17-openjdk-17.0.3.0.6-1.win.x86_64\bin\java.exe' 
'@C:\Users\USER\AppData\Local\Temp\cp_an4yazjlx40tgrue8924ju9ex.argfile' 'com.x2bee.api.member.X2beeApiMemberApplication'

(수정후)
& 'C:\tool\java\java-17-openjdk-17.0.3.0.6-1.win.x86_64\bin\java.exe' '@C:\tools\jmx.txt' '@C:\Users\USER\AppData\Local\Temp\cp_65i6cnpe2maxyuu7e07cj9na5.argfile' 'com.x2bee.api.member.X2beeApiMemberApplication' 
```

> [!INFO] 더 좋은 실행 방법
```hl:5 shell
이미 작성해둔 jmx.txt 파일을 이용한다.
아래 이미지에서 Run with Profile에서 
'@C:\tools\jmx.txt'
위를 작성하여 실행
```
![[Pasted image 20240701165846.png]]

> [!WARNING] 여기서 잠깐. jmx.txt 내용을 살펴보자.
> txt 파일을 사용한 이유는 단순 CLI에서 문장이 너무 길어서 ... 실행이 안되었다 ...
```shell
-Dcom.sun.management.jmxremote=true
-Dcom.sun.management.jmxremote.port=8091
-Dcom.sun.management.jmxremote.authenticate=false
-Dcom.sun.management.jmxremote.ssl=false
-cp C:\Users\USER\AppData\Local\Temp\cp_an4yazjlx40tgrue8924ju9ex.argfile
```

> [!NOTE] 해설
> 일단 적용이 되어야 다음을 기약 할 수 있으니 되면되는거야 식으로 동작까지 붙였다.
> 정성과 노력의 여지가 있다면 mvnw 실행으로 적용되도록 ...
#### [일단은 Jconsole]
정상 동작이 잘된다면 CLI `jconsole`에서 실행 된 Local Process가 노출되었다.
![[Pasted image 20240701131234.png]]

> [!NOTE] 이슈
> Jconsole에서 org.springframework.boot를 보면 다양한 정보가 나와야 하는 걸로 보이는데...
> 내 작업물에는 무언가(?) 빈약한 정보까지 밖에 나오지 않는다. 어떤 이슈인지를 모르겠다.
> 
> ex) org.springframework.boot 이미지
> 
> ![[Pasted image 20240701174332.png]]
> > Endpoint
> > >Beans
> > >Caches
> > >...
> > >Health
> > >Info
> > >Metrics
> > >등 ...
> 
> 최종 목적지는 여기에서 Metrics가 되겠다.

> [!NOTE] 여기에서 ... 목적분석을 다시 하였다.
> 무슨 이야기냐(?) 내 접근 방법에 의문을 든 것이다.
> 위 방법도 성공하면 좋은 case by가 될 것 이지만 사실 쓰고나니 나는 Endpoint에서 Metrcs 정보만 잘 얻으면 목표 달성 아닌가(?) 하여 생각하고 다시 찾아보니 이미 actuator 추가한 순간 어느 정도 방법은 정해져 있던 것이다.
> 
> 그래서 다시 돌아보았다 applicaion.yaml을 그리고 알게 된 사실 ...
> 예를 들어 http://localhost:8191/management 와 같이 접속해보면 이미 내가 어플리케이션에 정의해 둔 Open Endpoint들이 보이고 있는 것이다. 거기에서 metrics만 잘 열어서 프로메테우스와 연결하면 끝나는 걸 뭘 모르니 또 삽질을 한 것이다. 
> 
> 하여 살짝 applicaion.yaml에 정의해야 할 내용만 재정리하였다.

> [!INFO] 설명
> 여기에서 management.server.port는 metrics 정보를 수집할 포트가 된다. 
> applicaion을 service할 port가 아니다.
```applicaion.yaml shell
management.endpoint.metrics.enabled = true
management.endpoints.web.exposure.include = "metrics"
management.server.port = 8191
```

> [!WARNING] 이슈
> 위 내용까지 설정하고보니 단번에 떠오르는 이슈가 있다.
> 우아한 형제들에서 본 내용인 것 같은데. 일반적으로는 내가 열어둔 port 를 모르는 것이 맞지만.
> 혹여라도 노출되어 누군가 접근을 시도하면 우리 서버의 메트릭 정보를 모두 수집해 갈 수 있다는 것이다. 매우 위험 ... 하여 추가 해결 방법까지 도출해야. 완성이지 않을까 생각 된다.

#### [일단은 검증 or 테스팅]

일단 metrics 정보 노출 테스팅은 아래 내용 정도에서 끝이 난다.

> [!CODE] /metrics 내용확인
```shell
{
    "timestamp": "2024-07-01T19:08:45.2836911",
    "code": "0000",
    "message": null,
    "isProcess": null,
    "payload": {
        "names": [
            "application.ready.time",
            "application.started.time",
            ....
            "executor.active",
            "executor.completed",
            "executor.pool.core",
            "executor.pool.max",
            "executor.pool.size",
            "executor.queue.remaining",
            "executor.queued",
            "hikaricp.connections",
            "hikaricp.connections.acquire",
            "hikaricp.connections.active",
            "hikaricp.connections.creation",
            ...
            "jdbc.connections.active",
            "jdbc.connections.idle",
            "jdbc.connections.max",
            "jdbc.connections.min",
            "jvm.buffer.count",
            "jvm.buffer.memory.used",
            "jvm.buffer.total.capacity",
            ...
            "jvm.gc.live.data.size",
            "jvm.info",
            "jvm.memory.committed",
            "jvm.memory.max",
            "jvm.memory.usage.after.gc",
            "jvm.memory.used",
            "jvm.threads.daemon",
            "jvm.threads.live",
            "jvm.threads.peak",
            "jvm.threads.started",
            "jvm.threads.states",
            "logback.events",
            "process.cpu.time",
            "process.cpu.usage",
            "process.start.time",
            "process.uptime",
            "spring.security.filterchains",
            "spring.security.filterchains.ExceptionHandlerFilter.after",
            ...
            "system.cpu.count",
            "system.cpu.usage",
            "tomcat.sessions.active.current",
            "tomcat.sessions.active.max",
            "tomcat.sessions.alive.max",
            "tomcat.sessions.created",
            "tomcat.sessions.expired",
            "tomcat.sessions.rejected"
        ]
    }
}
```

> [!CODE] /metrics/jvm.info 내용확인
```shell
{
    "timestamp": "2024-07-01T19:10:44.747653",
    "code": "0000",
    "message": null,
    "isProcess": null,
    "payload": {
        "name": "jvm.info",
        "description": "JVM version info",
        "baseUnit": null,
        "measurements": [
            {
                "statistic": "VALUE",
                "value": 1
            }
        ],
        "availableTags": [
            {
                "tag": "application",
                "values": [
                    "x2bee-api-member"
                ]
            },
            {
                "tag": "vendor",
                "values": [
                    "ojdkbuild"
                ]
            },
            {
                "tag": "runtime",
                "values": [
                    "OpenJDK Runtime Environment"
                ]
            },
            {
                "tag": "version",
                "values": [
                    "17.0.3+6-LTS"
                ]
            }
        ]
    }
}
```
___
미완의 해결책.
#### [이슈:보안문제] 
> [!NOTE] Actuator 안전하게 사용
> 이 내용은 `Application Security`에 속하는 내용이 되나보다. 우형이 알려줬다.
> 

```java
// 아래와 같이 Role 전개한다는 이야기가 있다.
http.antMatchers("/actuator/**").hasRole("ADMIN")
```
