기존 팀블로그 내 작성글 이관 

[Spring Boot Batch 성능을 최적화하기 위한 Reader - 플래티어 연구소 테크 블로그 (tistory.com)](https://x2bee.tistory.com/27)
___

**Introduction**

[[Spring Boot Batch 설명](https://x2bee.tistory.com/22)] 게시물을 통해 구조와 설명을 확인한 후,

이 게시물에서는 Spring Boot Batch에서 성능을 최적화하기 위한 Reader를 구현하는 방법과 설명을 다루고 있습니다.

---

### 3.1. 최적화하기 위한 Reader 유형 소개

Reader는 데이터를 효율적으로 읽어오고, 처리 속도를 최적화해야 합니다.

데이터 양이 많고 복잡한 상황에서도 뛰어난 성능을 유지할 수 있도록 고려하여 Reader를 구성해야합니다.

#### 3.1.1. 성능을 최적화하기 위한 세 가지 Reader 설명

**JdbcPagingItemReader**

- JDBC를 기반으로 하는 데이터베이스에서 페이지별로 데이터를 읽어오는 데 특화된 Reader
- 주로 대용량의 데이터를 처리할 때 사용되며, 페이지 단위로 데이터를 읽어오므로 메모리 사용을 효율적으로 관리 가능
- Spring Batch에서 제공하는 페이징 쿼리를 실행하여 데이터를 읽어옴

**JdbcCursorItemReader**

- JDBC 커서를 활용하여 데이터베이스에서 데이터를 읽어오는 Reader
- 커서를 사용하므로 데이터를 한 번에 메모리에 로드하지 않고, 필요할 때마다 데이터를 가져와 처리 
- 대용량 데이터 처리 및 성능 최적화에 적합하며, 대량의 데이터를 메모리에 로딩하지 않기 때문에 메모리 효율적

**MyBatisCursorItemReader**

- MyBatis와 Spring Batch를 통합하여 데이터를 커서 방식으로 읽어오는 데 사용
- MyBatis SQL Mapper를 사용하여 데이터베이스 쿼리를 실행하고, 커서를 활용하여 데이터를 순차적으로 가져옴
- MyBatis의 강력한 객체 관계 매핑(ORM) 기능과 함께 사용할 수 있으며, 데이터베이스와의 상호작용을 효과적으로 관리 

### 3.2. 커스텀 Reader 작성

**QuerydslNoOffsetPagingItemReader (Custom Reader)**

- Spring Batch 프레임워크에서는 공식적으로 QueryDslItemReader를 지원하지 않는 점을 고려
- 이 방식은 JpaPagingItemReader에서 JPQL이 수행되는 부분을 중점적으로 교체
- doReadPage에서 entityManager.getTranscation을 제거  
    (제거해도 Chunk 단위로 트랜잭션이 보장되고 있기 때문에 결과적으로도 트랜잭션 관리 잘 작동됨)
- 기초적 데이터베이스 페이징 쿼리들은 offset 값이 커질수록 느리다는 점을 개선의 중점으로 둠
- order by, group by를 PK이외에 다른 기준으로 복잡하게 사용해야 한다면 비권장

**장점**

- offset 성능 이슈를 해결하기 위해 offset 없이 페이징 할 수 있는 빠른성능의 Reader
- querydsl의 타 안정성, 자동완성, 컴파일 단계 문법체크, 공백 이슈 대응 등의 장점을 모두 지원

**단점**

- Spring Batch 프레임워크에서 지원하지 않는 점
- 복잡한 데이터베이스 쿼리를 쓰게 된다면 활용하기 어려움

### 3.3. 실제 예제와 테스트

ItemWriter는 모두 동일한 형태

#### 3.3.1. 예제 1 - JdbcPagingItemReader

```
    @Bean
    public JdbcPagingItemReader<SampleRequest> sampleJdbcPagingReader(DataSource dbRodbDataSource) {
        return new JdbcPagingItemReaderBuilder<SampleRequest>()
        .pageSize(PAGE_SIZE)
        .currentItemCount(0)
        // .maxItemCount(CHUNK_SIZE)
        // .fetchSize(FETCH_SIZE)
        .dataSource(dbRodbDataSource)
        .rowMapper(new BeanPropertyRowMapper<>(SampleRequest.class))
        .queryProvider(queryProvider(dbRodbDataSource))
        .name("jdbcPagingItemReader")
        .build();
    }
    
    @Bean
    public PagingQueryProvider queryProvider(DataSource dbRodbDataSource) {
        String strDtm = "20201117 00:00:00";
        SqlPagingQueryProviderFactoryBean queryProvider = new SqlPagingQueryProviderFactoryBean();
        queryProvider.setDataSource(dbRodbDataSource);

        queryProvider.setSelectClause("*");
        queryProvider.setFromClause("from sample_mbr_base");
        queryProvider.setWhereClause("mbr_join_dtm > TO_TIMESTAMP('"+strDtm+"', 'YYYYMMDD HH24:MI:SS')");

        Map<String, Order> sortKeys = new HashMap<>(1);
        sortKeys.put("mbr_no", Order.ASCENDING);
        queryProvider.setSortKeys(sortKeys);

        try {
            return queryProvider.getObject();
        } catch (Exception e) {
            return null; // exception 세팅
        }
    }
```

#### 3.3.1. 예제 2 - JdbcCursorItemReader

```
@Bean
@StepScope
public JdbcCursorItemReader<SampleRequest> sampleJdbcReaderTest(@Value("#{jobParameters[strDtm]}") String strDtm) {
    DataSource dbRodbDataSource = (DataSource) ApplicationContextWrapper.getBean("dbRodbDataSource");
    HashMap<String, Object> queryMap = new HashMap<>();
    queryMap.put("mbr_join_dtm", strDtm);

    BoundSql boundSql = dbRodbSqlSessionFactory.getConfiguration().getMappedStatement("selectSampleList3").getBoundSql(queryMap);
    return new JdbcCursorItemReaderBuilder<SampleRequest>()
            .name("jdbcCursorItemReader")
            .dataSource(dbRodbDataSource)
            .sql(boundSql.getSql())
            .rowMapper(new BeanPropertyRowMapper<>(SampleRequest.class))
            .preparedStatementSetter(new ArgumentPreparedStatementSetter((getQueryValues(boundSql))))
            .fetchSize(1000)
            // .maxItemCount(1000) // 조회할 최대 아이템 수
            // .maxRows(1000) // ResultSet이 포함할 수 있는 최대 row 수
            .build();
}

@SuppressWarnings("unchecked")
private Object[] getQueryValues(BoundSql boundSql) {
    HashMap<String, Object> queryParameter = (HashMap<String, Object>) boundSql.getParameterObject();
    Object[] queryValues = new Object[queryParameter.size()];
    Iterator<ParameterMapping> iterator = boundSql.getParameterMappings().iterator();
    int index = 0;
    while(iterator.hasNext()){
        ParameterMapping pm = iterator.next();
        for (Entry<String, Object> key : queryParameter.entrySet()) {
            if(key.getKey().equals(pm.getProperty())){
                queryValues[index] = key.getValue();
                index++;
                break;
            }
        }
    }
    return queryValues;
}
```

#### 3.3.1. 예제 3 - MyBatisCursorItemReader

```
@Bean
@StepScope
public MyBatisCursorItemReader<SampleRequest> sampleMyBatisCursorItemTestReader(@Value("#{jobParameters[strDtm]}") String strDtm) {
    Map<String, Object> parameterValues = new HashMap<>();
    parameterValues.put("mbr_join_dtm", strDtm);
    return new MyBatisCursorItemReaderBuilder<SampleRequest>()
            .sqlSessionFactory(dbRodbSqlSessionFactory)
            .queryId("....rodb.sample.BatSampleMapper.selectSampleList3")
            .parameterValues(parameterValues)
            .build();
}
```

#### 3.3.1. 예제 4 - QuerydslNoOffsetPagingItemReader 

```
@Bean
@StepScope
public QuerydslNoOffsetPagingItemReader<QuerydslEntity> sampleQuerydslNoOffsetPaginItemReader(@Value("#{jobParameters[strDtm]}") String strDtm) {

    // localDateTime 세팅
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyyMMdd HH:mm:ss");
    LocalDateTime dateTime = LocalDateTime.parse(strDtm, formatter);

    // 1. No Offset 옵션 (QuerydslNoOffsetNumberOptions, QuerydslNoOffsetStringOptions)가 있음
    QuerydslNoOffsetStringOptions<QuerydslEntity> options = new QuerydslNoOffsetStringOptions<>(querydslEntity.mbrNo, QuerydslReaderExpression.ASC);

    // 2. Querydsl
    return new QuerydslNoOffsetPagingItemReader<>(entityManagerFactory, CHUNK_SIZE, options, queryFactory -> queryFactory
            .selectFrom(querydslEntity)
            .where(querydslEntity.mbrJoinDtm.after(dateTime))
        );
}
```

- QuerydslNoOffsetPagingItemReader의 경우는 추가 상세 설명이 필요하나, 아래 참고 URL 보고도 확인이 가능

```
select 
	q1_0.mbr_no,q1_0.addr,q1_0.email,q1_0.login_id,q1_0.mbr_join_dtm,q1_0.mbr_nm
from sample_mbr_base q1_0 
where q1_0.mbr_join_dtm>'09/10/2022 00:00:00.000' 
	and (q1_0.mbr_no>'101188418' and q1_0.mbr_no<='999999999')
order by q1_0.mbr_no fetch first 1000 rows only;
```

No Offset 옵션을 mbr_no로 주어 동작된 쿼리 모습

### 3.4. 결론

Spring Boot Batch에서 Reader를 선택하고 구성하는 것은 배치 성능 최적화에 매우 중요합니다.  
각 Reader 유형은 고유한 장점과 단점이 있으며, 대용량 데이터 처리에 큰 영향을 미칩니다. 따라서 Reader를 선택할 때에는 다양한 요소를 고려해야합니다. 특히, 커스텀 Reader를 작성하여 성능 최적화를 달성하는 것도 가능합니다.

위 과정에서 Spring Boot Batch의 Reader에 대한 이해를 높이고 성능을 최적하는데 도움이 되는 자료가 되었으면 좋겠습니다. 실제 데이터를 사용한 테스트 결과를 제시하지는 않았지만, 글의 구성에서 눈치 채신 대로 가장 우수한 성능을 보인 것은 커스텀 Reader로써 QueryDslNoOffsetPagingItemReader였습니다. 다음순위로는 MybatisCursorItemReader, JdbcCursorItemReader 그리고 JdbcPagingItemReader가 있었으며, 이 순서는 대상 데이터와 테스트 환경에 따라 약간 다를 수 있습니다. Reader를 선택하고 구성하는 것은 배치 작업에 중요한 결정 사항 입니다. 이 글이 Reader를 효과적으로 선택하고 구성하는 데 도움이 되었으면 좋겠습니다.

### 3.5. 참고 자료

사실 아래 링크는 참고 자료 수준이 아니고, 거의 전부를 긁어다가 적용했습니다.

> [Spring Batch와 Querydsl | 우아한형제들 기술블로그 (woowahan.com)](https://techblog.woowahan.com/2662/)

이외 기타 학습 링크

> [Spring boot :: QueryDSL을 사용해서 No Offset Paging 구현하기 (tistory.com)](https://wave1994.tistory.com/159)  
> [[if kakao 2022] Batch Performance를 고려한 최선의 Reader | 카카오페이 기술 블로그 (kakaopay.com)](https://tech.kakaopay.com/post/ifkakao2022-batch-performance-read/)