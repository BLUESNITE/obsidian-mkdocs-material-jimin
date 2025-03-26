> [!INFO] Jenkins Credentials
> 별다른 특이점 없이 사용자 계정 및 패스워드 로 이루어진 구성

![[Pasted image 20250324184344.png]]

*Harbor에서 프로젝트 생성: moon-dev*

![[Pasted image 20250325095455.png]]

```
echo "[Docker Image] Harbor Start"

def img = docker.build("${HARBOR_IMAGE_NAME}:latest", buildArgs)
docker.withRegistry("${HARBOR_REPO_URL}", "${HARBOR_REPO_CREDENTIALS_ID}") {
	retry(3) {
			try{
				img.push("${BUILD_NUMBER}")
				img.push("latest")
			} catch (e) {
				sleep(10)
			throw e
		}
	}
}
```

![[Pasted image 20250325154209.png]]

*Robot 계정 생성 (CI/CD용)*

![[Pasted image 20250325154302.png]]

새 로롯 계정 생성

![[Pasted image 20250325154444.png]]

pull push 권한 부여

![[Pasted image 20250325154526.png]]

![[Pasted image 20250325154548.png]]

이름 robot$moon-dev+harbor-robot
토큰 Yl8IhQ5tAjaM1RjceweMyH392jqcwNyG

*Kubernetes 측 설정 / imagePullSecrets 등록 (Harbor 인증)*

https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/

```
kubectl create secret docker-registry harbor-cred \
  --docker-server=harbor-dev.x2bee.com \
  --docker-username=robot$moon-dev+harbor-robot \
  --docker-password=xxxxxxxxxxxxxxxxx \
  --namespace=moon-dev
```

*네트워크 접근 가능 여부*
```
kubectl exec -n moon-dev <pod> -- nslookup harbor-dev.x2bee.com
```

*harbor secret을 네임스페이스에 등록하여 사용하는 방법*

```

kubectl create secret docker-registry harbor-secret \
  --docker-server=harbor-dev.x2bee.com \
  --docker-username=robot$moon-dev+harbor-robot \
  --docker-password=xxxxxxxxxxxxxxxxx \
  --namespace=moon-dev
```

![[Pasted image 20250326092115.png]]

템플릿 내용

```
spec:
 containers:
  - name: {{ .Values.application.name }}
    image: harbor-dev.x2bee.com/moon-dev/moon-x2bee-api-common:latest

imagePullSecrets:
- name: harbor-secret
```

*harbor secret을 어플리케이션에 등록하여 사용하는 방법*

아래와 같이 템플릿 등록하여 사용하려고 시도해보았으나 Sync 단계에서 실패

```
apiVersion: v1
kind: Secret
metadata:
  name: {{ .Values.application.name }}-docker-secret
  namespace: {{ .Values.application.namespace }}
  labels:
    app: {{ .Values.application.name }}
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: key
```

