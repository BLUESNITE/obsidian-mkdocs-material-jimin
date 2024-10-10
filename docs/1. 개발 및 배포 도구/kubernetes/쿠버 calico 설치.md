kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

kubectl apply -f calico.yaml

kubectl delete -f https://docs.projectcalico.org/manifests/calico.yaml

sudo systemctl status containerd

sudo systemctl status kubelet

sudo journalctl -u kubelet -xe

sudo journalctl -u kubelet -f

sudo journalctl -u kubelet -n 100

sudo journalctl -u containerd -n 100

```
sudo ctr -n k8s.io containers list
sudo ctr -n k8s.io tasks kill --all
sudo ctr -n k8s.io tasks rm --all
```

```
sudo curl -fsSLo /mnt/yaml/backup/calico.yaml https://raw.githubusercontent.com/k8s-1pro/install/main/ground/k8s-1.27/calico-3.25.1/calico.yaml

kubectl create -f calico.yaml
```

