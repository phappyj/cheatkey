#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Work Cheatkey — /en/tools/ global SEO tool pages generator

affiliates.json (link, promo code, measured prices) + the TOOLS copy below
are merged into static English pages:

  en/tools/index.html              list of every tested tool + comparison table
  en/tools/{slug}.html             one page per tool
  sitemap.xml                      KR hub, /en/, /tips/, tip pages, /en/tools/ pages, privacy

Usage:
    python3 scripts/build_en_seo_pages.py              # pages + sitemap
    python3 scripts/build_en_seo_pages.py --no-sitemap

Add a tool by adding an entry to TOOLS (and its id in affiliates.json for the
affiliate URL). Prices, free limits and test numbers must come from
affiliates.json's measured fields — do not type a number here that was not read
on the vendor's page or produced by our own test.
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
AFF = ROOT / "affiliates.json"
DEALS = ROOT / "deals.json"
TOOLS_DIR = ROOT / "en" / "tools"
SITEMAP = ROOT / "sitemap.xml"

SITE = "https://phappyj.github.io/cheatkey"
EN = SITE + "/en/"
TOOLS_URL = EN + "tools/"
OG_IMAGE = SITE + "/og.png"
GA_ID = "G-E23M7R0R8N"
BRAND = "Work Cheatkey"
TODAY = dt.date.today().isoformat()
PUBLISHED = "2026-11-25"

