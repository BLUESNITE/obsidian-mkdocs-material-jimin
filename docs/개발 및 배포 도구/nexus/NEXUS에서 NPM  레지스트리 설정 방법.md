> [!NOTE] Nexus NPM 설정기
> NPM 패키지 관리를 하기 위한 Nexus Repository Manager 사용 방법에 대해 소개합니다.
> Nexus는 NPM 저장소를 Hosted, Proxy, Group의 3가지 타입으로 분리하여 관리 할 수 있도록 지원하고 있습니다. 이를 통해서 내부 패키지를 직접 배포하고 캐싱하여 엔드포인트를 제공할 수 있습니다. 아래에서 설정 방법과 적용 내용 및 기대 효과에 대해 다루어보겠습니다.

#### 1. Nexus 저장소 타입 및 설정 방법

NPM 설정을 위해 Nexus에서는 **3가지 저장소 타입**을 사용합니다. 
- Hosted
- Proxy
- Group

**Hosted 저장소 생성**
Hosted는 내부에서 직접 생성한 NPM 패키지를 저장하는 공간입니다. 내부 업무자나 CI/CD 파이프라인 등에서 배포한 패키지를 Nexus에 업로드하고 관리할 수 있습니다.

1. Nexus 접속 → Settings (톱니바퀴) → **Repositories** → Create repository
2. npm (hosted) 선택
3. 설정값 입력
   Name : x2bee-vscode-ca-plugin
   Deployment policy: **Allow redeploy**
   Blob store: default

**Proxy 저장소 생성**
Proxy 저장소는 외부 NPM 공식 레지스트리를 프록시하여 캐시합니다. 이를 통해 외부 패키지에 대한 접근성이 향상되고 네트워크 부하를 감소 시킬 수 있습니다. 

1. Nexus 접속 → Settings (톱니바퀴) → **Repositories** → Create repository
2. npm (proxy) 선택
3. 설정값 입력
   Name : x2bee-vscode-ca-plugin-proxy
   Remote storage : https://registry.npmjs.org
   Blob store : default

**Group 저장소 생성**
Group 저장소는 Hosted와 Proxy 저장소를 하나의 그룹으로 묶어주어 개발자가 단일 레지스트리 엔드포인트에 접근 할 수 있도록 그룹핑 해주는 역할을 합니다. 

1. Nexus 접속 → Settings (톱니바퀴) → **Repositories** → Create repository
2. npm (group) 선택
3. 설정값 입력
   Name : x2bee-vscode-ca-plugin-group
   Blob store : default
   Member repositories: npm-hosted, npm-proxy 순서로 추가

#### 2. NPM 클라이언트 설정 및 명령어
Nexus에 설정한 저장소를 이용하기 위해 NPM 클라이언트 측에서 다음과 같이 CLI 명령어를 통해 수행 시킬 수 있습니다.

*로그인 및 패키지 배포*
```
npm login --registry=http://nexus-dev.x2bee.com/repository/x2bee-vscode-ca-plugin/

npm publish --registry=http://nexus-dev.x2bee.com/repository/x2bee-vscode-ca-plugin/
```

*패키지 설치*
```
npm install <your-package-name> --registry=http://nexus-dev.x2bee.com/repository/x2bee-vscode-ca-plugin-group/
```

![[Pasted image 20250415171417.png]]

이때 로그인이 안된다면 아래의 보안 설정을 수행해주어야합니다.

#### 3. 보안 관리 설정

Nexus에서는 보안관리 기능을 통해 접근 제어나 인증 토큰 정책을 설정할 수 있습니다. NPM 레지스트리의 경우 `npm Bearer Token Realm`을 적용하여 보다 안전하게 패키지를 배포하고 설치 관리할 수 있습니다.

Active 항목에 - *npm Bearer Token Realm* 적용

![[Pasted image 20250416110802.png]]

