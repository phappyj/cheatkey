#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
직장인 치트키 — AI 치트키(tips) 개별 SEO 페이지 생성기

deals.json 의 tips[] 를 읽어 다음을 만든다.
  tips/index.html          팁 전체 목록
  tips/tip-001.html ~ tip-00N.html   팁별 정적 페이지
  sitemap.xml              허브·/en/·/tips/·팁·/en/tools/ 전체 URL 갱신

사용:
    python3 scripts/build_tip_pages.py            # 페이지 + 사이트맵 생성
    python3 scripts/build_tip_pages.py --no-sitemap

tips 배열에 새 팁을 추가하고 이 스크립트만 다시 돌리면 페이지가 늘어난다.
새 팁의 검색용 제목/설명을 직접 다듬고 싶으면 아래 SEO_OVERRIDES 에 id를 추가한다.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEALS = ROOT / "deals.json"
TIPS_DIR = ROOT / "tips"
SITEMAP = ROOT / "sitemap.xml"

SITE = "https://phappyj.github.io/cheatkey"
OG_IMAGE = SITE + "/og.png"
GA_ID = "G-E23M7R0R8N"
BRAND = "직장인 치트키"
TODAY = dt.date.today().isoformat()

# 검색 유입용 제목·설명. 없으면 deals.json 값에서 자동 생성한다.
SEO_OVERRIDES = {
    "tip-011": {
        "title": "미팅 잡는 메일 3통을 링크 하나로, 예약 페이지 3단계 | 직장인 치트키",
        "desc": "예약 링크 하나 보내면 상대가 빈 시간을 직접 고릅니다. 확정 메일·리마인더·화상 링크까지 자동으로 나가는 예약 페이지 만드는 3단계와, 2026-11-27에 직접 열어 확인한 요금($9·7일 체험)·한국어 미지원 조건까지 정리했습니다.",
    },
    "tip-010": {
        "title": "매일 아침 메일 → 구글시트 자동 정리, 템플릿 하나 | 직장인 치트키",
        "desc": "거래처 메일을 엑셀에 옮겨 적던 일을 Make 템플릿 하나로 넘겼습니다. 무료 플랜 1,000크레딧·15분 간격이라는 실제 한도와 Core 조건까지 2026-11-26 요금 페이지에서 확인한 그대로 정리했습니다.",
    },
    "tip-009": {
        "title": "세미나 영상 하나로 쇼츠 클립·한국어 자막 뽑기 | 직장인 치트키",
        "desc": "30분 세미나·회의 녹화본 링크만 넣으면 클립 후보, 한국어 제목, 바이럴 점수, 한국어 자막까지 한 번에 나옵니다. 무료 범위와 클립 개수 기준 요금까지 직접 테스트한 조건 그대로 정리했습니다.",
    },
    "tip-008": {
        "title": "AI 티 나는 보고서, 제출 전 10초 검사·수정 | 직장인 치트키",
        "desc": "챗지피티로 쓴 보고서 문단을 붙여넣으면 AI 티 문장이 빨간 줄로 표시됩니다. 사내 메모체로 고쳐 쓰는 프롬프트와 무료 크레딧 조건, 직접 스캔한 점수까지 정리했습니다.",
    },
    "tip-007": {
        "title": "월요일 밀린 메일 답장, 초안부터 받는 법 | 직장인 치트키",
        "desc": "메일 스레드를 열면 답장 초안이 옆에 뜹니다. 톤·언어를 고르면 사내 말투로 다시 써 주고, 같은 방식으로 주간보고 초안까지 뽑는 3단계와 무료 플랜 조건입니다.",
    },
    "tip-006": {
        "title": "회의록 정리 1시간 → 1분, 녹음만 올리면 전사·요약 | 직장인 치트키",
        "desc": "회의 녹음·영상 파일을 올리면 화자 구분·타임스탬프 전사와 요약이 자동으로 나옵니다. 결정·할 일·리스크 3줄로 뽑는 프롬프트와 크레딧 과금 조건을 정리했습니다.",
    },
    "tip-005": {
        "title": "보고서를 30초 영상으로, 본문 붙여넣고 1분 | 직장인 치트키",
        "desc": "쓴 보고서 본문을 그대로 붙여넣으면 장면·자막·목소리까지 자동으로 붙습니다. 장면 5개로 나누는 프롬프트, 무료 체험 범위와 한국어 자막 확인 포인트까지.",
    },
    "tip-004": {
        "title": "PPT 15장 1시간 → 10분, 결론 3줄 프롬프트 | 직장인 치트키",
        "desc": "주제와 결론 3줄만 넣으면 표지·차트·본문 15장이 자동으로 구성됩니다. 보고용 슬라이드를 결론 우선으로 설계하는 프롬프트와 무료 범위·한국어 폰트 주의점입니다.",
    },
    "tip-003": {
        "title": "아침 브리핑 20분 → 0분, 메일·일정 자동 요약 3단계 | 직장인 치트키",
        "desc": "매일 아침 07:00, 지난 24시간 메일과 오늘 일정 요약이 메일 한 통으로 도착하게 만드는 3단계. 무료 플랜 크레딧으로 하루 1회 돌리는 조건까지 정리했습니다.",
    },
    "tip-002": {
        "title": "거절 메일 20초에 쓰는 3줄 공식 (정중하지만 단호하게) | 직장인 치트키",
        "desc": "관계는 지키고 각은 세우는 거절 메일을 20초에 뽑는 톤 공식 3줄. 상대·사정·대안만 채우면 되는 복사용 프롬프트와 일정 조율로 바꾸는 방법입니다.",
    },
    "tip-001": {
        "title": "회의록 30분을 30초로, 복붙 프롬프트 3줄 | 직장인 치트키",
        "desc": "회의 메모를 그대로 붙여넣고 결정·할 일·다음 안건 세 칸 표로 뽑는 프롬프트. 역할·재료·형식 3줄만 바꾸면 보고서에도 그대로 쓰는 방법입니다.",
    },
}

