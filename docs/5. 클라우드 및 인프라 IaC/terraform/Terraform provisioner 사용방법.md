> [!WARNING] 주의사항
> 테라폼에서 `provisioner`를 사용하면서 겪을 수 있는 주의사항입니다.

provisioner를 사용하는 코드의 작성순서가 중요했습니다.
예를들어 구성이 다음과 같다면 코드 전개 순서도 지켜야합니다.

1. provisioner "file" 선언
2. provisioner "remote-exec" inline 스크립트 작성
3. connection

다음은 예제와 함께 바른 작성법을 알아보겠습니다.

> [!DANGER] 잘못된 예시

```Shell
  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = var.keycontent
    host        = self.public_ip
  }
 
  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/ex.sh"
      ]
  }
 
  provisioner "file" {
    source      = "${path.root}/ex.sh"
    destination = "/tmp/ex.sh"
  }
```

> [!CHECK] 바른 예시

```Shell
  provisioner "file" {
    source      = "${path.root}/ex.sh"
    destination = "/tmp/ex.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/ex.sh"
      ]
  }
 
  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = var.keycontent
    host        = self.public_ip
  }
```

같은 소스 이지만, 전개 순서가 중요합니다.
사소하지만 누군가는 이 때문에 어려움을 겪을 수 있겠습니다
