> [!INFO] 정보
> Terraform에서 리소스를 정의하고 user_data 실행 로그 확인 하는 방법

> Terraform 인스턴스 생성 리소스

```Shell
resource "aws_instance" "ia-ubuntu-server" {
  ami           = "ami-04a81a99f5ec58529" // 우분투 20(x86)용 AMI ID
  instance_type = "t2.micro"

	....

	user_data = file("${path.module}/ex.tpl")

	....

}
```

> 실행 로그를 확인하는 방법

```Shell
journalctl -u cloud-final.service

journalctl -u cloud-final.service -f
```

> user_data에 template_file을 사용하는 예시

```Shell
data "template_file" "user_data" {
  template = file("${path.module}/aws-instance.tpl")
  vars = {
    instance_type  = var.instance_type
  }
}

resource "aws_instance" "ia-ubuntu-server" {
  ami           = var.ami
  instance_type = var.instance_type
  user_data              = data.template_file.user_data.rendered
 
  ....
 
}
```