CSS = """
  :root{
    --bg:#F8F9FA; --card:#FFFFFF; --line:#EAECEF; --line-2:#F1F2F4;
    --ink:#111827; --ink-2:#6B7280; --ink-3:#9CA3AF;
    --navy:#0F172A; --navy-2:#1E293B;
    --mint:#0E9F6E; --mint-deep:#0B7A55; --mint-soft:#ECFDF5; --mint-line:#BBF0DD;
    --coral:#F04438; --radius:18px; --max:560px;
    --shadow:0 1px 2px rgba(17,24,39,.04), 0 10px 28px -20px rgba(17,24,39,.18);
  }
  *{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
  html,body{margin:0;padding:0}
  html{background:var(--bg);scroll-behavior:smooth}
  body{
    background:var(--bg); color:var(--ink);
    font-family:"Pretendard Variable",Pretendard,-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",Roboto,sans-serif;
    font-size:16px; line-height:1.55; letter-spacing:-0.012em;
    -webkit-font-smoothing:antialiased; min-height:100dvh; word-break:keep-all;
  }
  a{color:inherit}
  .nav{position:sticky;top:0;z-index:30;background:rgba(248,249,250,.9);
    -webkit-backdrop-filter:saturate(160%) blur(14px);backdrop-filter:saturate(160%) blur(14px);
    border-bottom:1px solid rgba(17,24,39,.06)}
  .nav-in{max-width:var(--max);margin:0 auto;display:flex;align-items:center;gap:10px;
    padding:calc(9px + env(safe-area-inset-top)) 18px 9px}
  .brand{display:inline-flex;align-items:center;gap:6px;font-size:13.5px;font-weight:800;
    letter-spacing:-0.02em;color:var(--ink);text-decoration:none;white-space:nowrap}
  .brand .bolt{font-size:13px;line-height:1}
  .nav .chip{margin-left:auto;display:inline-flex;align-items:center;font-size:11.5px;font-weight:700;
    color:var(--ink-2);background:#fff;border:1px solid var(--line);border-radius:999px;
    padding:5px 10px;text-decoration:none;white-space:nowrap}
  .nav .chip:active{background:#F3F4F6}
  .shell{max-width:var(--max);margin:0 auto;padding:0 18px 72px}
  .crumb{display:flex;padding:14px 2px 0;font-size:12px;font-weight:700;color:var(--ink-2);
    text-decoration:none;align-items:center;gap:5px}
  .crumb .arw{color:var(--mint)}
  .article{background:var(--card);border:1px solid var(--line);border-radius:22px;
    box-shadow:var(--shadow);padding:20px 18px 18px;margin-top:10px}
  .tag{display:inline-block;font-size:9.5px;font-weight:800;letter-spacing:.05em;
    color:var(--mint);background:var(--mint-soft);border:1px solid var(--mint-line);
    border-radius:999px;padding:3px 9px;margin-bottom:11px}
  h1{font-size:24px;line-height:1.34;font-weight:800;letter-spacing:-0.045em;margin:0 0 9px}
  h1 .accent{color:var(--mint)}
  .lede{margin:0 0 12px;color:var(--ink-2);font-size:13.2px;font-weight:500;line-height:1.62}
  .meta{display:flex;align-items:center;gap:6px;flex-wrap:wrap;font-size:11px;font-weight:600;
    color:var(--ink-3);padding-bottom:15px;border-bottom:1px solid var(--line-2)}
  .meta .dot{color:#D1D5DB}
  h2{display:flex;align-items:center;gap:8px;font-size:15.5px;font-weight:800;
    letter-spacing:-0.03em;margin:24px 0 11px;line-height:1.3}
  h2 .k{flex:0 0 auto;font-size:10px;font-weight:800;color:var(--mint);letter-spacing:.06em}
  .steps{list-style:none;margin:0;padding:0;display:grid;gap:7px}
  .steps li{display:flex;align-items:flex-start;gap:10px;background:#FAFBFC;
    border:1px solid var(--line-2);border-radius:12px;padding:11px 12px}
  .steps .num{flex:0 0 21px;height:21px;border-radius:6px;background:#EEF0F3;color:var(--navy);
    font-weight:800;font-size:11px;display:grid;place-items:center;margin-top:1px;
    font-variant-numeric:tabular-nums}
  .steps .body{min-width:0}
  .steps .k{display:block;font-size:9.5px;font-weight:800;color:var(--mint);letter-spacing:.04em;margin-bottom:3px}
  .steps .v{font-size:13.4px;font-weight:600;color:#374151;line-height:1.5}
  .prompt{background:#F7F8FA;border:1px solid var(--line);border-radius:14px;overflow:hidden}
  .prompt-bar{display:flex;align-items:center;gap:8px;padding:8px 10px 8px 12px;
    border-bottom:1px solid var(--line);background:#FCFCFD}
  .prompt-bar .plabel{font-size:9px;font-weight:800;letter-spacing:.1em;color:var(--ink-3);text-transform:uppercase}
  .prompt-bar .copy{margin-left:auto;appearance:none;border:1px solid var(--navy);background:var(--navy);
    color:#fff;font:inherit;font-size:11.5px;font-weight:700;letter-spacing:-0.01em;
    padding:7px 11px;border-radius:9px;cursor:pointer;display:inline-flex;align-items:center;gap:5px}
  .prompt-bar .copy:active{transform:scale(.97)}
  .prompt-bar .copy svg{width:12px;height:12px;color:#6EE7B7}
  .prompt-bar .copy.done{background:var(--mint);border-color:var(--mint)}
  .prompt-body{margin:0;padding:12px 13px 14px;font-family:inherit;font-size:12.6px;line-height:1.72;
    color:#3F4753;white-space:pre-wrap;word-break:break-word}
  .prompt-foot{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:9px}
  .prompt-foot a{font-size:11.5px;font-weight:700;color:var(--ink-2);text-decoration:none;
    border-bottom:1px solid var(--line);padding-bottom:1px}
  .prompt-foot span{font-size:10.5px;color:var(--ink-3);font-weight:600}
  .note{background:linear-gradient(180deg,#F7FCF9 0%,#F2FAF6 100%);border:1px solid #DCF3E8;
    border-radius:14px;padding:13px 14px;margin:0}
  .note .label{display:block;font-size:9.5px;font-weight:800;letter-spacing:.06em;
    color:var(--mint-deep);margin-bottom:6px;text-transform:uppercase}
  .note p{margin:0;font-size:12.4px;line-height:1.7;color:#42554C;font-weight:500}
  .cta{display:block;margin-top:20px;text-decoration:none;background:var(--navy);color:#fff;
    border-radius:15px;padding:15px 16px;box-shadow:0 14px 30px -22px rgba(15,23,42,.9)}
  .cta:active{transform:scale(.99)}
  .cta .lbl{display:block;font-size:9.5px;font-weight:800;letter-spacing:.08em;color:#6EE7B7;margin-bottom:5px}
  .cta .txt{display:flex;align-items:center;gap:8px;font-size:14px;font-weight:800;line-height:1.4;letter-spacing:-0.02em}
  .cta .txt svg{flex:0 0 auto;width:15px;height:15px;color:#6EE7B7}
  .fine{margin:8px 1px 0;font-size:10.5px;line-height:1.6;color:var(--ink-3);font-weight:500}
  .more{margin-top:26px}
  .more-head{display:flex;align-items:baseline;gap:8px;margin-bottom:10px;padding:0 2px}
  .more-head b{font-size:13px;font-weight:800;letter-spacing:-0.03em}
  .more-head a{margin-left:auto;font-size:11px;font-weight:700;color:var(--ink-2);text-decoration:none}
  .more-list{display:grid;gap:8px}
  .more-list a{display:block;text-decoration:none;background:var(--card);border:1px solid var(--line);
    border-radius:14px;padding:13px 14px;box-shadow:0 1px 2px rgba(17,24,39,.03)}
  .more-list a:active{border-color:#D8DBE0}
  .more-list .t{display:block;font-size:13px;font-weight:800;letter-spacing:-0.03em;line-height:1.4;margin-bottom:3px}
  .more-list .t .accent{color:var(--mint)}
  .more-list .s{display:block;font-size:11px;font-weight:600;color:var(--ink-3)}
  .back{display:flex;align-items:center;justify-content:center;gap:6px;margin-top:22px;
    text-decoration:none;background:#fff;border:1px solid var(--line);border-radius:14px;
    padding:14px;font-size:12.5px;font-weight:800;color:var(--ink)}
  .back .arw{color:var(--mint)}
  footer{margin-top:26px;padding-top:18px;border-top:1px solid var(--line)}
  .disclosure{font-size:11px;line-height:1.75;color:#6B7280;font-weight:500;
    background:#F3F4F6;border-radius:12px;padding:12px 14px;margin:0}
  .colophon{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;
    margin-top:14px;font-size:10.5px;color:var(--ink-3);font-weight:500}
  .privacy-line{margin:8px 0 0;font-size:10.5px;font-weight:600}
  .privacy-line a{color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--line)}
  .dot-sep{margin:0 4px;color:var(--ink-3)}
  .toast{position:fixed;left:50%;bottom:24px;transform:translate(-50%,14px);opacity:0;
    pointer-events:none;background:var(--navy);color:#fff;font-size:12px;font-weight:700;
    padding:10px 16px;border-radius:999px;transition:opacity .18s ease,transform .18s ease;z-index:60}
  .toast.on{opacity:1;transform:translate(-50%,0)}

  /* ── 목록(/tips/) ── */
  .list-head{background:var(--card);border:1px solid var(--line);border-radius:22px;
    box-shadow:var(--shadow);padding:20px 18px 18px;margin-top:10px}
  .list-head h1{margin-bottom:8px}
  .list-head .lede{margin:0}
  .tlist{display:grid;gap:10px;margin-top:16px}
  .tlist a{display:block;text-decoration:none;background:var(--card);border:1px solid var(--line);
    border-radius:16px;padding:15px 15px 14px;box-shadow:0 1px 2px rgba(17,24,39,.03)}
  .tlist a:active{border-color:#D8DBE0}
  .tlist .no{font-size:10px;font-weight:800;letter-spacing:.06em;color:var(--mint);margin-bottom:6px;display:block}
  .tlist .t{display:block;font-size:15.5px;font-weight:800;letter-spacing:-0.04em;line-height:1.38;margin-bottom:5px}
  .tlist .t .accent{color:var(--mint)}
  .tlist .s{display:block;font-size:12px;line-height:1.6;color:var(--ink-2);font-weight:500}
  .tlist .g{display:block;margin-top:8px;font-size:10.5px;font-weight:700;color:var(--ink-3)}
  @media (min-width:520px){
    h1{font-size:26px}
    .article{padding:24px 22px 20px}
  }
"""


