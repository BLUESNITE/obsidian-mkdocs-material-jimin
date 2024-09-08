> [!TIP]
> IstioOperator의 설정과 관련된 작업은 주로 트래픽 처리량 증가, 성능 최적화, 안정성 향상, 및 시스템 요구 사항 변화에 따라 이루어집니다. 특히 대규모 시스템에서 다수의 동시 접속자나 높은 트래픽을 처리할 때 설정합니다.

_설정의 주요 목적_

- **확장성**: 시스템이 더 많은 트래픽과 동시 접속자를 처리할 수 있도록 설정을 조정합니다.
- **성능 향상**: 프록시의 처리 능력을 최적화하여 응답 시간과 처리량을 개선합니다.
- **안정성**: 과부하를 방지하고 시스템이 안정적으로 운영되도록 설정을 조정합니다.
- **대응력**: 예상치 못한 트래픽 피크나 이벤트에 대비하여 시스템이 원활하게 작동하도록 합니다.

> [!CHECK] Istio gateway를 관리하는 포인트는 두가지다.
>
> 1. Deployment
> 2. HorizontalPodAutoscaler (HPA)

먼저, deployment

> [!CHECK] Deployment 두가지 ingressgateway , engressgateway
> kubectl edit deployment istio-ingressgateway -n istio-system
> kubectl edit deployment istio-engressgateway -n istio-system

```Shell
spec.replicas 숫자 조정
resources.limits.cpu 숫자 조정
resources.limits.memory 숫자 조정

cpu와 memory는 기본 1, 2Gi 이었는데 변경하여 4, 8Gi로 할당.
```

> [!CHECK] HorizontalPodAutoscaler 에서 ingressgateway
>
> kubectl get hpa istio-ingressgateway -n istio-system -o yaml

```Shell
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: istio-ingressgateway
  namespace: istio-system
  labels:
    app: istio-ingressgateway
    install.operator.istio.io/owning-resource: custom-istiooperator
    install.operator.istio.io/owning-resource-namespace: istio-system
    istio: ingressgateway
    istio.io/rev: default
    operator.istio.io/component: IngressGateways
    operator.istio.io/managed: Reconcile
    operator.istio.io/version: 1.21.1
    release: istio
spec:
  maxReplicas: 10
  minReplicas: 3
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: istio-ingressgateway
```

---

> 객체 가져오기

```Shell
kubectl get deployment istio-ingressgateway -n istio-system -o yaml > istio-ingressgateway-latest.yaml
```
