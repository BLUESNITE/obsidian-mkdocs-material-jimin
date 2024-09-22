[Terraform]([Install | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/install) "Terraform install")

> [!NOTE] 우분투 인스톨

```
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

> [!NOTE] 오라클 리눅스 인스톨
> 
> - RHEL/CentOS

```
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
sudo yum -y install terraform
```

> [!NOTE] 윈도우 인스톨

```
choco install terraform

```

> [!NOTE] 탭 자동완성

```
touch ~/.bashrc
terraform -install-autocomplete
```

> [!TIP] 프로비저닝(Provisioning)"이란
> Terraform에서 _"프로비저닝(Provisioning)"이란_ 클라우드 *인프라 및 리소스를 정의*하고, *배포*하며, *관리*하는 과정을 의미합니다. Terraform은 인프라를 코드(Infrastructure as Code, IaC)로 정의하여 프로비저닝을 자동화하고 일관되게 수행할 수 있도록 합니다. 이 과정을 통해 다양한 클라우드 제공업체 및 서비스에서 리소스를 쉽게 생성하고 관리할 수 있습니다.
> 
> - 인프라 정의
> - 계획
> - 리소스 배포
> - 리소스 관리

> [연습 1] terraform init > 초기화

> [연습 2] terraform apply > 실행 적용

> [연습 3] terraform destroy > 컨테이너 중지

> [연습 4] terraform destroy -auto-approve > 확인 없이 수행

여기까지 수행하면 설치 후 기초 학습 종료.