# ────────────────────────── helpers ──────────────────────────
TAG_RE = re.compile(r"<[^>]+>")


def plain(s: str) -> str:
    """HTML 조각 → 순수 텍스트(메타·JSON-LD·미리보기용)."""
    return html.unescape(TAG_RE.sub("", s or "")).strip()


def esc(s: str) -> str:
    """텍스트·속성 공용 이스케이프(작은따옴표는 그대로 둬서 가독성 유지)."""
    return ((s or "")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def clip(text: str, n: int, word: bool = False) -> str:
    """문장 경계(또는 단어 경계)를 살려 n자 안으로 자른다."""
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= n:
        return text
    cut = text[:n]
    for mark in (". ", "다. ", "요. ", "! "):
        i = cut.rfind(mark)
        if i > n * 0.55:
            return cut[: i + 1].strip()
    if word:
        i = cut.rfind(" ")
        if i > n * 0.55:
            cut = cut[:i]
    return cut.rstrip(" ,·-—") + "…"


def ko_date(iso: str) -> str:
    try:
        d = dt.datetime.fromisoformat((iso or "").replace(" ", "T"))
    except ValueError:
        return ""
    return f"{d.year}. {d.month:02d}. {d.day:02d}."


def seo(tip: dict) -> tuple[str, str]:
    o = SEO_OVERRIDES.get(tip.get("id", ""), {})
    title = o.get("title") or (plain(tip.get("title", "")) + f" | {BRAND}")
    desc = o.get("desc") or clip(plain(tip.get("sub", "")), 150)
    return title, desc


def tip_url(tip_id: str) -> str:
    return f"{SITE}/tips/{tip_id}.html"


def is_aff(tip: dict) -> bool:
    link = tip.get("link") or ""
    return bool(tip.get("tool")) and link.startswith("http") and "instagram.com" not in link


def sorted_tips(tips: list[dict]) -> list[dict]:
    def no(t):
        try:
            return int(str(t.get("no") or "0"))
        except ValueError:
            return 0

    return sorted(tips, key=lambda t: no(t), reverse=True)


def related(tip: dict, tips: list[dict], n: int = 3) -> list[dict]:
    others = [t for t in sorted_tips(tips) if t.get("id") != tip.get("id")]
    tag = (tip.get("tag") or "").split("·")[-1].strip()
    same = [t for t in others if tag and tag in (t.get("tag") or "")]
    rest = [t for t in others if t not in same]
    return (same + rest)[:n]


# ────────────────────────── shared blocks ──────────────────────────
def head_meta(title: str, desc: str, canonical: str, og_type: str = "article",
              published: str | None = None, modified: str | None = None) -> str:
    extra = ""
    if published:
        extra += f'\n<meta property="article:published_time" content="{esc(published)}">'
        extra += '\n<meta property="article:section" content="AI 치트키">'
    if modified:
        extra += f'\n<meta property="article:modified_time" content="{esc(modified)}">'
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#F8F9FA">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{OG_IMAGE}">{extra}
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='24' fill='%23FFFFFF'/><text x='50' y='73' font-size='58' text-anchor='middle'>⚡</text></svg>">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">"""


def ga_snippet() -> str:
    return f"""<!-- Google Analytics 4 (Work Cheatkey · {GA_ID}) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_ID}');