# ────────────────────────── editorial copy ──────────────────────────
# Numbers below are transcribed from affiliates.json (measured on the dates in
# "checked") and from our own runs (Klap/OpusClip, Originality.ai). Anything a
# vendor only claims about itself is labelled as a claim in the copy.
TOOLS: list[dict] = [
    {
        "slug": "klap",
        "id": "klap",
        "name": "Klap",
        "cat": "Video & Shorts",
        "cat_key": "video",
        "icon": "✂️",
        "checked": "24 Nov 2026",
        "score": 4.2,
        "score_note": "Fewer clips, but usable as they came out. The view-only free plan is the only reason it is not a 4.5.",
        "title": "Klap vs OpusClip Tested (2026): 6 Clips vs 18 | Work Cheatkey",
        "desc": "Same 11:42 interview into Klap and OpusClip: 6 clean clips against 18, one moment cut four times. Free limit, $29/mo price and the catch on each.",
        "h1": "Klap vs OpusClip on the same 11:42 interview: 6 usable clips against 18 to sort",
        "lede": "I put one interview link into both tools on 24 November 2026, default settings, and counted what came out. Klap gave fewer clips and they were postable as they were. OpusClip gave three times as many, and four of them cut the same moment. This is the free limit, the price per clip, and the part the sales page leaves out.",
        "verdict": [
            ("Free", "One video, preview and edit only — no card, but nothing downloads"),
            ("Paid", "$29/mo for 100 clips · $14.50/mo if billed yearly ($174 a year)"),
            ("Catch", "A 1:42 Korean seminar returned 1 clip — quiet or short sources under-deliver"),
        ],
        "evidence": "One side-by-side run on 24 Nov 2026 with the same YouTube link and default settings, Klap's pricing page read on 24 Nov 2026, and Klap's own “Is Klap free?” FAQ. No clips were published from the test: exports need a paid plan.",
        "tested": [
            "<strong>11:42 interview</strong> (Blender Foundation, CC BY 3.0) through both tools: Klap returned <strong>6 clips</strong> scored 82 / 80 / 78 / 75 / 70 / 68, each with a one-line reason for the score.",
            "Cuts land <strong>inside</strong> the clip: transcript gaps and waveform holes are removed, captions are burned in word by word, and the frame keeps following the speaker.",
            "<strong>OpusClip on the same video</strong>: 18 clips, scores 84–73, but 4 re-cut the same Blender Cloud moment and 2 opened on a black frame. Its top pick (1:35) was one continuous take, and “Creative Commons” came back as “Graves Common”.",
            "A <strong>1:42 Korean seminar</strong> returned 1 clip with “not enough speech”. Clip count follows how much speech the source has, not how long it is.",
            "Source videos can run up to 3 hours, and you are billed <strong>per clip generated</strong>, not per minute.",
        ],
        "pricing": [
            ("Free", "1 video · preview and edit · no card · no downloads or posting"),
            ("Basic", "$29/mo · 100 clips a month · 1 user"),
            ("Pro", "$79/mo · 300 clips a month"),
            ("Pro+", "$189/mo · 1,000 clips a month"),
            ("Billed yearly", "$14.50 / $39.50 / $94.50 a month — $174 / $474 / $1,134 a year (save 50%)"),
            ("Code", "HEEJAE — 30% off the first payment on monthly checkout"),
        ],
        "pricing_note": "Klap's FAQ quotes the yearly figure inside the monthly sentence (“Basic is $14.50/month … ($29 … month to month)”). The plan cards are monthly; the yearly toggle is what saves 50%. Paid exports carry no Klap branding.",
        "steps": [
            ("Paste the link or upload the file", "Sources up to 3 hours are fine. Pick the language the video is spoken in — the caption pass depends on it."),
            ("Read the reason, not the score", "Every clip comes with a virality score and a line explaining it. The 68 was still the clip I would have posted."),
            ("Fix the captions, then export", "Repair names the transcript got wrong in the editor. Downloading and posting need a paid plan; the free account stops at preview."),
        ],
        "best_for": ["Interviews, podcasts and webinars where you would rather post 6 clips today than sort 18."],
        "skip_if": ["You need one free export to try it properly — nothing downloads on the free account.", "The recording is short or quiet (a 1:42 seminar gave one clip)."],
        "cta_label": "Try Klap free — 1 video, no card",
        "cta_sub": "Exports need a paid plan · code HEEJAE takes 30% off the first payment",
        "faq": [
            ("Is Klap free?", "Only for looking. A free account turns one video into clips you can preview and edit, no card required; downloading or posting them needs a paid plan, from $29/month for 100 clips."),
            ("Klap or OpusClip?", "On our single test, Klap produced fewer and cleaner clips, OpusClip more with duplicates. If you want volume to hand-pick from, OpusClip; if you want to post what comes out, Klap."),
            ("How many clips will I get from one video?", "It follows the speech: 6 from an 11:42 interview, 1 from a 1:42 seminar. Budget by minutes of talking, not minutes of video."),
            ("Does the HEEJAE code work?", "It came with this link and takes 30% off the first payment on monthly checkout. Check it on the billing screen before you pay."),
        ],
        "alts": ["taja-ai", "submagic", "quso-ai"],
    },
    {
        "slug": "loopcv",
        "id": "loopcv",
        "name": "LoopCV",
        "cat": "Job search",
        "cat_key": "auto",
        "icon": "📨",
        "checked": "25 Nov 2026",
        "score": 4.0,
        "score_note": "The free cap is honest and the €8.99 tier is priced fairly. It assumes a job title that the boards actually carry.",
        "title": "LoopCV Free Plan (2026): 10 Applications a Month | Work Cheatkey",
        "desc": "Free is a monthly cap, not a trial: 1 loop, 10 applications, 3 job boards, no card. Standard €8.99/mo — and where the dashboard numbers come from.",
        "h1": "LoopCV's free plan is a monthly cap, not a trial — 10 applications and one job title",
        "lede": "LoopCV takes your CV once, then applies for you every day: one “loop” per job title, per place. The free plan is real but small — one search, ten applications or emails and three job boards a month, no card and no time limit. Below is what each paid tier actually changes, and where the numbers on the sales page come from.",
        "verdict": [
            ("Free", "1 loop · 10 applications or emails · 3 job boards a month · no card"),
            ("Paid", "€8.99/mo for 20 loops and 100 applications · €7.33/mo on 3-month billing"),
            ("Catch", "Free applications sit at low priority, and one job title per loop"),
        ],
        "evidence": "Plan terms were read on loopcv.pro/pricing on 25 Nov 2026, both billing toggles, including the “Do I need a credit card?” FAQ. No LoopCV account has been run for this page: the dashboard figures are LoopCV's own published product screens, not our results.",
        "tested": [
            "<strong>Free (Basic Looper)</strong>: 1 job-title loop, 10 applications or emails, 3 job boards a month, low application priority, 2 AI CV checks.",
            "<strong>Standard €8.99/mo</strong>: 20 loops, 100 applications or emails, 20 job boards, medium priority, AI CV builder. Three-month billing is €7.33/mo (€22.00 every three months).",
            "<strong>Premium €29.99/mo</strong>: 50 loops, 300 applications, auto-fill for screening questions, sourcing from career pages.",
            "The pricing FAQ still says <strong>“from €9.99/month”</strong> while the Standard card reads <strong>€8.99</strong>. The card is what you are charged — read it on the checkout screen.",
            "The homepage says “30+ job boards”; the plan table caps free at 3 and paid at 20. Trust the table.",
        ],
        "pricing": [
            ("Free", "1 loop · 10 applications or emails · 3 job boards a month · no card, no time limit"),
            ("Standard", "€8.99/mo · 20 loops · 100 applications · 20 job boards (€7.33/mo on 3-month billing)"),
            ("Premium", "€29.99/mo · 50 loops · 300 applications · screening auto-fill (€22.49/mo on 3 months)"),
            ("Done for you", "€87.99/mo · €65.99/mo on 3-month billing"),
        ],
        "pricing_note": "The monthly and 3-month toggles were both read on 25 Nov 2026. A Black Friday code (BLACKFRIDAY2026, 15% off) was running with a countdown ending around 29 Nov — it is not part of the standing price, so check the banner before paying.",
        "steps": [
            ("Upload the CV once", "PDF in, then set the name and email signature that goes out with every application."),
            ("Build one loop per job title", "Search info → email template → preferences → review. One loop is one title plus one place; on free you get one loop a month."),
            ("Read Statistics, not your inbox", "Matches, emails sent, applications submitted, per loop. If a loop matches a lot and applies little, the email template is the problem."),
        ],
        "best_for": ["One clearly named job title that you want applied to in volume, in a city the boards cover."],
        "skip_if": ["You rewrite every cover letter by hand — that is not what this automates.", "The role is niche enough that the big boards do not carry it."],
        "cta_label": "Try LoopCV — 10 applications a month, free",
        "cta_sub": "No card · free is a monthly cap, not a trial · Standard €8.99/mo",
        "faq": [
            ("Is LoopCV free?", "Yes, with a monthly cap: 1 job-title loop, up to 10 applications or emails, 3 job boards, no credit card and no time limit. Paid starts at €8.99/month."),
            ("Do I need a credit card for the free plan?", "No. Their FAQ says the free plan needs no card, and the free plan does not expire."),
            ("Is it safe to let a tool apply for me?", "It sends in your name, so proofread the email template once and watch the first week of applications before you widen it. On free you are limited to ten a month anyway."),
            ("Does it work outside the US?", "A loop is a job title plus a place, so put your city or country in the loop. Which boards it can reach is capped by your plan."),
        ],
        "alts": ["make-com", "originality-ai", "speak-ai"],
    },
    {
        "slug": "submagic",
        "id": "submagic",
        "name": "Submagic",
        "cat": "Video & Shorts",
        "cat_key": "video",
        "icon": "💬",
        "checked": "24 Nov 2026",
        "score": 4.3,
        "score_note": "Cheapest paid tier in this list at $12/mo yearly. The free plan is a real one, as long as the watermark is acceptable.",
        "title": "Submagic Free Plan (2026): 15 Credits = 5 Videos | Work Cheatkey",
        "desc": "15 free credits a month is about five captioned uploads, no card — but every export is watermarked. Starter $19 ($12 yearly) caps a video at 2 min.",
        "h1": "Submagic's 15 free credits are about five captioned videos — and every export has a watermark",
        "lede": "Submagic takes a raw vertical clip and returns a captioned one with cuts, zooms and b-roll. On paper its free plan is the most generous here: 15 credits a month, no card. In practice the credit maths and the watermark decide whether it is usable for you.",
        "verdict": [
            ("Free", "15 credits a month ≈ 5 captioned uploads · no card"),
            ("Paid", "$19/mo, or $12/mo billed yearly ($144 a year) with 1080p and no watermark"),
            ("Catch", "Starter caps each video at 2 minutes, and free exports keep the watermark"),
        ],
        "evidence": "Plan terms read on submagic.co/pricing, app.submagic.co/signup and Submagic's help centre on 24 Nov 2026. No Submagic account was used to edit a video for this page: credit costs are their published rates, not a log of our usage.",
        "tested": [
            "<strong>Free: 15 credits a month.</strong> One captioned upload costs 3 credits, so about five videos; auto zooms, clean audio and other extras cost more on top.",
            "Free exports are <strong>watermarked</strong>. Removing the watermark is a paid feature — their help centre says so in the same sentence as the free allowance.",
            "Starter is <strong>$19/mo</strong> or <strong>$12/mo billed yearly</strong> ($144 a year): 45 credits, 1080p, no watermark — but each video is capped at 2 minutes.",
            "Credits reset monthly and <strong>unused credits do not roll over</strong>.",
            "The 123+ languages, 99% accuracy and 30+ caption styles are <strong>vendor claims</strong> on their homepage; we did not measure accuracy.",
        ],
        "pricing": [
            ("Free", "15 credits/mo ≈ 5 captioned videos · no card · watermark on export"),
            ("Starter", "$19/mo or $12/mo yearly ($144/yr) · 45 credits · 1080p · 2-minute cap"),
            ("Pro", "$39/mo or $23/mo yearly ($276/yr) · 120 credits · 5-minute duration · 2K"),
            ("Business", "$69/mo or $41/mo yearly ($492/yr) · 300 credits · 30-minute duration · 4K, API"),
        ],
        "pricing_note": "The pricing page opens on the yearly toggle, so the numbers you see first ($12 / $23 / $41) are monthly equivalents of the annual total. The monthly toggle reads $19 / $39 / $69.",
        "steps": [
            ("Upload the clip", "Vertical or landscape — it crops to 9:16 and works on the audio."),
            ("Pick a caption preset and let it edit", "The preset sets font, colour and animation; the silence cut and zoom come from the same pass."),
            ("Fix the two words it mishears, then export", "Names and product terms are what it gets wrong. On the free plan the export keeps the watermark."),
        ],
        "best_for": ["Shorts and Reels where the caption style is most of the edit."],
        "skip_if": ["Your source clips run past 2 minutes on the Starter plan.", "You need more than about five captioned videos a month without paying."],
        "cta_label": "Try Submagic free — 15 credits",
        "cta_sub": "No card · watermark on free exports · Starter $12/mo billed yearly",
        "faq": [
            ("How much is Submagic's free plan?", "15 credits a month, enough for about five captioned uploads, no card required. Every export on the free plan carries a Submagic watermark."),
            ("Why did my credits go faster than five videos?", "A captioned upload is 3 credits; auto zooms, clean audio and other extras each add credits, which leaves fewer videos."),
            ("Can I remove the watermark without paying?", "No. Watermark removal is part of the paid plans, from $19/month or $12/month billed yearly."),
            ("Which plan do I need for longer clips?", "Starter caps a video at 2 minutes; Pro allows 5 and Business 30, so pick by clip length before credit count."),
        ],
        "alts": ["klap", "taja-ai", "quso-ai"],
    },
    {
        "slug": "quso-ai",
        "id": "quso",
        "name": "quso.ai",
        "cat": "Video & Shorts",
        "cat_key": "video",
        "icon": "🎬",
        "checked": "21 Nov 2026",
        "score": 4.0,
        "score_note": "The 75 free credits are usable for a weekly cut. The 7-day retention is what stops it being a home for a small team.",
        "title": "quso.ai Review (2026): 75 Free Credits a Month | Work Cheatkey",
        "desc": "75 credits ≈ 75 minutes processed a month, 720p with a watermark, files kept 7 days, CutMagic on the first 3 videos. Yearly plans 50% off until 1 Dec 2026.",
        "h1": "quso.ai turns long recordings into vertical clips — with 75 free credits and a 7-day catch",
        "lede": "quso.ai, formerly vidyo.ai, cuts long videos and podcasts into captioned vertical clips. The free tier is usable for a weekly test: 75 credits, about 75 minutes processed. What keeps it a trial rather than a home is 720p, a watermark, and the fact that your files are deleted after seven days.",
        "verdict": [
            ("Free", "75 credits/mo ≈ 75 minutes · 720p · watermark · files kept 7 days"),
            ("Paid", "Lite $29/mo, or $174 a year while the 50% yearly offer runs"),
            ("Catch", "7-day retention on free — download the clips the same week"),
        ],
        "evidence": "Plan terms and the Black Friday offer were read on quso.ai/pricing on 21 Nov 2026, alongside the affiliate kit sent by quso.ai. No quso.ai account was used for this page; clip-quality claims are the vendor's.",
        "tested": [
            "<strong>Free</strong>: 75 credits a month (≈75 minutes processed), 720p exports with a quso.ai watermark, 7-day data retention, CutMagic on the first 3 videos.",
            "<strong>Yearly plans are 50% off</strong> at the time of writing (offer ends 1 Dec 2026, 23:59 IST) and the discount is kept at renewal: Lite <strong>$174/yr</strong> ($29 monthly), Essential $234/yr ($39), Growth $294/yr ($49).",
            "The 50% is applied <strong>without a code</strong> on the pricing page — do not go hunting for a coupon.",
            "Korean IPs are shown credit packs (100 credits ₩3,290) instead of subscriptions; the prices above are the US/global page.",
            "The <strong>7-day retention</strong> is the part to plan around: download what you need in the week you make it.",
        ],
        "pricing": [
            ("Free", "75 credits/mo · 720p · watermark · 7-day retention"),
            ("Lite", "$29/mo · $174 a year with the 50% yearly offer"),
            ("Essential", "$39/mo · $234 a year (50% off)"),
            ("Growth", "$49/mo · $294 a year (50% off)"),
        ],
        "pricing_note": "The yearly discount ends 1 Dec 2026 23:59 IST and stays on renewals while you keep the subscription. Monthly prices are unaffected.",
        "steps": [
            ("Paste the link or upload the recording", "A webinar, a podcast episode, a long meeting — the clip pass works off the transcript."),
            ("Let CutMagic pick the clips and captions", "It scores the moments and writes captions; on the free plan this runs on your first three videos."),
            ("Download the clips in the same week", "Free files are kept 7 days and export at 720p with a watermark until you subscribe."),
        ],
        "best_for": ["Cutting one webinar or podcast a week into vertical clips you post yourself."],
        "skip_if": ["You need 1080p, or files kept longer than a week, without paying."],
        "cta_label": "Try quso.ai free — 75 credits",
        "cta_sub": "Yearly 50% off until 1 Dec 2026, no code · 720p and watermark on free",
        "faq": [
            ("Is quso.ai free?", "Yes, 75 credits a month, which is about 75 minutes processed, at 720p with a watermark. Files are retained for 7 days."),
            ("What happens to my videos after 7 days?", "Free-plan files are deleted after 7 days. Download the clips you want to keep in the week you generate them."),
            ("Does the 50% yearly discount stay?", "According to quso.ai's offer, the discount is kept at every renewal while you stay subscribed. It ends 1 Dec 2026 for new signups."),
        ],
        "alts": ["klap", "taja-ai", "pictory"],
    },
    {
        "slug": "speak-ai",
        "id": "speakai",
        "name": "Speak AI",
        "cat": "Meetings",
        "cat_key": "slides",
        "icon": "🎧",
        "checked": "25 Nov 2026",
        "score": 4.1,
        "score_note": "Priced per seat with a clear credit rate. No free plan is the reason it is not higher.",
        "title": "Speak AI Review (2026): $20/Seat, No Free Plan | Work Cheatkey",
        "desc": "No free tier: a 7-day card-free trial, then $20/user/mo billed annually for 25 credits ≈ 25 hours of transcription. Pay-as-you-go rates too.",
        "h1": "Speak AI: $20 a seat, 25 hours of transcription, and no free plan — only a 7-day trial",
        "lede": "Speak AI records your meeting or takes the audio, transcribes it in 100+ languages, and lets you ask questions of the transcript afterwards. Pricing is per seat: $20 a user a month billed annually includes 25 credits, which their page equates to about 25 hours of standard transcription. There is no free tier — the trial is 7 days and needs no card.",
        "verdict": [
            ("Free", "None — 7-day trial, no card, cancel anytime"),
            ("Paid", "$20/user/mo billed annually ($240 a year) for 25 credits ≈ 25 hours"),
            ("Catch", "A card is required once the trial ends, even on pay-as-you-go credits"),
        ],
        "evidence": "Read on speakai.co/pricing on 25 Nov 2026 (plan cards, credit rates, trial terms). No Speak AI account was used for this page: transcription accuracy and language coverage are the vendor's claims, not our measurements.",
        "tested": [
            "<strong>No free plan.</strong> 7-day trial, no card, cancel anytime; a card is needed after the trial.",
            "<strong>Pro: $20/user/month</strong> billed annually ($240 a user a year, shown as 20% off). Includes 25 credits a seat — about 25 hours of standard transcription — and 10 GB storage.",
            "<strong>Pay as you go</strong>: 1 credit = $1, top up from 10 credits. Rates: 2 credits per hour of standard transcription, 3 per hour for premium languages, 4 per hour of meeting transcription.",
            "It can <strong>join the call</strong> (Zoom, Teams, Meet) instead of needing a recording — that is the workflow this site's stack uses for meeting notes.",
            "Enterprise is a custom build: white-label, custom domains, voice agents, unlimited seats.",
        ],
        "pricing": [
            ("Free", "No free plan · 7-day trial · no card"),
            ("Pro", "$20/user/mo billed annually ($240/user/yr) · 25 credits ≈ 25 hours · 10 GB"),
            ("Pay as you go", "$1 = 1 credit · 2 credits/hour transcription · top up from 10 credits"),
            ("Enterprise", "Custom · white-label, custom domains, unlimited seats"),
        ],
        "pricing_note": "Credits are per seat, so a five-person team multiplies the Pro price by five. If you only need a few hours a month, the pay-as-you-go credits are usually cheaper than a subscription — but they still need a card on file after the trial.",
        "steps": [
            ("Send it to the call, or upload the file", "Joining the meeting is the reason to use it over a recorder: no one has to remember to press record."),
            ("Read the summary, then the transcript", "The summary is the draft; the transcript is the evidence. Keep both for anything you will quote later."),
            ("Ask the transcript instead of re-listening", "“What did we decide on pricing?” beats scrubbing an hour of audio, and the answer stays searchable."),
        ],
        "best_for": ["People who live in meetings and need searchable transcripts, shared with a small team."],
        "skip_if": ["You need two or three hours a month — pay-as-you-go credits cover that without a seat."],
        "cta_label": "Try Speak AI free for 7 days",
        "cta_sub": "No card for the trial · Pro $20/user/mo billed annually",
        "faq": [
            ("Does Speak AI have a free plan?", "No. There is a 7-day trial with no card required, then a paid plan or pay-as-you-go credits. A card is needed after the trial."),
            ("How many hours is 25 credits?", "Speak AI equates 25 credits a seat to about 25 hours of standard transcription. Premium languages and meeting transcription cost more credits per hour."),
            ("Can it join my Zoom call?", "Yes — Speak AI can join Zoom, Teams and Meet to record and transcribe, which is how the meeting-notes workflow on this site runs."),
        ],
        "alts": ["make-com", "loopcv", "decktopus"],
    },
    {
        "slug": "taja-ai",
        "id": "taja",
        "name": "Taja AI",
        "cat": "Video & Shorts",
        "cat_key": "video",
        "icon": "📱",
        "checked": "23 Nov 2026",
        "score": 3.7,
        "score_note": "A trial that will not let you download is a demo, not a test. The $19 tier itself is reasonable.",
        "title": "Taja AI Review (2026): Trial Blocks Downloads | Work Cheatkey",
        "desc": "No free plan: a 7-day trial takes 4 videos but blocks downloads and watermark removal, so you pay from $19/mo to export. Terms and limits inside.",
        "h1": "Taja AI has no free plan, and the 7-day trial will not let you download the shorts",
        "lede": "Taja turns one long video into shorts, titles, tags, thumbnails and blog copy. The trial is 7 days and takes up to four long videos — but watermark removal and downloading shorts are both excluded, so you cannot judge a finished file until you subscribe.",
        "verdict": [
            ("Free", "None — 7-day trial, 4 long videos, no card, no downloads"),
            ("Paid", "$19/mo for 4 videos a month and 10 shorts each ($15.99/mo billed yearly)"),
            ("Catch", "The trial blocks watermark removal and Download Shorts — export starts on payment"),
        ],
        "evidence": "Read on taja.ai and taja.ai/pricing on 23 Nov 2026: plan cards, the full compare table and the pricing FAQ. No Taja account was used for this page.",
        "tested": [
            "<strong>Trial</strong>: 7 days, up to 4 long-form videos, 2 hours each, 5 GB import, up to 5 shorts per video, no card.",
            "<strong>Not in the trial</strong>: watermark removal and Download Shorts — both show “–” in the compare table, which is the detail the headline free-trial copy skips.",
            "<strong>Starter $19/mo</strong> ($15.99/mo billed yearly): 4 videos a month, 10 shorts per video, downloads, watermark removal, scheduling to all platforms, thumbnails.",
            "<strong>Professional $49/mo</strong> ($39.99 yearly): 10 videos, 20 shorts each. <strong>Teams $99/mo</strong> ($79.99 yearly): 5 users, unlimited videos.",
            "Auto-written titles and captions arrive as <strong>drafts</strong> — budget a pass for your channel's tone before publishing.",
        ],
        "pricing": [
            ("Free", "No free plan · 7-day trial · 4 videos · no downloads, no watermark removal"),
            ("Starter", "$19/mo or $15.99/mo yearly · 4 videos · 10 shorts each"),
            ("Professional", "$49/mo or $39.99/mo yearly · 10 videos · 20 shorts each"),
            ("Teams", "$99/mo or $79.99/mo yearly · 5 users · unlimited videos"),
        ],
        "pricing_note": "The pricing page opens on the annual toggle ($15.99 / $39.99 / $79.99 a month billed yearly). The monthly prices above come from the compare table below the cards.",
        "steps": [
            ("Import the long video", "Paste a YouTube link or upload up to 5 GB; the source can run 2 hours."),
            ("Generate the whole set", "Shorts, titles, tags, a thumbnail and a blog draft come out of one run."),
            ("Edit before you schedule", "Treat titles and captions as drafts. Scheduling is included, so the last step can be a queue rather than a download."),
        ],
        "best_for": ["A channel publishing several shorts from one recording every week."],
        "skip_if": ["You want to see a finished download before paying — the trial blocks exactly that."],
        "cta_label": "Try Taja AI for 7 days",
        "cta_sub": "No card · 4 videos · downloads only on paid plans",
        "faq": [
            ("Is there a free plan?", "No. Taja offers a 7-day free trial that optimises and repurposes up to 4 long-form videos. The trial needs no card."),
            ("What does the trial include?", "4 long videos up to 2 hours each, 5 GB import, up to 5 shorts per video, titles, tags and thumbnails — but not watermark removal or downloads."),
            ("Does the trial let me download shorts?", "No. The pricing compare table shows “–” for Download Shorts and watermark removal on the free-trial column, so exporting starts with a paid plan from $19/month."),
        ],
        "alts": ["klap", "submagic", "quso-ai"],
    },
    {
        "slug": "make-com",
        "id": "make",
        "name": "Make.com",
        "cat": "Automation",
        "cat_key": "auto",
        "icon": "⚙️",
        "checked": "23 Nov 2026",
        "score": 4.5,
        "score_note": "Free is genuinely useful for two or three small jobs, and $9/mo yearly removes every limit that matters.",
        "title": "Make.com Free Plan (2026): 1,000 Credits, 2 Flows | Work Cheatkey",
        "desc": "Free is real but capped: 1,000 credits a month, 2 active scenarios, runs no faster than every 15 minutes, credits expire. Core $9/mo yearly lifts all three.",
        "h1": "Make.com's free plan: 1,000 credits, two scenarios, and nothing faster than every 15 minutes",
        "lede": "Make is the glue behind most automation on this site: a row appears in a sheet, an AI step rewrites it, a message lands in Slack. The free plan is usable for real work — 1,000 credits a month across 3,500+ apps — as long as two active scenarios and a 15-minute floor are enough for the job.",
        "verdict": [
            ("Free", "1,000 credits/mo · 2 active scenarios · 15-minute minimum interval"),
            ("Paid", "Core $9/mo billed yearly ($10.59 monthly) — 10,000 credits, unlimited scenarios"),
            ("Catch", "Unused credits expire at the end of the term, and free runs no more often than every 15 minutes"),
        ],
        "evidence": "make.com/en/pricing read on 23 Nov 2026, on both the annual and monthly tabs. The register page sits behind a Cloudflare check, so the free-month offer was verified from the affiliate program terms rather than a fresh signup.",
        "tested": [
            "<strong>Free $0</strong>: 1,000 credits a month, 2 active scenarios, 15-minute minimum interval between runs, 5-minute max execution, 512 MB transfer, 7-day logs, 3,500+ apps.",
            "<strong>Core $9/mo billed yearly</strong> ($10.59 monthly): 10,000 credits, unlimited active scenarios, runs down to 1 minute, 40-minute execution, 30-day logs.",
            "<strong>Pro $16/mo yearly</strong> ($18.82 monthly) and <strong>Teams $29/mo yearly</strong> ($34.12 monthly) add volume and seats.",
            "<strong>No rollover</strong>: unused credits expire at the end of the billing term.",
            "New accounts get <strong>1 month of Core free</strong> through the affiliate offer — enough to test a faster interval before deciding.",
        ],
        "pricing": [
            ("Free", "$0 · 1,000 credits · 2 active scenarios · 15-minute floor · 7-day logs"),
            ("Core", "$9/mo billed yearly ($10.59 monthly) · 10,000 credits · unlimited scenarios · 1-minute floor"),
            ("Pro", "$16/mo yearly ($18.82 monthly) · 1,600+ credits tier"),
            ("Teams", "$29/mo yearly ($34.12 monthly)"),
        ],
        "pricing_note": "Credits replaced “operations” as the billing unit in August 2025, so older tutorials count operations. A run that polls every minute burns credits quickly; set the interval as wide as the job allows.",
        "steps": [
            ("Pick the trigger", "A new sheet row, a labelled email, a webhook. One trigger per scenario keeps the credit cost visible."),
            ("Add the AI step", "An AI or HTTP module that takes the text and returns the rewrite. Map only the fields you need — every mapped field can cost a credit."),
            ("Send it where you will read it", "Slack, Drafts, Notion. Turn it on and watch the first two runs in the log before you trust it."),
        ],
        "best_for": ["Two or three small automations that remove a weekly chore."],
        "skip_if": ["You need a scenario running every minute, or more than two active at once — that is Core."],
        "cta_label": "Build one free on Make.com",
        "cta_sub": "1,000 credits a month · 1 month of Core free for new accounts",
        "faq": [
            ("What does Make's free plan include?", "1,000 credits a month, 2 active scenarios, a 15-minute minimum interval between runs, 5-minute execution, 512 MB transfer, 7-day logs and 3,500+ apps."),
            ("Why did my scenario stop?", "On free, one of three limits: two scenarios already active, a run scheduled tighter than every 15 minutes, or the 1,000 credits used up."),
            ("Do unused credits roll over?", "No. Credits expire at the end of the term, so plan the month's automations rather than stockpiling."),
        ],
        "alts": ["speak-ai", "loopcv", "originality-ai"],
    },
    {
        "slug": "originality-ai",
        "id": "originality",
        "name": "Originality.ai",
        "cat": "Writing",
        "cat_key": "writing",
        "icon": "🛡️",
        "checked": "24 Nov 2026",
        "score": 4.0,
        "score_note": "The per-sentence highlighting is the useful part. The headline score is a signal, and their own guide says so.",
        "title": "Originality.ai Tested (2026): 98% AI on 159 Words | Work Cheatkey",
        "desc": "We spent 7 of the 100 free credits: 159 English words cost 2 credits and scored 98% AI; a Korean memo rewrite scored 95% original. Prices and caveat.",
        "h1": "Originality.ai: what 100 free credits actually buy, and why a 98% AI score is not proof",
        "lede": "I ran three real samples through the free plan: a 159-word English text, then two Korean rewrites of the same work memo. The detector does one job well — it shows which sentences read like a model — and its own guidance says the score is a signal for review, not proof of authorship.",
        "verdict": [
            ("Free", "100 credits once (10,000 words) · no monthly refill on the plan card"),
            ("Paid", "Pro $14.95/mo for 200,000 words · $12.95/mo billed yearly"),
            ("Catch", "A formal register scores as AI: a Korean report hit 97% AI, the same content as a memo 5%"),
        ],
        "evidence": "Scans run on app.originality.ai on 22 and 24 Nov 2026 on the free plan (AI Score only, detector v5.0); pricing read on originality.ai/pricing on 24 Nov 2026.",
        "tested": [
            "<strong>159-word English sample</strong>: 2 credits, <strong>98% Likely AI</strong> / 2% Likely Original, with a score per sentence.",
            "<strong>104-word Korean formal report</strong>: 2 credits, <strong>97% Likely AI</strong>.",
            "<strong>The same content as a 120-word work memo</strong>: 2 credits, <strong>95% Likely Original</strong> / 5% Likely AI.",
            "<strong>A half-formal rewrite</strong>: 1 credit, 86% Likely AI — the <em>register</em>, not the topic, is what the model flags.",
            "7 of the 100 free credits used across all scans (93 left). One credit covers 100 words, rounded up per chunk.",
            "Their own score guide: <em>“As AI detectors can make mistakes, the score should be considered as a signal for review, not proof of authorship or misconduct.”</em>",
        ],
        "pricing": [
            ("Free", "Plan card: 10,000 words / 100 credits, one time · compare table: 60 credits, 3 scans a day"),
            ("Pro", "$14.95/mo · 200,000 words · $12.95/mo billed yearly"),
            ("Enterprise", "$179/mo · custom volume, team seats, API"),
        ],
        "pricing_note": "The pricing page contradicts itself: the plan card says 100 credits one time, while the compare table below lists 60 credits with 3 scans a day. Both were on the page on 24 Nov 2026 — check your credit balance in the app rather than the marketing copy.",
        "steps": [
            ("Paste the text you are about to send", "A report, a proposal, a translation. The scan is per hundred words, so a long document eats credits fast."),
            ("Read the sentence highlights, not the headline", "The number gets the attention; the flagged sentences are the actual rewrite list."),
            ("Rewrite in a register you would speak, then rescan", "Our memo rewrite moved 97% AI to 5% AI without changing the meaning."),
        ],
        "best_for": ["Checking outbound content before a client, a hiring manager or an editor reads it."],
        "skip_if": ["You need a verdict you can defend to someone else — the vendor itself calls the score a signal for review."],
        "cta_label": "Run one scan on the free credits",
        "cta_sub": "100 credits once · Pro $14.95/mo for 200,000 words",
        "faq": [
            ("Is Originality.ai free?", "It has a one-time free allowance on the plan card (10,000 words / 100 credits). The compare table on the same page lists 60 credits with 3 scans a day, so read your balance in the app after signing up."),
            ("Why did 159 words cost 2 credits?", "One credit covers 100 words and the charge rounds up per chunk, so a 159-word scan bills as two credits."),
            ("Can it detect Korean text?", "Yes — our Korean samples were scanned and scored per sentence. A formal report register scored 97% AI, and the same content written as a memo scored 5% AI."),
            ("Should I trust the score?", "As a review signal, yes: it points you at sentences worth rewriting. As proof that a person or a model wrote something, no — Originality's own guide says the score can be wrong."),
        ],
        "alts": ["make-com", "speak-ai", "loopcv"],
    },
    {
        "slug": "pictory",
        "id": "pictory",
        "name": "Pictory",
        "cat": "Video & Shorts",
        "cat_key": "video",
        "icon": "🎥",
        "checked": "23 Nov 2026",
        "score": 3.8,
        "score_note": "A script-to-video tool with a fair trial, but 3 videos at 720p leaves little room to judge.",
        "title": "Pictory Trial (2026): 14 Days, 300 Credits, 720p | Work Cheatkey",
        "desc": "Trial: 14 days, 300 credits, 3 videos, 5-min max, 720p with a watermark, no card. Black Friday annual from $12.50/mo — and the code that does not stack.",
        "h1": "Pictory's trial: 14 days, 300 credits, three videos — and 720p with a watermark until you pay",
        "lede": "Pictory turns a script, a blog link or a deck into a voiced video with scenes and captions. The trial is card-free and two weeks long, which is enough for one real script — but three videos and a 720p watermark decide whether the free run tells you anything.",
        "verdict": [
            ("Free", "14-day trial · 300 credits (≈10 min of generation) · 3 videos · 720p + watermark"),
            ("Paid", "Black Friday annual from $12.50/mo (Starter, was $29) at the time of writing"),
            ("Catch", "Three videos at 720p in the trial, and the CHEATKEY code does not stack with the sale"),
        ],
        "evidence": "pictory.ai/pricing read on 23 Nov 2026 on the annual toggle, including the trial card and the Black Friday cards. No Pictory account was used for this page.",
        "tested": [
            "<strong>Trial</strong>: 14 days, 300 credits (up to about 10 minutes of generation), 3 videos, 5-minute maximum length, 500 MB storage, 720p max export, Pictory watermark, no card.",
            "<strong>Black Friday annual</strong> at the time of writing: Starter $12.50/mo (was $29), Professional $17.50/mo (was $59), Teams $59.50/mo (was $199) — <strong>no code needed</strong>.",
            "The dedicated code <strong>CHEATKEY</strong> does not stack with the Black Friday price. While the sale runs, take the sale.",
            "The 2 Dec end date shown on the pricing page on 20 Nov was <strong>gone on 23 Nov</strong> — treat the sale as “while it lasts” and check the page before you buy.",
            "Inputs: a script, a blog URL or a PPT; output is a voiced video with scenes, captions and a 9:16 option.",
        ],
        "pricing": [
            ("Free", "14-day trial · 300 credits · 3 videos · 5 min max · 720p · watermark"),
            ("Starter", "$12.50/mo on Black Friday annual (was $29)"),
            ("Professional", "$17.50/mo on Black Friday annual (was $59)"),
            ("Teams", "$59.50/mo on Black Friday annual (was $199)"),
        ],
        "pricing_note": "Those three figures are the Black Friday annual prices read on 23 Nov 2026, not standing prices. The trial needs no card, so you can test one script before any of this matters.",
        "steps": [
            ("Paste the script or the link", "A blog post URL, a script you wrote, or a deck you exported. The voice comes from the same pass."),
            ("Fix the scenes where they lag", "Scene length follows the script, so cut sentences rather than dragging scenes — it also keeps the 5-minute trial limit in reach."),
            ("Export after you subscribe", "The trial caps at 720p with a watermark; 1080p export is a paid feature."),
        ],
        "best_for": ["Explainer videos from text, where you would otherwise record a screen."],
        "skip_if": ["You need a clean sample without a watermark, or more than three videos, before deciding."],
        "cta_label": "Try Pictory free for 14 days",
        "cta_sub": "No card · 3 videos · 720p + watermark · Black Friday annual from $12.50/mo",
        "faq": [
            ("Is there a free plan?", "No, a 14-day trial: 300 credits, 3 videos, 720p with a watermark, no card required. Paid plans start from $12.50/mo on the Black Friday annual offer read on 23 Nov 2026."),
            ("Does the CHEATKEY code stack with Black Friday?", "No. The Black Friday price needs no code, and the dedicated code does not combine with it — use whichever is cheaper at checkout."),
            ("How long can a trial video be?", "5 minutes per video, and the trial allows 3 videos in total, which is about 10 minutes of generation across them."),
        ],
        "alts": ["quso-ai", "submagic", "decktopus"],
    },
    {
        "slug": "decktopus",
        "id": "decktopus",
        "name": "Decktopus",
        "cat": "Slides",
        "cat_key": "slides",
        "icon": "🖼️",
        "checked": "23 Nov 2026",
        "score": 3.6,
        "score_note": "A good first draft of a deck, but three slides at signup and 5 credits a slide means you cannot iterate before paying.",
        "title": "Decktopus (2026): No Free Plan, 3 Slides Free | Work Cheatkey",
        "desc": "Three slides at signup, then 5 credits a slide — there is no free plan. Pro $9.99/mo yearly, Business $19.99/seat, 66% off annual to 11 Dec 2026.",
        "h1": "Decktopus gives you three slides, then charges five credits a slide — there is no free plan",
        "lede": "Decktopus builds a deck from a prompt: outline, content, design, exportable to PPT and PDF. The catch is in the credit maths — the signup allowance covers three slides, and from there a generated slide costs five credits, so you build one deck, look at it, and then decide whether to pay.",
        "verdict": [
            ("Free", "No free plan · 3 slides covered at signup · 5 credits per slide after that"),
            ("Paid", "Pro $9.99/mo billed yearly · Business $19.99 per seat"),
            ("Catch", "No free plan, and every regenerated slide spends credits — iterate after paying, not before"),
        ],
        "evidence": "decktopus.com and its pricing page read on 23 Nov 2026: Pro and Business cards, signup credits, credit cost per slide and the Black Friday banner. No Decktopus account was used for this page.",
        "tested": [
            "<strong>No free plan.</strong> The signup allowance covers 3 slides; after that, each generated slide costs 5 credits.",
            "<strong>Pro $9.99/mo</strong> billed yearly; <strong>Business $19.99 a seat</strong>.",
            "<strong>Black Friday</strong> at the time of writing: 66% off annual plans until 11 Dec 2026.",
            "Output is a <strong>starting draft</strong>: the outline and structure carry the value, the layout needs your pass before it meets a client.",
            "Export to <strong>PPT</strong> is the reason to use it over a design tool — the deck keeps working in PowerPoint afterwards.",
        ],
        "pricing": [
            ("Free", "No free plan · 3 slides at signup · 5 credits per slide"),
            ("Pro", "$9.99/mo billed yearly"),
            ("Business", "$19.99 per seat"),
            ("Black Friday", "66% off annual plans until 11 Dec 2026"),
        ],
        "pricing_note": "The signup allowance is one-time, not a monthly free tier — there is no plan that keeps costing $0 after the first three slides.",
        "steps": [
            ("Describe the deck", "Audience, sections and tone in two or three sentences. Vague prompts return generic slides, and each regeneration costs credits."),
            ("Edit the outline before generating slides", "The outline is the cheap place to be wrong. Change it, then let the slides build."),
            ("Export to PPT or PDF and restyle", "The export is where the design becomes yours — fonts, colours and the two or three slides that always need a human."),
        ],
        "best_for": ["A first draft of a 10–15 slide deck in minutes, before the real editing starts."],
        "skip_if": ["You want to iterate freely — every regenerated slide spends credits, and there is no free tier to absorb that."],
        "cta_label": "Try Decktopus with 3 free slides",
        "cta_sub": "5 credits per slide after that · Pro $9.99/mo yearly · 66% off annual until 11 Dec 2026",
        "faq": [
            ("Is Decktopus free?", "No. A new account gets three slides at signup; generating more costs 5 credits a slide, on a paid plan from $9.99/month billed yearly."),
            ("How many slides do I get before paying?", "Three. Decktopus covers three slides with the signup allowance and charges 5 credits per slide after that, so a longer deck needs a plan."),
            ("Can I export to PowerPoint?", "Yes — Decktopus exports to PPT and PDF, which is usually the point: the deck keeps being editable in PowerPoint after the AI draft."),
        ],
        "alts": ["speak-ai", "make-com", "pictory"],
    },
]

