> [!NOTE] 만료시간 관리
> Redis에서 토큰(또는 키)의 만료 시간을 연장하려면 **`EXPIRE`** 또는 **`PEXPIRE`** 명령을 사용합니다.

*CLI*
```
EXPIRE <key> <seconds>
```

```
PEXPIRE <key> <milliseconds>
```

이전에 소개한 *Redis Insight*에 좌측 하단에 CLI 메뉴가 있습니다

![[Pasted image 20241129080419.png]]

해당 메뉴를 클릭하여 CLI 작성 수행합니다.

![[Pasted image 20241129080339.png]]

