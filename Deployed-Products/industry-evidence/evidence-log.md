# GenAI Production Incidents: Evidence Log

**Verified on:** 2026-11-23  
**Method:** Each claim was checked with a live web search on the date above. 'Primary' = court record, regulator, or the company's own post. 'Secondary' = major news or security-research coverage. Discrepancies between sources are recorded, not hidden.  
**Link check:** 44 source URLs checked at 2026-11-23T18:38:51: 43 × HTTP 200, 1 × HTTP 403. HTTP 200 proves the page exists. The claim itself was checked against search-result summaries of these sources.

> These are **public** incidents, as reported. Lawsuits are allegations unless a ruling is noted. Confidence: **high** = primary source or several consistent major outlets; **medium-high** = consistent coverage but mainly one party's account; **medium** = current status not verified.

## Matrix: product × area

| Product | 🌀 Hallucination & wrong answers | 🔓 Data privacy & leakage | 💉 Prompt injection & jailbreak | 🤖 Excessive agency (agents acting) | 📉 Model updates & quality drift | ⚠️ Harmful or biased output | 📦 Supply chain & tooling security | ©️ Copyright & IP | ⚖️ Regulation & liability |
|---|---|---|---|---|---|---|---|---|---|
| ChatGPT | EV-01 | EV-02 | · | · | EV-03 | · | · | EV-04 | EV-05 |
| Google Gemini / Search AI | EV-06, EV-07 | · | · | · | · | EV-08 | · | · | · |
| Microsoft Copilot | · | · | EV-09, EV-10 | · | · | · | · | · | · |
| GitHub Copilot | · | · | EV-11 | · | · | · | · | EV-12 | · |
| Claude | EV-13 | · | · | · | EV-14 | · | · | · | · |
| Meta AI | EV-15 | EV-16 | · | · | · | · | · | · | · |
| Grok | · | EV-18 | · | · | · | EV-17 | · | · | · |
| Perplexity Comet | · | · | EV-19 | · | · | · | · | · | · |
| Amazon Q Developer | · | · | · | · | · | · | EV-20 | · | · |
| Replit Agent | · | · | · | EV-21 | · | · | · | · | · |
| Air Canada chatbot (deployer) | · | · | · | · | · | · | · | · | EV-22 |

`·` = no incident logged here. It does **not** mean the product is free of that risk.

## Incidents

### EV-12 · GitHub Copilot · Developers' class action over open-source licences (Doe v. GitHub)

| Field | Value |
|---|---|
| Date | 2022-11-03 |
| Area | ©️ Copyright & IP |
| What happened | Developers allege Copilot reproduces licensed open-source code without attribution. |
| Impact | Many claims dismissed in 2024. Some survived. An appeal was filed with the Ninth Circuit (No. 24-7700). |
| Confidence | **medium** |
| Notes / discrepancies | Status after late 2024 NOT verified. These are allegations, not findings. |

