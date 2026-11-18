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
| `og.png` | 링크 공유 미리보기 이미지(1200×630). 바꿀 때는 `index.html`의 `og:image` 태그와 함께 교체 |
| `README.md` | 이 문서 |

## deals.json 구조

```json
{
  "updated": "2026-11-18T10:56:00+09:00",
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
  "published": "2026-11-18T12:30:00+09:00"
}
```

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
  "published": "2026-11-18T16:00:00+09:00"
}
```

- `comparison`을 2개 이상 넣으면 히어로 배지가 `N종 비교 1위 · 오늘의 원픽`으로 바뀌고 본문에 비교표가 그려집니다. 없으면 `specs`/`note` 기반 단일 리포트로 표시됩니다.
- 비교표 행은 `port`(포트) · `feats`(규격) · `weight`(무게) · `cons`(아쉬운 점) 고정. 없는 값은 `null` → 화면에 `—`.
- `best: true`인 항목만 연한 에메랄드 컬럼 + `BEST PICK` 뱃지로 강조됩니다. **가격은 실제 확인된 값만** 넣고 `priceNote`에 출처(쿠팡/다나와 등)를 남기세요.
- `specs`는 히어로 가격 아래 한 줄 요약(최대 3개, ` · `로 연결).

- `price` / `wasPrice`는 **숫자만** (원 단위, 쉼표 없이). 화면에서 `39,900원`으로 자동 포맷.
- `discount`는 문자열(`"33%"`).
- `deals`가 비어 있으면 자동으로 **“오늘 16:00 첫 검증 핫딜이 업데이트됩니다”** 안내 카드가 뜹니다.
- 카드 순서는 배열 순서 그대로입니다. **최신 항목을 배열 맨 앞에 넣으세요.**
- 핫딜 링크는 쿠팡 파트너스 제휴 링크. 페이지 하단에 파트너스 고지 문구가 고정 포함돼 있습니다.

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
