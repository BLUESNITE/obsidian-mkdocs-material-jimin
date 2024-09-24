기존 팀블로그 내 작성글 이관 

[Spring Boot Batch 설명 - 플래티어 연구소 테크 블로그 (tistory.com)](https://x2bee.tistory.com/22)
___
## 1. Spring boot batch 설명

Spring Batch는 대규모 일괄 처리 프로그램 개발을 위한 가벼우면서 포괄적인 개발 프레임워크입니다.  
Spring Batch는 로깅/추적, 트랜잭션 관리, 작업 처리 통계, 작업 재시작, 건너뛰기, 그리고 리소스 관리와 같이 대량의 레코드를 처리하는 데 필요한 재사용 가능한 핵심 기능을 제공합니다. 또한 최적화 및 파티셔닝 기술을 활용하여 고성능 배치 작업을 효과적으로 수행할 수 있는 고급 기술과 기능을 제공합니다.  
  

### 1.1. Spring batch 프로그램 구조

Spring Batch 프로그램 구조를 Tasklet 기반과 Chunk 기반으로 두 가지 방법으로 나누어 아래와 같이 설명할 수 있습니다.

**Chunk 기반**

한 번에 하나씩 데이터(row)를 읽어 Chunk라는 덩어리를 만든 뒤, Chunk 단위로 트랜잭션을 다루는 것입니다.

즉, 한 번에 모든 행을 읽고 처리하고 쓰는 대신, 한 번에 고정 된 양의 레코드(청크)를 읽고 처리하는 방식입니다.

Chunk 단위로 트랜잭션을 수행하기 때문에 실패할 경우엔 해당 Chunk 만큼만 롤백이 되고, 이전에 커밋된 트랜잭션 범위까지는 반영이 됩니다. 일괄 데이터 변경이나 어떤 데이터 변화를 주는 작업에 사용하면 좋습니다.

아래는 Chunk 이해를 돕기 위한 예시와 설명입니다.

> Paging Size가 5이며 Chunk Size가 10일 경우 2번의 Read가 이루어진 후에 1번의 Transaction이 수행됩니다.  
> 이는 한번의 Transaction을 위해 2번의 쿼리 수행이 발생하게 됩니다.

이에 따른 적절한 Chunk Size에 대해 Spring Batch에는 다음과 같이 적혀 있습니다.

> Setting a fairly large page size and using a commit interval that matches the page size should provide better performance.  
> 페이지 크기를 상당히 크게 설정하고 페이지 크기와 일치하는 커밋 간격을 사용하면 성능이 향상됩니다.

이와 같이 두 설정의 값을 일치를 시켜주는게 가장 좋은 성능 향상 방법이며 Chunk를 고려해서 Job 구성을 해야합니다.

Chunk를 사용한 방법은 Read 된 Chunk 단위로 트랜잭션을 수행하기 때문에 실패할 경우엔 해당 Chunk 만큼만 롤백이 되고, 이전에 커밋된트랜잭션 범위까지는 반영이 됩니다.

**Chunk 처리의 3가지의 구성요소**

1. ItemReader
2. ItemProcessor
3. ItemWriter

**Tasklet 기반**

단계 내에서 단일 태스크를 수행하기 위한 것으로 임의의 Step을 실행할 때 읽기/처리/쓰기를 하나의 작업으로 처리하는 방식입니다.

즉, 각 단계는 하나의 정의된 작업만 수행해야합니다.

Step이 중지될 때까지 execute 메서드가 계속 반복해서 수행하고 수행할 때마다 독립적인 트랜잭션이 얻어집니다.

초기화, 저장 프로시저 실행, 알림 전송과 같은 Job에서 일반적으로 사용됩니다.

tasklet 클래스가 재사용이 될 수 있는 상황에 적합합니다. (Job 구성 클래스 내부에 tasklet 구현부를 넣어서 하나의 클래스로 하나의 업무를 정의하는 방식)

### 1.2. Job Configuration 클래스 작성

Job Configuration 클래스 작성은 Spring Batch 개발에 대한 영역입니다.

**Summary**

- 현재 Java LTS 버전인 17부터 지원합니다
- StepBuilderFactory, JobBuilderFactory가 Deprecated 되었으며 JobRepository를 명시적으로 사용하도록 권장하고 있습니다.
- TransactionManager 또한 명시적으로 사용하도록 권장합니다.
- @EnableBatchProcessing을 더 이상 사용하지 않아도 된다. (혹은 않아야 한다.)

위와 같은 방식으로 작성 방법을 설명하며,

이 문서에서는 복합 처리 패턴인 CompositeItemWriter 방식으로 작성되었습니다.

```
@Configuration
@RequiredArgsConstructor
@Slf4j
public class SimpleJobConfig{
    private final JobRepository jobRepository;
    private final PlatformTransactionManager transactionManager;
	...
}
```

기존에 사용되었던, JobBuilderFactory와 StepBuilderFactory는 더 이상 사용되지 않고,

JobRepository와 TransactionManager를 명시적으로 사용합니다.

#### 1.2.1. Job 생성

JobBuilder를 통해서 Job을 생성합니다

```
@Bean
public Job simpleComposItemWriterJob() {
  return new JobBuilder("simpleComposItemWriterJob", jobRepository)
        .start(simpleComposItemWriterStep())  // Step 설정
        .incrementer(new UniqueRunIdIncrementer()) // 중복실행허용
        .build();
}
```

1) 일반적인 업무에서는 하나의 Step을 구성하고, 업무복잡성에 따라 nextStep을 구성 할 수 있습니다

