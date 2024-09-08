> conf 파일을 기록

```shell
server {
    listen       80;  # 서버가 80 포트에서 리스닝하도록 설정
    server_name  common.x2bee-tech.com;  # 서버 이름 설정

    location / {
        proxy_redirect off;  # 프록시 리다이렉트 비활성화
        proxy_http_version 1.1;  # 프록시 HTTP 버전을 1.1로 설정
        proxy_pass_header Server;  # 서버 헤더를 클라이언트에 전달
        proxy_set_header X-Scheme $scheme;  # 사용된 스키마(http 또는 https)를 헤더에 설정
        proxy_set_header Host $host;  # 요청의 호스트 이름을 헤더에 설정
        proxy_set_header X-Real-IP $remote_addr;  # 클라이언트의 IP 주소를 헤더에 설정
        proxy_set_header X-Forwarded-Proto $scheme;  # 프로토콜 타입을 헤더에 설정
        proxy_set_header Upgrade $http_upgrade;  # WebSocket 등의 Upgrade 요청 처리
        proxy_set_header Connection "";  # Connection 헤더 설정 (WebSocket 지원)
        proxy_pass http://192.168.122.83:31096;  # 실제 요청을 전달할 서버 주소

        proxy_set_header Connection "";  # 중복된 Connection 헤더 설정, 제거 필요
        keepalive_timeout 0;  # keepalive 타임아웃을 0으로 설정하여 비활성화
        keepalive_requests 0;  # keepalive 요청 수를 0으로 설정하여 비활성화
    }
}
```