# ────────────────────────── style ──────────────────────────
CSS = """
  :root{
    --bg:#F8F9FA; --card:#FFFFFF; --line:#EAECEF; --line-2:#F1F2F4;
    --ink:#111827; --ink-2:#6B7280; --ink-3:#9CA3AF;
    --navy:#0F172A; --navy-2:#1E293B;
    --mint:#0E9F6E; --mint-deep:#0B7A55; --mint-soft:#ECFDF5; --mint-line:#BBF0DD;
    --amber:#B45309; --amber-soft:#FFF7ED; --amber-line:#FBE7CB;
    --max:620px; --pad:18px;
    --shadow:0 1px 2px rgba(17,24,39,.04), 0 10px 28px -20px rgba(17,24,39,.18);
  }
  *{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
  html,body{margin:0;padding:0}
  html{background:var(--bg);scroll-behavior:smooth}
  body{
    background:var(--bg);color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,"Helvetica Neue",Arial,sans-serif;
    font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased;
    letter-spacing:-0.008em;min-height:100dvh;overflow-wrap:break-word;
  }
  a{color:inherit}
  .nav{position:sticky;top:0;z-index:30;background:rgba(248,249,250,.9);
    -webkit-backdrop-filter:saturate(160%) blur(14px);backdrop-filter:saturate(160%) blur(14px);
    border-bottom:1px solid rgba(17,24,39,.06)}
  .nav-in{max-width:var(--max);margin:0 auto;display:flex;align-items:center;gap:10px;
    padding:calc(9px + env(safe-area-inset-top)) var(--pad) 9px}
  .brand{display:inline-flex;align-items:center;gap:6px;font-size:13.5px;font-weight:800;
    letter-spacing:-0.02em;color:var(--ink);text-decoration:none;white-space:nowrap}
  .brand .bolt{font-size:13px;line-height:1}
  .nav .chip{margin-left:auto;display:inline-flex;align-items:center;font-size:11.5px;font-weight:700;
    color:var(--ink-2);background:#fff;border:1px solid var(--line);border-radius:999px;
    padding:5px 10px;text-decoration:none;white-space:nowrap}
  .nav .chip:active{background:#F3F4F6}
  .shell{max-width:var(--max);margin:0 auto;padding:0 var(--pad) 64px}
  .crumb{display:inline-flex;padding:14px 2px 0;font-size:12.5px;font-weight:700;color:var(--ink-2);
    text-decoration:none;align-items:center;gap:5px}
  .crumb .arw{color:var(--mint)}
  .article{background:var(--card);border:1px solid var(--line);border-radius:22px;
    box-shadow:var(--shadow);padding:20px 18px 18px;margin-top:10px}
  .tag{display:inline-block;font-size:9.5px;font-weight:800;letter-spacing:.06em;
    color:var(--mint);background:var(--mint-soft);border:1px solid var(--mint-line);
    border-radius:999px;padding:3px 9px;margin-bottom:11px;text-transform:uppercase}
  h1{font-size:25px;line-height:1.3;font-weight:800;letter-spacing:-0.035em;margin:0 0 10px}
  .lede{margin:0 0 14px;color:#4B5563;font-size:14.5px;font-weight:500;line-height:1.68}
  .meta{display:flex;align-items:center;gap:7px;flex-wrap:wrap;font-size:11.5px;font-weight:600;
    color:var(--ink-3);padding-bottom:15px;border-bottom:1px solid var(--line-2)}
  .meta .dot{color:#D1D5DB}
  h2{font-size:16.5px;font-weight:800;letter-spacing:-0.028em;margin:26px 0 11px;line-height:1.35;
    display:flex;align-items:baseline;gap:8px}
  h2 .k{font-size:10px;font-weight:800;color:var(--mint);letter-spacing:.08em;flex:0 0 auto}
  .score{display:flex;align-items:center;gap:12px;background:linear-gradient(180deg,#F9FBFC 0%,#F4F7F9 100%);
    border:1px solid var(--line);border-radius:14px;padding:12px 13px;margin:6px 0 4px}
  .score .num{flex:0 0 auto;display:grid;place-items:center;width:52px;height:52px;border-radius:13px;
    background:var(--navy);color:#fff;font-size:17px;font-weight:800;letter-spacing:-0.04em}
  .score .num small{font-size:9px;font-weight:700;color:#9FB3C8;letter-spacing:.02em}
  .score .txt{font-size:12.2px;line-height:1.55;color:#4B5563;font-weight:600}
  .score .txt b{display:block;font-size:9.5px;letter-spacing:.08em;color:var(--ink-3);
    text-transform:uppercase;margin-bottom:3px;font-weight:800}
  .verdict{list-style:none;margin:12px 0 0;padding:0;display:grid;gap:7px}
  .verdict li{display:flex;gap:10px;align-items:flex-start;border:1px solid var(--line-2);
    border-radius:12px;padding:10px 12px;background:#FCFCFD;font-size:13px;line-height:1.55;color:#374151;font-weight:500}
  .verdict .kk{flex:0 0 52px;font-size:9.5px;font-weight:800;letter-spacing:.06em;color:var(--mint);
    text-transform:uppercase;padding-top:2px}
  .verdict .vv{min-width:0}
  .verdict .vv b{font-weight:800;color:var(--ink)}
  ul.plain{margin:0;padding-left:0;list-style:none}
  ul.plain li{position:relative;padding-left:18px;margin:0 0 9px;font-size:13.4px;line-height:1.65;color:#374151}
  ul.plain li:before{content:"";position:absolute;left:2px;top:8px;width:6px;height:6px;border-radius:2px;
    background:var(--mint);opacity:.55}
  ul.plain strong,b{color:var(--ink)}
  .evidence{background:var(--amber-soft);border:1px solid var(--amber-line);border-radius:12px;
    padding:11px 13px;margin:0 0 13px;font-size:12.2px;line-height:1.62;color:#7C4A12;font-weight:500}
  .evidence b{color:#8A3F04;font-weight:800;letter-spacing:.02em}
  table{width:100%;border-collapse:collapse;font-size:12.8px;margin:0}
  .tbl{overflow:hidden;border:1px solid var(--line);border-radius:14px;background:#fff}
  .tbl th{background:#F7F8FA;text-align:left;font-size:10px;letter-spacing:.06em;text-transform:uppercase;
    color:var(--ink-3);font-weight:800;padding:9px 12px;border-bottom:1px solid var(--line)}
  .tbl td{padding:10px 12px;border-bottom:1px solid var(--line-2);vertical-align:top;
    line-height:1.5;color:#374151;font-weight:500}
  .tbl tr:last-child td{border-bottom:none}
  .tbl td:first-child{font-weight:800;color:var(--ink);white-space:nowrap;font-size:12.3px}
  .note{margin:9px 0 0;font-size:11.8px;line-height:1.62;color:var(--ink-2);font-weight:500}
  .note b{color:var(--ink)}
  ol.steps{list-style:none;margin:0;padding:0;display:grid;gap:8px}
  ol.steps li{display:flex;gap:11px;align-items:flex-start;background:#FAFBFC;border:1px solid var(--line-2);
    border-radius:13px;padding:12px 13px}
  ol.steps .num{flex:0 0 22px;height:22px;border-radius:7px;background:#EEF0F3;color:var(--navy);
    font-weight:800;font-size:11px;display:grid;place-items:center;margin-top:1px;font-variant-numeric:tabular-nums}
  ol.steps .body{min-width:0}
  ol.steps .k{display:block;font-size:10px;font-weight:800;color:var(--mint);letter-spacing:.05em;
    text-transform:uppercase;margin-bottom:3px}
  ol.steps .v{font-size:13.2px;font-weight:600;color:#374151;line-height:1.55}
  .cta{display:block;margin-top:18px;text-decoration:none;background:var(--navy);color:#fff;
    border-radius:16px;padding:16px 16px 15px;box-shadow:0 16px 32px -24px rgba(15,23,42,.9)}
  .cta .lbl{display:block;font-size:9.5px;font-weight:800;letter-spacing:.09em;color:#6EE7B7;margin-bottom:6px;text-transform:uppercase}
  .cta .txt{display:flex;align-items:center;gap:9px;font-size:15px;font-weight:800;line-height:1.4;letter-spacing:-0.02em}
  .cta .txt svg{flex:0 0 auto;width:16px;height:16px;color:#6EE7B7}
  .cta .sub{display:block;margin-top:7px;font-size:11.5px;line-height:1.55;color:#C7D2DD;font-weight:600}
  .fine{margin:9px 1px 0;font-size:10.8px;line-height:1.6;color:var(--ink-3);font-weight:500}
  .cols{display:grid;gap:8px}
  .colbox{border:1px solid var(--line);border-radius:13px;padding:12px 13px;background:#fff}
  .colbox.yes{background:#F7FCF9;border-color:#DCF3E8}
  .colbox.no{background:#FDF8F7;border-color:#F7E2DE}
  .colbox .h{font-size:10px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;margin-bottom:6px}
  .colbox.yes .h{color:var(--mint-deep)}
  .colbox.no .h{color:#B42318}
  .colbox p{margin:0 0 5px;font-size:12.8px;line-height:1.6;color:#374151;font-weight:500}
  .colbox p:last-child{margin:0}
  .alts{display:grid;gap:8px}
  .alts a{display:flex;align-items:center;gap:10px;text-decoration:none;background:#fff;
    border:1px solid var(--line);border-radius:13px;padding:11px 12px}
  .alts .ic{flex:0 0 32px;width:32px;height:32px;border-radius:9px;background:#F3F4F6;display:grid;
    place-items:center;font-size:15px}
  .alts .nm{font-size:13.2px;font-weight:800;letter-spacing:-0.02em;display:block}
  .alts .ds{font-size:11px;color:var(--ink-3);font-weight:600;display:block;margin-top:1px}
  .alts .go{margin-left:auto;color:var(--mint-deep);font-weight:800;font-size:12px}
  details.faq{border-bottom:1px solid var(--line-2);padding:11px 1px}
  details.faq:last-of-type{border-bottom:none}
  details.faq summary{cursor:pointer;font-size:13.4px;font-weight:800;letter-spacing:-0.02em;
    list-style:none;display:flex;align-items:center;gap:8px}
  details.faq summary::-webkit-details-marker{display:none}
  details.faq summary:after{content:"+";margin-left:auto;color:var(--mint);font-weight:800;font-size:15px}
  details.faq[open] summary:after{content:"–"}
  details.faq p{margin:7px 0 2px;font-size:12.8px;line-height:1.68;color:#4B5563;font-weight:500}
  .back{display:flex;align-items:center;justify-content:center;gap:6px;margin-top:22px;
    text-decoration:none;background:#fff;border:1px solid var(--line);border-radius:14px;
    padding:14px;font-size:12.5px;font-weight:800;color:var(--ink)}
  .back .arw{color:var(--mint)}
  footer{margin-top:26px;padding-top:18px;border-top:1px solid var(--line)}
  .disclosure{font-size:11px;line-height:1.75;color:#6B7280;font-weight:500;background:#F3F4F6;
    border-radius:12px;padding:12px 14px;margin:0}
  .foot-links{display:flex;gap:12px;flex-wrap:wrap;margin-top:13px;font-size:11px;font-weight:700}
  .foot-links a{color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--line);padding-bottom:1px}
  .colophon{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-top:12px;
    font-size:10.5px;color:var(--ink-3);font-weight:500}
  /* ── list page ── */
  .listhead{background:var(--card);border:1px solid var(--line);border-radius:22px;box-shadow:var(--shadow);
    padding:20px 18px 18px;margin-top:10px}
  .llist{display:grid;gap:9px;margin-top:14px}
  .llist a{display:flex;gap:11px;align-items:flex-start;text-decoration:none;background:#fff;
    border:1px solid var(--line);border-radius:14px;padding:12px 13px}
  .llist .ic{flex:0 0 34px;width:34px;height:34px;border-radius:10px;background:#F3F4F6;display:grid;
    place-items:center;font-size:16px}
  .llist .nm{display:flex;align-items:center;gap:6px;flex-wrap:wrap;font-size:13.8px;font-weight:800;
    letter-spacing:-0.022em;line-height:1.35}
  .llist .bh{font-size:9.5px;font-weight:800;color:var(--mint-deep);background:var(--mint-soft);
    border:1px solid var(--mint-line);border-radius:5px;padding:1px 5px}
  .llist .ds{display:block;margin-top:3px;font-size:11.8px;line-height:1.5;color:var(--ink-2);font-weight:500}
  .llist .sc{margin-left:auto;flex:0 0 auto;font-size:10.5px;font-weight:800;color:var(--ink-3)}
  @media (min-width:560px){
    h1{font-size:28px}
    .article{padding:24px 22px 20px}
    .lede{font-size:15px}
    .cols{grid-template-columns:1fr 1fr}
    .alts{grid-template-columns:1fr 1fr}
  }
  @media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

# ────────────────────────── helpers ──────────────────────────
TAG_RE = re.compile(r"<[^>]+>")


def esc(s: str) -> str:
    return ((s or "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def plain(s: str) -> str:
    return html.unescape(TAG_RE.sub("", s or "")).strip()


def clip(text: str, n: int) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= n:
        return text
    cut = text[:n]
    i = cut.rfind(" ")
    return (cut[:i] if i > n * 0.6 else cut).rstrip(" ,.;:") + "…"


def tool_url(slug: str) -> str:
    return f"{TOOLS_URL}{slug}.html"


def by_slug(slug: str) -> dict:
    for t in TOOLS:
        if t["slug"] == slug:
            return t
    raise KeyError(slug)


def load_aff() -> dict:
    data = json.loads(AFF.read_text(encoding="utf-8"))
    return {t["id"]: t for t in data.get("tools", [])}


def read_minutes(t: dict) -> int:
    body = " ".join([t["lede"], t["evidence"], " ".join(plain(x) for x in t["tested"]),
                     " ".join(q + " " + a for q, a in t["faq"])])
    return max(2, math.ceil(len(body.split()) / 220))


# ────────────────────────── shared blocks ──────────────────────────
def head_meta(title: str, desc: str, canonical: str, og_type: str = "article") -> str:
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#F8F9FA">
<link rel="canonical" href="{esc(canonical)}">
<link rel="alternate" hreflang="en" href="{esc(canonical)}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(plain(title))}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='24' fill='%23FFFFFF'/><text x='50' y='73' font-size='58' text-anchor='middle'>⚡</text></svg>">"""


