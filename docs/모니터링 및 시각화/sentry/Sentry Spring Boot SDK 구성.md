> [!NOTE] 메이븐

```bash
SENTRY_AUTH_TOKEN=Click to generate token
```

위와 같은 *SENTRY_AUTH_TOKEN* 이 첫번째로 필요하다.

우선 Sentry로 돌아가서 토큰을 생성해보자.

![[Pasted image 20250418135311.png]]

위와 같은 이미지 화면에서 Auth tokens을 생성 진행 할 수 있다.

![[Pasted image 20250418135633.png]]

*생성된 토큰*

```
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
```

*.env에 하단 변수 추가*

```
SENTRY_OTLP_ENABLED=true
```

*location /api/v2/otel/ 블록을 relay에 proxy하도록 추가*
```
    # OpenTelemetry OTLP 경로 추가
    location /api/v2/otel/ {
        proxy_pass http://relay;
    }
```