</script>"""


def nav(back_href: str, back_label: str) -> str:
    return f"""<div class="nav">
  <div class="nav-in">
    <a class="brand" href="../"><span class="bolt">⚡</span>{BRAND}</a>
    <a class="chip" href="{back_href}">{back_label}</a>
  </div>
</div>"""


def footer() -> str:
    return f"""  <footer>
    <p class="disclosure">
      이 페이지는 쿠팡 파트너스·해외 AI 툴 제휴 활동의 일환으로, 링크를 통한 가입·결제 시 일정액의 수수료를 제공받습니다.
      가격·무료 범위·요금제는 수시로 바뀌니 결제 직전 판매처에서 최종 확인해 주세요.
    </p>
    <div class="colophon">
      <span>© 2026 {BRAND} · @cheatkey.work</span>
      <span>자료 확인 2026. 11. 25.</span>
    </div>
    <p class="privacy-line">
      <a href="../privacy.html">Privacy Policy · 개인정보처리방침</a>
      <span class="dot-sep">·</span>
      <a href="../terms.html">이용약관</a>
      <span class="dot-sep">·</span>
      <a href="../en/">English</a>
    </p>
  </footer>"""


TRACKER = f"""<script>
(function () {{
  "use strict";
  function track(event, params) {{
    try {{ if (typeof gtag === "function") gtag("event", event, params || {{}}); }} catch (e) {{}}
  }}
  /* 제휴 CTA 클릭 — 허브와 같은 affiliate_click 이벤트로 집계 */
  document.addEventListener("click", function (e) {{
    var a = e.target.closest ? e.target.closest("a[href]") : null;
    if (!a) return;
    var tool = a.getAttribute("data-aff");
    if (!tool) return;
    track("affiliate_click", {{
      tool_name: tool,
      category: a.getAttribute("data-cat") || "AI Tips",
      location: a.getAttribute("data-loc") || "tip_page",
      link_url: a.href
    }});
  }});
  /* 프롬프트 복사 */
  var toast = document.getElementById("toast");
  function showToast(msg) {{
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add("on");
    clearTimeout(showToast._t);
    showToast._t = setTimeout(function () {{ toast.classList.remove("on"); }}, 1800);
  }}
  function legacyCopy(text) {{
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.top = "-1000px";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try {{ ok = document.execCommand("copy"); }} catch (err) {{ ok = false; }}
    document.body.removeChild(ta);
    return ok;
  }}
  document.addEventListener("click", function (e) {{
    var btn = e.target.closest ? e.target.closest("[data-copy]") : null;
    if (!btn) return;
    var text = btn.getAttribute("data-copy") || "";
    function done(ok) {{
      if (!ok) {{ showToast("복사가 안 되면 프롬프트를 길게 눌러 선택해 주세요"); return; }}
      btn.classList.add("done");
      var label = btn.querySelector(".copy-label");
      if (label) {{
        var prev = label.textContent;
        label.textContent = "복사됨";
        setTimeout(function () {{ label.textContent = prev; btn.classList.remove("done"); }}, 1600);
      }}
      showToast("프롬프트를 복사했습니다");
      track("prompt_copy", {{ tip_id: btn.getAttribute("data-tip") || "" }});
    }}
    if (navigator.clipboard && navigator.clipboard.writeText) {{
      navigator.clipboard.writeText(text).then(function () {{ done(true); }}, function () {{ done(legacyCopy(text)); }});
    }} else {{
      done(legacyCopy(text));
    }}
  }});
}})();
</script>"""


def cta_block(tip: dict) -> str:
    link = tip.get("link") or ""
    label = (tip.get("linkLabel") or "원문 보기").replace("→", "").strip()
    if is_aff(tip):
        attrs = (f'href="{esc(link)}" target="_blank" rel="noopener sponsored" '
                 f'data-aff="{esc(tip.get("tool"))}" data-cat="AI Tips" data-loc="tip_page"')
        kicker = "이번 주에 한 번 써보기 · 제휴 링크"
        fine = "가격·무료 범위는 결제 화면에서 최종 확인하세요. 링크를 통한 가입 시 수수료가 발생할 수 있습니다."
    else:
        attrs = f'href="{esc(link)}" target="_blank" rel="noopener"'
        kicker = "이번 주에 한 번 써보기"
        fine = "외부 채널로 이동합니다."
    arrow = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')
    return f"""    <a class="cta" {attrs}>
      <span class="lbl">{esc(kicker)}</span>
      <span class="txt">{esc(label)} {arrow}</span>
    </a>
    <p class="fine">{esc(fine)}</p>"""


# ────────────────────────── tip page ──────────────────────────
def build_tip_page(tip: dict, tips: list[dict]) -> str:
    tid = tip["id"]
    title_plain, desc = seo(tip)
    canonical = tip_url(tid)
    published = tip.get("published") or "2026-11-18T09:00:00+09:00"
    no = tip.get("no") or ""
    tag = tip.get("tag") or "AI 치트키"

    def step_key(s: dict, i: int) -> str:
        # "1 링크 넣기" 처럼 앞에 번호가 이미 있으면 배지 번호와 겹치므로 떼어낸다
        return re.sub(r"^\s*\d+\s*[.)]?\s*", "", str(s.get("k", ""))) or str(s.get("k", ""))

    steps_html = "".join(
        f'<li><span class="num">{esc(str(i + 1))}</span>'
        f'<span class="body"><span class="k">{esc(step_key(s, i))}</span>'
        f'<span class="v">{esc(s.get("v", ""))}</span></span></li>'
        for i, s in enumerate(tip.get("steps") or [])
    )

    prompt = tip.get("prompt") or ""
    chars = len(re.sub(r"\s", "", plain(tip.get("title", "")) + plain(tip.get("sub", ""))
                       + "".join(plain(s.get("v", "")) for s in tip.get("steps") or [])
                       + plain(tip.get("note", "")) + prompt))
    read_min = max(1, math.ceil(chars / 450))

    copy_icon = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
                 'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                 '<rect x="9" y="9" width="12" height="12" rx="2.5"/><path d="M5 15V5a2 2 0 0 1 2-2h8"/></svg>')

    hint = ("괄호 안 예시는 내 상황으로 바꿔 넣으세요."
            if re.search(r"\(예|（예", prompt)
            else "복사해서 ChatGPT·클로드에 붙여넣으면 됩니다.")

    prompt_block = ""
    if prompt:
        prompt_block = f"""    <h2><span class="k">02</span>복사해서 그대로 쓰는 프롬프트</h2>
    <div class="prompt">
      <div class="prompt-bar">
        <span class="plabel">Prompt</span>
        <button class="copy" type="button" data-copy="{esc(prompt)}" data-tip="{esc(tid)}">
          {copy_icon}<span class="copy-label">복사하기</span>
        </button>
      </div>
      <pre class="prompt-body">{esc(prompt)}</pre>
    </div>
    <div class="prompt-foot">
      <a href="https://chatgpt.com/" target="_blank" rel="noopener">ChatGPT에서 열기 ↗</a>
      <span>{esc(hint)}</span>
    </div>
