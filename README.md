# ⚡ 직장인 치트키 — 링크 페이지

`@cheatkey.work` 인스타그램 프로필에 거는 무료 링크 모음 페이지.
GitHub Pages로 서빙됩니다: **https://phappyj.github.io/cheatkey/**

- 브랜드: 화이트 매거진 톤 — 배경 `#F8F9FA` · 카드 `#FFFFFF` + `1px solid #EAECEF` · 본문 `#111827` · 보조 `#6B7280`
- 포인트: 딥네이비 `#0F172A`(헤더·CTA) + 에메랄드 `#0E9F6E`(강조·BEST PICK) · 할인 뱃지 코랄 `#F04438`
- 모바일 퍼스트(390px 최우선, 최대 폭 480px, 단일 컬럼). **첫 화면(390×844)에 히어로 CTA까지 스크롤 없이 보이도록 여백 관리**
- 폰트: Pretendard CDN(jsDelivr) 사용. 그 외 외부 라이브러리 없음 (`index.html` + `deals.json` 단일 구조)

## 파일

| 파일 | 역할 |
|---|---|
| `index.html` | 페이지 전체(디자인·렌더링). **평소엔 건드릴 일 없음** |
| `deals.json` | 카드 데이터. 08:30·12:30 AI 치트키 / 16:00·19:30 핫딜 자동화가 **여기만 추가**하면 됨 |
| `scripts/build_tip_pages.py` | `deals.json`의 `tips`를 읽어 `/tips/` SEO 페이지·목록·`sitemap.xml` 자동 생성 (**팁 추가 후 반드시 실행**) |
| `scripts/build_en_seo_pages.py` | `en/tools/` 영문 툴 테스트 페이지 10개·목록·`sitemap.xml` 생성 (**툴 추가·가격 변경 후 실행**) |
| `tips/` | 팁별 정적 SEO 페이지(`tip-001.html`~`tip-009.html`) + 목록(`index.html`) — 스크립트가 생성 |
| `en/tools/` | 영문 툴 테스트 SEO 페이지(`klap.html`~`decktopus.html`) + 목록(`index.html`) — 스크립트가 생성 |
| `sitemap.xml` | 허브·`/en/`·`/tips/`·팁·`/en/tools/` URL 전체 — 두 스크립트가 같은 결과로 갱신 |
| `og.png` | 링크 공유 미리보기 이미지(1200×630). 바꿀 때는 `index.html`의 `og:image` 태그와 함께 교체 |
| `README.md` | 이 문서 |

## deals.json 구조

```json
{
  "updated": "2026-11-18T10:56:00+09:00",
  "viewsAsOf": "2026-11-25 06:00",
  "tips":  [ ...AI 치트키 카드... ],
  "deals": [ ...핫딜 카드... ]
}
```

### tips 배열 (AI 치트키)

```json
{
  "id": "tip-002",
  "no": "02",
  "tag": "AI · 엑셀",
  "title": "제목 — <span class=\"accent\">강조</span> 가능",
  "sub": "한 줄 부제",
  "steps": [
    { "k": "1 역할", "v": "지시 내용" },
    { "k": "2 재료", "v": "지시 내용" }
  ],
  "note": "카드 하단 보충 한 줄 (선택)",
  "prompt": "복사 버튼으로 넘길 프롬프트 전문",
  "link": "https://www.instagram.com/p/XXXX/",
  "linkLabel": "인스타 원문 보기",
  "published": "2026-11-18T12:30:00+09:00",
  "views": 1300,
  "tool": "Decktopus"
}
```

- `views`(유튜브 쇼츠 누적 조회수)가 **300 이상이면 '🔥 인기 프롬프트' 배지**가 붙고 카드가 최상단으로 올라갑니다(인기끼리는 최신순, 나머지는 최신순).
- `tool`이 있으면 링크 버튼이 `affiliate_click`(`data-aff`)으로 집계되고 `rel="sponsored"`가 붙습니다(인스타 링크는 제외).
- 카드 제목·`3단계 가이드 · 프롬프트 전문 보기` 링크는 `/tips/{id}.html`로 갑니다. **팁을 추가하면 반드시 아래 SEO 페이지 생성 스크립트를 돌려야 링크가 깨지지 않습니다.**

