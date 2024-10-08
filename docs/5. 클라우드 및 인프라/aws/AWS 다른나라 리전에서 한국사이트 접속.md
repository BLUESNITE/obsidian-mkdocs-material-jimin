> [!INFO] 주저리
> 상품데이터를 자동 스크래핑 하는 Python 소스를 작성하고, 여러 리전에서 데이터를 자동화 스크래핑 전략을 작성해두었다. 그런데 AWS 오사카 리전에서 쿠팡 접속이 안되지 뭔가 ... 내부에서는 이유를 모르니 온갖 뇌피셜이 오갔고, 안된다만 난무하였 ... 짜증이 ... 무튼 해결방법을 찾아보았다.

> [!TIP] 작업의 내용
> 위 내용은 AWS 오사카 리전에서 VPC 내의 인스턴스들이 한국의 DNS 서버를 사용하도록 설정한 방법이다. 물론 이 방법만 있는건 아니겠지만 Terraform을 활용하고 있는 내겐 빠르고 쉬운 방법으로 와닿았기 때문에 이와 같이 작업을 하였다.

**여러가지 방법**

- VPC의 DHCP 옵션 세트 수정
- 개별 인스턴스 설정, 인스턴스 내에서 직접 DNS 서버를 지정
- Route 53의 서비스를 사용하여 특정 도메인에 대한 쿼리를 한국 DNS 서버로 전달

#### DHCP 옵션 세트를 수정 가이드

![[Pasted image 20240902091408.png]]

> [!NOTE] DHCP 옵션 세트에 작성 내용
> 옵션이름 : Korean-DNS-Options
> 도메인 이름 : ec2.internal
> 도메인 이름 서버 : _223.5.5.5, 223.6.6.6_
> 나머지 기재사항 없음

_추가정보 - 한국에서 사용할 수 있는 주요 DNS 서버 목록_

```shell
- KT (Korea Telecom)
    - 168.126.63.1
    - 168.126.63.2

- SK 브로드밴드
    - 210.220.163.82
    - 219.250.36.130

- LG U+
    - 164.124.101.2
    - 203.248.252.2

- 네이버 DNS
    - 223.5.5.5
    - 223.6.6.6

- 구글 퍼블릭 DNS (한국 서버)
    - 8.8.8.8
    - 8.8.4.4

- Cloudflare DNS (한국 서버 포함)
    - 1.1.1.1
    - 1.0.0.1

- KISA (한국인터넷진흥원) DNS
    - 202.30.143.11
    - 202.30.143.12
```

#### Terraform에의 반영

```Shell
# DHCP 옵션 정의
resource "aws_vpc_dhcp_options" "ia-dhcp-options" {
  domain_name         = "ec2.internal"
  domain_name_servers = ["223.5.5.5", "223.6.6.6"]

  tags = {
    Name = "ia-dhcp-options"
  }
}
```