"""

    note_block = ""
    if tip.get("note"):
        note_block = f"""    <h2><span class="k">03</span>솔직한 무료·유료 조건</h2>
    <aside class="note">
      <span class="label">직접 확인한 조건</span>
      <p>{esc(tip["note"])}</p>
    </aside>
"""

    rel = related(tip, tips)
    rel_html = "".join(
        f'<a href="{esc(t["id"])}.html">'
        f'<span class="t">{t.get("title", "")}</span>'
        f'<span class="s">{esc(plain(t.get("tag", "")))} · 3단계 + 복사용 프롬프트</span></a>'
        for t in rel
    )

    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": canonical + "#article",
                "headline": clip(title_plain, 110),
                "description": desc,
                "datePublished": published,
                "dateModified": published,
                "inLanguage": "ko-KR",
                "image": [OG_IMAGE],
                "author": {"@type": "Organization", "name": BRAND, "url": SITE + "/"},
                "publisher": {
                    "@type": "Organization",
                    "name": BRAND,
                    "logo": {"@type": "ImageObject", "url": OG_IMAGE},
                },
                "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
                "articleSection": tag,
                "keywords": ", ".join(
                    [plain(tag), plain(tip.get("title", ""))] + ([tip["tool"]] if tip.get("tool") else [])
                ),
            },
            {
                "@type": "HowTo",
                "@id": canonical + "#howto",
                "name": clip(plain(tip.get("title", "")), 110),
                "description": clip(plain(tip.get("sub", "")), 160),
                "inLanguage": "ko-KR",
                "step": [
                    {
                        "@type": "HowToStep",
                        "position": i + 1,
                        "name": step_key(s, i),
                        "text": plain(s.get("v", "")),
                    }
                    for i, s in enumerate(tip.get("steps") or [])
                ],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": BRAND, "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "AI 치트키 전체", "item": SITE + "/tips/"},
                    {"@type": "ListItem", "position": 3, "name": plain(tip.get("title", ""))},
                ],
            },
        ],
    }
    ld = json.dumps(jsonld, ensure_ascii=False, indent=2)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
{head_meta(title_plain, desc, canonical, "article", published, published)}
<style>{CSS}</style>
{ga_snippet()}
<script type="application/ld+json">
{ld}
</script>
</head>
<body>

{nav("../", "허브로")}

<div class="shell">
  <a class="crumb" href="../"><span class="arw">←</span> {BRAND} 전체 허브로</a>

  <main>
    <article class="article">
      <span class="tag">{esc(tag)}{' · ' + esc(no) if no else ''}</span>
      <h1>{tip.get("title", "")}</h1>
      <p class="lede">{esc(tip.get("sub", ""))}</p>
      <div class="meta">
        <span>{ko_date(published)}</span>
        <span class="dot">·</span>
        <span>읽는 데 {read_min}분</span>
        <span class="dot">·</span>
        <span>프롬프트 1탭 복사</span>
      </div>

      <h2><span class="k">01</span>3단계면 끝</h2>
      <ol class="steps">{steps_html}</ol>
{prompt_block}{note_block}      <h2><span class="k">{'04' if prompt_block and note_block else '03'}</span>한 번만 써볼 링크</h2>
{cta_block(tip)}
    </article>

    <section class="more">
      <div class="more-head">
        <b>다른 AI 치트키</b>
        <a href="./">전체 {len(tips)}개 →</a>
      </div>
      <div class="more-list">{rel_html}</div>
    </section>

    <a class="back" href="../"><span class="arw">←</span> {BRAND} 전체 허브로</a>
  </main>

{footer()}
</div>

<div class="toast" id="toast" role="status" aria-live="polite"></div>

{TRACKER}
</body>
</html>
"""


