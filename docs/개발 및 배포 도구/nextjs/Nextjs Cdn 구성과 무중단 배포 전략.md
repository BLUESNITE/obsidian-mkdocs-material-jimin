> [!NOTE] CDN 구성의 이점
> 1. 빠른 응답 속도 - 여러 서버에 콘텐츠를 배포하여 배포 지연시간을 최소화
> 2. 무중단 배포 - 정적 파일을 CDN에 저장하여 새 버전 배포 시에도 서비스가 중단 되지 않음
> 3. 서버 부하 감소 - 정적 리소스를 CDN이 제공하므로 서버 부담이 줄어듬
> 4. 캐싱 활용 - 반복 요청에 대한 응답 속도가 빨라지고 비용이 절감됨
#### Nextjs에서 CDN을 활용하는 방법
Nextjs에서는 빌드된 숨겨진 폴더 .next 폴더의 .next/static 폴더를 CDN으로 업로드하여 정적 리소스를 CDN이 대신 제공하도록 설정 할 수 있습니다.

#### CDN에 관리 하는 방법
별달리 특별한 방법이 있는건 아니고, 기본 아키텍처를 이해를 하고있어야 작업 포인트를 잡을 수가 있다.
지금 관리하고 있는 프로젝트의 아키텍처 기본 구성은 아래와 같다.

- 소스관리 깃프로젝트
- CI/CD 파이프라인 관리 젠킨스
- 배포 환경 Kubernetes
- CDN 관리 FTP로 정적 파일 배포

**젠킨스 파이프 라인에서의 구성 및 워크플로**

젠킨스 파이프라인에서 결국 이미지를 생성하게 되는데, cdn이 정상적으로 잘 유지되고 관리되기 위해서는 정적파일이 생성 이미지 전,후로 유지 관리가 될 필요가 있었다. 이에 워크플로를 아래와 같이 작성하였다.

1. Docker Image 생성 전 단계
   (.next/static 폴더를 Docker Image 기반으로 추출하여 CDN 위치에 FTP 업로드)  
2. Docker Image 생성
   (새로운 변경 사항이 반영된 Docker Image 생성)
3. Docker Image 변경 내용 업데이트
   (다시 .next/static을 Docker Image 기반으로 추출하여 CDN 위치에 FTP 업로드)
4. CDN 파일 정리
   (FTP 서버에 .next/static 누적 폴더가 3개 이상일 경우, 가장 오래된 폴더 삭제)
5. ArgoCD 동기화
   (최신 Docker Image로 ArgoCD를 통해 동기화 및 배포 진행)

*왜 이렇게 구성해야 했을까?*

Nextjs에서 정적 파일 static assets을 CDN에 설정해두면 배포하는 과정에서
무중단 배포(Zero Downtime Deployment)를 경험할 수 있다. 이를 보장하기 위해서 아래와 같은 구성 관리를 하게 된다.

위에서 설명한 워크플로에 따라 배포 되었을때 배포 전후의 디렉토리 변화를 관찰해보자.

![[Pasted image 20250204111534.png]]

배포 전 후로 변화가 관찰이 되는가?
최종 수정일자로도 판단 할 수있지만 이해하기 쉽게 변화된 디렉토리를 가지고 관찰해보자.

> 배포 전

```
/media
/css
/IQ8Z50T_DIZHGYkH8TFP7   <- (1번 폴더, 이전 이미지의 static 파일)
/szv9_kV9ybQ5J941hgj-T   <- (2번 폴더, 현재 사용 중인 이미지의 static 파일)
/chunks
```

> 배포 후

```
/media
/css
/szv9_kV9ybQ5J941hgj-T   <- (2번 폴더, 기존 유지)
/kZdP-0_4eXLBZB3MRV7ri   <- (3번 폴더, 새로운 배포 이미지의 static 파일)
/chunks
```

1번 IQ8Z50T_DIZHGYkH8TFP7
2번 szv9_kV9ybQ5J941hgj-T
3번 kZdP-0_4eXLBZB3MRV7ri

폴더 이름으로 명칭하면 어려우니 1번 2번 3번으로 명명하겠다.

1번 폴더 -> 배포 이전, 즉 이전 이미지에서 추출된 .next/static 폴더로 배포 후에 삭제됨

