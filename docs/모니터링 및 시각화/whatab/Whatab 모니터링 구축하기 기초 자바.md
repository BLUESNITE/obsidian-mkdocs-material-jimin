> [!CHECK] 와탭 주요포인트 확인
> 1. 파이프라인에서 **whatap_agent** 디렉토리 확인 (필요에따라 폴더명으로 구분)
> 2. **whatap** 이 적용되는 버전의  **Dockerfile** 을 별도로 관리 (추후 제거 가능하도록)
> 3. 쿠버네티스 환경에서는 ConfigMap/Secret로 **whatap.conf, paramkey.txt** 주입
> 4. Node와 Java 언어에따라 적용 방법이 조금 차이가 있음

### 1. 파이프라인 공통 라이브러리 복사 단계 예시

*copyLibrarys 함수* 에서 플래그 변수에 따라서 의존성 세팅을 진행함. 

```
(asis code)

        } else if(ENABLE_SAMPLE_WHATAB == "Y" && PRJ_TARGET == "stg") {
            sh """#!/bin/bash
            cp -r scm/docker/DockerfileStg project/Dockerfile &> /dev/null
            rm -rf project/whatap_agent
            mkdir -p project/whatap_agent
            cp -r scm/whatap_agent_stg/* project/whatap_agent &> /dev/null
            """
            
(tobe code)

// Case 매핑 (src, dest)
def mappings = [
	"ENABLE_SAMPLE_WHATAB" : [
	["scm/docker/Dockerfile_whatab", "project/Dockerfile"]
	,["scm/whatap_agent_${stg/prd}", "project/whatap_agent"]
]
```

### 2. Whatap 관련 복사 파일 설명

![[Pasted image 20260202170224.png]]

**핵심파일 3가지**
- paramkey.txt (최초 현행유지)

- whatab.agent (Java 프로젝트에 필요 -> Dockerfile 내용에 이어짐)

- whatap.conf

	- 해당 파일에서 변수값 확인 필요

	- license=x245s45s4s54s54s5s45s (세팅값 확인)

	- whatap.server.host=10.100.0.22 (설치형일때 서버 hostip)

### 3. Whatap Dockerfile 빌드파일 내용설명

**Dockerfile**

Whatab관련 주요 소스라인

(와탭 홈설정)

- ENV WHATAP_HOME /app

(와탭 에이전트를 프로젝트 <-> 프로젝트 홈디렉토리로 copy)

- COPY ./whatap_agent/. /app/

(javaagent로 앱 실행)

- 1. Java 실행 시 Whatap agent를 먼저 로딩 (-javaagent)

- 2. 스프링부트 jar 실행 방식 뒤 -> -DX-APP-NAME=${PRJ_NMAE} 위치가 -jar뒤라서 해당 변수부터는 애플리케이션 argument로 전달

- 3. 재정리 (JVM 시스템 프로퍼티 x) , (*프로그램 인자 o*) / JVM 시스템 프로퍼티의 의도라면 -jar 앞에 배치
  
```
ENTRYPOINT java -javaagent:${WHATAP_HOME}/whatap.agent-2.2.67.jar -Dwhatap.oname=${PRJ_TARGET} --add-opens=java.base/java.lang=ALL-UNNAMED ${JAVA_OPTS} -jar /app/${APP_NAME} -DX-APP-NAME=${PRJ_NAME}
```

*dockerfile 전체*

```
FROM bbb.azurecr.io/aaa-backend/openjdk:17-jdk-alpine

ARG PRJ_NAME=${PRJ_NAME:-app}
ARG FILE_EXT=jar
ARG JAVA_OPTS_MEM=${JAVA_OPTS_MEM}
ARG TZ="Asia/Seoul"

ENV APP_NAME app.${FILE_EXT:-jar}

RUN echo prj_name ${PRJ_NAME} app_name ${APP_NAME} file_ext ${FILE_EXT} FILE_EXT:-jar ${FILE_EXT:-jar}

ENV JAVA_OPTS -Djava.security.egd=file:/dev/./urandom -Djava.awt.headless=true -Dfile.encoding=UTF-8 -Dsun.net.inetaddr.ttl=0 -Duser.timezone=${TZ} -Dlog4j2.formatMsgNoLookups=true \
              -server ${JAVA_OPTS_MEM} \
              -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/heapdump.bin \
              -XX:NewSize=256m -XX:MaxNewSize=512m -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m -XX:+DisableExplicitGC

ENV WHATAP_HOME /app

RUN apk update && apk add --no-cache fontconfig ttf-dejavu
RUN addgroup appuser
RUN adduser -G appuser appuser -H --disabled-password
USER appuser

EXPOSE 80

VOLUME /tmp

WORKDIR /
RUN if [ -d "./lgdacom" ]; then cp -r ./lgdacom /lgdacom; fi

# Whatap 설치
USER root
RUN mkdir /app
WORKDIR /app

COPY target/app.${FILE_EXT:-jar} app.${FILE_EXT:-jar}
COPY ./whatap_agent/. /app/

RUN chown -R appuser /app
USER appuser

ENTRYPOINT java -javaagent:${WHATAP_HOME}/whatap.agent-2.2.67.jar -Dwhatap.oname=${PRJ_TARGET} --add-opens=java.base/java.lang=ALL-UNNAMED ${JAVA_OPTS} -jar /app/${APP_NAME} -DX-APP-NAME=${PRJ_NAME}
```