def ga_snippet() -> str:
    return f"""<!-- Google Analytics 4 (Work Cheatkey · {GA_ID}) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_ID}');
</script>"""


def nav() -> str:
    return f"""<div class="nav">
  <div class="nav-in">
    <a class="brand" href="../"><span class="bolt">⚡</span>{BRAND}</a>
    <a class="chip" href="./">All tool tests</a>
  </div>
</div>"""


def footer(today: str) -> str:
    return f"""  <footer>
    <p class="disclosure">
      <b>Affiliate disclosure.</b> Links to the tools on this page are affiliate links: if you subscribe through
      one, I may earn a commission at no extra cost to you — you pay the price the provider charges. I only write up
      tools I would put in my own workflow, and every free plan or trial described here is the same offer the
      provider gives anyone. Prices, plans and free limits change; check the provider's checkout before paying.
    </p>
    <div class="foot-links">
      <a href="./">All tool tests</a>
      <a href="../">Work Cheatkey</a>
      <a href="../../privacy.html">Privacy Policy</a>
      <a href="../../terms.html">Terms</a>
      <a href="../../">한국어 페이지</a>
    </div>
    <div class="colophon">
      <span>© 2026 {BRAND} · @workcheatkeyai</span>
      <span>Prices checked {today}</span>
    </div>
  </footer>"""