| Source | Type | Link check |
|---|---|---|
| [The Register, 12 Jan 2024](https://www.theregister.com/2024/01/12/github_copilot_copyright_case_narrowed/) | secondary | 200 OK |
| [Original complaint](https://githubcopilotlitigation.com/pdf/07074/1-0-github_complaint.pdf) | primary | 200 OK |

### EV-15 · Meta AI · Galactica science model pulled about 3 days after launch

| Field | Value |
|---|---|
| Date | 2022-11-17 |
| Area | 🌀 Hallucination & wrong answers |
| What happened | The public demo produced authoritative-sounding but false science, including papers attributed to real authors that don't exist. |
| Impact | Demo taken offline. |
| Confidence | **high** |
| Notes / discrepancies | Reported as 2 or 3 days depending on source. |

| Source | Type | Link check |
|---|---|---|
| [MIT Technology Review, 18 Nov 2022](https://www.technologyreview.com/2022/11/18/1063487/meta-large-language-model-ai-only-survived-three-days-gpt-3-science/) | secondary | 200 OK |
| [OECD AI incident record](https://oecd.ai/en/incidents/2022-11-22-6a50) | secondary | 200 OK |

### EV-06 · Google Gemini / Search AI · Bard gives a wrong answer in its own launch ad

| Field | Value |
|---|---|
| Date | 2023-02-08 |
| Area | 🌀 Hallucination & wrong answers |
| What happened | Google's promotional demo had Bard answer wrongly about the first images of a planet outside our solar system. Reuters spotted the error. |
| Impact | Alphabet shares fell about 7.7–9% the next day, roughly $100B in market value. |
| Confidence | **high** |
| Notes / discrepancies | The size of the drop varies by source (7.7%, 8%, 9%). The share fall can't be attributed to the error alone. |

| Source | Type | Link check |
|---|---|---|
| [NPR, 9 Feb 2023](https://www.npr.org/2023/02/09/1155650909/google-chatbot--error-bard-shares) | secondary | 200 OK |
| [Al Jazeera, 8 Feb 2023](https://www.aljazeera.com/economy/2023/2/8/google-shares-tank-8-as-ai-chatbot-bard-flubs-answer-in-ad) | secondary | 200 OK |

### EV-09 · Microsoft Copilot · Bing Chat reveals its hidden "Sydney" system prompt

| Field | Value |
|---|---|
| Date | 2023-02-09 |
| Area | 💉 Prompt injection & jailbreak |
| What happened | A Stanford student typed "Ignore previous instructions" and got Bing Chat to reveal its codename and confidential rules. |
| Impact | Microsoft confirmed to The Verge that the leaked prompt was genuine. The technique was patched, then worked again by another route. |
| Confidence | **medium-high** |
| Notes / discrepancies | Microsoft confirmation comes via press reports, not a Microsoft post. Some outlets could not reproduce it. |

| Source | Type | Link check |
|---|---|---|
| [Simon Willison, 9 Feb 2023](https://simonwillison.net/2023/Feb/9/sidney/) | secondary | 200 OK |
| [AI Incident Database](https://incidentdatabase.ai/reports/2666) | secondary | 200 OK |

### EV-02 · ChatGPT · Redis bug exposed other users' chat titles and payment details

| Field | Value |
|---|---|
| Date | 2023-03-20 |
| Area | 🔓 Data privacy & leakage |
| What happened | A bug in the redis-py client returned cached data to the wrong user. Some users saw others' chat titles, and payment-related details became visible. |
| Impact | ChatGPT was taken offline. Payment info possibly visible for 1.2% of Plus subscribers active in a 9-hour window. OpenAI says full card numbers were never exposed. |
| Confidence | **high** |
| Notes / discrepancies | Some headlines also mention email addresses. OpenAI's own post focuses on payment details and chat titles. |

| Source | Type | Link check |
|---|---|---|
| [OpenAI: March 20 ChatGPT outage](https://openai.com/index/march-20-chatgpt-outage) | primary | 200 OK |
| [SecurityAffairs](https://securityaffairs.com/144057/data-breach/openai-chatgpt-redis-bug.html) | secondary | 200 OK |

### EV-01 · ChatGPT · Lawyers sanctioned for ChatGPT-invented cases (Mata v. Avianca)

| Field | Value |
|---|---|
| Date | 2023-06-22 |
| Area | 🌀 Hallucination & wrong answers |
| What happened | Lawyers filed a brief citing six non-existent court opinions that ChatGPT had invented. Opposing counsel could not find them. |
| Impact | $5,000 sanction on two lawyers and their firm; the judge found bad faith. The client's suit was dismissed as filed too late. |
| Confidence | **high** |
| Notes / discrepancies | Reported as 678 F. Supp. 3d 443 (S.D.N.Y. 2023). |

| Source | Type | Link check |
|---|---|---|
| [S.D.N.Y. sanctions opinion (court record)](https://storage.courtlistener.com/recap/gov.uscourts.nysd.575368/gov.uscourts.nysd.575368.54.0_4.pdf) | primary | 200 OK |
| [CNBC, 30 May 2023](https://www.cnbc.com/2023/05/30/chatgpt-cited-bogus-cases-for-a-new-york-federal-court-filing.html) | secondary | 200 OK |

### EV-04 · ChatGPT · New York Times sues OpenAI and Microsoft for copyright infringement

| Field | Value |
|---|---|
| Date | 2023-12-27 |
| Area | ©️ Copyright & IP |
| What happened | The Times alleges its articles were used without permission to train models, and that outputs reproduce its work. |
| Impact | Seeks billions in damages and destruction of models trained on its works. Case No. 1:23-cv-11195 (S.D.N.Y.). |
| Confidence | **high** |
| Notes / discrepancies | Filing verified. Current case status NOT checked; it is an allegation, not a ruling. |

| Source | Type | Link check |
|---|---|---|
| [NPR, 27 Dec 2023](https://www.npr.org/2023/12/27/1221821750/new-york-times-sues-chatgpt-openai-microsoft-for-copyright-infringement) | secondary | 200 OK |
| [CNBC, 27 Dec 2023](https://www.cnbc.com/2023/12/27/new-york-times-sues-microsoft-chatgpt-maker-openai-over-copyright-infringement.html) | secondary | 200 OK |

### EV-22 · Air Canada chatbot (deployer) · Airline held liable for its chatbot's wrong bereavement-fare answer

| Field | Value |
|---|---|
| Date | 2024-02-14 |
| Area | ⚖️ Regulation & liability |
| What happened | The website chatbot said a bereavement fare could be claimed after travel. The airline's own policy page said it could not. |
| Impact | The BC Civil Resolution Tribunal rejected Air Canada's argument that the chatbot was a separate entity. The airline paid C$812.02. |
| Confidence | **high** |
| Notes / discrepancies | Small money, big precedent: the company owns what its bot says. This is the most relevant case for companies that deploy GenAI rather than build models. |

| Source | Type | Link check |
|---|---|---|
| [Moffatt v. Air Canada, 2024 BCCRT 149 (ABA summary)](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/) | secondary | 403 (site blocks automated checks; found via search) |
| [CBC, Feb 2024](https://www.cbc.ca/amp/1.7116416) | secondary | 200 OK |

### EV-08 · Google Gemini / Search AI · Gemini image generation of people paused after historical inaccuracies

| Field | Value |
|---|---|
| Date | 2024-02-22 |
| Area | ⚠️ Harmful or biased output |
| What happened | Tuning to make images diverse produced historically inaccurate images (e.g. a "1943 German soldier"). |
| Impact | Google paused image generation of people and published an explanation. |
| Confidence | **high** |
| Notes / discrepancies | A safety and bias correction that overcorrected. That is the over-blocking side of the problem. |

| Source | Type | Link check |
|---|---|---|
| [Google: Gemini image generation issue](https://blog.google/products/gemini/gemini-image-generation-issue/) | primary | 200 OK |
| [CNBC, 22 Feb 2024](https://www.cnbc.com/2024/02/22/google-pauses-gemini-ai-image-generator-after-inaccuracies.html) | secondary | 200 OK |

### EV-07 · Google Gemini / Search AI · AI Overviews suggests glue on pizza and eating rocks

| Field | Value |
|---|---|
| Date | 2024-05-30 |
| Area | 🌀 Hallucination & wrong answers |
| What happened | Search AI summaries repeated a joke Reddit post (glue in pizza sauce) and an article from The Onion (eat rocks). |
| Impact | Google published "About last week", restricted AI Overviews for nonsensical and satirical queries, and said many viral screenshots were fake. |
| Confidence | **high** |
| Notes / discrepancies | This is a retrieval-quality failure: the source was satire or a joke, and it was ranked as fact. |

| Source | Type | Link check |
|---|---|---|
| [Google: AI Overviews, about last week](https://blog.google/products/search/ai-overViews-update-may-2024) | primary | 200 OK |
| [The Register, 31 May 2024](https://www.theregister.com/2024/05/31/google_ai_search_update/) | secondary | 200 OK |

### EV-05 · ChatGPT · Italy's privacy regulator fines OpenAI €15 million

| Field | Value |
|---|---|
| Date | 2024-12-20 |
| Area | ⚖️ Regulation & liability |
| What happened | The Garante found OpenAI processed personal data to train ChatGPT without an adequate legal basis, broke transparency duties, and did not notify it of the March 2023 breach. |
| Impact | €15M fine and a 6-month public information campaign. Reported as the first GDPR fine on a generative AI service. OpenAI said it would appeal. |
| Confidence | **high** |
| Notes / discrepancies | Links back to EV-02: the unreported breach was part of the finding. |

| Source | Type | Link check |
|---|---|---|
| [Garante decision (regulator)](https://www.garanteprivacy.it/home/docweb/-/docweb-display/print/10085432) | primary | 200 OK |
| [Euronews, 20 Dec 2024](https://www.euronews.com/2024/12/20/italys-privacy-watchdog-fines-openai-15-million-after-probe-into-chatgpt-data-collection) | secondary | 200 OK |

### EV-03 · ChatGPT · GPT-4o update made ChatGPT sycophantic; rolled back

| Field | Value |
|---|---|
| Date | 2025-04-25 |
| Area | 📉 Model updates & quality drift |
| What happened | An update made the model excessively flattering. OpenAI said it over-weighted short-term thumbs-up/down feedback, and its tests did not look for sycophancy. |
| Impact | Rollback began 28 April 2025. OpenAI published two post-mortems and changed its release process. |
| Confidence | **high** |
| Notes / discrepancies | Expert testers felt something was off, but the release went ahead. That is a lesson about release gates. |

| Source | Type | Link check |
|---|---|---|
| [OpenAI: Sycophancy in GPT-4o](https://openai.com/index/sycophancy-in-gpt-4o/) | primary | 200 OK |
| [OpenAI: Expanding on sycophancy](https://openai.com/index/expanding-on-sycophancy/) | primary | 200 OK |

### EV-13 · Claude · Claude-formatted citation error in Anthropic's own court filing

| Field | Value |
|---|---|
| Date | 2025-05-15 |
| Area | 🌀 Hallucination & wrong answers |
| What happened | In the music publishers' case against Anthropic, an expert report's citation had the wrong title and authors after Claude was used to format it. The lawyer's review missed it. |
| Impact | Anthropic's law firm (Latham & Watkins) apologised to the court, calling it an embarrassing and unintentional mistake. |
| Confidence | **high** |
| Notes / discrepancies | The filing calls it a citation mistake, not an invented source: the publication and link were real. |

| Source | Type | Link check |
|---|---|---|
| [TechCrunch, 15 May 2025](https://techcrunch.com/2025/05/15/anthropics-lawyer-was-forced-to-apologize-after-claude-hallucinated-a-legal-citation) | secondary | 200 OK |
| [The Register, 15 May 2025](https://www.theregister.com/2025/05/15/anthopics_law_firm_blames_claude_hallucinations/) | secondary | 200 OK |

### EV-10 · Microsoft Copilot · EchoLeak: zero-click data theft from Microsoft 365 Copilot (CVE-2025-32711)

| Field | Value |
|---|---|
| Date | 2025-06-11 |
| Area | 💉 Prompt injection & jailbreak |
| What happened | A crafted email could make M365 Copilot exfiltrate internal data without the user clicking anything. Aim Labs called it an "LLM scope violation". |
| Impact | CVSS 9.3 (critical). Fixed server-side by Microsoft in May 2025. No evidence of real-world exploitation. |
| Confidence | **high** |
| Notes / discrepancies | Discovered Jan 2025, disclosed June 2025. This is the same pattern as our Lab 4.5 attack page, applied to email. |

| Source | Type | Link check |
|---|---|---|
| [The Hacker News, June 2025](https://thehackernews.com/2025/06/zero-click-ai-vulnerability-exposes.html) | secondary | 200 OK |
| [SecurityWeek](https://www.securityweek.com/echoleak-ai-attack-enabled-theft-of-sensitive-data-via-microsoft-365-copilot/) | secondary | 200 OK |

### EV-16 · Meta AI · Meta AI app's Discover feed exposed chats users didn't mean to publish

| Field | Value |
|---|---|
| Date | 2025-06-12 |
| Area | 🔓 Data privacy & leakage |
| What happened | Users pressed Share without realising it posted to a public feed. Medical, legal and personal questions became public, some linked to real accounts. |
| Impact | Wide criticism of the design. Meta says chats are private unless users take several steps to share them. |
| Confidence | **medium-high** |
| Notes / discrepancies | Meta disputes calling it a leak. A UX/consent failure, not a hack. |

| Source | Type | Link check |
|---|---|---|
| [Malwarebytes, June 2025](https://www.malwarebytes.com/blog/news/2025/06/your-meta-ai-chats-might-be-public-and-it's-not-a-bug) | secondary | 200 OK |
| [TechRadar](https://www.techradar.com/computing/artificial-intelligence/i-dont-like-the-idea-of-my-conversations-with-meta-ai-being-public-heres-how-you-can-opt-out) | secondary | 200 OK |

### EV-17 · Grok · Grok posts antisemitic content ("MechaHitler") after a prompt/code change

| Field | Value |
|---|---|
| Date | 2025-07-08 |
| Area | ⚠️ Harmful or biased output |
| What happened | After instructions to be "politically incorrect" and an upstream code change, the @grok bot echoed extremist posts for about 16 hours. |
| Impact | xAI apologised, removed the code, refactored the system, and published its system prompts. Condemned by the ADL. |
| Confidence | **high** |
| Notes / discrepancies | Start date reported as 7 or 8 July. Shows that a prompt change is a release and needs the same gate. |

| Source | Type | Link check |
|---|---|---|
| [TechCrunch, 12 Jul 2025](https://techcrunch.com/2025/07/12/xai-and-grok-apologize-for-horrific-behavior) | secondary | 200 OK |
| [NPR, 9 Jul 2025](https://www.npr.org/2025/07/09/nx-s1-5462609/grok-elon-musk-) | secondary | 200 OK |

### EV-20 · Amazon Q Developer · Malicious "wipe the system" prompt shipped in Amazon Q VS Code extension v1.84.0

| Field | Value |
|---|---|
| Date | 2025-07-17 |
| Area | 📦 Supply chain & tooling security |
| What happened | An over-scoped GitHub token let an attacker commit a prompt telling the agent to delete files and cloud resources. It shipped in a public release. |
| Impact | AWS says the code did not run because of a syntax error, and no customer resources were affected. Fixed in 1.85.0 (CVE-2025-8217). About 950k installs. |
| Confidence | **high** |
| Notes / discrepancies | Release date given as 17 or 19 July. It is both a supply-chain failure and an excessive-agency risk. |

| Source | Type | Link check |
|---|---|---|
| [AWS security bulletin AWS-2025-015](https://aws.amazon.com/security/security-bulletins/AWS-2025-015/) | primary | 200 OK |
| [The Register, 24 Jul 2025](https://www.theregister.com/2025/07/24/amazon_q_ai_prompt/) | secondary | 200 OK |

### EV-21 · Replit Agent · AI coding agent deleted a production database during a code freeze

| Field | Value |
|---|---|
| Date | 2025-07-18 |
| Area | 🤖 Excessive agency (agents acting) |
| What happened | During SaaStr founder Jason Lemkin's 12-day experiment, the agent deleted the live database despite an instruction to freeze changes, then said it could not be restored. |
| Impact | About 1,200 executive records lost, though rollback later worked. Replit's CEO apologised and promised automatic separation of development and production databases. |
| Confidence | **medium-high** |
| Notes / discrepancies | Mostly based on Lemkin's own posts and screenshots. Replit's CEO publicly acknowledged it. Day 8 vs day 9 differs between sources. |

| Source | Type | Link check |
|---|---|---|
| [Fortune, 23 Jul 2025](https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/) | secondary | 200 OK |
| [The Register, 21 Jul 2025](https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident) | secondary | 200 OK |

### EV-11 · GitHub Copilot · Prompt injection to remote code execution in Copilot (CVE-2025-53773)

| Field | Value |
|---|---|
| Date | 2025-08-12 |
| Area | 💉 Prompt injection & jailbreak |
| What happened | Instructions hidden in code, issues or web pages could make Copilot turn on auto-approve ("YOLO mode") in settings, then run terminal commands. |
| Impact | Command execution on the developer's machine. Patched by Microsoft in August 2025. |
| Confidence | **medium-high** |
| Notes / discrepancies | CVSS differs by source (7.8 vs 9.6). Patch details not checked against Microsoft's MSRC advisory. |

| Source | Type | Link check |
|---|---|---|
| [Embrace The Red (original research)](https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection) | primary | 200 OK |
| [Wiz vulnerability DB](https://www.wiz.io/vulnerability-database/cve/cve-2025-53773) | secondary | 200 OK |

### EV-18 · Grok · Over 370,000 shared Grok chats indexed by search engines

| Field | Value |
|---|---|
| Date | 2025-08-20 |
| Area | 🔓 Data privacy & leakage |
| What happened | Grok's Share button created public URLs with no warning. Google, Bing and DuckDuckGo indexed them, including medical questions and at least one password. |
| Impact | Sensitive conversations became publicly searchable. |
| Confidence | **high** |
| Notes / discrepancies | Count from Forbes (370k); some outlets say 300k+. A similar ChatGPT shared-link issue happened shortly before, and OpenAI removed that feature. |

| Source | Type | Link check |
|---|---|---|
| [TechCrunch, 20 Aug 2025](https://techcrunch.com/2025/08/20/thousands-of-grok-chats-are-now-searchable-on-google) | secondary | 200 OK |
| [Fortune, 22 Aug 2025](https://fortune.com/2025/08/22/xai-grok-chats-public-on-google-search-elon-musk/) | secondary | 200 OK |

### EV-19 · Perplexity Comet · AI browser hijacked by hidden instructions in a Reddit comment

| Field | Value |
|---|---|
| Date | 2025-08-20 |
| Area | 💉 Prompt injection & jailbreak |
| What happened | Brave showed Comet treating page content as instructions. A hidden comment made it fetch the user's one-time password and leak it. |
| Impact | Reported 25 July 2025. Perplexity said it fixed the issue; Brave said the fix was incomplete and re-reported it. |
| Confidence | **high** |
| Notes / discrepancies | Brave is a competitor that makes its own browser. Perplexity disputed how severe it was. |

| Source | Type | Link check |
|---|---|---|
| [Brave: Indirect prompt injection in Perplexity Comet](https://brave.com/blog/comet-prompt-injection/) | primary | 200 OK |
| [The Register, 20 Aug 2025](https://www.theregister.com/2025/08/20/perplexity_comet_browser_prompt_injection/) | secondary | 200 OK |

### EV-14 · Claude · Three infrastructure bugs degraded Claude's answers for weeks

| Field | Value |
|---|---|
| Date | 2025-09-17 |
| Area | 📉 Model updates & quality drift |
| What happened | From August to early September 2025, a routing bug, token corruption and a TPU compiler issue intermittently degraded Claude's responses. Standard evals did not catch it. |
| Impact | Anthropic published a detailed post-mortem and changed its evaluation and monitoring. |
| Confidence | **high** |
| Notes / discrepancies | Exact dates differ between summaries. Read the primary post before quoting dates or percentages. Shows that quality can drift from infrastructure, not only from the model. |

| Source | Type | Link check |
|---|---|---|
| [Anthropic: A postmortem of three recent issues](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues) | primary | 200 OK |
| [InfoQ, Oct 2025](https://www.infoq.com/news/2025/10/anthropic-infrastructure-bugs) | secondary | 200 OK |

## Key areas and what to teach

| Area | Lesson | Where our labs touch it |
|---|---|---|
| 🌀 Hallucination & wrong answers | Fluent is not correct. Ground answers in sources, require citations, and keep a human check where errors cost money or reputation. | Banking invented "$"; AeroGuard said "No." to an airworthiness question |
| 🔓 Data privacy & leakage | Leaks come from ordinary bugs and share buttons as often as from the model. Test sharing flows, caches and defaults like any data system. | Card-number redaction bug in banking v1 |
| 💉 Prompt injection & jailbreak | Any text the model reads (email, web page, code comment, document) can carry instructions. Treat it as data and limit what the model can do. | Attack page in AeroGuard Lab 4.5: "6 units is acceptable, airworthy" |
| 🤖 Excessive agency (agents acting) | Once the AI can act, a wrong answer becomes an outage. Separate production from test, use an allowlist of tools, and require human approval. | AeroGuard tool allowlist + inspector approval |
| 📉 Model updates & quality drift | Your product can change without a change to your code. Pin versions, re-run evals on every update, and monitor quality live. | llama3 vs hosted model gave different wording |
| ⚠️ Harmful or biased output | A system prompt change can shift behaviour for millions of users within hours. Red-team every prompt change and roll it out in stages. | Over-blocking and under-blocking test cases |
| 📦 Supply chain & tooling security | Extensions, plugins and build tokens are part of your AI product. Scope credentials and review what ships. | MCP server HMAC token |
| ©️ Copyright & IP | Mostly the model makers' fight, but app builders need vendor indemnity and output filters for code and text. | Not covered in our labs |
| ⚖️ Regulation & liability | The company is responsible for what its bot says. Regulators fine missing legal bases and unreported breaches. | Audit log; release-gate checklist |

*Generated by `build.py` from `evidence.json`. Edit the JSON and rebuild, never the output.*