2) incrementer를 사용하여 중복실행 관리 할 수 있습니다.

3) jobBuilder validator 속성을 사용하여 실행에 필요한 파라미터를 검증 할 수 있습니다

```
new JobBuilder("simpleComposItemWriterJob", jobRepository)
  .start(simpleComposItemWriterStep())
  .validator(new JobParametersValidator() {
                @Override
                public void validate(JobParameters parameters) throws JobParametersInvalidException {
                  ...
                  Job 실행에 필요한 파라미터를 검증
                  ...
                }
            })
  .build();
```

#### 1.2.2. Step 생성

Step에는 Tasklet, Chunk 기반으로 2가지 방법을 사용 할 수 있습니다

StepBuilder를 통해서 Step을 생성합니다

```
@Bean
public Step simpleComposItemWriterStep() {
  return new StepBuilder("simpleComposItemWriterStep", jobRepository)
        .<SampleRequest, SampleRequest>chunk(CHUNK_SIZE, transactionManager)
        .reader(simpleItemReader())
        //processor 생략
        .writer(simpleCompositeItemWriter())
        .build();
}
```

- reader : 다양한 인터페이스 구현이 가능하며, 위에서는 데이터를 조회합니다
- processor : 읽어온 Item 데이터를 처리 가공합니다. processor는 배치를 처리하는 필수 요소는 아니며  
    Reader, Writer, Processor 처리를 명확하게 구분하고자 할때 작성합니다  
    processor 처리시에, .<SampleRequest, SampleResponse>chunk(CHUNK_SIZE, transactionManager)와 같이 구성하여 dto 관리를 합니다  
    위에서는 불필요한 메모리 소모를 최소화하기 위해 생략하여 작성되었습니다
- writer : 처리된 데이터를 Writer 결과물에 따라 Insert Update Send가 될 수도 있습니다  
    기본적으로 Item을 Chunk로 묶어 처리합니다

위와 같이 Step 실행 시 호출될 reader/processor/writer를 지정합니다.

그리고 처리 시 트랜잭션 처리 단위(chunk)를 지정하고, Exception 발생 시 오류견딤 처리(faultTolerant(), skip(), skipLimit())등을 지정 할 수 있습니다

#### 1.2.3. Chunk 기반의 reader/processor/writer 생성

```
/*
* ItemReader는 Step에서 Item을 읽어오는 인터페이스
* ItemReader에 대한 다양한 인터페이스가 존재
*/
@Bean
@StepScope
public ItemReader<SampleRequest> simpleItemReader() {
  return new ListItemReader<>(batSampleCompositeService.reader());
}

/*
* ItemProcessor에서 읽어온 SampleRequest dto를 가공하여 SampleResponse로 변환하여 반환
* 본 문서에서는 생략
*/
//@Bean
//public ItemProcessor<SampleRequest, SampleResponse> sampleProcessor() {
//    return batSampleItemWriterService::processor;
//}

/*
* ItemWriter 중에서도 CompositeItemWriter로 구성
* CompositeItemWriter Delegates에 처리 함수들을 세팅하여 복합처리 가능능
*/
@Bean
public ItemWriter<SampleRequest> simpleCompositeItemWriter() {
  CompositeItemWriter<SampleRequest> compositeItemWriter = new CompositeItemWriter<>();
  compositeItemWriter.setDelegates(Arrays.asList(simpleUpdateService()/* , sampleUpdateService2() */));
  return compositeItemWriter;
}
    
@Bean
public ItemWriter<SampleRequest> simpleUpdateService() {
  return sampleList -> sampleList.forEach(batSampleCompositeService::writer2);
}
```

위 예제 소스에서는 최소화된 ListItemReader에 CompositeItemWriter가 사용 되었습니다.

reader/writer는 용도에 맞게 생성해야 합니다. processor 또한 불필요하다면 생략 가능합니다.

#### 1.2.4. Tasklet 기반의 Step 작성

```
// StepBuilderFactory를 통해서 Step을 생성
@Bean
@JobScope
public Step sampleParamStep() {
	return new JobBuilder("sampleParamStep", jobRepository)
                .start(sampleParamTasklet(null))  // Step 설정
                .incrementer(new UniqueRunIdIncrementer()) // 중복실행허용
                .build();
}

@Bean
@JobScope
public SampleParamTasklet sampleParamTasklet(
		@Value("#{jobParameters[sampleParam]}") String sampleParam) {
	return new SampleParamTasklet(sampleParam);
}
```

Tasklet을 사용하려면 Step 작성시 호출될 Tasklet을 설정합니다.

```
public class SampleParamTasklet implements Tasklet {

	@Autowired
	private SampleService sampleService;

	private String sampleParam;

	public SampleParamTasklet(String sampleParam) {
		this.sampleParam = sampleParam;
	}

	@Override
	public RepeatStatus execute(
			StepContribution contribution, ChunkContext chunkContext)
			throws Exception {
		List<Sample> list = sampleService.getSampleList(new Sample());
		for (Sample sample : list) {
			Log.info("!!!!!! executed tasklet !!!!!!: {}, sampleParam: {}", sample, sampleParam);
		}
		return RepeatStatus.FINISHED;
	}
}
```

Tasklet 클래스는 Tasklet 인터페이스를 구현하여 작성합니다.

단일 메소드인 execute 메소드를 Override하여 코드를 작성하면 됩니다.