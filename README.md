# ai-crawler-access-check

**Krijgen ChatGPT, Claude en Perplexity echt toegang tot je website?** Je robots.txt kan GPTBot of ClaudeBot toestaan, terwijl een firewall, CDN of hostingpartij ze toch een 403 geeft. Dit script vraagt een URL op met de user-agent van 17 AI- en zoekcrawlers en zet de HTTP-status naast wat je robots.txt zegt.

Het is één Python-bestand, zonder afhankelijkheden (alleen Python 3).

## Voor wie

- Ondernemers en webbouwers die willen weten of hun site vindbaar is in AI-zoekmachines.
- Iedereen die in robots.txt AI-bots toestaat en wil controleren of dat ook echt zo uitpakt.

## Gebruik

```bash
python3 ai_crawler_access_check.py https://example.nl
python3 ai_crawler_access_check.py example.nl --path /llms.txt --json
```

- `--path` test een ander pad dan de homepage.
- `--json` geeft de uitkomst machineleesbaar terug, handig voor scripts.

## Voorbeeld van de uitvoer

Een echte site (oktober 2026): robots.txt staat alles toe, maar de firewall van de hostingpartij blokkeert de trainingscrawlers.

```
GPTBot               allow       403    OpenAI training  <-- blocked despite robots.txt
OAI-SearchBot        allow       200    ChatGPT search
ClaudeBot            allow       403    Anthropic training  <-- blocked despite robots.txt
PerplexityBot        allow       200    Perplexity search
CCBot                allow       403    Common Crawl (training data)  <-- blocked despite robots.txt
```

Lees dit zo: `allow` is wat robots.txt zegt, het getal is wat de server werkelijk terugstuurt. Staat er een 403 bij een bot die je wel wilt toelaten, dan zit het probleem bij de server, niet in robots.txt. Los het op bij je host of in de instellingen van je CDN.

## Beperkingen

Sommige firewalls controleren echte crawlers op IP-adres. Deze test laat blokkades op basis van user-agent zien, de meest voorkomende oorzaak. Een 200 hier is dus geen bewijs dat de echte bot er ook doorheen komt.

Documentatie van de bots: [OpenAI](https://platform.openai.com/docs/bots) en [Google](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers).

## Zie ook

- [geo-aeo-checklist-nl](https://github.com/Joepify/geo-aeo-checklist-nl): de volledige checklist voor vindbaarheid in AI-zoekmachines.
- [geo-case-joepify](https://github.com/Joepify/geo-case-joepify): de case waarin dit probleem werd gevonden.

## Laat het mij doen

Ik zorg dat AI-crawlers je site kunnen lezen en los blokkades bij je host op. Vaste prijs: €495 eenmalig voor de setup, daarna €249 per maand (excl. btw). [Meer over de website check](https://www.joepify.nl/website-apk?utm_source=github&utm_medium=readme&utm_campaign=ai-crawler-access-check) of [stuur een WhatsApp-bericht](https://wa.me/31687195043?text=Hoi%20Ayoub%2C%20ik%20kom%20via%20GitHub%20%28ai-crawler-access-check%29%20en%20wil%20hulp%20met%20ai%20crawlers.).

## Over Joepify

[Joepify](https://www.joepify.nl?utm_source=github&utm_medium=readme&utm_campaign=ai-crawler-access-check) is een webbureau aan de Metaalhof 27 in Rotterdam. Ayoub Assaidi bouwt websites en webshops en publiceert hier de tools die hij zelf gebruikt. Wil je je site laten doorlichten, begin dan met de gratis [website check](https://www.joepify.nl/website-apk?utm_source=github&utm_medium=readme&utm_campaign=ai-crawler-access-check).

## English

Does your robots.txt say "allow" while a firewall or CDN still returns 403 to AI crawlers? This single-file Python 3 script (no dependencies) requests a URL with the user-agent of 17 AI and search crawlers and prints the HTTP status next to the robots.txt verdict. Use `--path` for another path and `--json` for machine-readable output. It detects user-agent based blocking only; firewalls that verify crawlers by IP will not show up.

## Licentie

MIT, zie [LICENSE](LICENSE).
