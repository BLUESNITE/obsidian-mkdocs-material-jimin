> [!TIP] 사전에 aws cli 등 사전 설치는 완료 된 것으로 본다.

> 자격증명

```shell
aws configure
```

> 클러스터에 IAM 사용자나 역할을 매핑

```shell hl:1
--cluster <클러스터명>만 수정하여 사용

eksctl create iamidentitymapping --region ap-northeast-2 --cluster MOON-STAGE --arn arn:aws:iam::318919594903:user/jeongzmin --group system:masters
```

> kubeconfig 파일을 업데이트하여 kubectl 명령을 해당 클러스터에 연결

```shell hl:1
--name <클러스터명>만 수정하여 사용

aws eks update-kubeconfig --region ap-northeast-2 --name MOON-STAGE
```

> 조금 편하게 쓰기

```powershell hl:1
$CLUSTER_NAME = "LOTTE-TEST"

eksctl create iamidentitymapping --region ap-northeast-2 --cluster $CLUSTER_NAME --arn arn:aws:iam::318919594903:user/jeongzmin --group system:masters

aws eks update-kubeconfig --region ap-northeast-2 --name $CLUSTER_NAME
```
