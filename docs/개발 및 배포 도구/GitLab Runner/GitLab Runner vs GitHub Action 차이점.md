> [!CHECK] GitLab Runner
> GitLab Runner는 GitLab.com (SaaS) 또는 self-hosted GitLab 인스턴스 모두와 연동될 수 있습니다.
> 
> GitLab Runner는 GitLab 8.0 (2015년 출시) 부터 사용되기 시작했습니다.
> GitLab Runner는 독립적으로 설치가능합니다.

**앞서 알아보기 GitLab Runner와 GitHub Action의 차이점**

| *항목*                   | **GitLab Runner**                                          | **GitHub Actions**                                                 |
| ---------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------ |
| *소속*                   | GitLab 제품군                                                 | GitHub 제품군                                                         |
| *CI/CD 정의 파일*          | .gitlab-ci.yml                                             | .github/workflows/*.yml                                            |
| *실행 엔진*                | GitLab Runner (별도 설치 필요)                                   | GitHub Actions Runner                                              |
| *호스팅 방식*               | Self-hosted GitLab에서는 반드시 별도 GitLab Runner 설치 필요           | GitHub Hosted Runner (기본 제공) - Self-hosted Runner도 설정 가능           |
| *Runner 설치*            | 유저가 직접 설치 및 등록 필요<br>(self-managed 경우)                     | 기본 제공되며, self-hosted도 가능                                           |
| *Runner 유형 (Executor)* | 다양: shell, docker, docker+machine, kubernetes, ssh, custom | 제한적: ubuntu-latest, windows-latest, macos-latest 또는 self-hosted 지정 |
| *종속성*                  | GitLab 서버 + Runner 필요                                      | GitHub만 있으면 작동<br>(Actions는 서버리스 구조처럼 작동)                          |
| *배포 대상 통합*             | Kubernetes, AWS, GCP, SSH, Docker 등과 통합 쉬움                 | AWS, Azure, GCP 등 다양한 공식 Action으로 통합                               |
| *CI/CD as code*        | .gitlab-ci.yml 하나로 모든 파이프라인 정의                             | 여러 .yml 파일로 워크플로우 분리 가능                                            |
| *에이전트 확장성*             | 쿠버네티스에 GitLab Runner 자동 스케일링 가능                            | self-hosted runner도 auto-scale 가능하지만 직접 구성해야 함                     |
|                        |                                                            |                                                                    |

