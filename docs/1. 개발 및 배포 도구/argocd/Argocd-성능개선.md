> [!NOTE] 성능개선
> 동기화 작업시 Argocd 동작시간이 너무 오래걸려서 찾게 되었다.
> 
> (실제 커맨드라인)
> argocd app sync ${appName} --project ${project} --strategy ${strategy}

**ConfigMap 확인하기:**
``` Shell
kubectl get cm argocd-cm -n argocd -o yaml
```

**ConfigMap 수정하기:**
``` Shell
apiVersion: v1
data:
  url: https://argocd.dev.x2bee-tech.com
  server.config: |
    resource:
      requests:
        cpu: "500m"  # 예시: CPU 요구사항을 0.5 Core로 설정
        memory: "1024Mi"  # 예시: 메모리 요구사항을 1Gi로 설정
      limits:
        cpu: "1"  # 예시: 최대 CPU 사용을 1 Core로 설정
        memory: "2048Mi"  # 예시: 최대 메모리 사용을 2Gi로 설정
    sync:
      concurrency: 10  # 예시: 동시에 처리할 Sync 요청 수 설정
      parallelism: 2  # 예시: 병렬로 처리할 Sync 요청 수 설정
kind: ConfigMap
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"ConfigMap","metadata":{"annotations":{},"labels":{"app.kubernetes.io/name":"argocd-cm","app.kubernetes.io/part-of":"argocd"},"name":"argocd-cm","namespace":"argocd"}}
  creationTimestamp: "2024-05-24T01:35:01Z"
  labels:
    app.kubernetes.io/name: argocd-cm
    app.kubernetes.io/part-of: argocd
  name: argocd-cm
  namespace: argocd
  resourceVersion: "3385000"
  uid: e14ae8b2-a1e6-4742-8870-355d9122d9bc

```

**Argocd sync 동기화 개선:**
``` Shell
argocd app sync ${appName} --revision HEAD --prune=true --force=true --dry-run=false --apply-out-of-sync-only=false --server-side=false --replace=false
```

**Argocd 명령어 옵션 설명:**
- `argocd app sync app-name`: `app-name` 애플리케이션 동기화
- `--revision HEAD`: `HEAD` 리비전
- `--prune=false`: Prune 작업을 비활성화
- `--dry-run=false`: Dry run을 비활성화
- `--apply-only=false`: Apply only를 비활성화
- `--force=false`: Force 적용을 비활성화
- `--skip-schema-validation=false`: 스키마 검증을 비활성화
- `--auto-create-namespace=false`: 네임스페이스 자동 생성을 비활성화
- `--prune-last=false`: Prune last를 비활성화
- `--apply-out-of-sync-only=false`: Out of sync 항목만 적용을 비활성화
- `--respect-ignore-differences=false`: Ignore differences를 비활성화
- `--server-side=false`: 서버 사이드 적용을 비활성화
- `--prune-propagation-policy foreground`: Prune 전파 정책을 foreground로 설정
- `--replace=false`: Replace를 비활성화
- `--retry=false`: Retry를 비활성화

> [!NOTE] 참고
> Jenkins에서 수행하는 Argo CD CLI 명령어가 의도대로 작동하는지 확인하고, 파이프라인에 추가[!!]

