> [!NOTE] 주저리
> Git commit 외 기능을 오랜만에 사용면 rebase나 revent 같은 작업이 익숙하지 않을 때가 있습니다. VSCode에서도 절차에 따라 헷갈릴 수 있습니다. 이번에 VSCode를 사용해서 수행하는 과정을 정리해보았습니다.

**작업환경 VSCode**

![[Pasted image 20241122085750.png]]

`소스 제어 리포지토리` or `소스 제어` 이외 기능 관리는 `REPOSITORIES`를 통해서 진행

아래에는 GUI 캡쳐이미지

![[Pasted image 20241122090413.png]]

Commit 작업에서 우클릭하여 확인할 수 있는 `컨텍스트` 목록

![[Pasted image 20241122090504.png]]

- Reset Current Branch to Commit
  (선택한 브랜치로 리셋 - 이후 데이터 모두 제거됨)
- Reset Current Branch to Previous Commit
  (현재 브랜치를 이전 커밋 상태로 리셋)
- Rebase Current Branch onto Commit
  (현재 브랜치를 선택한 커밋 위에 리베이스 - 재정렬 또는 히스토리 청소)

*소스 롤백 작업*

내가 선호하는 방법은 Rebase를 통한 불필요 커밋 소스와 이력 삭제
( 이는 선택적으로 롤백하기 좋은 플랜 )

![[Pasted image 20241122090913.png]]

`Interactive Rebase` 를 통해서 수동으로 작업 진행 (수정, 병합, 삭제)

![[Pasted image 20241122091151.png]]

- pick - 해당 커밋 유지
- reword - 해당 커밋 메세지 수정
- edit - 해당 커밋 수정 진행 (리베이스 중단)
- squash - 현재 커밋을 이전과 합침 (병합)
- fixup - 현재 커밋을 바로 이전 커밋과 합칩니다 (단순히 코드 정리 밋 커밋 합칠때 사용)
- drop - 해당 커밋을 삭제

![[Pasted image 20241122091526.png]]

위와 같이 진행시 이전 case drop 되고, 직전 커밋 789가 유지
이 시점에 동기화 진행시 진행 했던 rebase 작업이 초기화 되며 rollback

![[Pasted image 20241122091713.png]]

*커밋 & 푸쉬 진행*

```
PS C:\project\core-project\x2bee-pipeline> git push origin main --force
warning: redirecting to https://gitlab.x2bee.com/tech-team/x2bee-pipeline.git/
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 16 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (8/8), 797 bytes | 797.00 KiB/s, done.
Total 8 (delta 4), reused 0 (delta 0), pack-reused 0 (from 0)
remote: GitLab: You are not allowed to force push code to a protected branch on this project.
To http://gitlab.x2bee.com/tech-team/x2bee-pipeline.git
 ! [remote rejected] main -> main (pre-receive hook declined)
error: failed to push some refs to 'http://gitlab.x2bee.com/tech-team/x2bee-pipeline.git'
```

*강제 푸쉬 허용으로*

Settings → Repository → Protected Branches 메뉴로

![[Pasted image 20241122092855.png]]

*재수행*
```
git push origin main --force
```

