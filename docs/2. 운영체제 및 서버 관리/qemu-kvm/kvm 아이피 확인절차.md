> 머신이름 확인

```
virsh
> list
```

![[Pasted image 20240703145933.png]]

> 머신의 맥정보 확인

```
virsh domiflist <rocky9-master>
```

![[Pasted image 20240703145957.png]]

> 머신의 아이피 확인

```
arp -an | grep "<52:54:00:a7:5b:05>"
```

![[Pasted image 20240703150032.png]]
