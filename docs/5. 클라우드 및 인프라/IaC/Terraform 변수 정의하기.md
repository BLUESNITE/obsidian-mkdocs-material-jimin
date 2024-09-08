#### Terraform 변수 정의

> [!INFO]
> 예시 코드와 함께 Terraform에서 변수 정의하고 사용하는 방법을 익힙니다.
> Terraform은 HashiCorp Configuration Language(HCL)를 가진 언어입니다.

```Shell
variable "image_id" {
  type = string
}

variable "availability_zone_names" {
  type    = list(string)
  default = ["us-west-1a"]
}

variable "ami_id_maps" {
  type = map
  default = {}
}
```

#### Terraform 리소스에서 변수적용 예시

```Shell
resource "aws_vpc" "default" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "vpc-${var.vpc_name}"
  }
}
```