# ────────────────────────── index page ──────────────────────────
def build_index_page(tips: list[dict]) -> str:
    canonical = SITE + "/tips/"
    title = f"AI 치트키 {len(tips)}개 전체 목록 — 회의록·보고서·PPT·영상 프롬프트 | {BRAND}"
    desc = (f"직장인 치트키가 직접 써보고 정리한 AI 치트키 {len(tips)}개. 회의록·거절 메일·PPT·보고서·영상·자동화를 "
            "3단계와 복사용 프롬프트, 솔직한 무료 조건까지 한 페이지에 모았습니다.")

    rows = []
    for t in sorted_tips(tips):
        tag = plain(t.get("tag", ""))
        rows.append(f"""      <a href="{esc(t['id'])}.html">
        <span class="no">{esc(t.get('no', ''))} · {esc(tag)}</span>
        <span class="t">{t.get('title', '')}</span>
        <span class="s">{esc(clip(plain(t.get('sub', '')), 90, word=True))}</span>
        <span class="g">{ko_date(t.get('published', ''))} · 3단계 + 프롬프트</span>
      </a>""")
    rows_html = "\n".join(rows)

    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": canonical + "#page",
                "name": title,
                "description": desc,
                "inLanguage": "ko-KR",
                "url": canonical,
                "isPartOf": {"@type": "WebSite", "name": BRAND, "url": SITE + "/"},
            },
            {
                "@type": "ItemList",
                "name": f"AI 치트키 {len(tips)}개",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": i + 1,
                        "url": tip_url(t["id"]),
                        "name": plain(t.get("title", "")),
                    }
                    for i, t in enumerate(sorted_tips(tips))
                ],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": BRAND, "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "AI 치트키 전체"},
                ],
            },
        ],
    }
    ld = json.dumps(jsonld, ensure_ascii=False, indent=2)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
{head_meta(title, desc, canonical, "website")}
<style>{CSS}</style>
{ga_snippet()}
<script type="application/ld+json">
{ld}
</script>
</head>
<body>

