> [!NOTE] 도커 fluentbit 컨테이너 이미지를 활용한 로그 관리 수집 그리고 opensearch 연동

> [!CHECK] Fluent Bit (이미지) : 
> C 언어로 만들어진 초경량 버전입니다. OpenSearch를 포함한 주요 플러그인들이 내장(built-in)되어 있어 별도의 설치가 필요 없습니다. 또한, 경량화를 위해 쉘(`sh`)이나 `gem` 같은 도구가 이미지 안에 포함되어 있지 않습니다.

#### 1. 기본 설치
Fluent Bit은 경량화된 로그 수집기입니다. 우리는 Docker 컨테이너에서 수집되는 로그를 Opensearch에 전달하는 형태로 사용합니다. 아래는 Docker compose 파일과 fluent-bit.conf 파일에 내용을 구성하고 Opensearch로 로그를 전송하도록 구성한 기본예시입니다.

**fluentbit-compose.yaml**

- image : 컨테이너 내부에서 여러가지를 확인하기위해 debug 이미지를 사용했습니다.
- network_mode : 호스트 네트워크를 사용합니다 (24224)

```
services:
  fluent-bit:
    image: fluent/fluent-bit:4.0.3-debug
    container_name: fluent-bit
	network_mode: host
    volumes:
      - ./fluent-bit.conf:/fluent-bit/etc/fluent-bit.conf
    restart: unless-stopped
```

**fluent-bit.conf**

fluent-bit 구성은 대표적으로 [SERVICE] , [INPUT], [OUTPUT] 으로 이루어집니다.

- SERVICE : 로그 레벨과 로그의 수집/전송 주기 그리고 포그라운드(Docker에서 off 필수) 실행 여부 설정
- INPUT : 수신위치와 프로토콜 그리고 포트를 설정
- OUTPUT : Match를 통해서 태그와 일치하는 로그를 전송 설정하고 Opensearch 인증조건을 작성

> [!TIP] 도커 컨테이너 생성 예시
> `docker run -d --network host --name ${DOCKER_CONTAINER_NAME} --log-driver=fluentd --log-opt tag=${DOCKER_CONTAINER_NAME} --log-opt fluentd-address=127.0.0.1:24224 ${DOCKER_IMAGE_NAME}:latest`

```
########################################
# SERVICE
########################################
[SERVICE]
    Flush        1
    Log_Level    info
    Daemon        Off
########################################
# INPUTS (Project Specific)
########################################
[INPUT]
    Name          forward
    Listen        0.0.0.0
    Port          24224

########################################
# OUTPUTS (Project Specific)
########################################
[OUTPUT]
    Name         opensearch
    Match        aurora-x2bee-api-common_stg.logs
    Index        x2bee-api-common-%Y.%m.%d
    Host         opensearch-stg.x2bee.com
    Port         443
    TLS          On
    TLS.Verify   Off
    HTTP_User    admin
    HTTP_Passwd  **************
    Suppress_Type_Name On
    Logstash_Format Off

########################################
# ---- 반복 생략 ----
########################################
[OUTPUT]
    Name         opensearch
    Match        aurora-x2bee-api-bo_stg.logs
    Index        x2bee-api-bo-%Y.%m.%d
    Host         opensearch-stg.x2bee.com
    Port         443
    TLS          On
    TLS.Verify   Off
    HTTP_User    admin
    HTTP_Passwd  **************
    Suppress_Type_Name On
    Logstash_Format Off
########################################
# ---- 반복 생략 ----
########################################
```

#### 2. Lua 스크립트로 FILTER 설정

반복되는 Output 구성을 해야하는 경우가 생긴다면 Lua 스크립트를 작성하여 효과적인 구성을 할 수 있습니다.

**fluentbit-compose.yaml**

```
services:
  fluent-bit:
    image: fluent/fluent-bit:4.0.3-debug
    container_name: fluent-bit
    network_mode: host
    volumes:
      - ./fluent-bit.conf:/fluent-bit/etc/fluent-bit.conf
      - ./extract_tag.lua:/fluent-bit/etc/extract_tag.lua
    restart: unless-stopped
```

**extract_tag.lua**

- string.match(...) : 정규표현식을 통해 aurora-와 stg.logs 사이의 서비스명을 추출
- record["log_index_prefix"] : 추출된 값을 로그 레코드의 필드로 삽입

```
function cb_extract_tag(tag, timestamp, record)
    record["log_index_prefix"] = string.match(tag, "^aurora%-(.-)_stg%.logs$")
    return 1, timestamp, record
end
```

**fluent-bit.conf**

- SERVICE에 Lua 스크립트 필터 파일 등록
- 태그에서 서비스명 추출하여 log_index_prefix 필드 삽입
- log_index_prefix 필드를 기반으로 OpenSearch Index 구성 
  *(Logstash_Prefix_Key log_index_prefix)*

```
[SERVICE]
    Flush        1
    Log_Level    info
    Daemon       Off
    Lua_File     extract_tag.lua

[INPUT]
    Name         forward
    Listen       0.0.0.0
    Port         24224

# STEP 1: tag → record["log_index_prefix"]
[FILTER]
    Name         lua
    Match        aurora-x2bee-*_stg.logs
    script       extract_tag.lua
    call         cb_extract_tag

# STEP 2: OpenSearch에 log_index_prefix를 prefix로 사용
[OUTPUT]
    Name                opensearch
    Match               aurora-x2bee-*_stg.logs
    Host                opensearch-stg.x2bee.com
    Port                443
    TLS                 On
    TLS.Verify          Off
    HTTP_User           admin
    HTTP_Passwd         ************
    Suppress_Type_Name  On
    Logstash_Format     On
    Logstash_Prefix_Key log_index_prefix
    Logstash_DateFormat %Y.%m.%d
    Retry_Limit         5

# fallback
[OUTPUT]
    Name    stdout
    Match   *
```

#### 3. Opensearch에서 확인하기

**Dev Tools에서 확인**

`GET _cat/indices?s=index`

![[Pasted image 20250709133624.png]]