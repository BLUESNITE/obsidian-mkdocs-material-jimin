### 부트로더 설정

> [!INFO] /etc/default/grub 파일을 수정
> GRUB는 리눅스 시스템이 부팅될 때 어떤 커널 옵션을 사용할지 정의하는 부트로더입니다.
> 이 설정으로 시스템의 성능, 전원, 보안 등 최적화 하고 */etc/default/grub* 파일을 통해 관리합니다.

```shell
sudo nano /etc/default/grub
```

> [!TIP] GRUB_CMDLINE_LINUX_DEFAULT
> 부트로더 설정 중 *GRUB_CMDLINE_LINUX_DEFAULT* 는 시스템 부팅 시 커널에 전달할 특정 파라미터를 설정하는 항목입니다. 각 설정 옵션은 커널의 동작을 제어하는 역할을 합니다.

```shell
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash module.sig_enforce=0 nopti no5lvl intel_idle.max_cstate=1"
```

- `quiet`, `splash` : 부팅 시 불필요한 메시지와 로그를 숨기고 사용자 경험을 개선
- `module.sig_enforce=0` : 서명되지 않은 커널 모듈 로드 허용
- `nopti` : 보안을 희생하고 CPU 성능을 최적화
- `no5lvl` : 인텔 CPU에서 5단계 페이지 테이블을 비활성화하여 호환성 문제 해결
- `intel_idle.max_cstate=1` : CPU가 깊은 절전 모드로 진입하지 않도록 제한하여 성능 유지

#### GRUB 업데이트

파일을 저장하고 나와서 GRUB 설정을 업데이트해야 합니다.
아래 명령어로 파일의 변경내용을 시스템의 부트로더에 반영합니다.
다음 재부팅시 변경된 내용이 적용됩니다.

```shell
sudo update-grub
```

___
### 절전모드 관리

```shell
systemctl status sleep.target suspend.target hibernate.target hybrid-sleep.target
```

![[Pasted image 20241007090414.png]]

**gsettings 으로 설정 방법**

```shell
gsettings get org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type
gsettings get org.gnome.settings-daemon.plugins.power sleep-inactive-battery-type

(확인 후)
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing'
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-type 'nothing'
```

![[Pasted image 20241007090446.png]]

(아래의 오류 발생하지 않으면 적용 테스트)

![[Pasted image 20241007090624.png]]

> [!WARNING] 문제 발생시
> dbus-launch가 시스템에 없어서 실행 불가 > 설치진행
>  
> (cli)
> sudo apt-get install dbus-x11
> sudo systemctl start dbus

**터미널 기반 설정 방법**

```shell
sudo nano /etc/systemd/logind.conf
 
(옵션확인 및 적용)
IdleAction=ignore 
IdleActionSec=0
 
sudo systemctl restart systemd-logind
```

GNOME GUI 설정을 변경하지 않고 서버의 절전 모드를 방지 적용.

