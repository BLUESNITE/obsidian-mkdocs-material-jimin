> [!TIP] Software & Updates 진행
#### Additional Drivers
![[Pasted image 20240930131052.png]]

*옵션 설명*
- **NVIDIA driver metapackage from nvidia-driver-550**
  : 검증된 최신 버전의 NVIDIA 독점 드라이버 550
- **NVIDIA driver metapackage from nvidia-driver-535**
  : 버전 535의 독점 드라이버
- **NVIDIA driver metapackage from nvidia-driver-535-open (open kernel)**
  : 오픈 커널을 사용하는 버전 535 드라이버
- **NVIDIA driver metapackage from nvidia-driver-550-open (open kernel)**
  : 오픈 커널을 사용하는 버전 550 드라이버
- **NVIDIA Server Driver metapackage from nvidia-driver-535-server**
  : 서버에 최적화된 버전 535 드라이버
- **X.Org X server -- Nouveau display driver**
  : 현재 사용 중인 오픈 소스 드라이버

*적절한 드라이버 선택*
우분투 서버 환경에서는 주로 백엔드에서 CUDA를 사용하는 머신러닝, 데이터 처리, 또는 GPU 가속이 필요한 애플리케이션에 더 초점을 맞춥니다. 따라서 서버 환경에 가장 적합한 NVIDIA 드라이버 옵션은 안정성과 성능을 모두 고려한 드라이버를 선택하는 것이 중요 포인트.

제안된 드라이버 옵션 중, **서버 환경에 적합한 것은** 
NVIDIA Server Driver metapackage from nvidia-driver-535-server (proprietary)

이 드라이버는 서버 환경에 최적화된 버전으로, 데스크탑용 드라이버와 달리 서버에서 안정적이고 장기적으로 GPU 리소스를 활용할 수 있도록 설계되었습니다. 서버 환경에서 높은 안정성을 유지하면서도 GPU 가속을 활용한 연산 작업에 적합한 드라이버입니다.

> [!CHECK] 설치 후 확인
> nvidia-smi

![[Pasted image 20240930134949.png]]

**분석 내용**

*상단 정보:*
- NVIDIA-SMI 535.183.06: 설치된 NVIDIA 드라이버의 버전
- Driver Version: 535.183.06: GPU가 사용하는 드라이버 버전
- CUDA Version: 12.2: 설치된 CUDA 버전 
  (CUDA는 GPU 가속을 위한 NVIDIA의 병렬 컴퓨팅 플랫폼)

*GPU 정보:*
- GPU > 0 (NVIDIA GeForce RTX 4060): 장착된 GPU의 모델명
- Persistence-M > Off Persistence : 모드가 비활성화되어 있음
- Bus-Id > 00000000:E1:00.0 : GPU가 사용 중인 PCI 버스의 ID
- Disp.A > Off : 디스플레이 어댑터가 비활성화된 상태
- Volatile Uncorr. ECC > N/A : ECC(오류 정정 코드)를 지원하지 않거나 설정되지 않았음
- Fan > 0% : GPU의 팬이 현재 작동하지 않고 있음
- Temp > 37C : GPU의 현재 온도
- Perf > P8 : GPU의 현재 전력 성능 상태 (P8은 저전력 상태)
- Pwr Usage/Cap > 130W : 현재 GPU의 전력 사용량(130W)
- Memory-Usage >: 8MiB / 8188MiB : GPU의 사용 중인 메모리(8MiB)와 총 메모리 용량(8188MiB)
- GPU-Util > 0% : GPU의 사용률이 0%
- Compute M. > Default : GPU가 기본 연산 모드를 사용 중임을 나타냅니다.

*Processes 정보:*
- PID > 3380 : 현재 GPU를 사용하는 프로세스의 PID(프로세스 ID)
- Type > G : 이 프로세스가 그래픽 관련 작업에 사용되고 있음
- Process name > /usr/lib/xorg/Xorg : 이 프로세스는 X 서버와 관련된 프로세스
- GPU Memory Usage > 4Mi : 이 프로세스가 GPU 메모리 중 4MiB를 사용중

*요약:*
요약하자면, 이 시스템은 NVIDIA GeForce RTX 4060 GPU를 사용하고 있으며, 현재 GPU는 낮은 전력 모드(P8)에 있고, 그래픽 서버(Xorg)가 약간의 GPU 메모리(4MiB)를 사용하고 있는 상태입니다. GPU 사용률은 0%로 현재 특별한 GPU 작업은 수행되지 않는 상태입니다.

*원격데스크톱 및 부팅(DP&HDMI) 확인*
+ (+) 버전에 맞는 CUDA Tool Kit 설치 필수 

[CUDA 설치과정](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=24.04&target_type=deb_local "CUDA 설치과정")

![[Pasted image 20240930152938.png]]

![[Pasted image 20240930152956.png]]

```
apt-get -y install cuda-toolkit-12-6
apt-get install -y cuda-drivers
```

*GPU 사용 확인*

#### Gnome-shell 추가 되면서 동작사항 업데이트
nvidia-smi를 다시 확인해보면... gnome-shell 이 추가되었다.
![[Pasted image 20240930153406.png]]

여기서 운좋게 캐치.

*xrdp 설정내용 수정 후 테스트*
```shell
root@tech:/etc/xrdp# cat startwm.sh
#!/bin/sh
# xrdp X session start script (c) 2015, 2017, 2021 mirabilos
# published under The MirOS Licence

# Rely on /etc/pam.d/xrdp-sesman using pam_env to load both
# /etc/environment and /etc/default/locale to initialise the
# locale and the user environment properly.

if test -r /etc/profile; then
        . /etc/profile
fi

if test -r ~/.profile; then
        . ~/.profile
fi

test -x /etc/X11/Xsession && exec /etc/X11/Xsession
exec /bin/sh /etc/X11/Xsession

#test -x /usr/bin/startxfce4 && exec /usr/bin/startxfce4
#exec /bin/sh /usr/bin/startxfce4
```

sudo systemctl restart xrdp 후 접속

**연관성**:
- NVIDIA 드라이버가 설치되지 않았거나 잘못 설치된 경우, `X11/Xsession`과 같은 그래픽 환경에서 GPU를 제대로 활용하지 못해 `xrdp` 연결이 실패할 수 있음
- `cuda-drivers`를 설치하면서 NVIDIA 드라이버가 업데이트되어 X 서버와의 호환성이 개선되고, 이로 인해 `xrdp` 세션에서 화면이 정상적으로 출력되었을 수도 있음