## AI 치트키 개별 SEO 페이지 (`/tips/`)

검색 유입용 정적 페이지입니다. 목록: **https://phappyj.github.io/cheatkey/tips/**

```bash
cd cheatkey-site
python3 scripts/build_tip_pages.py        # tips/*.html + tips/index.html + sitemap.xml 생성
# 팁 추가/수정 후
python3 scripts/build_tip_pages.py && git add deals.json tips sitemap.xml \
  && git commit -m "tip: 업데이트" && git push
```

- `deals.json`의 `tips[]`만 고치고 스크립트를 돌리면 팁마다 페이지가 자동으로 생깁니다(`tip-001`~`tip-00N`, 새 팁 자동 포함).
- 각 페이지 구성: 고유 `<title>`·`<meta name="description">`·`canonical`·OG/Twitter 카드, JSON-LD(`Article` + `HowTo` + `BreadcrumbList`), 3단계 가이드, 복사 버튼이 달린 프롬프트 전문, `note`(솔직한 무료/유료 조건), 제휴 CTA(`rel="sponsored"`·`data-aff`), GA4(`G-E23M7R0R8N`), 상·하단 '전체 허브로' 링크, 다른 팁 3개 내부링크.
- 검색용 `<title>`·`description`을 직접 다듬으려면 `scripts/build_tip_pages.py`의 `SEO_OVERRIDES`에 `id`를 키로 넣으세요. 없으면 `title`/`sub`에서 자동 생성합니다.
- GA4 이벤트: 페이지뷰(`/tips/...`) + `affiliate_click`(`data-loc="tip_page"`) + `prompt_copy`(`tip_id`).
- `sitemap.xml`은 스크립트가 허브·`/en/`·`/tips/`·팁 전체·`privacy.html`을 한 번에 다시 씁니다. Search Console 사이트맵(`sitemap.xml`)은 그대로 두면 재수집됩니다.

## 영문 툴 테스트 개별 SEO 페이지 (`/en/tools/`)

글로벌 검색 유입용 영문 정적 페이지입니다. 목록: **https://phappyj.github.io/cheatkey/en/tools/**

```bash
cd cheatkey-site
python3 scripts/build_en_seo_pages.py        # en/tools/*.html + en/tools/index.html + sitemap.xml
# 툴·가격·실측치 수정 후
python3 scripts/build_en_seo_pages.py && git add en sitemap.xml README.md \
  && git commit -m "en tools: 업데이트" && git push
```

- 현재 10개: `klap` · `loopcv` · `submagic` · `quso-ai` · `speak-ai` · `taja-ai` · `make-com` · `originality-ai` · `pictory` · `decktopus`. 링크(제휴 URL·프로모 코드)는 `affiliates.json`의 `url`/`promo_code`에서 읽어 오고, 본문 수치는 스크립트의 `TOOLS` 항목에 적힌 값입니다.
- **숫자 규칙**: `affiliates.json`의 실측 필드(`pricing`·`free_plan`·`honest_limit`·`pricing_checked`)와 우리가 직접 돌린 테스트 결과만 적습니다. 벤더 자체 주장(“99% accuracy” 등)은 `vendor claims`로 표시하고, 계정을 만들어 쓰지 않은 툴은 `evidence` 문단에 "no account was used for this page"로 명시합니다.
- 각 페이지 구성: 고유 `<title>`·`<meta name="description">`·`canonical`·OG/Twitter, JSON-LD(`Review` + `SoftwareApplication` + `FAQPage` + `BreadcrumbList`), Work Cheatkey 점수(5점), 무료/유료/함정 3줄 요약, `What we checked`(검증 방법·실측 수치), 가격표 + 가격 메모, 3단계 워크플로, 제휴 CTA(`rel="sponsored"`·`data-aff`·`data-loc="en_tool_page"`), 적합/비적합, FAQ(`<details>`), 다른 툴 3개 내부링크, 상·하단 `← Back to Work Cheatkey`.
- **툴 추가**는 `TOOLS`에 항목 하나 추가 + `affiliates.json`에 해당 `id` 링크가 있으면 끝입니다. `alts`·`slug`·`score`도 함께 채우세요. `index.html`의 비교표와 목록은 `TOOLS`에서 자동 생성됩니다.
- 영문 허브 `en/index.html` 연결: 툴 목록 카드는 **이름 영역 → `/en/tools/{slug}.html`, `↗` 화살표 → 제휴 링크**, Verified Stack 카드는 **본문 → 테스트 페이지, `Try X ↗` 버튼 → 제휴 링크**, 히어로 픽에는 `Full test →` 링크가 붙습니다. 허브에는 `Tests` 칩과 푸터 `Tool tests` 링크도 있습니다.
- GA4: 페이지뷰 + `affiliate_click`(`data-loc="en_tool_page"`). 허브의 `hero_pick`·`stack`·`tools` 집계와 구분됩니다.
- `sitemap.xml`은 `build_tip_pages.py`를 돌려도 `/en/tools/` URL이 빠지지 않습니다(두 스크립트가 같은 24개 URL을 씁니다).