TRACKER = """<script>
(function () {
  "use strict";
  function track(event, params) {
    try { if (typeof gtag === "function") gtag("event", event, params || {}); } catch (e) {}
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a[data-aff]") : null;
    if (!a) return;
    track("affiliate_click", {
      tool_name: a.getAttribute("data-aff") || "",
      category: a.getAttribute("data-cat") || "",
      location: a.getAttribute("data-loc") || "en_tool_page",
      link_url: a.href
    });
  });
})();
</script>"""

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def cta_block(t: dict, url: str) -> str:
    return f"""    <a class="cta" href="{esc(url)}" target="_blank" rel="noopener sponsored"
       data-aff="{esc(t['name'])}" data-cat="{esc(t['cat'])}" data-loc="en_tool_page">
      <span class="lbl">Affiliate link · {esc(t['name'])}</span>
      <span class="txt">{esc(t['cta_label'])} {ARROW}</span>
      <span class="sub">{esc(t['cta_sub'])}</span>
    </a>
    <p class="fine">You pay the provider's price; I may earn a commission. Terms and free limits are theirs and can
    change — the numbers here are what their pricing page said on the date listed at the top.</p>"""


# ────────────────────────── tool page ──────────────────────────
def build_page(t: dict, aff: dict) -> str:
    a = aff.get(t["id"], {})
    url = a.get("url") or ""
    if not url:
        raise SystemExit(f"affiliates.json 에 '{t['id']}' 링크가 없습니다.")
    canonical = tool_url(t["slug"])
    title, desc = t["title"], t["desc"]

    verdict = "".join(
        f'<li><span class="kk">{esc(k)}</span><span class="vv">{v}</span></li>'
        for k, v in t["verdict"]
    )
    tested = "".join(f"<li>{x}</li>" for x in t["tested"])
    pricing_rows = "".join(
        f"<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>" for k, v in t["pricing"]
    )
    steps = "".join(
        f'<li><span class="num">{i + 1}</span><span class="body">'
        f'<span class="k">{esc(k)}</span><span class="v">{esc(v)}</span></span></li>'
        for i, (k, v) in enumerate(t["steps"])
    )
    best = "".join(f"<p>{esc(x)}</p>" for x in t["best_for"])
    skip = "".join(f"<p>{esc(x)}</p>" for x in t["skip_if"])
    faq_html = "".join(
        f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(ans)}</p></details>'
        for q, ans in t["faq"]
    )
    alts_html = "".join(
        f'<a href="{esc(by_slug(s)["slug"])}.html"><span class="ic">{by_slug(s)["icon"]}</span>'
        f'<span><span class="nm">{esc(by_slug(s)["name"])}</span>'
        f'<span class="ds">{esc(by_slug(s)["verdict"][0][0])}: {esc(clip(plain(by_slug(s)["verdict"][0][1]), 46))}</span></span>'
        f'<span class="go">→</span></a>'
        for s in t["alts"]
    )
    app_name = a.get("name", t["name"])
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Review",
                "@id": canonical + "#review",
                "name": plain(title),
                "headline": plain(t["h1"]),
                "description": plain(desc),
                "datePublished": PUBLISHED,
                "dateModified": TODAY,
                "inLanguage": "en",
                "url": canonical,
                "author": {"@type": "Organization", "name": BRAND, "url": EN},
                "publisher": {"@type": "Organization", "name": BRAND, "url": EN},
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": t["score"],
                    "bestRating": 5,
                    "worstRating": 1,
                    "description": plain(t["score_note"]),
                },
                "reviewBody": plain(t["lede"]),
                "positiveNotes": {"@type": "ItemList", "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "name": plain(x)}
                    for i, x in enumerate(t["best_for"])
                ]},
                "negativeNotes": {"@type": "ItemList", "itemListElement": [
                    {"@type": "ListItem", "position": lib_i + 1, "name": plain(x)}
                    for lib_i, x in enumerate(t["skip_if"])
                ]},
                "itemReviewed": {
                    "@type": "SoftwareApplication",
                    "name": app_name,
                    "applicationCategory": "BusinessApplication",
                    "operatingSystem": "Web",
                    "url": url,
                    "offers": {
                        "@type": "Offer",
                        "price": "0",
                        "priceCurrency": "USD",
                        "description": plain(t["verdict"][0][1]),
                    },
                },
            },
            {
                "@type": "SoftwareApplication",
                "@id": canonical + "#app",
                "name": app_name,
                "applicationCategory": "BusinessApplication",
                "operatingSystem": "Web",
                "url": url,
                "description": plain(desc),
            },
            {
                "@type": "FAQPage",
                "@id": canonical + "#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": plain(q),
                        "acceptedAnswer": {"@type": "Answer", "text": plain(ans)},
                    }
                    for q, ans in t["faq"]
                ],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": BRAND, "item": EN},
                    {"@type": "ListItem", "position": 2, "name": "Tool tests", "item": TOOLS_URL},
                    {"@type": "ListItem", "position": 3, "name": app_name},
                ],
            },
        ],
    }
    ld = json.dumps(jsonld, ensure_ascii=False, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_meta(title, desc, canonical)}
