> [!NOTE] 실전으로 배우는 ansible

_설치_

```
python3.11 -m pip install ansible
```

_venv_

```
cd /data
python3.11 -m venv ansible-env
source ansible-env/bin/activate
pip install ansible

```

**Ansible 시작하기**

```
cd /data
mkdir ansible_quickstart
cd ansible_quickstart
```

_인벤토리 작성_

```
[myhosts]
192.168.2.170
192.168.2.175
192.168.2.243
```

> 확인

```
ansible-inventory -i inventory.ini --list
```

_패스워드 접속을 위한 세팅_

```
sudo dnf install -y sshpass
```

> 확인

```
ansible myhosts -m ping -i inventory.ini --ask-pass
```

**python3.11**

```
sudo dnf install epel-release -y
sudo dnf install python3.11 -y
python3.11 --version
```

_hosts 생성_

```
myhosts:
  hosts:
    host_170:
      ansible_host: 192.168.2.170
    host_175:
      ansible_host: 192.168.2.175
```

**# 플레이북 만들기**

플레이북은 Ansible이 관리형 노드를 배포하고 구성하는 데 사용하는 형식의 자동화 IaC

_실습 예시 - playbook.yaml_

```
- name: My first play
  hosts: myhosts
  tasks:
   - name: Ping my hosts
     ansible.builtin.ping:

   - name: Print message
     ansible.builtin.debug:
       msg: Hello world
```

> [!INFO] 신규옵션 --ask-pass
> 앤서블에서 플레이북 ssh 접속에 필요한 인증으로 패스워드 요청을 하도록 유도

> 확인

```
ansible-playbook -i inventory.ini playbook.yaml --ask-pass
```

잘 몰라도 실행이 되었으면 우선은 패스.
![[Pasted image 20241104085345.png]]

_실습 예시 2 - playbook-setup.yaml_

```
- name: My first play
  hosts: myhosts
  become: true  # sudo 권한 사용
  tasks:
    - name: Ping my hosts
      ansible.builtin.ping:

    - name: Install yum-utils
      ansible.builtin.yum:
        name: yum-utils
        state: present

    - name: Add HashiCorp repository for Terraform
      ansible.builtin.command:
        cmd: "yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo"
      args:
        creates: /etc/yum.repos.d/hashicorp.repo  # 이미 repo 파일이 존재하면 다시 실행하지 않음

    - name: Install Terraform
      ansible.builtin.yum:
        name: terraform
        state: present
```

> [!INFO] 신규옵션 --ask-become-pass
> 앤서블에서 플레이북 실행시 sudo 권한이 필요한 태스크들에서 sudo 암호를 요구하기 때문에.
> 해당 옵션을 추가하여 비밀번호를 요청하도록 유도

> 확인

```
ansible-playbook -i inventory.ini playbook-setup.yaml --ask-pass --ask-become-pass
```
