# Media & Publishing GenAI: Product Evidence Log

**Scope:** Products deployed or incidents reported between January 2023 and December 2025 (within the last ~3 years)  
**Verified on:** 2026-11-23  
**Rule:** Every fact below carries a source number [S#] pointing to that product's source list. If no source we found describes a stage (e.g. pre-deployment testing), the field says 'Not publicly disclosed' instead of guessing. Dates are given to the day only when a source states the day; otherwise to the month.  
**Totals:** 21 products · 103 individually sourced facts · 61 source URLs  
**Link check (2026-11-23T19:27:18):** 57 × 200, 4 × 403. A 200 proves the page exists. The claims were checked against search-result summaries of these sources.

**Fact-level check:** 51 × 🟡 human-checked (keywords ≥50%), 48 × ✅ matched on cited page, 4 × ✅ matched on another source. `verify_facts.py` fetches each cited page and looks for the fact's numbers and quoted phrases. Facts with neither are scored by keyword overlap.

## Summary table

| ID | Date | Company | Product | Challenges | Outcome | Confidence |
|---|---|---|---|---|---|---|
| M01 | 2023-01-12 | CNET (Red Ventures) | Internal AI engine for finance explainers | Factual errors, Hidden AI / fake bylines | Corrections issued, Paused or suspended | high |
| M02 | 2023-02 | Men's Journal (Arena Group) | AI-generated health articles | Factual errors, Hidden AI / fake bylines | Corrections issued, Company disputes the account | high |
| M03 | 2023-03-30 | BuzzFeed | "Buzzy the Robot" AI-assisted travel guides | Factual errors, Editorial governance and labour | Continued with changes | high |
| M04 | 2023-07 | G/O Media (Gizmodo / io9) | "Gizmodo Bot" AI articles | Factual errors, Editorial governance and labour | Corrections issued, Continued with changes, Legal, union or regulatory action | high |
| M05 | 2023-08 | Microsoft (MSN / Microsoft Travel) | Algorithmic travel articles | Tone and context failures, Factual errors | Content removed or retracted, Company disputes the account | medium-high |
| M06 | 2023-08-19 | Gannett (USA TODAY network) | LedeAI high-school sports recaps | Factual errors, Third-party / syndicated content, Editorial governance and labour | Paused or suspended, Corrections issued | high |
| M07 | 2023-09-14 | Microsoft (MSN) | Aggregated / rewritten obituary | Tone and context failures, Third-party / syndicated content, Factual errors | Content removed or retracted, Company disputes the account | medium-high |
| M08 | 2023-10-30 | Microsoft (MSN) + The Guardian | AI-generated reader polls on news articles | Tone and context failures, Third-party / syndicated content | Tool or feature shut down, Content removed or retracted | high |
| M09 | 2023-11-27 | Sports Illustrated (Arena Group) | Product reviews under AI-generated author profiles | Fabricated people, books or events, Hidden AI / fake bylines, Third-party / syndicated content | Content removed or retracted, Company disputes the account | medium-high |
| M10 | 2024-04 | X (Grok) | AI-written trending news summaries (Explore) | Fabricated people, books or events, Bad source material, Factual errors | Company disputes the account | high |
| M11 | 2024-05 | Google | AI Overviews in Search (impact on publishers) | Bad source material, Factual errors, Traffic and revenue impact | Continued with changes, Legal, union or regulatory action | high |
| M12 | 2024-05-30 | Hoodline | AI-generated local news under AI persona bylines | Hidden AI / fake bylines, Fabricated people, books or events, Bad source material | Continued with changes | high |
| M13 | 2024-12 | Apple | Apple Intelligence notification summaries (news apps) | Factual errors, Fabricated people, books or events, Third-party / syndicated content | Paused or suspended, Continued with changes | high |
| M14 | 2025-01-15 | Bloomberg | AI-Powered News Summaries (Terminal) | Factual errors | Corrections issued, Continued with changes | high |
| M15 | 2025-01-27 | Quartz (G/O Media) | "Quartz Intelligence Newsroom" | Factual errors, Bad source material, Hidden AI / fake bylines | Continued with changes, Company disputes the account | medium-high |
| M16 | 2025-03 | Los Angeles Times | "Insights" AI viewpoint and bias notes on opinion pieces | Tone and context failures, Editorial governance and labour | Content removed or retracted, Tool or feature shut down | medium-high |
| M17 | 2025-05-18 | Chicago Sun-Times & Philadelphia Inquirer (via King Features / Hearst) | Syndicated "Heat Index" summer insert | Fabricated people, books or events, Third-party / syndicated content, Editorial governance and labour | Vendor or contributor relationship ended | high |
| M19 | 2025-06 | Ventures Media (Elle Belgium, Psychologies, Marie Claire…) | AI articles under invented journalist profiles | Fabricated people, books or events, Hidden AI / fake bylines | Continued with changes | high |
| M18 | 2025-06-02 | Wikimedia Foundation (Wikipedia) | "Simple Article Summaries" AI pilot | Editorial governance and labour, Factual errors | Paused or suspended | high |
| M21 | 2025-07-11 | Politico (Axel Springer) | "Report Builder" and live AI summaries (LETO) | Factual errors, Editorial governance and labour | Legal, union or regulatory action, Tool or feature shut down | high |
| M20 | 2025-08-21 | Wired & Business Insider (and others) | Freelance articles that were AI-generated fiction (inbound content) | Fabricated people, books or events, Third-party / syndicated content, Hidden AI / fake bylines | Content removed or retracted, Vendor or contributor relationship ended | high |

## Products in detail

### M01 · CNET (Red Ventures): Internal AI engine for finance explainers

*Digital publisher · 2023-01-12 · confidence **high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • CNET ran a trial of an "internally designed AI engine" to write finance explainers. [S1] · ✅ matched on cited page<br>• Readers were not clearly told: the AI authorship came to light through outside reporting, after which CNET acknowledged it. [S2] · 🟡 human-checked (keywords ≥50%) |
| 🚨 After deployment | • The Register showed CNET's compound-interest explainer got its own example wrong (a $10,000 deposit earning 3% interest). [S2] · ✅ matched on cited page<br>• Some corrections noted CNET "replaced phrases that were not entirely original". [S1] · ✅ matched on cited page |
| 🏁 Outcome | • 41 of the 77 AI-written articles were corrected. [S1] · ✅ matched on cited page<br>• CNET paused publishing articles produced by the AI model. Owner Red Ventures had also used it on Bankrate and CreditCards.com. [S4] · 🟡 human-checked (keywords ≥50%) |
| ⚠️ Discrepancies | Total article count is reported as 75, 77 or 78. 41/77 is the most-cited figure. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [Engadget: CNET corrected 41 of its 77 AI-written articles](https://www.engadget.com/cnet-corrected-41-of-its-77-ai-written-articles-201519489.html?src=rss) | secondary | 200 OK |
| S2 | [The Register, 19 Jan 2023](https://www.theregister.com/2023/01/19/cnet_reviewing_ai_authored_stories/) | secondary | 200 OK |
| S3 | [Gizmodo, Jan 2023](https://gizmodo.com/cnet-ai-chatgpt-news-robot-1849996151) | secondary | 200 OK |
| S4 | [DeepLearning.AI The Batch: CNET pauses AI articles](https://www.deeplearning.ai/the-batch/cnet-pauses-its-practice-of-writing-news-articles-with-ai/) | secondary | 200 OK |

### M02 · Men's Journal (Arena Group): AI-generated health articles

*Magazine · 2023-02 · confidence **high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • Arena Group had bought Men's Journal in December 2022. The AI article ran under a generic "Men's Fitness Editors" byline. [S1] · ✅ matched on cited page<br>• Pre-launch medical review: not publicly disclosed. *(no source: not publicly disclosed)* |
| 🚨 After deployment | • The article "What All Men Should Know About Low Testosterone" was reviewed by Bradley Anawalt (UW Medical Center), who found 18 specific errors. [S1] · ✅ matched on cited page |
| 🏁 Outcome | • The article was substantially rewritten after Futurism contacted Arena. Arena said "these early experiments are a work in progress". [S2] · ✅ matched on cited page |
| ⚠️ Discrepancies | Men's Journal acknowledged some, but not all, of the 18 errors. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [Futurism: Men's Journal errors in AI health article](https://futurism.com/neoscope/magazine-mens-journal-errors-ai-health-article) | secondary | 200 OK |
| S2 | [The Daily Beast: Men's Journal corrects errors](https://www.thedailybeast.com/mens-journal-corrects-errors-in-ai-generated-health-story/) | secondary | 200 OK |
| S3 | [Nieman Lab reading note](https://www.niemanlab.org/reading/mens-journal-publishes-serious-errors-in-first-ai-generated-health-article/) | secondary | 200 OK |

### M03 · BuzzFeed: "Buzzy the Robot" AI-assisted travel guides

*Digital publisher · 2023-03-30 · confidence **high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • BuzzFeed described the guides as an "experiment" with its AI writing tools, using staff answers to an internal questionnaire on underrated travel picks. [S1] · ✅ matched on cited page |
| 🚨 After deployment | • Futurism found 40+ travel guides written with ChatGPT or a similar chatbot. [S1] · ✅ matched on cited page<br>• Almost every guide used the phrase "hidden gem". "Gem" appeared about 25 times across a handful of stories. [S1] · ✅ matched on cited page<br>• Nieman Lab described the guides as comically bland and similar to one another. [S2] · 🟡 human-checked (keywords ≥50%) |
| 🏁 Outcome | • BuzzFeed defended them as an experiment. Whether the experiment continued after 2023 is not documented in the sources found. [S1] · 🟡 human-checked (keywords ≥50%) |
| ⚠️ Discrepancies | How much human editing each guide got is not established by the sources. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [Futurism: BuzzFeed publishing articles by AI](https://futurism.com/buzzfeed-publishing-articles-by-ai) | secondary | 200 OK |
| S2 | [Nieman Lab, Mar 2023](https://www.niemanlab.org/2023/03/are-buzzfeeds-ai-generated-travel-articles-bad-in-a-scary-new-way-or-a-familiar-old-way/) | secondary | 200 OK |
| S3 | [SiliconANGLE, 30 Mar 2023](https://siliconangle.com/2023/03/30/buzzfeeds-new-ai-generated-travel-articles-dystopian-bad-dream/) | secondary | 200 OK |

### M04 · G/O Media (Gizmodo / io9): "Gizmodo Bot" AI articles

*Digital publisher · 2023-07 · confidence **high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • G/O Media called it a "modest test" of AI content. [S1] · ✅ matched on cited page<br>• The io9 deputy editor said no one at io9 took part in editing or publishing it, so newsroom review was bypassed. [S2] · 🟡 human-checked (keywords ≥50%) |
| 🚨 After deployment | • "A Chronological List of Star Wars Movies & TV Shows" was not in chronological order (e.g. The Clone Wars listed after The Rise of Skywalker). [S1] · ✅ matched on cited page<br>• The deputy editor flagged 18 concerns, corrections and comments. [S2] · ✅ matched on cited page<br>• The error-filled article still ranked on Google's first page for "Star Wars movies". [S3] · ✅ matched on cited page |
| 🏁 Outcome | • The GMG Union called the move unethical and unacceptable. [S2] · 🟡 human-checked (keywords ≥50%)<br>• Management planned to keep publishing AI content (including on Jalopnik and The A.V. Club), per internal memos reported by Vox. [S1] · 🟡 human-checked (keywords ≥50%) |
| ⚠️ Discrepancies | Which AI tool was used is unconfirmed (single indirect source), so it is not stated here. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [Futurism: io9 staff horrified](https://futurism.com/the-byte/io9-horrified-ai-generated-article) | secondary | 200 OK |
| S2 | [TheWrap: Gizmodo editor slams AI article](https://www.thewrap.com/ai-gizmodo-io9-star-wars-article-retraction) | secondary | 200 OK |
| S3 | [Futurism: AI Star Wars article ranking on Google](https://futurism.com/gizmodo-ai-star-wars-article-google) | secondary | 200 OK |

### M05 · Microsoft (MSN / Microsoft Travel): Algorithmic travel articles

*Aggregator / portal · 2023-08 · confidence **medium-high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • Byline was "Microsoft Travel". Editorial review process: not publicly disclosed. [S1] · ✅ matched on cited page |
| 🚨 After deployment | • "Headed to Ottawa? Here's what you shouldn't miss!" listed the Ottawa Food Bank as the No. 3 attraction and told visitors to go "on an empty stomach". [S1] · ✅ matched on cited page<br>• The food bank said encouraging people to 'visit us on an empty stomach' was "incredibly insensitive and insulting". [S1] · ✅ matched on cited page |
| 🏁 Outcome | • Microsoft removed the article. A spokesperson said the content "was generated through a combination of algorithmic techniques" and that Microsoft pairs technology with content editors. [S1] · 🟡 human-checked (keywords ≥50%) |
| ⚠️ Discrepancies | Some outlets called it AI-written. Microsoft described it as algorithmic techniques plus editors, so the exact cause is disputed. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [CTV News Ottawa](https://ottawa.ctvnews.ca/microsoft-removes-article-recommending-15-things-to-do-in-ottawa-including-visit-the-ottawa-food-bank-1.6524918) | secondary | 200 OK |
| S2 | [Daily Hive](https://dailyhive.com/canada/microsoft-ai-article-food-bank-ottawa) | secondary | 200 OK |

### M06 · Gannett (USA TODAY network): LedeAI high-school sports recaps

*Newspaper group · 2023-08-19 · confidence **high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • Gannett used a third-party vendor, LedeAI, to generate recaps across local papers. [S1] · 🟡 human-checked (keywords ≥50%)<br>• Whether newsrooms reviewed recaps before publication: Gannett did not answer the question. [S1] · 🟡 human-checked (keywords ≥50%) |
| 🚨 After deployment | • The Columbus Dispatch ran a recap describing a game as "a close encounter of the athletic kind". [S1] · ✅ matched on another source<br>• Similar stories ran in the Louisville Courier Journal, AZ Central, Florida Today and the Milwaukee Journal Sentinel. [S1] · 🟡 human-checked (keywords ≥50%)<br>• LedeAI's CEO regretted errors, unwanted repetition and awkward phrasing in articles from August 19. [S1] · ✅ matched on cited page |
| 🏁 Outcome | • Gannett paused LedeAI in all local markets using it and said it would keep evaluating vendors. [S1] · 🟡 human-checked (keywords ≥50%)<br>• USA TODAY network updated its AI-generated sports articles to correct errors. [S2] · 🟡 human-checked (keywords ≥50%) |
| ⚠️ Discrepancies | None material. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [KSL / AP: Gannett to pause AI experiment](https://www.ksl.com/article/50720151/gannett-to-pause-ai-experiment-after-botched-high-school-sports-articles) | secondary | 200 OK |
| S2 | [Yahoo: USA Today updates every AI-generated sports article](https://news.yahoo.com/usa-today-updates-every-ai-134945528.html) | secondary | 200 OK |
| S3 | [Axios Columbus, 28 Aug 2023](https://www.axios.com/local/columbus/2023/08/28/dispatch-gannett-ai-newsroom-tool) | secondary | 403: site blocks automated checks; found via web search |

### M07 · Microsoft (MSN): Aggregated / rewritten obituary

*Aggregator / portal · 2023-09-14 · confidence **medium-high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • MSN syndicated content from partner sites. How this piece was produced: MSN declined to answer. [S2] · 🟡 human-checked (keywords ≥50%) |
| 🚨 After deployment | • An obituary of former NBA player Brandon Hunter ran under the headline "Brandon Hunter useless at 42". [S1] · ✅ matched on cited page<br>• The text was garbled (e.g. "handed away on the age of 42"), and it appeared to reword a TMZ Sports story. [S1] · ✅ matched on cited page |
| 🏁 Outcome | • The obituary was taken down. Microsoft did not confirm it was AI-generated. [S3] · 🟡 human-checked (keywords ≥50%) |
| ⚠️ Discrepancies | The piece came from a small partner site (reported as Race Track or TalkBasket.net). Microsoft never confirmed AI involvement. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [Futurism, 14 Sep 2023](https://futurism.com/msn-ai-brandon-hunter-useless) | secondary | 200 OK |
| S2 | [Scientific American](https://www.scientificamerican.com/article/dont-blame-ai-plagiarism-is-turning-digital-news-into-hot-garbage/) | secondary | 200 OK |
| S3 | [Search Engine Land](https://searchengineland.com/microsoft-brandon-hunter-useless-ai-obituary-432008) | secondary | 200 OK |

### M08 · Microsoft (MSN) + The Guardian: AI-generated reader polls on news articles

*Aggregator / portal · 2023-10-30 · confidence **high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • MSN automatically added AI-generated polls to licensed publisher articles. The publisher (The Guardian) had no role in the poll. [S1] · 🟡 human-checked (keywords ≥50%) |
| 🚨 After deployment | • Next to a Guardian story on the death of Lilie James, 21, MSN ran a poll asking whether it was murder, accident or suicide. [S1] · ✅ matched on cited page<br>• Readers blamed the Guardian and its reporter. [S2] · 🟡 human-checked (keywords ≥50%) |
| 🏁 Outcome | • Guardian Media Group CEO Anna Bateson wrote to Microsoft president Brad Smith citing "significant reputational damage". [S1] · ✅ matched on another source<br>• A Microsoft spokesperson said it had "deactivated its poll feature" and was "investigating the cause of the inappropriate content". [S2] · ✅ matched on cited page |
| ⚠️ Discrepancies | Axios dates the poll's removal to Monday 30 Oct; one caption says 31 Oct. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [Axios, 31 Oct 2023](https://www.axios.com/2023/10/31/guardian-microsoft-generative-ai-poll-death) | secondary | 200 OK |
| S2 | [Futurism: Microsoft AI poll](https://futurism.com/microsoft-ai-poll-guardian) | secondary | 200 OK |

### M09 · Sports Illustrated (Arena Group): Product reviews under AI-generated author profiles

*Magazine · 2023-11-27 · confidence **medium-high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • Content came from a third-party supplier, according to Arena Group. [S2] · 🟡 human-checked (keywords ≥50%) |
| 🚨 After deployment | • Futurism found bylines such as "Drew Ortiz" and "Sora Tanaka" with AI-generated headshots and invented bios. [S1] · ✅ matched on cited page<br>• The profiles vanished from the site after Futurism asked about them. [S1] · 🟡 human-checked (keywords ≥50%) |
| 🏁 Outcome | • Arena Group denied publishing AI-generated content and blamed the third-party vendor. [S2] · 🟡 human-checked (keywords ≥50%)<br>• The Sports Illustrated Union said it was "horrified" and demanded transparency. [S1] · ✅ matched on cited page |
| ⚠️ Discrepancies | Futurism relied partly on anonymous sources, and Arena disputes that the content was AI-generated. The fake profiles themselves were documented. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [Futurism, 27 Nov 2023](https://futurism.com/sports-illustrated-ai-generated-writers) | secondary | 200 OK |
| S2 | [KTVU: Arena Group denies, blames third party](https://www.ktvu.com/sports/sports-illustrated-parent-company-denies-publishing-ai-generated-articles-blames-third-party) | secondary | 200 OK |

### M10 · X (Grok): AI-written trending news summaries (Explore)

*Social platform · 2024-04 · confidence **high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • X shipped it with fine print: "Grok is an early feature and can make mistakes." [S1] · ✅ matched on cited page |
| 🚨 After deployment | • Fans joked Klay Thompson was "throwing bricks" after a 0-for-10 game. Grok turned this into a story about him vandalising homes in Sacramento with bricks. [S1] · ✅ matched on cited page<br>• It invented details (broken windows, a police investigation) and placed the story at No. 5 on trending. [S2] · 🟡 human-checked (keywords ≥50%) |
| 🏁 Outcome | • No correction or statement found in the sources. The disclaimer was X's only stated safeguard. [S1] · 🟡 human-checked (keywords ≥50%) |
| ⚠️ Discrepancies | How long it stayed trending differs ("briefly at #5" vs "for days"). |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [Engadget](https://www.engadget.com/xs-ai-bot-is-so-dumb-it-cant-tell-the-difference-between-a-bad-game-and-vandalism-172707401.html?src=rss) | secondary | 200 OK |
| S2 | [Futurism](https://futurism.com/the-byte/elon-musk-ai-accuses-nba-player-criminal-vandalism) | secondary | 200 OK |

### M11 · Google: AI Overviews in Search (impact on publishers)

*Search / aggregator · 2024-05 · confidence **high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • Pre-launch testing details: not publicly disclosed. *(no source: not publicly disclosed)* |
| 🚨 After deployment | • AI Overviews suggested glue on pizza (from an old Reddit joke) and eating rocks (from The Onion). [S2] · 🟡 human-checked (keywords ≥50%)<br>• Google said it struggled with nonsensical queries and satirical content, and that many viral screenshots were fake. [S1] · 🟡 human-checked (keywords ≥50%) |
| 🏁 Outcome | • Google restricted AI Overviews for nonsensical and satirical queries, and kept the feature. [S1] · 🟡 human-checked (keywords ≥50%)<br>• Sept 2025: Penske Media (Rolling Stone, Billboard, Variety) sued Google, citing "significant declines in clicks" and affiliate revenue down more than a third from its peak. Google called the claims "meritless". [S3] · ✅ matched on cited page |
| ⚠️ Discrepancies | Penske's traffic and revenue figures are allegations in a lawsuit, not court findings. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [Google: AI Overviews, about last week](https://blog.google/products/search/ai-overViews-update-may-2024) | primary | 200 OK |
| S2 | [The Register, 31 May 2024](https://www.theregister.com/2024/05/31/google_ai_search_update/) | secondary | 200 OK |
| S3 | [TechCrunch: Penske Media sues Google](https://techcrunch.com/2025/09/14/rolling-stone-owner-penske-media-sues-google-over-ai-summaries) | secondary | 200 OK |

### M12 · Hoodline: AI-generated local news under AI persona bylines

*Local news network · 2024-05-30 · confidence **high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • Hoodline began filling its sites with AI-generated articles the year before. In April 2024 it announced an "AI" label next to writer names. [S2] · 🟡 human-checked (keywords ≥50%) |
| 🚨 After deployment | • Articles ran under invented bylines (e.g. "Nina Singh-Hudson") with AI-generated headshots and bios. [S3] · ✅ matched on another source<br>• Nieman Lab found stories leaned heavily on police press releases, and the AI personas had no real beats. [S1] · 🟡 human-checked (keywords ≥50%) |
| 🏁 Outcome | • The CEO said the personas, beats and cities were assigned at random, and planned to turn them into AI news anchors for short videos. [S1] · 🟡 human-checked (keywords ≥50%) |
| ⚠️ Discrepancies | Critics say the AI label is easy to miss. Hoodline's side comes only from its CEO's interviews. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [Nieman Lab, Jun 2024](https://www.niemanlab.org/2024/06/whats-in-a-byline-for-hoodlines-ai-generated-local-news-everything-and-nothing/) | secondary | 200 OK |
| S2 | [CNN via ABC17: fake bylines](https://abc17news.com/money/cnn-business-consumer/2024/05/30/a-national-network-of-local-news-sites-is-publishing-ai-written-articles-under-fake-bylines-experts-are-raising-alarm/) | secondary | 200 OK |
| S3 | [Techdirt](https://www.techdirt.com/?p=442349) | secondary | 403: site blocks automated checks; found via web search |

### M13 · Apple: Apple Intelligence notification summaries (news apps)

*Platform / device · 2024-12 · confidence **high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • Shipped as part of Apple Intelligence. Beta labelling and italic styling were only added after the complaints. [S1] · 🟡 human-checked (keywords ≥50%) |
| 🚨 After deployment | • A summary of a BBC alert falsely said Luigi Mangione had shot himself. BBC News filed a formal complaint in December 2024. [S2] · 🟡 human-checked (keywords ≥50%) |
| 🏁 Outcome | • iOS 18.3 temporarily disabled summaries for news and entertainment apps (Jan 2025). [S1] · ✅ matched on cited page<br>• Apple added italics for summaries, a beta warning, and a per-app off switch. The BBC welcomed the pause. [S2] · 🟡 human-checked (keywords ≥50%) |
| ⚠️ Discrepancies | Whether news summaries later returned is not covered in the sources found. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [MacRumors: iOS 18.3 removes news summaries](https://www.macrumors.com/2025/01/16/ios-18-3-news-notifications-removed/) | secondary | 200 OK |
| S2 | [TechCrunch, 16 Jan 2025](https://techcrunch.com/2025/01/16/apple-pauses-ai-notification-summaries-for-news-after-generating-false-alerts) | secondary | 200 OK |

### M14 · Bloomberg: AI-Powered News Summaries (Terminal)

*Financial news / wire · 2025-01-15 · confidence **high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • Launched in January 2025: three bullet-point AI summaries at the top of Bloomberg News stories on the Terminal. [S2] · 🟡 human-checked (keywords ≥50%) |
| 🚨 After deployment | • By late March 2025, Bloomberg had corrected at least three dozen AI summaries (per The New York Times). [S1] · 🟡 human-checked (keywords ≥50%)<br>• Errors included when Trump's broader auto tariffs would apply, and the year Canadian tariffs were imposed. [S1] · 🟡 human-checked (keywords ≥50%) |
| 🏁 Outcome | • Bloomberg said 99% of AI summaries meet its editorial standards. [S1] · ✅ matched on cited page<br>• Bloomberg kept the feature running. [S2] · 🟡 human-checked (keywords ≥50%) |
| ⚠️ Discrepancies | Some aggregators say 30 corrections, others 36. "At least three dozen" is the more common figure. A November 2025 expansion appeared in search results, but its source page (bloomberg.com/company) blocks automated access, so it is left out. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [Washington Times, 29 Mar 2025 (reporting NYT)](https://m.washingtontimes.com/news/2025/mar/29/bloombergs-use-ai-summaries-articles-leads-numerous-corrections/) | secondary | 200 OK |
| S2 | [Talking Biz News](https://talkingbiznews.com/media-news/bloomberg-has-a-rocky-start-with-ai-summaries/) | secondary | 200 OK |

### M15 · Quartz (G/O Media): "Quartz Intelligence Newsroom"

*Digital publisher · 2025-01-27 · confidence **medium-high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • G/O Media called it "purely experimental" and said editorial staff review each story before publication. [S1] · ✅ matched on cited page |
| 🚨 After deployment | • It repeatedly cited "Devdiscourse", itself apparently an automated news site. [S2] · ✅ matched on cited page<br>• It gave a wrong headline on the Boeing Starliner astronauts ("took their first spacewalk"). [S3] · ✅ matched on cited page<br>• TechCrunch flagged a self-contradicting headline: "Jobless claims rise slightly as continuing claims set a record". [S1] · 🟡 human-checked (keywords ≥50%) |
| 🏁 Outcome | • Futurism later reported that Quartz fired its writers after the move to AI content. [S4] · 🟡 human-checked (keywords ≥50%) |
| ⚠️ Discrepancies | Earliest coverage says the articles weren't disclosed as AI; G/O says staff review them. The date of the firing report was not captured. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [TechCrunch, 27 Jan 2025](https://techcrunch.com/2025/01/27/quartz-has-been-quietly-publishing-ai-generated-news-articles) | secondary | 200 OK |
| S2 | [Futurism: Quartz AI articles errors](https://futurism.com/quartz-ai-generated-articles-slop-errors) | secondary | 200 OK |
| S3 | [Futurism: Quartz AI article on Boeing astronauts](https://futurism.com/quartz-ai-generated-article-boeing-astronauts) | secondary | 200 OK |
| S4 | [Futurism: Quartz fires writers](https://futurism.com/quartz-fires-writers-ai-slop) | secondary | 200 OK |

### M16 · Los Angeles Times: "Insights" AI viewpoint and bias notes on opinion pieces

*Newspaper · 2025-03 · confidence **medium-high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • Pre-launch evaluation: not publicly disclosed in the sources found. *(no source: not publicly disclosed)* |
| 🚨 After deployment | • On a column about Anaheim's 1920s KKK council members, Insights generated a note that framed the Klan as something other than an explicitly hate-driven movement. The New York Times' Ryan Mac flagged it. [S1] · ✅ matched on cited page |
| 🏁 Outcome | • The note was removed from that article about a day after launch, and the tool was later taken offline. [S1] · 🟡 human-checked (keywords ≥50%)<br>• A later report said the paper had "moved on" from the AI bias meter. [S2] · ✅ matched on cited page |
| ⚠️ Discrepancies | The column's author argued the AI was clumsy but did not defend the KKK. No official LA Times statement was found. Launch day not stated in the sources (early March 2025; the column ran 25 Feb). |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [TheWrap: LA Times pulls AI tool](https://thewrap.com/la-times-pulls-ai-tool-for-kkk-gaffe) | secondary | 200 OK |
| S2 | [Yahoo: LA Times has moved on from AI bias meter](https://www.yahoo.com/news/la-times-moved-ai-driven-004548906.html) | secondary | 200 OK |
| S3 | [Column author Gustavo Arellano's response](https://www.yahoo.com/news/commentary-did-ai-really-defend-110031273.html) | secondary | 200 OK |

### M17 · Chicago Sun-Times & Philadelphia Inquirer (via King Features / Hearst): Syndicated "Heat Index" summer insert

*Newspaper · 2025-05-18 · confidence **high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • The insert was licensed content from King Features. The Inquirer said its newsroom was not involved in producing it. [S1] · 🟡 human-checked (keywords ≥50%) |
| 🚨 After deployment | • 10 of the 15 books in the summer reading list do not exist, e.g. "The Last Algorithm", attributed to Andy Weir. [S2] · ✅ matched on cited page<br>• The freelance writer said he used AI to compile the list. [S1] · 🟡 human-checked (keywords ≥50%) |
| 🏁 Outcome | • King Features denounced the AI use and cut ties with the freelancer. [S1] · 🟡 human-checked (keywords ≥50%)<br>• Chicago Public Media acknowledged the list was created with an AI tool. [S1] · 🟡 human-checked (keywords ≥50%) |
| ⚠️ Discrepancies | None material (10 of 15 ≈ "two-thirds"). |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [NPR, 20 May 2025](https://www.npr.org/2025/05/20/nx-s1-5405022/fake-book-list-ai-chicago-sun-times) | secondary | 200 OK |
| S2 | [CBS Chicago](https://www.cbsnews.com/amp/chicago/news/summer-reading-ai-generated-titles-chicago-sun-times) | secondary | 200 OK |
| S3 | [NBC News](https://www.nbcnews.com/tech/tech-news/chicago-sun-admits-summer-book-guide-included-fake-ai-generated-titles-rcna208325) | secondary | 200 OK |

### M19 · Ventures Media (Elle Belgium, Psychologies, Marie Claire…): AI articles under invented journalist profiles

*Magazine · 2025-06 · confidence **high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • Ventures Media first claimed the articles were "proofread and edited by the editorial team". That statement was later removed. [S1] · ✅ matched on cited page<br>• The publisher told VRT it was a test by the tech team: articles fully generated by AI, not reviewed by editors, published under aliases and kept separate from the newsroom. [S3] · 🟡 human-checked (keywords ≥50%) |
| 🚨 After deployment | • More than half of the articles on Elle's Flemish website in the previous three months were partly or fully AI-generated, under the names Marta Peeters and Sophie Vermeulen. [S1] · 🟡 human-checked (keywords ≥50%)<br>• Sophie Vermeulen's profile photo came from This Person Does Not Exist, a site that generates fake faces with AI. [S1] · 🟡 human-checked (keywords ≥50%)<br>• In June, 44 of 46 online articles on Psychologies were credited to a fake author. [S1] · ✅ matched on cited page<br>• That persona, "Femke", presented herself as a psychologist. The chair of the Psychologists' Commission called it misleading. [S2] · ✅ matched on cited page |
| 🏁 Outcome | • The articles now carry the notice "This content was generated with the help of AI". [S1] · ✅ matched on cited page |
| ⚠️ Discrepancies | The '403 articles' count and a planned complaint appeared in search summaries but could not be found on the live pages, so they are left out. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [Brussels Times](https://www.brusselstimes.com/belgium/1650005/felmish-broadcasters-discovers-massive-ai-use-in-popular-magazines/) | secondary | 200 OK |
| S2 | [EBU Spotlight fact-check dispatch (VRT Elle investigation)](https://spotlight.ebu.ch/p/fact-check-dispatch-racist-tropes) | secondary | 200 OK |
| S3 | [NOS (Dutch)](https://nos.nl/l/2572829) | secondary | 200 OK |

### M18 · Wikimedia Foundation (Wikipedia): "Simple Article Summaries" AI pilot

*Encyclopedia · 2025-06-02 · confidence **high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • A planned 2-week mobile pilot for about 10% of opted-in readers. Neowin reported it used Cohere's open-weight Aya model. [S1] · ✅ matched on another source |
| 🚨 After deployment | • Editors objected that it would give an unaccountable voice top billing with no editorial control, and would do "immediate and irreversible harm" to readers and to trust. [S2] · ✅ matched on cited page |
| 🏁 Outcome | • The Foundation paused the trial on day two. It said it was still interested in AI summaries for uses such as accessibility. [S1] · 🟡 human-checked (keywords ≥50%) |
| ⚠️ Discrepancies | The model attribution (Aya) comes from a single outlet. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [TechCrunch, 11 Jun 2025](https://techcrunch.com/2025/06/11/wikipedia-pauses-ai-generated-summaries-pilot-after-editors-protest) | secondary | 200 OK |
| S2 | [404 Media](https://www.404media.co/wikipedia-pauses-ai-generated-summaries-after-editor-backlash/) | secondary | 200 OK |
| S3 | [PC Gamer](https://www.pcgamer.com/software/ai/wikipedia-pauses-ai-summary-experiment-after-editors-say-it-would-do-immediate-and-irreversible-harm-to-our-readers-and-to-our-reputation-as-a-decently-trustworthy-and-serious-source) | secondary | 200 OK |

### M21 · Politico (Axel Springer): "Report Builder" and live AI summaries (LETO)

*News publisher · 2025-07-11 · confidence **high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • The union contract required 60 days' notice and good-faith bargaining before AI tools with material job impact. The Guild argued Politico skipped this. [S2] · ✅ matched on cited page<br>• Management argued Report Builder sat "outside the newsroom" because product and engineering built it. [S2] · ✅ matched on cited page |
| 🚨 After deployment | • The arbitrator found Report Builder produced "erroneous and even absurd" outputs and was never coded to follow Politico's stylebook. [S2] · ✅ matched on cited page |
| 🏁 Outcome | • The arbitrator ruled for the PEN Guild (late 2025). [S2] · 🟡 human-checked (keywords ≥50%)<br>• Politico later agreed to shut down both AI tools. [S1] · 🟡 human-checked (keywords ≥50%) |
| ⚠️ Discrepancies | The union is reported as 225+ or about 250 members. The primary source is the union itself. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [NewsGuild: Politico agrees to shut down both AI tools](https://newsguild.org/victory-politico-agrees-to-shut-down-both-ai-tools-at-center-of-landmark-arbitration) | primary | 200 OK |
| S2 | [Nieman Lab, Dec 2025: arbitrator finds safeguards violated](https://www.niemanlab.org/2025/12/politico-management-violated-key-ai-adoption-safeguards-arbitrator-finds/) | secondary | 200 OK |
| S3 | [Press Gazette: News not slop](https://pressgazette.co.uk/news/news-not-slop-politico-ai/) | secondary | 200 OK |

### M20 · Wired & Business Insider (and others): Freelance articles that were AI-generated fiction (inbound content)

*Magazine / digital publisher · 2025-08-21 · confidence **high***

| Stage | Evidence |
|---|---|
| 🧰 Before deployment | • Not a product they built. The AI content arrived through freelance submissions under the byline "Margaux Blanchard". [S1] · ✅ matched on cited page |
| 🚨 After deployment | • At least six publications ran the byline. Wired caught it when the writer couldn't supply payment details. [S1] · 🟡 human-checked (keywords ≥50%) |
| 🏁 Outcome | • Wired and Business Insider removed the features. [S1] · 🟡 human-checked (keywords ≥50%)<br>• Publications took down or amended the affected articles, and many journalists added extra steps to verify experts before quoting them. [S1] · 🟡 human-checked (keywords ≥50%)<br>• Business Insider later removed 38 essays under other bylines and deleted 19 author pages (per The Washington Post). [S2] · ✅ matched on cited page |
| ⚠️ Discrepancies | The 38/19 figures are second-hand from Washington Post reporting. |

| # | Source | Type | Link check |
|---|---|---|---|
| S1 | [Press Gazette](https://pressgazette.co.uk/publishers/digital-journalism/wired-and-business-insider-remove-ai-written-freelance-articles/) | secondary | 200 OK |
| S2 | [The Daily Beast: Business Insider deletes dozens of articles](https://www.thedailybeast.com/business-insider-deletes-dozens-of-articles-after-ai-scam-probe) | secondary | 200 OK |

## Industry study

### S1 · BBC and EBU: News integrity in AI assistants (2025-10-21)

• Across 18 countries and 14 languages, 45% of AI answers had at least one significant issue. [S3] · ✅ matched on cited page<br>• 31% of responses showed serious sourcing problems: missing, misleading or incorrect attribution. [S3] · ✅ matched on cited page<br>• Gemini had significant issues in 76% of responses (EBU release; the page blocks automated checks). [S1] · ✅ matched on cited page

*Why it matters:* It shows publishers' content gets distorted even when the publisher is not the one using AI. (A BBC-only comparison of 51% vs 37% appeared in search summaries but could not be matched on the fetched pages, so it is left out.)

- S1: [EBU press release](https://www.ebu.ch/news/2025/10/ai-s-systemic-distortion-of-news-is-consistent-across-languages-and-territories-international-study-by-public-service-broadcaste) (primary, 403: site blocks automated checks; found via web search)
- S2: [EBU report: News integrity in AI assistants](https://www.ebu.ch/research/open/report/news-integrity-in-ai-assistants) (primary, 403: site blocks automated checks; found via web search)
- S3: [NPR, 21 Oct 2025](https://www.npr.org/sections/npr-extra/2025/10/21/g-s1-94424/global-study-on-news-integrity-in-ai-assistants-shows-need-for-safeguards-and-improved-accuracy) (secondary, 200 OK)

## Research log

Run on 2026-11-23. Live web search (standard mode); results summarised by the search tool; claims cross-checked across at least two outlets where available.

| Query | Product | Result |
|---|---|---|
| CNET AI-generated articles errors corrections January 2023 | M01 | confirmed |
| Men's Journal AI-generated testosterone article 18 errors Futurism February 2023 Arena Group | M02 | confirmed |
| BuzzFeed AI-generated travel guides "hidden gem" repetitive Futurism 2023 Buzzy | M03 | confirmed |
| Gizmodo AI-generated Star Wars article errors G/O Media July 2023 io9 | M04 | confirmed; AI tool attribution left out (single indirect source) |
| Microsoft MSN AI travel guide Ottawa Food Bank tourist attraction August 2023 | M05 | confirmed; cause disputed |
| Gannett pauses LedeAI high school sports articles August 2023 | M06 | confirmed |
| MSN AI obituary Brandon Hunter "useless at 42" September 2023 | M07 | confirmed; AI involvement not confirmed by Microsoft |
| Guardian Microsoft AI poll woman death Sydney MSN reputational damage October 2023 | M08 | confirmed |
| Sports Illustrated AI-generated fake author profiles Futurism November 2023 Arena Group | M09 | confirmed; company disputes |
| Grok X Explore AI news summary false headline Klay Thompson vandalism bricks April 2024 | M10 | confirmed |
| Google AI Overviews glue on pizza eat rocks May 2024 | M11 | confirmed |
| Penske Media sues Google AI Overviews traffic decline September 2025 | M11 | confirmed (allegations) |
| Hoodline AI-generated local news fake reporter bylines Nieman Lab 2024 | M12 | confirmed |
| Apple suspends Apple Intelligence news notification summaries BBC complaint January 2025 iOS 18.3 | M13 | confirmed; later status not found |
| Bloomberg AI-generated news summaries corrections dozens 2025 | M14 | confirmed; count 30 vs 36 |
| Quartz AI-generated articles "Quartz Intelligence Newsroom" errors 2024 | M15 | confirmed for Jan 2025; no 2024 coverage found |
| Los Angeles Times Insights AI tool Ku Klux Klan removed March 2025 | M16 | confirmed; characterisation contested |
| Chicago Sun-Times Philadelphia Inquirer AI summer reading list fake books King Features May 2025 | M17 | confirmed |
| Wikipedia pauses AI-generated article summaries editor backlash June 2025 Wikimedia | M18 | confirmed |
| Elle Belgium fake AI journalists articles 2025 Ventures Media | M19 | confirmed via outlets reporting VRT |
| Wired Business Insider remove articles fake freelancer Margaux Blanchard AI August 2025 | M20 | confirmed |
| Politico AI tools Report Builder errors union arbitration PEN Guild 2025 | M21 | confirmed |
| BBC research AI assistants news answers significant issues 51% February 2025 EBU study 45% October 2025 | S1 | confirmed |
| Live page check: Brussels Times, NOS, EBU Spotlight (Elle Belgium) | M19 | facts re-checked against page text; 2 unsupported details removed |

**Considered but not included:**

- Irish Times AI-generated hoax op-ed (May 2023): Not searched/verified in this pass, so excluded under the no-assumption rule.
- News Corp Australia AI-produced local articles (2023): Not a documented failure in sources found; excluded.

*Generated by `build.py` from `data/`. Edit the JSON, never this file.*
