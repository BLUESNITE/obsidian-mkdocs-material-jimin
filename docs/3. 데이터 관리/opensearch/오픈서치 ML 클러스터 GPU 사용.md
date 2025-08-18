> [!NOTE] ML 클러스터를 사용하고 싶어서 진행한 내용

### 1. 오픈서치에서의 자료

[GPU 가속](https://docs.opensearch.org/latest/ml-commons-plugin/gpu-acceleration/ "GPU 가속") , [what-in-the-ml](https://opensearch.org/blog/what-in-the-ml-is-going-on-around-here/ "what-in-the-ml")

오픈서치 내에서 ML 모델 사용으로 GPU 가속이라고 번역된 페이지의 내용을 읽어보면.
상당히 어렵고. 감을 잡기가 별따기 수준이다.


나름의 해석을 하자면 아래와 같다

**지원되는 이미지**

   => You can use GPU acceleration with both [Docker images](https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/supported-tags.md) with CUDA 11.6 and [Amazon Machine Images (AMIs)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html)

```  
=> (구글 번역) 모두에서 GPU 가속을 사용할 수 있습니다 CUDA 11.6을 사용한 Docker 이미지와 Amazon Machine Image(AMI)
   
=> (GPT 번역) CUDA 11.6이 포함된 Docker 이미지와 Amazon 머신 이미지(AMI) 모두에서 GPU 가속을 사용할 수 있습니다.
```

위와 같이 글번역 & 원문 해석이 되는데 이걸 알아먹을 턱이있나 ... 삽질을 다하고 나서야 알았다

```
=> 오픈서치 Docker Image 지는 CUDA 11.6 이랑 호환되게 작성되어 있으니 (CUDA 버전을 꼭 맞춰라)
```

사실 이모저모의 경험으로 처음부터 CUDA를 맞춰야하는거 아닌가 하는 의심은 백번도 더 들었는데.

내 CUDA를 오픈서치 도커이미지에 맞추는 건 너무 불편하고 어려운 일이다 또한 ML 모델 등에서 어떤 CUDA 버전을 원하는지 알고 함부로 하겠나 ...

### 2. 해서 해본 방법

1) 오픈서치 커뮤니티 파헤치기

2) 오픈서치 슬랙 커뮤니티 들어가서 채팅기록보기

3) 오픈서치 구글 네이버 챗지피티 제미나이 클로드 그록한테 물어보기

4) 도커 허브에서 오픈서치 이미지 죄다 찾아서 보기

*결국 위 항목을 싹다 해봤는데 결국은 커뮤니티가 답이었다*

