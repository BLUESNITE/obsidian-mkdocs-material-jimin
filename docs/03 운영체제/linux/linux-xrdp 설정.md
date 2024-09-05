> XRDP 접속 가능하도록 설정 내용
``` Shell
/etc/xrdp

(기본 내용)
#test -x /etc/X11/Xsession && exec /etc/X11/Xsession
#exec /bin/sh /etc/X11/Xsession

(수정 내용)
test -x /usr/bin/startxfce4 && exec /usr/bin/startxfce4
exec /bin/sh /usr/bin/startxfce4

위와 같이 수정하면 gnome 환경은 아니지만 xfce4 접속가능
```

> XRDP 재실행
``` Shell
sudo systemctl restart xrdp
```

> 윈도우 이슈 사항

만약 *윈도우 원격데스크톱으로 연결시 Gnome 연결이 안된다면.* 설정을 바꾸기 전에 다를 Tool의 RDP로 접속 시도를 해보자. 되는 경우가 있다.

나의 경우는 `MobaXterm RDP`로 해결하여 잘 사용하고있다.
