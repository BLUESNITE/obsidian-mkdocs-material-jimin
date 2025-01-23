> [!NOTE] 히스토리
> Nextjs 언어 프로젝트의 CDN을 구성하기 위해서 구성한 docker 이미지를 가지고 젠킨스에서 .next 폴더를 FTP 업로드 하기 위해서 다음의 내용을 구성 진행해보았습니다. 아래 내용은 그 기록물입니다.

#### Jenkins에 Plugins 설치하기 
[publish-over-ftp 링크](https://plugins.jenkins.io/publish-over-ftp/ "publish-over-ftp 링크")

젠킨스 파이프라인에서 FTP 파일 업로드를 수행하기 위해서 플러그인 `Publish Over FTP` 를 설치 진행합니다.

![[Pasted image 20250123095218.png]]

설치가 완료되었다면 구성해야할 내용이 한가지 있습니다.

1. System FTP Sever 내용 작성

우선 FTP Server에 작성해주어야 할 내용은 아래 이미지와 같고,
이때 `Name` 항목이 파이프라인에서 사용됩니다.
이외 다른 항목들을 모두 기입후 우측 하단의 `Test Configuration` 버튼으로 연결확인을 할 수 있습니다.

![[Pasted image 20250123095442.png]]

#### Groovy 파이프라인 소스 작성하기

> 작성 내용

```
dir("/var/jenkins_home/mnt/${APP_NAME}-next-${PRJ_TARGET}") {
    script {
        ftpPublisher alwaysPublishFromMaster: true,
        continueOnError: false,
        failOnError: false,
        publishers: [
            [
                configName: "ftp-(Jenkins에서 설정한 FTP 서버 이름)",  // 이 항목이 위에서 Name
                transfers: [
                    [
                        asciiMode: false,          // 바이너리 모드로 업로드
                        cleanRemote: true,      // 업로드 전에 기존 파일 삭제 안 함 
                        excludes: '',                // 제외할 파일 없음
                        flatten: false,              // 디렉터리 구조 유지
                        makeEmptyDirs: true, // 빈 디렉터리 생성 안 함
                        noDefaultExcludes: false, // 기본 제외 규칙 사용
                        patternSeparator: '[, ]+', // 파일 패턴 구분자
                        remoteDirectory: '/',        // FTP 서버 업로드 경로
                        remoteDirectorySDF: false, // 날짜별 디렉터리 생성 안 함
                        removePrefix: '',                // 경로에서 제거할 접두사 없음
                        sourceFiles: '**/*'             // 업로드할 파일 경로 또는 파일명 명시
                    ]
                ],
                usePromotionTimestamp: false,
                useWorkspaceInPromotion: false,
                verbose: true
            ]
        ]
    }
}
```

*동작 요약*
1
1. Jenkins는 dir() 디렉터리로 이동
2. 해당 디렉터리의 모든 파일(/)을 FTP 서버에 업로드
3. 업로드 전에 cleanRemote: true로 FTP 경로(/)의 모든 파일을 삭제

___

위와 같이 젠킨스에 플러그인을 설치하고, 파이프라인을 작성함으로써 FTP 파일 업로드 구성이 완성됩니다.