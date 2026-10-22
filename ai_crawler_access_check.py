#!/usr/bin/env python3
"""ai-crawler-access-check: what do AI crawlers really get from your site?

robots.txt can allow a bot while a firewall, CDN or host still blocks it with 403.
This tool requests a URL with the user-agent of each major AI crawler and reports
the HTTP status, next to what robots.txt says. No dependencies.

Note: real crawlers are verified by IP by some firewalls; this test only shows
user-agent based blocking, which is the most common cause.

Usage:
    python3 ai_crawler_access_check.py https://example.nl
    python3 ai_crawler_access_check.py example.nl --path /llms.txt --json

Made by Joepify (https://www.joepify.nl), MIT licence.
"""
import argparse, json, sys, time, urllib.error, urllib.request, urllib.robotparser

BOTS = {
    # name: (user-agent string, purpose)
    "GPTBot": ("Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.2; +https://openai.com/gptbot)", "OpenAI training"),
    "OAI-SearchBot": ("Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)", "ChatGPT search"),
    "ChatGPT-User": ("Mozilla/5.0 (compatible; ChatGPT-User/1.0; +https://openai.com/bot)", "ChatGPT user fetch"),
    "ClaudeBot": ("Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)", "Anthropic training"),
    "Claude-SearchBot": ("Mozilla/5.0 (compatible; Claude-SearchBot/1.0)", "Claude search"),
    "Claude-User": ("Mozilla/5.0 (compatible; Claude-User/1.0)", "Claude user fetch"),
    "PerplexityBot": ("Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)", "Perplexity search"),
    "Perplexity-User": ("Mozilla/5.0 (compatible; Perplexity-User/1.0)", "Perplexity user fetch"),
    "Google-Extended": ("Mozilla/5.0 (compatible; Google-Extended)", "Gemini training token"),
    "Googlebot": ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)", "Google Search / AI Overviews"),
    "bingbot": ("Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)", "Bing / Copilot"),
    "Applebot": ("Mozilla/5.0 (compatible; Applebot/0.1)", "Apple / Siri"),
    "CCBot": ("CCBot/2.0 (https://commoncrawl.org/faq/)", "Common Crawl (training data)"),
    "MistralAI-User": ("Mozilla/5.0 (compatible; MistralAI-User/1.0)", "Mistral Le Chat fetch"),
    "Amazonbot": ("Mozilla/5.0 (compatible; Amazonbot/0.1)", "Amazon / Alexa"),
    "meta-externalagent": ("meta-externalagent/1.1", "Meta AI"),
    "DuckAssistBot": ("DuckAssistBot/1.0", "DuckDuckGo assist"),
    "browser": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36", "normal visitor (baseline)"),
}


def status(url, ua):
    req = urllib.request.Request(url, headers={"User-Agent": ua}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, len(r.read(200000))
    except urllib.error.HTTPError as e:
        return e.code, 0
    except Exception as e:
        return f"error: {type(e).__name__}", 0


def main():
    ap = argparse.ArgumentParser(description="Check what AI crawlers get from a site.")
    ap.add_argument("site")
    ap.add_argument("--path", default="/")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    base = a.site if a.site.startswith("http") else "https://" + a.site
    base = base.rstrip("/")
    url = base + a.path
    rp = urllib.robotparser.RobotFileParser(base + "/robots.txt")
    try:
        rp.read()
    except Exception:
        rp = None
    rows = []
    for name, (ua, purpose) in BOTS.items():
        code, size = status(url, ua)
        allowed = rp.can_fetch(name, url) if rp else None
        rows.append({"bot": name, "purpose": purpose, "robots_allows": allowed, "http_status": code, "bytes": size})
        time.sleep(0.4)
    if a.json:
        print(json.dumps({"url": url, "results": rows}, indent=2))
        return
    print(f"URL: {url}\n")
    print(f"{'bot':20} {'robots.txt':11} {'HTTP':6} purpose")
    for r in rows:
        rb = {True: "allow", False: "disallow", None: "?"}[r["robots_allows"]]
        flag = "  <-- blocked despite robots.txt" if r["robots_allows"] and r["http_status"] in (401, 403, 429, 503) else ""
        print(f"{r['bot']:20} {rb:11} {str(r['http_status']):6} {r['purpose']}{flag}")
    print("\nBlocked bots that robots.txt allows usually mean a firewall/CDN/host rule. Guide (Dutch): https://www.joepify.nl/gevonden-worden-in-chatgpt")


if __name__ == "__main__":
    sys.exit(main())
