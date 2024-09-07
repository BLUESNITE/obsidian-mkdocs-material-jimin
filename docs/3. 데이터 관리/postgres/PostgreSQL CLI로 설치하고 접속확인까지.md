> [!NOTE] 아래의 내용은 `apt-get install postgresql postgresql-contrib` 수행 후 기본 접속까지
> 기본 OS는 우분투 서버입니다.
> 다음에 동일한 작업시 편하게 수행하기 위해 작성하였습니다.
```shell
systemctl list-units --type=service

systemctl start postgresql.service
```

> 기본디렉토리
```shell
/etc/postgresql/16/main
```

> 내용수정 postgresql.conf
```shell
listen_addresses = '*' (추가)
```

> 내용수정 pg_hba.conf
```shell
host    postgres    postgres    192.168.2.215/32    md5
```

```shell
sudo -u postgres psql
ALTER USER postgres PASSWORD 'tech';
```