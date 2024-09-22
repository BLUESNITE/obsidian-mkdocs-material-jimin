> [!INFO] 설명
> Qdrant. 효율적이고, 확장 가능하며, 빠릅니다.
> Qdrant는 가장 진보된 벡터 데이터베이스로, 최고 수준의 RPS(초당 처리량), 최소한의 지연 시간, 빠른 인덱싱, 높은 정확도와 제어력을 제공하며 그 외에도 다양한 기능을 갖추고 있습니다.

![[Pasted image 20240920162109.png]]
### Qdrant는 어떻게 작동하나요?

1. 먼저 모든 데이터를 저장할 [컬렉션을](https://api.qdrant.tech/api-reference/collections/create-collection) 만들어야 합니다.
2. 그런 다음 데이터 [포인트를](https://api.qdrant.tech/api-reference/points/upsert-points) upsert하고 사용자 지정 [페이로드](https://api.qdrant.tech/api-reference/points/set-payload)로 보강합니다.
3. 전체 컬렉션을 사용하면 [검색을](https://api.qdrant.tech/api-reference/search/points) 실행하여 관련 결과를 찾을 수 있습니다.
4. 컬렉션은 [스냅샷을 생성하고, 다운로드하고, 복원](https://api.qdrant.tech/api-reference/snapshots/list-snapshots)할 수 있습니다.
5. 준비가 되면 프로덕션을 위한 [분산 시스템을](https://api.qdrant.tech/api-reference/distributed/create-shard-key) 설정합니다.

**Docker**
```
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./qdrant_storage:/qdrant/storage:z
```

**EndPoint**
```
- REST API: http://192.168.2.165:6333/
- Web UI: http://192.168.2.165:6333/dashboard
- GRPC API: http://192.168.2.165:6334/
```

