> [!NOTE] 설명
> k-NN 플러그인을 활성화하거나 비활성화합니다.
> 네이티브 라이브러리 인덱스 생성에 사용되는 스레드 수입니다. 이 값을 낮게 유지하면 k-NN 플러그인의 CPU 영향이 줄어들지만 인덱싱 성능도 저하됩니다.

```
PUT _cluster/settings
{
 "persistent": {
   "knn.algo_param.index_thread_qty": 4,
   "knn.plugin.enabled": true
 }
}
```