[오픈서치 커뮤니티의 왕자](https://forum.opensearch.org/u/pablo/summary "오픈서치 커뮤니티의 왕자")

![[Pasted image 20250814151219.png]]

그는 오픈서치의 신이다.

그가 알려준 글 [자료 글](https://forum.opensearch.org/t/gpu-acceleration-not-working-on-gcp-gke-gpus/26177/3/ "자료 글")

해당 링크에서 댓글을 읽어보면 이걸 적용했습니다 ~ 라고 하며 도커파일을 하나 던져주었다

내심 왜이렇게 불친절하지 하면서도 지푸라기 태우는 심정으로 내용을 살펴보니

cuda12.4로 내가 딱 원하는 버전 이고 캡쳐 이미지 또한 인식된게 보였다

![[Pasted image 20250814151500.png]]

#### 3. 오픈서치 ML 클러스터 구성 및 CUDA12.4

여기부터 본격 적용내용이다.

**파일 목록**

```
opensearch-ml-compose.yaml 도커컴포즈파일
Dockerfile 도커파일
opensearch-onetime-setup.sh 도커파일에서 실행하는 스크립트
djl_cache 빈 디렉터리
```

*내용은 소스와 함께 설명*

opensearch-ml-compose.yaml

```
version: "3.9"

x-opensearch-env: &opensearch-env
  # OpenSearch 기본 환경 변수
  cluster.name: opensearch-cluster
  bootstrap.memory_lock: "true" # 메모리를 잠가 스왑을 피합니다
  OPENSEARCH_INITIAL_ADMIN_PASSWORD: "Xxxxxxxxxxx!1"

  # 보안 비활성
  plugins.security.ssl.http.enabled: false
  plugins.security.ssl.transport.enabled: false
  plugins.security.disabled: true

  # ML 작업은 ML 노드에서만
  plugins.ml_commons.only_run_on_ml_node: "true"

  # JVM 메모리 , - DJL 기본 엔진을 PyTorch로 지정 (가능하면 GPU를 우선 선택)(중요)
  OPENSEARCH_JAVA_OPTS: "-Xms8g -Xmx8g -Dai.djl.default_engine=PyTorch"

services:
  opensearch-ml-gpu:
    # === 이미지 빌드 ===
    build:
      context: .                # 위 Dockerfile이 있는 디렉터리
      dockerfile: Dockerfile
      args:
        OS_VER: "3.1.0"         # OpenSearch 버전
        PYTORCH_VERSION: "2.5.1"  # pytorch/pytorch 태그 앞부분 (예: 2.5.1)
    image: opensearch-ml-gpu:3.1.0-torch2.5.1-cu124
    container_name: opensearch-ml-gpu

    # === GPU 할당 (Docker Engine 19.03+ / NVIDIA Container Toolkit 필요) ===
    gpus:
      - device_ids: ["0"]         # 0번 GPU 고정
        capabilities: [gpu]
    environment:
      <<: *opensearch-env
      node.name: opensearch-ml1
      node.roles: '["ml"]'

      # 아래 내용은 나의 내부 서버 정보 (hostMain, hostMain 정의내용은 extra_hosts에 있다)
      discovery.seed_hosts: "hostMain:9301,hostMain:9310"
      network.publish_host: "192.168.2.243"

      # NVIDIA 런타임 힌트 (선택)
      NVIDIA_VISIBLE_DEVICES: "all"
      NVIDIA_DRIVER_CAPABILITIES: "compute,utility"

    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536

    volumes:
      - os-ml-data:/usr/share/opensearch/data
      - ./djl_cache:/usr/share/opensearch/data/djl_cache # DJL 엔진/모델 캐시 공유

    ports:
      - "9200:9200"   # REST
      - "9300:9300"   # transport
      - "9600:9600"   # performance analyzer
      - "9650:9650"   # (필요 시) ML 관련 포트

    extra_hosts:
      - "hostMain:192.168.2.171"
      - "hostGPU1:192.168.2.243"

    healthcheck: # healthcheck 실패시 자동재실행
      test: ["CMD", "bash", "-lc", "curl -fsS http://localhost:9200 >/dev/null || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 30s
    restart: unless-stopped

volumes:
  os-ml-data:
```

Dockerfile

```
###################
# ---- build-time arguments you’ll most likely tweak --------------------------
# ---- 빌드할때 자주 바꿀 인자들
###################
ARG OS_VER                          # target OpenSearch release / 오픈서치 버전
ARG PYTORCH_VERSION         # target PyTorch release (GPU build) / PyTorch 버전 (빌드용)


###################
# ---- stage 1: pull the official OpenSearch binary bundle --------------------
# ---- 공식 오픈서치 번들 가져오기
###################
FROM public.ecr.aws/opensearchproject/opensearch:${OS_VER} AS source


###################
# ---- stage 2: CUDA / PyTorch runtime image ----------------------------------
# ---- CUDA PyTorch 실행 이미지
###################
# Pick a pytorch/pytorch tag that matches the torch version *and*
# a CUDA toolchain you have on the host.  CUDA 12.1 + cuDNN 8 works well
# with recent nvidia-driver 535+.
# 호환에 맞는 PyTorch 버전에다가 호스트에 설치된 CUDA 툴체인까지 호환되는 태그를 찾아 적용
# NVIDIA 드라이버 535+ 환경에서는 CUDA12.1+cuDNN 8 조합이 좋음
# 여기서는 cuda12.4 + cuDNN9 (조합사용)
FROM pytorch/pytorch:${PYTORCH_VERSION}-cuda12.4-cudnn9-devel


###################
# ---- basic OS / user setup --------------------------------------------------
# ---- 사용자 설정
###################
ARG UID=1000
ARG GID=1000
ARG OPENSEARCH_HOME=/usr/share/opensearch

RUN addgroup --gid ${GID} opensearch \
 && adduser  --uid ${UID} --gid ${GID} --home ${OPENSEARCH_HOME} opensearch


###################
# ---- Python extras you need in the container --------------------------------
# ---- 컨테이너에서 필요한 Python을 추가
###################
# transformers ≥ 4.41 works with Torch 2.7; pin if you like
# transformers 4.41 이상은 Torch 2.7과 호환
RUN pip install --no-cache-dir transformers


###################
# ---- install OS-level dependencies (e.g., curl) -----------------------------
# ---- OS 레벨 의존성에 기타등등 설치
###################
USER root

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*


###################
# ---- copy the OpenSearch distribution from the helper stage -----------------
# ---- 헬퍼 단계에서 OpenSearch 배포본을 복사
###################
COPY --from=source --chown=${UID}:${GID} ${OPENSEARCH_HOME} ${OPENSEARCH_HOME}
WORKDIR ${OPENSEARCH_HOME}


###################
# ---- expose Java & OpenSearch CLI on the default PATH -----------------------
# ---- 기본 PATH에 JAVA랑 오픈서치 CLI를 노출
###################
# The tarball still ships its own JDK (now version 21).  Keep the same layout.
# 오픈서치 배포본 기본 자바 버전인 21을 유지
RUN echo "export JAVA_HOME=${OPENSEARCH_HOME}/jdk"             >  /etc/profile.d/java_home.sh \
 && echo "export PATH=\$PATH:\$JAVA_HOME/bin"                 >> /etc/profile.d/java_home.sh

ENV JAVA_HOME=${OPENSEARCH_HOME}/jdk
ENV PATH=$PATH:${JAVA_HOME}/bin:${OPENSEARCH_HOME}/bin

# k-NN native library path (needed for FAISS / cuVS)
# k-NN 플러그인 네이티브 라이브러리 경로를 LD_LIBRARY_PATH에 추가
ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${OPENSEARCH_HOME}/plugins/opensearch-knn/lib"


###################
# ---- switch to non-root, perform one-time setup, keep optional flags --------
# ---- root 사용자가 아닌것으로 전환해서 1회성 설정을 수행
###################
USER ${UID}

# • Disable the demo security configuration during the image build
# 이미지 빌드 시점에 데모 보안 설정 설치를 비활성화 가능
# • Leave the security plugin in place (default) so you can choose at runtime
# 보안 플러그인은 그대로 두고 DISABLE_SECURITY_PLUGIN만 비활성화 가능
#   whether to disable it with `DISABLE_SECURITY_PLUGIN=true`

#ARG DISABLE_INSTALL_DEMO_CONFIG=true
#ARG DISABLE_SECURITY_PLUGIN=false
#(중요) 오픈서치 설치시 초기 비밀번호 필수
ARG OPENSEARCH_INITIAL_ADMIN_PASSWORD=Xxxxxxxxxxx!1

#(중요) 아래에서 따로 설명
RUN ./opensearch-onetime-setup.sh


###################
# ---- network ports ----------------------------------------------------------
# ---- 설정 포트
###################
EXPOSE 9200 9300 9600 9650


###################
# ---- metadata & start-up ----------------------------------------------------
# ---- 메타데이터 시작 설정
###################
ARG BUILD_DATE
ARG NOTES
LABEL org.opencontainers.image.created=$BUILD_DATE \
      org.opencontainers.image.version=$OS_VER \
      org.opencontainers.image.description="OpenSearch ${OS_VER} with PyTorch ${PYTORCH_VERSION} GPU runtime" \
      org.opencontainers.image.notes="$NOTES"

ENTRYPOINT ["./opensearch-docker-entrypoint.sh"]
CMD ["opensearch"]
```

[opensearch-onetime-setup.sh](https://github.com/opensearch-project/docker-images/blob/main/2.x/bin/opensearch-onetime-setup.sh "opensearch-onetime-setup.sh")

이제 마지막 파일이다. 해당파일은 링크에서 별도로 찾아서 배껴적었다.

```
#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
# 이 파일에 대한 기여는 Apache-2.0 또는 호환되는 오픈소스 라이선스로 제공되어야 합니다.

# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
# 이 스크립트는 OpenSearch tarball 배포판을 위한 1회성 초기 설정을 수행합니다.
# 데모 보안 설정을 설치하고 Performance Analyzer(성능 분석기) 를 설정합니다.

# This script performs one-time setup for the OpenSearch tarball distribution.
# It installs a demo security config and sets up the performance analyzer

export OPENSEARCH_HOME=`dirname $(realpath $0)`
export OPENSEARCH_PATH_CONF=$OPENSEARCH_HOME/config
cd $OPENSEARCH_HOME

# DISABLE_INSTALL_DEMO_CONFIG 값이 true가 아닌 경우, 데모 보안 구성 설치 스크립트(install_demo_configuration.sh)를 실행합니다.

# DISABLE_SECURITY_PLUGIN 값이 true이면 opensearch.yml에 plugins.security.disabled: true를 기록하여 보안 플러그인을 비활성화합니다. 그렇지 않으면(기본) 활성 상태로 둡니다.

##Security Plugin
SECURITY_PLUGIN="opensearch-security"
if [ -d "$OPENSEARCH_HOME/plugins/$SECURITY_PLUGIN" ]; then
    if [ "$DISABLE_INSTALL_DEMO_CONFIG" = "true" ]; then
        echo "Disabling execution of install_demo_configuration.sh for OpenSearch Security Plugin"
    else
        echo "Enabling execution of install_demo_configuration.sh for OpenSearch Security Plugin"
        bash $OPENSEARCH_HOME/plugins/$SECURITY_PLUGIN/tools/install_demo_configuration.sh -y -i -s
    fi

    if [ "$DISABLE_SECURITY_PLUGIN" = "true" ]; then
        echo "Disabling OpenSearch Security Plugin"
        sed -i '/plugins.security.disabled/d' $OPENSEARCH_PATH_CONF/opensearch.yml
        echo "plugins.security.disabled: true" >> $OPENSEARCH_PATH_CONF/opensearch.yml
    else
        echo "Enabling OpenSearch Security Plugin"
        sed -i '/plugins.security.disabled/d' $OPENSEARCH_PATH_CONF/opensearch.yml
    fi
fi

## Perf Plugin
## 성능 플러그인
PA_PLUGIN="opensearch-performance-analyzer"

# opensearch-performance-analyzer 플러그인 구동에 필요한 JVM 옵션 블록이 config/jvm.options에 없으면 다음 항목을 추가합니다

# OpenDistro Performance Analyzer (주석 라벨)
# Dclk.tck=<시스템 클럭 틱>
# Djdk.attach.allowAttachSelf=true
# Djava.security.policy=<성능 분석기용 보안 정책 파일 경로>
# add-opens=jdk.attach/sun.tools.attach=ALL-UNNAMED

if ! grep -q '## OpenDistro Performance Analyzer' $OPENSEARCH_PATH_CONF/jvm.options; then
   CLK_TCK=`/usr/bin/getconf CLK_TCK`
   echo >> $OPENSEARCH_PATH_CONF/jvm.options
   echo '## OpenDistro Performance Analyzer' >> $OPENSEARCH_PATH_CONF/jvm.options
   echo "-Dclk.tck=$CLK_TCK" >> $OPENSEARCH_PATH_CONF/jvm.options
   echo "-Djdk.attach.allowAttachSelf=true" >> $OPENSEARCH_PATH_CONF/jvm.options
   echo "-Djava.security.policy=$OPENSEARCH_PATH_CONF/$PA_PLUGIN/opensearch_security.policy" >> $OPENSEARCH_PATH_CONF/jvm.options
   echo "--add-opens=jdk.attach/sun.tools.attach=ALL-UNNAMED" >> $OPENSEARCH_PATH_CONF/jvm.options
fi
```

**위 3가지 파일 요약 설명**

오픈서치 사이트에서 확인 되었듯이 CUDA 버전을 호스트 환경에 맞추려면 opensearch 이미지를 기준으로 순정 바이너리 파일들을 복사하여 런타임 베이스가 되는 pytorch cuda에 세팅 진행해야한다

런타임 pytorch cuda 이미지에 오픈서치 세팅시 사용자 및 HOME 디렉토리 그리고 필요로하는 파이선 패키지 등을 복사이동하고 런타임 1회성 스크립트를 실행 시킵시다

#### 4. 오픈서치 GPU 사용 모니터링

이전에 찾았던 venv 활성화와 모니터링 실행 커맨드

```
source ~/venv-gpu/bin/activate
nvitop
```

*오픈서치에서 java로 GPU 사용 확인*

![[Pasted image 20250814161156.png]]