<style>{CSS}</style>
{ga_snippet()}
<script type="application/ld+json">
{ld}
</script>
</head>
<body>

{nav()}

<div class="shell">
  <a class="crumb" href="../"><span class="arw">←</span> Back to Work Cheatkey</a>

  <main>
    <article class="article">
      <span class="tag">{esc(t['cat'])} · checked {esc(t['checked'])}</span>
      <h1>{esc(t['h1'])}</h1>
      <p class="lede">{esc(t['lede'])}</p>
      <div class="meta">
        <span>Updated 25 Nov 2026</span>
        <span class="dot">·</span>
        <span>{read_minutes(t)} min read</span>
        <span class="dot">·</span>
        <span>Prices read {esc(t['checked'])}</span>
      </div>

      <div class="score">
        <span class="num">{t['score']}<small>/5</small></span>
        <span class="txt"><b>Work Cheatkey score</b>{esc(t['score_note'])}</span>
      </div>

      <ul class="verdict">{verdict}</ul>

      <h2><span class="k">01</span>What we checked</h2>
      <p class="evidence"><b>How this page was made.</b> {esc(t['evidence'])}</p>
      <ul class="plain">{tested}</ul>

      <h2><span class="k">02</span>Pricing, as it was on {esc(t['checked'])}</h2>
      <div class="tbl"><table>
        <thead><tr><th>Plan</th><th>What you get</th></tr></thead>
        <tbody>{pricing_rows}</tbody>
      </table></div>
      <p class="note">{esc(t['pricing_note'])}</p>

      <h2><span class="k">03</span>The 3-step workflow</h2>
      <ol class="steps">{steps}</ol>

