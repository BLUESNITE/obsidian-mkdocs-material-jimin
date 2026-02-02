> [!CHECK] 와탭 주요포인트 확인
> package.json dependencies ("whatap": "^0.5.6")

*.env.{dev/stg/prd}.set*

```
WHATAP_ENABLED=N
WHATAP_PROJECTACCESSKEY=
WHATAP_PCODE=37521
WHATAP_SAMPLERATE=100

WHATAP_LICENSE=
WHATAP_SERVER_HOST=
WHATAP_SERVER_PORT=6600
```

*next.config.js*

contentSecurityPolicy

```
script-src repo.whatap-browser-agent.io/rum/prod/
connect-src rum-ap-northeast-2.whatap-browser-agent.io
```

env: *ConfigProvider 설정이 필요한 곳에서 환경변수를 사용하기위한 설정*

```
  env: {
    WHATAP_ENABLED: process.env.WHATAP_ENABLED,
    WHATAP_PROJECTACCESSKEY: process.env.WHATAP_PROJECTACCESSKEY,
    WHATAP_PCODE: process.env.WHATAP_PCODE,
    WHATAP_SAMPLERATE: process.env.WHATAP_SAMPLERATE,
    WHATAP_LICENSE: process.env.WHATAP_LICENSE,
	WHATAP_SERVER_HOST: process.env.WHATAP_SERVER_HOST,
	WHATAP_SERVER_PORT: process.env.WHATAP_SERVER_PORT,
  }
```

webpack

```
  webpack: (config, { isServer }) => {
    if (isServer) {
      config.externals = [...config.externals, 'whatap']
    }
    return config
  },
```

___

**Node 프로젝트의 경우 deployment.yaml에서 변수 주입까지 확인 필요**

```
spec:
	template:
		spec:
			containers:
				-name: {application.name}
				 env:
					- name:
					  value: 
		            - name: whatap.name
		              valueFrom:
		                fieldRef:
		                  fieldPath: metadata.name
		            - name: WHATAP_JAVA_AGENT_PATH
		              value: "/app/whatap.agent-2.2.67.jar"
		            - name: OKIND
		              value: "{{ .Values.application.name }}"
		            - name: WHATAP_OKIND
		              value: "{{ .Values.application.name }}"
		            {{ if eq .Values.application.namespace "aaa-stg" }}
		            - name: license
		              value: "x210gdopq8lpb-z7f3s1ko6ihhqb-x40suulp55afbr"
		            - name: whatap.server.host
		              value: "10.100.0.22"
		            {{ end }}
		            {{ if eq .Values.application.namespace "aaa-prd" }}
		            - name: license
		              value: "x20ogpd6482ug-x7bus2kh2mf5p2-x276fissh5mg4q"
		            - name: whatap.server.host
		              value: "10.100.0.22"
		            {{ end }}
		            - name: whatap.micro.enabled
		              value: "true"
```

**위 설정까지가 기본적인 환경 셋업**

소스파일 적용 (*configProvider.tsx* , *server.ts* )

*configProvider.tsx* (project /src/lib/providers/ConfigProvider.tsx )

- 클라이언트측 RUM (RUM = Real User Monitoring)

```
export const ConfigContext = createContext<object>({
  uuid: '',
});
export default function ConfigProvider({ children }) {
  const configState = setInitData();

  useEffect(() => {
    const whatapEnabled = process.env.WHATAP_ENABLED;
    if (whatapEnabled === 'Y') {
      const projectAccesskey = process.env.WHATAP_PROJECTACCESSKEY;
      const pCode = process.env.WHATAP_PCODE;
      let sampleRate = process.env.WHATAP_SAMPLERATE;
      if (isNaN(Number(sampleRate)) || (Number(sampleRate) < 0 || Number(sampleRate) > 100)) {
        sampleRate = String(100);
      }
      const script = document.createElement('script');
      script.innerHTML = `
      (function (w, h, _a, t, a, b) {
        w = w[a] = w[a] || {
          config: {
            projectAccessKey: "${projectAccesskey}",
            pcode: ${pCode},
            sampleRate: ${sampleRate},
            proxyBaseUrl: "https://rum-ap-northeast-2.whatap-browser-agent.io/",
          },
        };
        a = h.createElement(_a);
        a.async = 1;
        a.src = t;
        t = h.getElementsByTagName(_a)[0];
        t.parentNode.insertBefore(a, t);
      })(window, document, 'script', 'https://repo.whatap-browser-agent.io/rum/prod/v1/whatap-browser-agent.js', 'WhatapBrowserAgent', '');
    `;
      document.head.appendChild(script);

      return () => {
        document.head.removeChild(script);
      };
    }
  });

  return (
    <ConfigContext.Provider value={configState}>
      {children}
    </ConfigContext.Provider>
  );
}
```

*server.ts* (project /루트 )

- Node 프로세스가 시작될때 Whatap 모듈을 로딩
- Node APM 에이전트는 보통 앱 초기 부팅부터 로딩돼야 (먼저) http db 등을 후킹해서 트레이싱 가능
- 서버측 APM

```
require("whatap");

const WhatapAgent = require('whatap').NodeAgent;

const {createServer} = require('http')
const {parse} = require('url')
const next = require('next')

const dev = process.env.NODE_ENV
const hostname = 'localhost'
const port = 3000

const app = next({dev, hostname, port})
const handle = app.getRequestHandler()

process.env.WHATAP_NAME = "aaa-fo-{ip2}-{ip3}"
process.env.WHATAP_SERVER_PORT="6600"

app.prepare().then(() => {
    createServer(async (req, res) => {
        try {
            const parsedUrl = parse(req.url, true)
            const {pathname, query} = parsedUrl

            /**
            * Render the page.
            */
            await handle(req, res, parsedUrl);
        } catch (err) {
            console.error('Error occurred handling', req.url, err)
            res.statusCode = 500
            res.end('internal server error')
        }
    })
    .once('error', (err) => {
        console.error(err)
        process.exit(1)
    })
    .listen(port, () => {
        console.log(`> Ready on http://${hostname}:${port}`)
    })
})
```