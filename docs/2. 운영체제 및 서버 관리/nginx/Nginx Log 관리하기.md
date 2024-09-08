> 파일 확인

```shell
find . -type f -name 'access*'
find . -type f -name 'error*'
```

> crontab -e

```shell
0 7 * * * find /var/log/nginx/labs -type f -name 'access*' -exec rm {} \;
0 7 * * * find /var/log/nginx/labs -type f -name 'error*' -exec rm {} \;
```

> Log 디렉토리 설정하기

```shell
server {
    access_log /var/log/nginx/labs/access.log;
    error_log /var/log/nginx/labs/error.log;
}
```