{cta_block(t, url)}

      <h2><span class="k">04</span>Who it fits, and who it does not</h2>
      <div class="cols">
        <div class="colbox yes"><div class="h">Worth it if</div>{best}</div>
        <div class="colbox no"><div class="h">Skip it if</div>{skip}</div>
      </div>

      <h2><span class="k">05</span>Questions people ask</h2>
      {faq_html}

      <h2><span class="k">06</span>More field tests</h2>
      <div class="alts">{alts_html}</div>
    </article>

    <a class="back" href="../"><span class="arw">←</span> Back to Work Cheatkey</a>
  </main>

{footer(t['checked'])}
</div>

{TRACKER}
</body>
</html>
"""


# ────────────────────────── index page ──────────────────────────
def build_index() -> str:
    canonical = TOOLS_URL
    title = f"AI Tool Tests: Free Limits & Real Prices (2026) | {BRAND}"
    desc = ("Every AI tool I have priced and run for office work — Klap, LoopCV, Submagic, Make.com, Speak AI and more. "
            "The free limit, the first paid price and the one catch, read off each vendor's own pricing page.")
    rows = []
    for t in TOOLS:
        rows.append(f"""      <a href="{esc(t['slug'])}.html">
        <span class="ic" aria-hidden="true">{t['icon']}</span>
        <span><span class="nm">{esc(t['name'])}<span class="bh">{esc(t['cat'])}</span></span>
        <span class="ds">{esc(clip(plain(t['verdict'][0][1]), 78))}</span></span>
        <span class="sc">{t['score']}/5</span>
      </a>""")
    rows_html = "\n".join(rows)

    table_rows = "".join(
        f"<tr><td><a href=\"{esc(t['slug'])}.html\" style=\"text-decoration:none\">{esc(t['name'])}</a></td>"
        f"<td>{esc(plain(t['verdict'][0][1]))}</td>"
        f"<td>{esc(plain(t['verdict'][1][1]))}</td></tr>"
        for t in TOOLS
    )

    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": canonical + "#page",
                "name": plain(title),
                "description": plain(desc),
                "inLanguage": "en",
                "url": canonical,
                "isPartOf": {"@type": "WebSite", "name": BRAND, "url": EN},
            },
            {
                "@type": "ItemList",
                "name": "AI tools tested by Work Cheatkey",
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "url": tool_url(t["slug"]), "name": t["name"]}
                    for i, t in enumerate(TOOLS)
                ],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": BRAND, "item": EN},
                    {"@type": "ListItem", "position": 2, "name": "Tool tests"},
                ],
            },
        ],
    }
    ld = json.dumps(jsonld, ensure_ascii=False, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_meta(title, desc, canonical, "website")}
<style>{CSS}</style>
{ga_snippet()}
<script type="application/ld+json">
{ld}
</script>
</head>
<body>

{nav()}

<div class="shell">
  <a class="crumb" href="../"><span class="arw">←</span> Back to Work Cheatkey</a>

  <main>
    <header class="listhead">
      <span class="tag">Tool tests · {len(TOOLS)} tools</span>
      <h1>Every AI tool I have priced, and the one catch on each</h1>
      <p class="lede">No “top 50” list. These are the tools that appear in my own workflow, each page written from
      the vendor's pricing page on a dated check plus a real run where I had one. You get the free limit, the first
      paid price, and the thing the sales page does not say.</p>
    </header>

    <section class="llist" aria-label="Tool tests">
{rows_html}
    </section>

    <section>
      <h2><span class="k">→</span>Free limit and first price, side by side</h2>
      <div class="tbl"><table>
        <thead><tr><th>Tool</th><th>Free</th><th>First paid</th></tr></thead>
        <tbody>{table_rows}</tbody>
      </table></div>
      <p class="note">Checked on the dates inside each page (21–25 Nov 2026). Vendors change free tiers without
      notice — the page date tells you how fresh the number is.</p>
    </section>

    <a class="back" href="../"><span class="arw">←</span> Back to Work Cheatkey</a>
  </main>

{footer("25 Nov 2026")}
</div>

</body>
</html>
"""


