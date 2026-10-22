# ai-crawler-access-check

**What do AI crawlers really get from your site?** robots.txt can allow GPTBot or ClaudeBot while a firewall, CDN or host still returns 403. This tool requests a URL with the user-agent of 17 AI and search crawlers and shows the HTTP status next to what robots.txt says. One Python file, no dependencies.

```bash
python3 ai_crawler_access_check.py https://example.nl
python3 ai_crawler_access_check.py example.nl --path /llms.txt --json
```

Example (a real site, October 2026): robots.txt allows everything, but the hosting firewall blocks the training crawlers:

```
GPTBot               allow       403    OpenAI training  <-- blocked despite robots.txt
OAI-SearchBot        allow       200    ChatGPT search
ClaudeBot            allow       403    Anthropic training  <-- blocked despite robots.txt
PerplexityBot        allow       200    Perplexity search
CCBot                allow       403    Common Crawl (training data)  <-- blocked despite robots.txt
```

Limits: some firewalls verify real crawlers by IP; this test shows user-agent based blocking, the most common cause. Bot documentation: [OpenAI](https://platform.openai.com/docs/bots) · [Google](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers)

Guide (Dutch): https://www.joepify.nl/gevonden-worden-in-chatgpt · Checklist: [geo-aeo-checklist-nl](https://github.com/Joepify/geo-aeo-checklist-nl)

Made by [Joepify](https://www.joepify.nl), Rotterdam. MIT licence.