### deals 배열 (핫딜)
```json
{
  "id": "deal-001",
  "title": "상품명(쿠팡 표기 그대로)",
  "shortTitle": "짧은 상품명 (스티키바·alt용, 선택)",
  "seller": "쿠팡 · 로켓배송",
  "price": 39900,
  "wasPrice": 59900,
  "discount": "33%",
  "image": "img/deal-001.jpg",
  "link": "https://link.coupang.com/a/XXXXX",
  "note": "직접 써보고 남긴 한 줄 (선택)",
  "specs": ["히어로 요약 1", "히어로 요약 2", "히어로 요약 3"],
  "verdict": "3종 비교 한 줄 결론",
  "comparison": [
    {
      "name": "정식 모델명",
      "short": "표 머리글용 짧은 이름",
      "price": 22900,
      "priceNote": "쿠팡 / 다나와 최저가",
      "port": "C 2 + A 1",
      "feats": "GaN · 접지 · PPS",
      "weight": "150g",
      "cons": "아쉬운 점 한 줄",
      "best": true
    }
  ],
  "published": "2026-11-18T16:00:00+09:00",
  "views": 1162
}
```

- `comparison`을 2개 이상 넣으면 히어로 배지가 `N종 비교 1위 · 오늘의 원픽`으로 바뀌고 본문에 비교표가 그려집니다. 없으면 `specs`/`note` 기반 단일 리포트로 표시됩니다.
- 비교표 행은 `port`(포트) · `feats`(규격) · `weight`(무게) · `cons`(아쉬운 점) 고정. 없는 값은 `null` → 화면에 `—`.
- `best: true`인 항목만 연한 에메랄드 컬럼 + `BEST PICK` 뱃지로 강조됩니다. **가격은 실제 확인된 값만** 넣고 `priceNote`에 출처(쿠팡/다나와 등)를 남기세요.
- `specs`는 히어로 가격 아래 한 줄 요약(최대 3개, ` · `로 연결).

- `price` / `wasPrice`는 **숫자만** (원 단위, 쉼표 없이). 화면에서 `39,900원`으로 자동 포맷.
- `discount`는 문자열(`"33%"`).
- `deals`의 **첫 항목(`deals[0]`)은 히어로**(사진·가격·CTA + 3종 비교표)로 나오고, 아래 `02 인기 핫딜 모아보기`에는 **히어로를 뺀 나머지를 `views` 내림차순으로 정렬해 상위 4개만** 보여줍니다(2×2 그리드). 나머지는 `이전 핫딜 N개 더보기` 버튼 뒤로 접힙니다.
- **`views` = 해당 상품 쇼츠의 유튜브 누적 조회수**(06:00 스캔 값). 없으면 0으로 보고 맨 뒤(접힘 영역)로 가며, 최신 발행 순으로 정렬됩니다. **새 핫딜은 `deals` 맨 앞에 넣기만 하면 히어로로 올라가고 나머지 정렬은 자동**입니다.
- 조회수를 갱신할 때는 `deals[i].views`와 루트 `viewsAsOf`(예: `"2026-11-25 06:00"`)를 함께 고쳐 주세요(페이지 하단에 기준 시각이 표시됩니다).
- 카드 순서는 `views` 정렬이 우선입니다. 배열 순서는 히어로(최신 원픽) 결정에만 쓰입니다. **최신 항목을 배열 맨 앞에 넣으세요.**
- 핫딜 링크는 쿠팡 파트너스, Make.com 링크는 Make 제휴 링크. 페이지 하단에 제휴 고지 문구가 고정 포함돼 있습니다.

