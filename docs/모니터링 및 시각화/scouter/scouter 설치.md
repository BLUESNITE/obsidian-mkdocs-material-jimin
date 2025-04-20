> [!NOTE] Title
> Scouter는 3가지 요소가 필요하다 호스트에이전트, 자바에이전트, 클라이언트

> 서버

```shell
services:
  scouter-server:
    container_name: scouter-server
    image : scouterapm/scouter-server:2.7.0
    restart : always
    environment:
      - SC_SERVER_ID=SCCOUTER-COLLECTOR
      - NET_HTTP_SERVER_ENABLED=true
      - NET_HTTP_API_SWAGGER_ENABLED=true
      - NET_HTTP_API_ENABLED=true
      - MGR_PURGE_PROFILE_KEEP_DAYS=2
      - MGR_PURGE_XLOG_KEEP_DAYS=5
      - MGR_PURGE_COUNTER_KEEP_DAYS=15
      - JAVA_OPT=-Xms1024m -Xmx1024m
    volumes:
      - /data/scouter-data/logs:/home/scouter-server/logs
      - /data/scouter-data/sc-data:/home/scouter-server/database
    ports:
      - 6180:6180
      - 6100:6100
      - 6100:6100/udp
```

> 클라이언트

> 자바에이전트 실행

```shell
# FROM docker.dev.x2bee-tech.com/library/openjdk:17-jdk-alpine
FROM openjdk:17-jdk-alpine

ARG PRJ_NAME
ARG PRJ_LOWER
ARG FULL_APP_NAME
ARG JAVA_OPTS_MEM
ARG FILE_EXT
ARG TZ
ARG BASE_JENKINS_DIR

ENV PRJ_NAME=${PRJ_NAME}
ENV PRJ_LOWER=${PRJ_LOWER}
ENV FULL_APP_NAME=${FULL_APP_NAME}
ENV JAVA_OPTS_MEM=${JAVA_OPTS_MEM}
ENV FILE_EXT=jar
ENV TZ="Asia/Seoul"
ENV BASE_JENKINS_DIR="/var/jenkins_home/workspace/base-pipeline/scm/scouter"

ENV APP_NAME app.${FILE_EXT:-jar}
ENV JAVA_OPTS -Djava.security.egd=file:/dev/./urandom -Djava.awt.headless=true -Dfile.encoding=UTF-8 -Dsun.net.inetaddr.ttl=0 -Duser.timezone=${TZ} -Dlog4j2.formatMsgNoLookups=true \
              -server ${JAVA_OPTS_MEM} \
              -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/heapdump.bin \
              -XX:NewSize=128m -XX:MaxNewSize=256m -XX:MetaspaceSize=128m -XX:MaxMetaspaceSize=256m -XX:+DisableExplicitGC

RUN apk update && apk add --no-cache fontconfig ttf-dejavu
RUN addgroup appuser
RUN adduser -G appuser appuser -H --disabled-password

EXPOSE 80
VOLUME /tmp
WORKDIR /

# 루트 경로에 복사
COPY target/app.${FILE_EXT:-jar} app.${FILE_EXT:-jar}
COPY target/app.${FILE_EXT:-jar} /app/app.${FILE_EXT:-jar}

# scouter 설치
COPY ./scouter/. /app/

USER root
RUN chown -R appuser /app

WORKDIR /app
RUN unzip app.jar -d ./
RUN ls

USER appuser

#ENTRYPOINT java ${JAVA_OPTS} -jar /$APP_NAME
ENTRYPOINT java -javaagent:/app/agent.java/scouter-agent-java.jar -Dadd-opensjava.base/java.lang=ALL-UNNAMED -Djdk.attach.allowAttachSelf=true -Dscouter.config=/app/agent.java/conf/scouter.conf -Dobj_name=${PRJ_NAME} ${JAVA_OPTS} -jar /app/${APP_NAME}
```
