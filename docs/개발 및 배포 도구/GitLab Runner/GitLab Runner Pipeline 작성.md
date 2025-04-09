> [!NOTE] Pipeline을 원활히 작성하기 위해 옵션들을 파악분석

```
(- Docker Executor를 사용하는 경우, 실행 환경 컨테이너 이미지를 지정.)
image: alpine:latest

(- 파이프라인 단계(순서) 정의)
stages:
  - build #1단계
  - test #2단계
  - deploy #3단계

(- Job build 이름은 반드시 stages:에서 정의된 이름 중 하나여야 함.)
build_job:1
  stage: build
  (- 실제로 실행할 쉘 명령어 리스트)
  script:
    - echo "🔨 빌드 중입니다"

test_job:
  stage: test
  script:
    - echo "🧪 테스트 수행 중입니다"

deploy_job:
  stage: deploy
  script:
    - echo "🚀 배포 시작합니다"
  (- Job이 언제 실행될지를 제어.)
  when: manual
```

*stages*

고정된 설정으로 가는 것이 아니라 stages 구성에 필요한 단계를 업무 프로세스에 맞추어
작성하여 적용하면됨

예시
- prepare 초기 준비 작업 (환경 세팅 등)
- build 코드 컴파일, 빌드
- lint 코드 정적 분석, 스타일 검사
- package 빌드 결과 패키징 (zip, jar 등)
- deploy 서버 배포, 컨테이너 배포 등
- cleanup 작업 후 임시 파일 제거 등 정리 단계

*when*

- on_success 이전 단계가 **성공했을 때** 실행 (기본값)
- on_failure 이전 단계가 **실패했을 때만** 실행
- always 이전 단계 결과와 관계없이 **항상 실행**
- 사용자가 **수동으로 버튼을 눌러야 실행**
- **지연된 시간 이후 자동 실행** (start_in: 필요)
- 이 Job을 **절대 실행하지 않음** (rules 등과 조합됨)


*only: / except (Deprecated): 또는 rules (권장)*

main 브랜치에서만 실행

```
job1:
  script: echo "main 브랜치에서만 실행"
  only:
    - main
```

main 브랜치만 제외

```
job2:
  script: echo "main 브랜치에서 제외"
  except:
    - main
```

태그에서만 실행 브랜치는 제외

```
job3:
  script: echo "태그에서만 실행하고, 브랜치는 제외"
  only:
    - tags
  except:
    - branches
```

rules:는 if: 문법을 통해 더 유연하고 논리적인 조건 분기를 지원

브랜치에 따라 실행케이스 정의

```
job1:
  script: echo "브랜치에 따라 다르게 실행"
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: always
    - if: '$CI_COMMIT_BRANCH == "develop"'
      when: manual
    - when: never
```

옵션
- if: 조건식 ($CI_* 환경 변수 사용)
- when: always, never, manual, delayed
- start_in: when: delayed일 때만 사용
- changes: 특정 파일/경로 변경 여부 조건
- exists: 파일 존재 여부 조건
- allow_failure: 실패해도 파이프라인은 성공으로 간주

특정 파일이 수정되었을때 실행

```
job_doc:
  script: echo "문서 파일 수정 시 실행"
  rules:
    - changes:
        - docs/**/*  # docs 디렉토리 안 파일들
```

특정 파일이 존재할때 실행

```
job_exists:
  script: echo "특정 파일이 있을 때 실행"
  rules:
    - exists:
        - deploy/config.yml
```

특정 커밋 메세지를 분석하여 실행

```
run_job:
  stage: test
  script:
    - echo "🚀 main 브랜치에서 커밋 메시지가 'run'으로 시작할 때 실행됨"
  rules:
    - if: '$CI_COMMIT_BRANCH == "main" && $CI_COMMIT_MESSAGE =~ /^run.*/'
      when: always
    - when: never
```

```
stages:
  - deploy

image: alpine:latest

before_script:
  - apk add --no-cache openssh

deploy-txt-files:
  stage: deploy
  tags:
    - runners-runners-project
  variables:
    GIT_STRATEGY: none
  rules:
    - if: '$CI_COMMIT_BRANCH == "main" && $CI_COMMIT_MESSAGE =~ /^run.*/'
      exists:
        - word.txt
      when: always
    - when: never
  script:
    - echo "🔐 SSH 키 구성 중..."
    - mkdir -p ~/.ssh
    - echo "$EC2_SSH_KEY" > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa

    - echo "📦 .txt 파일 목록 확인:"
    - ls -l *.txt || echo "전송할 .txt 파일이 없습니다."

    - echo "🚀 EC2 서버로 .txt 파일 전송 중..."
    - for file in *.txt; do
        [ -f "$file" ] || continue
        echo "   ▶ $file 전송 중...";
        scp -o StrictHostKeyChecking=no "$file" "$EC2_HOST:$EC2_PATH";
      done

    - echo "✅ 전송 완료"
```