# ────────────────────────── sitemap ──────────────────────────
def build_sitemap() -> str:
    def url(loc: str, pri: str, freq: str = "weekly") -> str:
        return (f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
                f"    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>\n  </url>")

    parts = [
        url(SITE + "/", "1.0", "daily"),
        url(EN, "0.9", "daily"),
        url(SITE + "/tips/", "0.8", "weekly"),
    ]
    try:
        tips = json.loads(DEALS.read_text(encoding="utf-8")).get("tips") or []
    except (OSError, ValueError):
        tips = []
    def tip_no(t):
        try:
            return int(str(t.get("no") or 0))
        except ValueError:
            return 0
    for t in sorted(tips, key=tip_no, reverse=True):
        parts.append(url(f"{SITE}/tips/{t['id']}.html", "0.7", "monthly"))
    parts.append(url(TOOLS_URL, "0.8", "weekly"))
    for t in sorted(TOOLS, key=lambda x: f"{x['slug']}.html"):
        parts.append(url(tool_url(t["slug"]), "0.7", "monthly"))
    parts.append(url(SITE + "/privacy.html", "0.3", "yearly"))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(parts) + "\n</urlset>\n")


# ────────────────────────── main ──────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-sitemap", action="store_true")
    args = ap.parse_args()

    aff = load_aff()
    TOOLS_DIR.mkdir(parents=True, exist_ok=True)

    written = []
    for t in TOOLS:
        p = TOOLS_DIR / f"{t['slug']}.html"
        p.write_text(build_page(dict(t, cta_sub=t["cta_sub"]), aff), encoding="utf-8")
        written.append(p)

    idx = TOOLS_DIR / "index.html"
    idx.write_text(build_index(), encoding="utf-8")
    written.append(idx)

    if not args.no_sitemap:
        SITEMAP.write_text(build_sitemap(), encoding="utf-8")

    for p in written:
        print(f"{p.relative_to(ROOT)}  ({p.stat().st_size:,} bytes)")
    if not args.no_sitemap:
        n = SITEMAP.read_text(encoding="utf-8").count("<url>")
        print(f"sitemap.xml  ({SITEMAP.stat().st_size:,} bytes, URL {n}개)")


if __name__ == "__main__":
    main()