## 영문 허브 (/en)

글로벌 영어 채널 `Work Cheatkey (@workcheatkeyai)`용 별도 페이지: **https://phappyj.github.io/cheatkey/en/**

- 쿠팡·핫딜 섹션은 넣지 않고, 영문 프롬프트 2종(회의록·거절 메일) + 제휴 툴 섹션을 둡니다.
- `en/index.html`은 `deals.json`을 읽지 않는 **독립 정적 페이지**입니다(수동 편집).
- 구조(2026-11-19 개편): **히어로 픽 1개 → Verified Stack 3개 → `View all tested tools (N)` 접힘 목록**
  - 히어로 픽: 그 주 쇼츠에서 소개한 툴(2026-11-25 현재 LoopCV). 데스크톱에서는 히어로 카드가 2단(좌: 카피 / 우: 픽 카드)입니다.
  - Verified Stack: 잡 하나당 하나 — 현재 Make.com(자동화) · Speak AI(회의) · Decktopus(슬라이드). `#stack` 안의 `.scard` 3개를 고치면 됩니다. Granola는 Dub 파트너 심사가 끝나면 Speak AI 자리를 대체할 후보(링크 발급 전).
  - 접힘 목록: 나머지 툴 전체. `.allbody`는 기본 `hidden`, `#alltoggle` 클릭으로 펼칩니다. 툴을 추가·삭제하면 `#allcount`와 카테고리 칩 개수는 **스크립트가 DOM에서 자동 계산**하므로 손대지 않아도 됩니다(칩도 실제로 툴이 있는 카테고리만 표시).
  - 테스트 페이지가 있는 툴은 카드 이름이 `/en/tools/{slug}.html`로 가고 `↗`만 제휴 링크입니다. 테스트 페이지가 없는 툴(Pixa·Fliki·Rytr·Revid·Lunacal)은 카드 전체가 제휴 링크입니다.
  - 스택으로 툴을 올리면 접힘 목록에서는 빼고, 반대도 마찬가지로 맞춰 주세요.
- 제휴 링크·수수료·정산 상태는 `affiliates.json`에 툴별로 기록합니다(`status`, `placed_on`).
- 개인정보처리방침: **https://phappyj.github.io/cheatkey/privacy.html** (국·영문). 제휴 링크 추가 시 이 문서의 "제휴 링크" 표도 갱신하세요.

## GA4 (Work Cheatkey)

- 속성: **Work Cheatkey** (phappyj@gmail.com GA 계정 `a398168083`), 데이터 스트림 `https://phappyj.github.io/cheatkey/` (스트림 ID 16371466781)
- **측정 ID `G-E23M7R0R8N`** — `index.html`, `en/index.html` `<head>`에 gtag.js로 직접 설치(2026-11-19)
- 커스텀 이벤트: `affiliate_click`(tool_name, category, location, link_url), `filter_tools`(category, results), `prompt_copy`(prompt_name), `open_all_tools` / `close_all_tools`(영문 허브 접힘 목록), `tips_jump`(location — 한국어 허브 인기 프롬프트 퀵 점프), `deals_more`(expanded, total — 핫딜 더보기/접기)
- 영문 툴 카드 CTA에는 `data-aff` / `data-cat` / `data-loc` 속성을 달아야 집계됩니다. `data-loc` 값: `hero_pick` · `stack` · `tools` · `workflows` · `make_card` · `hero_card` · `en_tool_page`
- 정책 변경 시 `privacy.html` 03·05절의 GA4 고지도 같이 갱신합니다.

## 수동 업데이트 방법

```bash
cd cheatkey-site
# deals.json 수정 후
git add deals.json && git commit -m "deal: 11/18 16:00 업데이트" && git push
```

푸시 후 Pages 반영까지 30~60초.

## 로컬 확인

```bash
cd cheatkey-site && python3 -m http.server 8080
# http://localhost:8080
```

> `index.html`을 파일로 직접 열면(`file://`) `deals.json` fetch가 막혀 내장 기본 카드만 보입니다. 로컬 서버로 확인하세요.
