# AI 아키텍처

> 프레임워크 : FastAPI + LangChain
> AI 모델 : OpenAI GPT-4

## 전체 아키텍처 흐름 요약

```plaintext
[외부 API] → (채용공고 JSON 응답)
        ↓
[🌐 백엔드 서버 (FastAPI)]
        ↓
[📦 ChatGPT API 호출 (프롬프트 + 채용공고 JSON + 사용자 정보)]
        ↓
[✅ 정리된 분석 결과 (충족, 부족, 역량 추천)]
        ↓
[REST API 형태로 프론트엔드에 응답]
```

## 구성 요소 정리

1. 외부 채용공고 API 호출
2. ChatGPT 프롬프트 구성

```
기초 틀
[채용공고]
{job_posting}

[사용자 정보]
기술 스택: {user_info['skills']}
희망 연봉: {user_info['salary']}
희망 복지: {user_info['benefits']}
희망 근무 지역: {user_info['location']}

[질문]
- 어떤 항목을 충족하나요?
- 부족한 조건은 무엇인가요?
- 어떤 역량을 키우면 좋을까요?
```

- 추가적인 정보 : 보유 경력 연차, 관심 직무, 자격증/수상/프로젝트, 지원 형태, 학력, 보유 언어/레벨 등

--프롬프트 구체화--

```
[페르소나 역할 안내]
당신은 신입 및 경력 개발자 채용 컨설팅을 제공하는 AI 전문가입니다. 사용자의 역량과 희망 조건을 기반으로 채용공고를 분석하여, 충족 조건과 부족 조건을 식별하고, 적합한 커리어 성장 방향을 제시해야 합니다. 신입의 경우에는 실무 경험이 부족할 수 있으므로 성장 가능성과 학습 의지를 고려하여 피드백을 구성해 주세요.

[채용공고]
{job_posting}

[사용자 정보]
- 기술 스택: {user_info['skills']}
- 보유 경력: {user_info['experience_years']}년
- 신입 여부: {"예" if user_info['is_entry_level'] else "아니오"}
- 희망 연봉: {user_info['salary']}
- 희망 근무지역: {user_info['location']}
- 선호 복지: {user_info['benefits']}
- 관심 직무: {user_info['target_position']}
- 자격증: {user_info['certifications']}
- 외국어 능력: {user_info['languages']}

[요청]
아래 항목을 분류해서 자세히 분석해 주세요:

1. ✅ **충족 조건**
   - 사용자가 해당 채용공고에서 이미 충족하고 있는 조건을 구체적으로 정리해 주세요.
   - 기술 스택, 지역, 연봉, 복지, 우대사항 등을 기준으로 항목별로 나눠 주세요.

2. ❌ **부족한 조건**
   - 공고에서 요구하거나 우대하는 항목 중 사용자와 맞지 않거나 부족한 조건을 항목별로 나눠서 정리해 주세요.
   - 왜 부족한지 간단한 이유도 함께 적어 주세요.

3. 📌 **추천 역량 개발**
   - 사용자가 이 채용공고에 더 적합해지기 위해 개발해야 할 역량이나 경험을 3가지 이상 구체적으로 제안해 주세요.
   - 추천 기술/자격증/경험 예시도 포함해 주세요.
   - 신입의 경우 실무 경험이 부족하므로 프로젝트/학습 방향도 포함해 주세요.

4. 💬 **요약**
   - 위 내용을 한 문단으로 간단히 요약해 주세요 (300자 이내).
```

3. OpenAI API 호출
4. 전체 API 엔드포인트

## 보안

- `.env` 에 키값 등 정보 보관 후 `python-dotenv` 로 불러오기
- 외부 API 사용자 입력 값은 항상 유효성 검사

## 폴더 구조

```
# ai-job-matcher/
# ├── app/
# │   ├── main.py                ← FastAPI 엔트리포인트
# │   ├── gpt_service.py         ← LangChain + OpenAI 연동
# │   ├── job_fetcher.py         ← 외부 API에서 채용공고 불러오는 모듈
# │   ├── prompt_builder.py      ← 프롬프트 조립기
# │   └── schemas.py             ← Pydantic 모델 정의
# ├── requirements.txt
# ├── .gitignore
# └── .env                       ← OpenAI API 키 등 환경변수
# -------------------------------
```


## .env

```plaintext
OPENAI_API_KEY=your-api-key
JOB_API_BASE=URL
```
