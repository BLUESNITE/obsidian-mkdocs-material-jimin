기존 팀블로그 내 작성글 이관 

[Spring Boot Batch 설명 - 플래티어 연구소 테크 블로그 (tistory.com)](https://x2bee.tistory.com/22)
___
### 2. Spring Boot Batch 학습

이 게시물에서는 Spring Boot Batch를 작성할 때 핵심 요소 중 하나인

Reader의 다양한 유형에 대한 샘플 코드와 설명을 다루고 있습니다.

**유형**

- sampleFileJob
- sampleCompositeWriterJob
- sampleMyBatisCursorJob
- sampleJdbcCursorJob
- sampleJdbcPagingJob

---

#### 2.1. sampleFileJob

sampleFileJob은 reader에 FlatFileItemReader를 사용하여 CSV 파일을 조회하는 샘플입니다

```
@Bean
@StepScope
public FlatFileItemReader<SampleFileRequest> sampleFileReader() {
  String[] names = new String[] {"name", "description"};
  return new FlatFileItemReaderBuilder<SampleFileRequest>()
        .name("sampleFileRequest")
        .resource(new ClassPathResource("/csv/sample_data.csv"))
        .linesToSkip(1)
        .targetType(SampleFileRequest.class)
        .delimited().delimiter(",")
        .names(names)
        .build();
}
```

**FlatFileItemReaderBuilder 옵션**

- name : 키를 계산하는 데 사용되는 이름 (필수항목)
- resource : CSV 파일 Path
- linesToSkip : 파일을 시작 시 건너뛸 줄 수
- targetType : 반환될 클래스
- names : 순서대로 반환되는 필드 내의 각 필드 이름

#### 2.2. sampleCompositeWriterJob

simpleCompositeItemWriterJob과 다른 점은 중간 processor를 생략하지 않은 점입니다.

processor 처리 단계에서 잠재적으로 수정된 항목이나 새 항목을 반환하며,

이때 input은 SampleRequest이고 output은 SampleResponse로 변환되어 반환됩니다

```
@Bean
public ItemProcessor<SampleRequest, SampleResponse> sampleProcessor() {
  return batSampleCompositeService::processor;
}
```

#### 2.3. sampleMyBatisCursorJob

MybatisCursorItemReader와 MybatisBatchItemWriter를 사용한 예제입니다.

MybatisCursorItemReader는 setQueryId 속성으로 지정된 쿼리를 실행하여 selectCursor() 메서드를 사용하여 요청된 데이터를 검색합니다.

read() 메서드가 호출될 때마다 cursor의 다음 요소를 반환하며, 요소가 더 이상 남아 있지 않을 때까지 반복합니다.

MybatisBatchItemWriter는 모든 아이템을 배치로 구문을 일괄 실행하기 위해 sqlSessionTemplate에서 배치 작업을 처리하는 writer입니다.

write() 메서드가 호출될 때 실행될 매핑 구문 아이디를 제공해야 합니다

```
@Resource(name = "dbRodbSqlSessionFactory")
private final SqlSessionFactory dbRodbSqlSessionFactory;
    
@Resource(name = "dbRwdbSqlSessionFactory")
private final SqlSessionFactory dbRwdbSqlSessionFactory;

@Bean
public MyBatisCursorItemReader<SampleRequest> sampleMyBatisCursorItemReader() {
  Map<String, Object> parameterValues = new HashMap<>();
  return new MyBatisCursorItemReaderBuilder<SampleRequest>()
        .sqlSessionFactory(dbRodbSqlSessionFactory)
        .queryId("....sample.BatSampleMapper.selectSampleList")
        .parameterValues(parameterValues)
        .build();
}

@Bean
public ItemWriter<SampleRequest> sampleMyBatisBatchItemWriter() {
  return new MyBatisBatchItemWriterBuilder<SampleRequest>()
        .sqlSessionFactory(dbRwdbSqlSessionFactory)
        .assertUpdates(false)
        .itemToParameterConverter(item -> {
          Map<String, Object> parameter = new HashMap<>();
          parameter.put("sysModrId", "BATCH");
          parameter.put("name", item.getName());
          return parameter;
        })
        .statementId("....sample.BatSampleTrxMapper.updateSample")
        .build();
}
```

#### 2.4. sampleJdbcCursorJob

JdbcCursorItemReaderBuilder와 JdbcBatchItemWriterBuilder를 사용한 예제입니다.

이 예제는 대용량 처리 퍼포먼스를 최대화하기 위해 JDBC 사용을 중점적으로 다루며,

쿼리를 직접 작성하는 대신 iBatis Map을 읽어와서 적용하는 샘플입니다.

```
@Bean
@StepScope
public JdbcCursorItemReader<SampleRequest> sampleJdbcReader() {
    DataSource dbRodbDataSource = (DataSource) ApplicationContextWrapper.getBean("dbRodbDataSource");
    HashMap<String, Object> queryMap = new HashMap<>();
    queryMap.put("name", "James");
    queryMap.put("sysRegrId", "SYSTEM");

    BoundSql boundSql = dbRodbSqlSessionFactory.getConfiguration().getMappedStatement("selectSampleJdbcList").getBoundSql(queryMap);
    return new JdbcCursorItemReaderBuilder<SampleRequest>()
            .name("jdbcCursorItemReader")
            .dataSource(dbRodbDataSource)
            .sql(boundSql.getSql())
            .rowMapper(new BeanPropertyRowMapper<>(SampleRequest.class))
            .preparedStatementSetter(new ArgumentPreparedStatementSetter((getQueryValues(boundSql))))
            .fetchSize(1000)
            .maxItemCount(1000) // 조회할 최대 아이템 수
            .maxRows(1000) // ResultSet이 포함할 수 있는 최대 row 수
            .build();
}
```

Spring Batch에서 제공되는 JdbcCursorItemReader구현체로 DataSource로부터 얻은 연결을 통하여 SQL문을 실행하고

이를 ResultSet을 이용하여 커서 기반으로 데이터를 가져옵니다. JdbcCursorItemReader는 JdbcCursorItemReaderBuilder을 통하여 생성 할 수 있으며 예제는 위와 같습니다.

**JdbcBatchItemWriterBuilder 속성**

- assertUpdates : true이면 모든 아이템이 삽입이나 수정되었는지 검증합니다. 적어도 하나의 항목이 행을 업데이트 하거나 삭제하지 않을경우 예외 throw를 할지 설정
- beanMapped : POJO 기반으로 insert SQL의 Values를 매핑
- itemPreparedStatementSetter : 작성자가 직접 구성, columnMapped가 호출되지 않은 경우에만 사용가능

```
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

여기서 위의 getQueryValues 함수를 사용하지 않고, QueryValues를 파라미터를 나열하여 세팅해도 무방합니다.

```
.preparedStatementSetter(new ArgumentPreparedStatementSetter(new String[]{"aaa", "bbb"}))
```

```
@Bean // beanMapped()을 사용할때는 필수
public JdbcBatchItemWriter<SampleRequest> jdbcBatchItemWriter() {
    DataSource dbRwdbDataSource = (DataSource) ApplicationContextWrapper.getBean("dbRwdbDataSource");
    BoundSql boundSql = dbRwdbSqlSessionFactory.getConfiguration().getMappedStatement("updateSample2").getBoundSql(new SampleRequest());
    String sql = boundSql.getSql();
    return new JdbcBatchItemWriterBuilder<SampleRequest>()
            .dataSource(dbRwdbDataSource)
            .assertUpdates(true)
            .sql(sql)
            .itemPreparedStatementSetter((item, ps) -> {
                ps.setString(1, "SYSTEM");
                ps.setString(2, item.getName());
            })
            // .beanMapped()
            .build();
}
```

**JdbcBatchItemWriterBuilder 속성**

- assertUpdates : true이면 모든 아이템이 삽입이나 수정되었는지 검증합니다. 적어도 하나의 항목이 행을 업데이트 하거나 삭제하지 않을경우 예외 throw를 할지 설정
- beanMapped : POJO 기반으로 insert SQL의 Values를 매핑
- itemPreparedStatementSetter : 작성자가 직접 구성, columnMapped가 호출되지 않은 경우에만 사용가능

#### 2.5. sampleJdbcPagingJob

JdbcPagingItemReaderBuilder와 PagingQueryProvider를 사용한 예제입니다.

이 예제는 다른 Job과의 차이를 확인 하기 위해 주로 다루고 있습니다.

jdbc 페이징 설정이 중점적이며, SqlPagingQueryProviderFactoryBean을 통해서 쿼리를 작성하게 됩니다.

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
```

**JdbcPagingItemReaderBuilder 속성**

- pageSize : 페이지/쿼리당 요청할 레코드 수
- currentItemCount : 현재 항목의 색인으로, 다시 시작할 때 어디에서 시작할지 나타내기 위해 사용
- maxItemCount : 읽을 항목의 최대 개수를 구성
- fetchSize : 각 가져오기로 반환할 레코드 수에 대한 기본 RDBMS에 대한 힌트
- dataSource : (필수) 쿼리를 수행할 DataSource
- rowMapper : (필수) 쿼리 결과를 객체에 매핑하는 데 사용되는 Mapper
- queryProvider : 필요한 쿼리를 제공하기 위한 PagingQueryProvider
- name : Key를 계산하는데 사용되는 이름

```
@Bean
public PagingQueryProvider queryProvider(DataSource dbRodbDataSource) {
    String strDtm = "20201117 00:00:00";
    SqlPagingQueryProviderFactoryBean queryProvider = new SqlPagingQueryProviderFactoryBean();
    queryProvider.setDataSource(dbRodbDataSource);

    queryProvider.setSelectClause("*");
    queryProvider.setFromClause("from sample_mb");
    queryProvider.setWhereClause("mbr_join_dtm > TO_TIMESTAMP('"+strDtm+"', 'YYYYMMDD HH24:MI:SS')");

    Map<String, Order> sortKeys = new HashMap<>(1);
    sortKeys.put("mbr_no", Order.ASCENDING);
    queryProvider.setSortKeys(sortKeys);

    try {
        return queryProvider.getObject();
    } catch (Exception e) {
        return null; // 의도 exception 세팅
    }
}
```

**SqlPagingQueryProviderFactoryBean 속성**

- dataSource : 설정할 dataSource
- selectClause : SQL 쿼리 문자열의 select 절
- fromClause : SQL 쿼리 문자열의 from 절
- whereClause : SQL 쿼리 문자열의 where 절
- groupClause : SQL 쿼리 문자열의 SQL GROUP BY 절
- sortKeys : sort를 설정할 sortKeys