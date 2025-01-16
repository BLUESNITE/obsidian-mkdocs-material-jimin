> [!NOTE] 비하인드
> 프로젝트를 수행하는데 SMTP 이 간단한 장르로 한달이상 애를 먹었다. 해서. 비슷한 일이 발생하면 빠르게 대응하기 위해서 이력과 기록물을 남긴다. 
> 이는 보통의 수행 레벨에서 정보(부정확한)만을 가지고 해결하기 위한 처절한 싸움이며 해결 솔루션을 도출하기 위한 노력이다.

<주의> 감정이 많이 들어간 상처받은 워딩이 많이 들어감

___
### 첫번째 기본 정보

SMTP를 진행하는데 전달 받은 내용은 고작 해봐야 아래와 같은 정보였다.

```
smtp server : abc.smtp-domain.com
smtp port : 25
smtp user : sender
smtp password : pw-sample
smtn sender : sender@domain.com
```

첫번째 허들. 잘못된 정보.
위와 같이 내용을 전달받았습니다. 하지만 인증이 되지 않습니다. 확인 부탁드립니다.
라는 요청을 로봇처럼 두번이상 한 것 같지만. 로봇 같은 답변만 받았다. 되는데 무슨소리야?
이 얼마나 개떡같은 소리일까 ...

> 해결을 위한 솔루션

```
1. SMTP 테스트 사이트 이용
2. Python 소스를 작성하여 빠르게 검증
```

전달 받은 정보가 정확한지. 최소한의 인증 값은 맞는지 확인하기 위해 위와 같이 사이트를 이용하거나 빠르게 작성 확인 할 수 있는 소스를 작성 해 볼 수 있다. 내 경우에는 두가지 다 수행하였다. 

```
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server = "abc.smtp-domain.com"  # SMTP 서버 호스트
smtp_port = 25  # SMTP 서버 포트 (평문)
smtp_user = "sender@domain.com"  # SMTP 인증 계정
smtp_password = "pw-sample"  # SMTP 인증 비밀번호

sender_email = "sender@domain.com"  # 발신자 이메일
receiver_email = "blue@abc.com"  # 수신자 이메일
subject = "Test Email from Pod"  # 이메일 제목
body = "test send"

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))  # 이메일 본문 추가

try:
    print("Connecting to the SMTP server...")
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
    
        server.set_debuglevel(1)  # 디버그 모드 활성화 (SMTP 통신 로그 출력)

		print("Connected to SMTP server successfully.")
        
        print("Starting TLS...")
        
        #server.starttls()
        
        print("TLS started successfully.")
        
        print("Logging in to the SMTP server...")
        
        server.login(smtp_user, smtp_password)
        
        print("Logged in to SMTP server successfully.")
        
        print("Sending email...")
        
        server.sendmail(sender_email, receiver_email, message.as_string())
        
        print("Email sent successfully!")
        
except Exception as e:
        print(f"Error occurred: {e}")
```

소스에서 바뀐 내용을 찾았다면 눈썰미가 굉장히 좋은사람입니다.

잘못된 정보 때문에 배포 & 반영을 수십번 할게 아니라 위와 같이 솔루션으로 선행 확인이 필요하고,
필요시에는 `sender` 에서 `sender@domain.com` 와 같이 짜집기(?) 하여 정보를 때려 맞춰야 할 수도 있다.

### 두번째 메일 전송 프로토콜
smtp를 쓴다고하면 정확히는 메일 전송 프로토콜을 쓴다는 개념을 이해하고 있어야한다.
이는 무슨이야긴고 하면 정확히 서비스하는 메일전송이 어떤 프로토콜로 하고 있는지 알아야 하기 때문이다.

```
SMTP(Simple Mail Transfer Protocol) 전자 메일을 전송하는 프로토콜로, 메일을 보내는데 사용이 됩니다.
SMTP는 TCP 프로토콜을 기반으로 동작하며, 일반적으로는 25 포트와 465(SSL), 587(TLS)를 사용합니다.
```

여기서 또 뚜껑이 열릴뻔한 부분이. 분명 사용하고 있는. 서비스하고 있는. 발송이 되고 있는.
전송 방식이 25 포트를 쓰고있으니 그걸로 보내세요. 라는 답변이었다.

이또한 잘못된 정보였으니. 최종 사용하는 서비스 방식은 465(SSL) 방식이었다. 이 또한도 미완의 작업이었다.
왜냐하면 SSL 방식을 사용하려면 그에 맞는 설정을 해주어야 하기 때문이다.

위 Python 소스에도 있거나 없는 옵션 항목이 있으니 아래와 같은 설정들이다.

