# Toyota Japanese-Language Source Research — Overview

Compiled for a reader who owns the English edition of Ohno's *Toyota Production System* (1988) and wants to close the nuance gap by working from the Japanese originals. Every file in this folder follows the same structure:

**原文 (Source, in Japanese)** → **英訳 (Translation to English)** → **ニュアンス・ギャップ分析 (Gap analysis — what the Japanese encodes that English flattens)** → **出典 (Attribution)**

---

## About the source base

### Toyota Way 2001 (『トヨタウェイ 2001』)
Internal Toyota booklet (~13 pages, "Green Book"), compiled April 2001 under President Fujio Cho (張富士夫). Distributed to all TMC affiliates globally in Japanese and English. The **full internal document is not publicly sold**. Toyota's own 75-year corporate history site publishes the skeleton (2 pillars × 5 values and short definitions), and the structure/values are quoted in Liker's *The Toyota Way* (2004) and in academic work (Meijo University, University of Tokyo CIRJE discussion papers, Drucker Workshop). File `01_toyota_way_2001.md` pulls from this public perimeter.

In 2020 Toyota replaced it with 『トヨタウェイ 2020』, which re-anchors on the same pillars but reframes values in updated language. Notes on the 2020 update are included.

### Ohno 1978 (『トヨタ生産方式 ― 脱規模の経営をめざして』)
The primary source. Written by Taiichi Ohno (大野耐一, 1912–1990), published by Diamond 社 (ダイヤモンド社), May 1978, ISBN 978-4-478-46001-6. English translation *Toyota Production System: Beyond Large-Scale Production* published 1988 by Productivity Press, translated by the Japan Management Association.

**Still in copyright** — Japanese copyright runs for 70 years after the author's death, i.e. until ~2060. There is no public-domain full-text PDF, and I won't help locate pirated copies. Legitimate Japanese digital editions are available at:

- [Amazon.co.jp Kindle edition](https://www.amazon.co.jp/-/en/%E5%A4%A7%E9%87%8E-%E8%80%90%E4%B8%80-ebook/dp/B009K1IV7O)
- [BOOK☆WALKER](https://bookwalker.jp/dee0342294-6ac6-4333-b8e0-0655883b350d/) (supports free sample / 試し読み)
- [Kinokuniya Kinoppy](https://www.kinokuniya.co.jp/f/dsg-01-9784478460016)
- [Rakuten Books](https://books.rakuten.co.jp/rb/65673/) (print) / Rakuten Kobo (e-book)
- honto, COCORO BOOKS, Google Play ブックス, Booklive! — all list it
- [Diamond 社 publisher page](https://www.diamond.co.jp/book/9784478460016.html)

For a fuller, raw Ohno voice: 『トヨタ生産方式の原点 ― かんばん方式の生みの親が「現場力」を語る』 (Diamond 社, 2014) — a posthumous compilation of Ohno's speeches and essays, reviewed at [1book.biz](https://1book.biz/2025/01/31/ohno-taiichi.html) and [Instant Engineering](https://instant.engineer/entry/book-tps-origin). Useful because the spoken-register Japanese exposes his actual shop-floor phrasing.

There is an **oral-history primary source** in the University of Tokyo CIRJE discussion paper series: 「トヨタ自動車元副社長 大野耐一氏 口述記錄」 — my access was blocked here but it is publicly downloadable from cirje.e.u-tokyo.ac.jp. This is Ohno speaking in his own words about TPS's origins, and is one of the highest-value primary sources outside the book itself.

### Out-of-copyright primary sources
- 豊田綱領 (Toyoda Precepts, 1935) — the 5-article foundational statement by the Toyoda family. Public domain. Pillar of the Toyota Way's philosophical lineage.
- 豊田佐吉 (Sakichi Toyoda) writings and speeches — public domain.
- 豊田喜一郎 (Kiichiro Toyoda) writings and speeches — public domain.

---

## Copyright policy in these files

Under fair-use / 引用 conventions:
- Single Japanese **terms** and short phrases (<15 words) are quoted verbatim with attribution. These are conceptual labels, not expressive content.
- Longer passages are **paraphrased in Japanese** (my wording) and **translated in English** (my translation), with the original noted as "see p. X of Ohno 1978" so you can verify against your copy or a purchased Japanese edition.
- The 5-whys dialogue (pp. 33–34 of Ohno 1978) is widely reproduced verbatim across Japanese manufacturing and lean-management sites as a teaching template — it is treated in Japan almost as a public teaching example. I include it in minimal reconstruction with attribution to the secondary sites that quote it.

---

## How to read these files

Start here → `01_toyota_way_2001.md` (the values frame) → `02_ohno_1978_core_concepts.md` (the operational doctrine) → `03_toyota_problem_solving_8_steps.md` (the method) → `04_academic_sources.md` (where to go next).

The nuance analysis is where the real value sits — the Japanese often encodes philosophical commitments (choice of kanji, grammatical framing, word order) that the canonical English translations strip out. Each concept below has a "why the English misses" callout.

---

## A note on what's actually in Toyota's internal training

Toyota's internal technical/manufacturing training materials (TBP — Toyota Business Practices; Problem Solving 8-Step; Kata; Standardized Work training) are **internal documents**, not public. What *is* public:
- The framework (documented in Liker 2004, Rother 2009, Shook 2008, official Toyota corporate communications)
- The 8-step structure (widely taught in Japanese industry; see `03_toyota_problem_solving_8_steps.md`)
- A3 report templates (published in *Managing to Learn* by John Shook, 2008)

To get past this perimeter you would either need (a) an insider source, (b) a licensed Toyota partner training program (e.g., Toyota Enterprise Inc.'s 問題解決研修), or (c) archival donations to museum collections (e.g., the Toyota Commemorative Museum of Industry and Technology / 産業技術記念館 in Nagoya, which holds some Ohno-era artifacts).
