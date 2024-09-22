## 1. 소개

> [!INFO] 글설명
> 쿠버네티스 워커노드에서 컨테이너를 운영하다 보면 디스크 공간이 부족해지는 문제가 발생 할 수 있습니다. 특히 **/var/lib/containerd** 경로에 디스크 공간이 충분하지 않으면 다양한 문제를 발생 시킵니다. 이 글에서는 containerd 디스크 공간 문제를 해결하는 방법을 알아보겠습니다.

> [!CHECK] 주저리
> 개인적으로 이러한 이슈들이 큰 어려움으로 느껴진다. 이유인 즉슨 정확한 원인 규명과 동일 이슈에 대한 정보나 경험이 부족해서인듯하다. 어찌되었건 내 경우에는 On-Premise 환경의 서버데스크톱 3대를 운용하고 있고, 서버데스크톱에 노드 클러스터를 각각 VM 로키리눅스 OS에 설치 운용하고있다.

---

## 2. 작업진행

> 여유 공간이 가장 필요한 경로

디스크 공간이 많이 사용되는 경로를 확인

```shell
du -sh /var/lib/containerd
```

> 여유 공간 확인

LVM(Logical Volume Manager)을 사용하여 볼륨 그룹의 여유 공간을 확인

```
sudo vgdisplay rl
```

> 출력예시를 통해서 `Free PE / Size` 항목에 여유 공간이 있는지 확인

```
[root@xxxxxxxxxx]# sudo vgdisplay rl
  --- Volume group ---
  VG Name               rl
  System ID
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  4
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                2
  Open LV               1
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               <169.00 GiB
  PE Size               4.00 MiB
  Total PE              43263
  Alloc PE / Size       4863 / <19.00 GiB
  Free  PE / Size       38400 / 150.00 GiB
  VG UUID               yAOMvh-pytw-cNBr-ikVl-Rdpm-TejE-rC07ly
```

> 논리 볼륨 확장

```
sudo lvextend -L +10G /dev/rl/root
sudo xfs_growfs /
```

> 디렉토리 용량 확인

```
df -h /var/lib/containerd
```

---

## 3. 정리

> [!INFO] 정리
> **가상 머신 환경** 에서 넉넉하게 디스크 사이즈를 잡아도 필요한 부분의 실제 디스크 할당은 조금 다르게 이루어질 수 있었습니다. 그러나 LVM을 확인하여 필요한 디스크 공간을 확장 가능합니다.
> 
> 이번 예시에서는 워커노드의 주요 컨테이너 운영 위치인 `/var/lib/containerd`에 최초 20기가 이하로 할당되어 있던 **디스크 사이즈를 60기가** 까지 확장했습니다.