> JAVA

```java
Properties prop = new Properties();

prop.put("mail.transport.protocol", "smtp");
prop.put("mail.smtp.host", host);
prop.put("mail.smtp.port", port);
// prop.put("mail.smtp.starttls.enable", "true");
prop.put("mail.smtp.auth", "true");
prop.put("mail.smtp.socketFactory.port", port);
prop.put("mail.smtp.socketFactory.class", "javax.net.ssl.SSLSocketFactory");
prop.put("mail.smtp.ssl.enable", "true");
```

당연히(?) 587 포트를 쓰지 않기 때문에 starttls 속성은 주석처리했다.
소스 이야기는 잠시 뒤로하고, 조금 더 필요한 이야기부터하자.

> 인증 정보 설정

```
465(SSL) 방식을 쓰거나 쓰고있다면 인증 정보 설정과 인증 정보 등록이 필요합니다.
SMTP 서버가 발신자의 신원을 확인하고 무단 (스팸) 사용을 방지 하기 위한 설정입니다.
이때 SMTP 서버는 인증된 사용자가 아닌 경우 요청을 거부합니다.
```

> [!TIP] SMTP와 SMTPS
> 465 (SSL/SMTPS) : SSL을 통해 암호화된 SMTP. 전송이 시작되기 전에 암호화 연결을 설정
> 587 (SMTP with STARTTLS) : 평문으로 연결한 후 STARTTLS 명령으로 암호화 연결을 시작

위와 같은 이유 때문에 SMTP 서버에서 메일 발송 요청을 하게 되는 우리 서비스의 경우 쿠버네티스 Pod 에서 요청을 하기 때문에 그 위치에서의 요청이 인증된 사용자로 등록이 되어있어야 합니다.

이 부분에서도 굉장히 뚜껑(?) 열릴뻔한게 그들은. SMTP 서버를 설정하고 관리하는 주체는 어떤 작업이 들어가야하는지 알고있음에도 실질적인 요청을 받지 않았기 때문에 아무런 조치도 해주지 않고 그냥 발송하면 됩니다. 라는식의 뻐꾸기 같은 답변만 해왔다. 내가 조금더 고수이거나 그들이 조금의 일말의 친절함을 배풀었다면, 인증이 안되어서 발송이 안될 수 있다라는 결론을 쉽게 도출했을 것이다.  

### 세번째 전송 프로토콜의 세부옵션

위에서 이미 한번 작성을 했기 때문에 별도의 설명 없이 바로 내용을 풀어본다하면

587(TLS) 방식을 쓰게 된다면 옵션 중 `mail.smtp.starttls.enable=true` 와 같은 설정을 하게 될 것이다.
465(SSL) 방식에는 `mail.smtp.auth=true` `mail.smtp.ssl.enable=true` 설정을 하게 될 것이고,
25(평문) 방식에서는 많은 옵션들이 생략가능하다.

한데, 이 또한도 알 수 없었고 어떤 것을 사용하는지 정보의 공유가 안되었던 상태에서 작업을 진행했기 때문에 여러 차례의 테스트베드가 필요했고 펑고하듯이 줬다 뺐다 하며 설정하게 되었다.

### 네번째 솔루션 아닌 해결

어쨌든 해결은 했다. 이 정도 스트레스 받았는데 해결도 못하면 뒤로 까부라져 뒈져버렸을 것이다.
하지만 잡설 보다 솔루션 아닌 해결 방법이 필요할지 모르니 지금 판단되는 가장 빠른 솔루션을 정리해보자.

```
1. SMTP 전송 정보의 검증은 가급적 웹사이트를 이용해서 빠르게 확인하자
2. 배포 프로세스가 있어 복잡성을 줄이기 위해 Python을 사용하자 (telnet 등의 방법도 있지만 더쉽다고 느껴짐)
3. 반드시 서비스하는 포트와 프로토콜 방식(25, 465, 587)을 확인받자
4. 프로토콜 방식에 따른 추가적인 설정을 인하자
```

사실 위 방법도 필요없이 가능하면 SMTP 서버를 관리하는 주체에 가이드라인을 받을 수 있다면 베스트겠다.
우린 1도 도움을 받거나 확인을 받을 수 없었다.

___

이렇게 감성적인(?) 화를 풀어 놓듯 작성한 글은 처음인데 후에 부끄럽거나 도움이 안된다고 판단되면 적게 쓰거나 삭제를 하고, 긍정적인 판단이 된다면 또 다른 컨텐츠 글을 추가 작성해볼 요량이다.