{nav("../", "허브로")}

<div class="shell">
  <a class="crumb" href="../"><span class="arw">←</span> {BRAND} 전체 허브로</a>

  <main>
    <header class="list-head">
      <span class="tag">AI 치트키 · 전체 {len(tips)}개</span>
      <h1>야근을 줄이는 AI 치트키 <span class="accent">{len(tips)}개</span></h1>
      <p class="lede">회의록·거절 메일·PPT·보고서·영상·자동화까지, 실제로 돌려보고 남은 것만 정리했습니다.
      각 페이지에 3단계 실행 순서와 복사용 프롬프트, 무료로 어디까지 되는지가 같이 있습니다.</p>
    </header>

    <section class="tlist">
{rows_html}
    </section>

    <a class="back" href="../"><span class="arw">←</span> {BRAND} 전체 허브로</a>
  </main>

{footer()}
</div>

{TRACKER}
</body>
</html>
"""


# ────────────────────────── sitemap ──────────────────────────
def build_sitemap(tips: list[dict]) -> str:
    def url(loc: str, pri: str, freq: str = "weekly") -> str:
        return (f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
                f"    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>\n  </url>")

    parts = [
        url(SITE + "/", "1.0", "daily"),
        url(SITE + "/en/", "0.9", "daily"),
        url(SITE + "/tips/", "0.8", "weekly"),
    ]
    for t in sorted_tips(tips):
        parts.append(url(tip_url(t["id"]), "0.7", "monthly"))
    # build_en_seo_pages.py 가 만든 영문 툴 테스트 페이지도 같은 사이트맵에 남긴다
    tools_dir = ROOT / "en" / "tools"
    if tools_dir.is_dir():
        parts.append(url(SITE + "/en/tools/", "0.8", "weekly"))
        for p in sorted(tools_dir.glob("*.html")):
            if p.name != "index.html":
                parts.append(url(f"{SITE}/en/tools/{p.name}", "0.7", "monthly"))
    parts.append(url(SITE + "/privacy.html", "0.3", "yearly"))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(parts)
            + "\n</urlset>\n")


# ────────────────────────── main ──────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-sitemap", action="store_true")
    args = ap.parse_args()

    data = json.loads(DEALS.read_text(encoding="utf-8"))
    tips = data.get("tips") or []
    if not tips:
        raise SystemExit("deals.json 에 tips 가 없습니다.")

    TIPS_DIR.mkdir(exist_ok=True)
    written = []
    for tip in tips:
        p = TIPS_DIR / f"{tip['id']}.html"
        p.write_text(build_tip_page(tip, tips), encoding="utf-8")
        written.append(p)

    idx = TIPS_DIR / "index.html"
    idx.write_text(build_index_page(tips), encoding="utf-8")
    written.append(idx)

    if not args.no_sitemap:
        SITEMAP.write_text(build_sitemap(tips), encoding="utf-8")

    for p in written:
        print(f"{p.relative_to(ROOT)}  ({p.stat().st_size:,} bytes)")
    if not args.no_sitemap:
        print(f"sitemap.xml  ({SITEMAP.stat().st_size:,} bytes, "
              f"URL {SITEMAP.read_text(encoding='utf-8').count('<url>')}개)")


if __name__ == "__main__":
    main()
