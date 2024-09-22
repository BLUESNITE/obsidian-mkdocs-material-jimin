**커맨드 라인에서 디렉토리 항상 풀경로 보기**

```hl:1,3
echo 'export PS1="\[\e[0;32m\]\u@\h\[\e[0m\]:\[\e[1;34m\]\w\[\e[0m\]\$ "' >> ~/.bashrc

source ~/.bashrc
```

**쿠버네티스 자동완성기능**

```hl:2,5,8,11
# kubectl 명령어에 대한 자동완성 기능 활성화
echo "source <(kubectl completion bash)" >> ~/.bashrc

# k 관련 키워드에 kubectl 추가
echo 'alias k=kubectl' >>~/.bashrc

# k 누르고 탭치면 kubectl 자동완성 제안!
echo 'complete -o default -F __start_kubectl k' >>~/.bashrc

# 변경 사항 현재 세션에 적용
source ~/.bashrc
```
