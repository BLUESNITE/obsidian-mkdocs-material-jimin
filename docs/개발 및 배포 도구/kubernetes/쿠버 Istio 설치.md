**다운로드**
```bash
curl -L https://istio.io/downloadIstio | sh -
```

```
[root@user]# curl -L https://istio.io/downloadIstio | sh -
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  100   102  100   102    0     0    377      0 --:--:-- --:--:-- --:--:--   377
  100  4899  100  4899    0     0   5383      0 --:--:-- --:--:-- --:--:-- 11776

Downloading istio-1.23.2 from https://github.com/istio/istio/releases/download/1.23.2/istio-1.23.2-linux-amd64.tar.gz ...

Istio 1.23.2 Download Complete!
Istio has been successfully downloaded into the istio-1.23.2 folder on your system.

Next Steps:
See https://istio.io/latest/docs/setup/install/ to add Istio to your Kubernetes cluster.

To configure the istioctl client tool for your workstation,
add the /home/tech/k8s/istio-1.23.2/bin directory to your environment path variable with: export PATH="$PATH:/home/tech/k8s/istio-1.23.2/bin"

Begin the Istio pre-installation check by running:
istioctl x precheck

Need more information? Visit https://istio.io/latest/docs/setup/install/
```

**다운로드 완료, 그리고 다음단계 안내**

- Istio를 쿠버네티스 클러스터에 설치하려면 [https://istio.io/latest/docs/setup/install/](https://istio.io/latest/docs/setup/install/) 문서를 참고하십시오.
- `istioctl` 클라이언트 도구를 사용하려면, 환경 변수 `PATH`에 `/home/tech/k8s/istio-1.23.2/bin` 디렉터리를 추가해야 합니다.
```
export PATH="$PATH:/home/tech/k8s/istio-1.23.2/bin"
```

- Istio 설치 전에 필요한 사전 체크를 위해 다음 명령을 실행하십시오.
```
istioctl x precheck
```

**실행결과**
```
[root@k8s-master k8s]# istioctl x precheck
   ✔ No issues found when checking the cluster. Istio is safe to install or upgrade!
   To get started, check out https://istio.io/latest/docs/setup/getting-started/
```

**설치**
```
istioctl install --set profile=default
```

![[Pasted image 20241011084258.png]]

**네임스페이스 레이블링 (필수)**
```
kubectl label namespace <your-namespace> istio-injection=enabled
```