2번 폴더 -> 새 이미지를 생성하기 전, 현재 서비스 중인 이미지에서 추출한 .next/static 폴더로 배포 후에도 유지

3번 폴더 -> 새로운 이미지를 생성한 후 ArgoCD에 Sync 전파를 하기 전에 업로드한 폴더로 배포 후 신규 생성됨

**과정의 정리**

1. 배포 이전 이미지에서 업로드 되어 있던 정적 파일 1번 폴더
2. 현재 서비스에 이용 중인 이미지에서 업로드한 2번 폴더
3. 새로운 이미지를 생성 후 업로드한 3번 폴더
4. 이미지 정상 생성이 완료 된 후에 가장 오래된 1번 폴더 제거
5. Argocd를 통해 새로운 배포 이미지로 전환
6. 사용자는 무중단으로 최신 정적 리소스를 지속해서 제공받음

이와 같은 과정으로 인하여 기존 정적파일을 유지하면서 새로운 변경사항을 업데이트 하는 무중단 배포 파이프 라인이 구성.

#### Nextjs에 설정 하는 방법
next.config.js에서 assetPrefix 설정하면 되는데 이 부분은 Nextjs 에서 너무 친절히 가이드를 해주고 있어서 별도에 설명을 생략하고 링크를 남겨둠

https://nextjs.org/docs/app/api-reference/config/next-config-js/assetPrefix#set-up-a-cdn

#### 파이프라인에서의 구성
Nextjs 어플리케이션에서 .next/static 폴더를 언제 어떻게 접근하여 CDN으로 정적 리소스 관리를 할 수 있을지 고민이었다. 특히 ... CI/CD 파이프라인에서 어느 시점에서 올려서 관리하는 것이 best practice 일지 너무나 고민이 되었는데 특히 .next/static 폴더를 추출하여 업로드/배포 하는 사례를 찾기 어려웠다. 

파이프라인 소스를 살펴보다가 Docker 이미지 자체를 사용하는게 어떨가 하는 생각이 들었다.
이때 궁금했던 점 한가지가 있다.

Docker Image 속에 있는 .next 폴더 내용은 계속해서 바뀔까? 바뀌지 않을까? Kubernetes Pod에도 똑같은 내용으로 똑같이 다 적용이 되기는 하는 걸까 ...

도커 컨테이너와 쿠버네티스 컨테이너에서 우선 검증을 진행해 보았다.

Nexus에서 확인한 `docker pull x2bee-backend/<fo_project>:latest` Pull 받아 Create해서 폴더를 확인하고,

Kubernestes Pod에 접속해서도 확인해보았다. 

CLI 로 직접 확인하는 것이 가장 속이 시원하다.

아래는 kubernetes Pod에서의 확인 내용이다.

보면 .next 폴더는 숨겨져있어서 보이지 않는다 그냥 cd .next

![[Pasted image 20250204130018.png]]

이어서 static 폴더안을 확인해보면 아래와 같이 확인이 가능하다

![[Pasted image 20250204131032.png]]

여기에서 폴더명도 기타 정보도 동일한 이미지를 사용했을때 같은 내용으로 Pod 및 컨테이너가 생성되는 것을 확인 해 볼 수있다.

이를 기반으로 정적 리소스를 추출하여 CDN에 올리면 무중단이 되겠다는 감이 왔다.

**파이프라인 Groovy 스크립트**

docker image를 통해서 정적 리소스를 파이프라인 스크립트에서 추출하는 방법은 아래와 같다.

특히 docker cp 명령어를 사용하면 굉장히 쉽다.

아래와 같이 public 및 .next/static 두 정적 리소스 폴더들을 복사한 후 FTP 파일 업로드 진행한다.

```
docker create --name temp-container ${DOCKER_IMAGE_NAME}:latest

docker cp temp-container:/app/public /var/jenkins_home/mnt/${APP_NAME}/
docker cp temp-container:/app/.next/static /var/jenkins_home/mnt/${APP_NAME}/_next/
```

이를 통해서 Nextjs 정적 리소스를 효율적으로 관리 무중단 배포를 완성 시킬 수 있었다.

마지막으로 여유가 된다면 아래의 다른 구현 방법들도 시도해봤으면 좋겠다. 

- 쿠버네티스 PV
- AWS S3
- Docker 볼륨으로 마운트
- 기타 스토리지

