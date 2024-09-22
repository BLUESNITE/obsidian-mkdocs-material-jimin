## 1. 소개

> [!INFO] 글설명
> **sample**로서,

> [!CHECK] 주저리
> ...

---
## 2. 설치

설치 방법이랄게 있을까 ...
옵시디언 플러그인 `Execute Code`을 검색해서 설치하자 ...

---

## 3. 사용법

> [!NOTE] 아래는 모두 코드블럭을 통해서 미리 실행 할 수 있는 코드들이다
> 나는 잘 활용하지 못하지만.. 누군간 잘 쓰지 않을까?

> [!TIP] 소개 및 사용법
> 이 플러그인을 사용하면 노트의 코드 블록에서 코드 조각을 실행할 수 있습니다. 플러그인은 지원되는 언어의 코드 블록에 대한 '실행' 버튼을 추가합니다. 이를 클릭하면 블록의 코드가 실행됩니다. 실행 후 실행 결과가 표시됩니다. 대화형 입력 요소는 코드 조각이 사용자 입력을 예상할 때 만들어집니다. 결과는 실행이 완료된 후에만 표시됩니다. 지금은 실행된 프로그램에 명령줄의 텍스트를 입력할 수 없습니다.
> 
> 출처 : [twibiral/obsidian-execute-code: 노트의 코드를 실행하기 위한 Obsidian 플러그인. (github.com)](https://github.com/twibiral/obsidian-execute-code)

> 자바 스크립트

```javascript
function hello(name) {
  console.log(`Hello ${name}!`);
}

hello("Bob");
```

> 파워쉘

```powershell
echo "Hello World!"
```

> 파워쉘 (도커 컨테이너 확인)

```powershell
docker ps -a
```

> 파워쉘 (도커 컨테이너 상태 확인)

```powershell
sudo service docker status
```
