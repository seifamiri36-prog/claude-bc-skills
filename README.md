# Claude BC Skills — Business Central / AL für Claude Code

Drei [Claude-Code-Skills](https://code.claude.com/docs/en/skills) für Microsoft Dynamics 365
Business Central, entstanden in einem realen BC-28.3-Projekt (AL-Extension für die
österreichische Baubranche, lokaler Docker-Container, eigene Testsuite). Inhalt auf Deutsch;
English summary at the bottom.

**Der Kern in einem Satz:** Standard-Tabellen, -Felder und -Ereignisse werden **nachgeschlagen,
nicht erinnert** — ein `grep` in die mitgelieferten Extrakte liefert in einer Sekunde einen Beleg,
wo ein Name aus dem Gedächtnis eine Vermutung wäre.

## Was drin ist

| Skill | Was er kann | Umfang |
|---|---|---|
| **`business-central`** | Rahmen für BC-Projekte (AL-Extension, API-Anbindung, Satelliten-Apps) **plus das Nachschlagewerk**: Felder, Objekt-IDs und Ereignis-Andockstellen des BC-28.3-Standards als grep-bare Textdateien, mit Anleitung und Neuerzeugungs-Skript | 1.364 Tabellen · 23.370 Felder · 14.183 Standardobjekte · 23.629 Ereignisse · 5 Referenzdokumente |
| **`bc-al-cookbook`** | „Wie macht man X in AL?" — 254 destillierte Muster aus Erik Hougaards ~350 Video-Demos, je Muster: Technik, Code-Essenz, **Fallstricke**, Quellordner, Praxis-Relevanz. HTTP/REST/OAuth, JSON/XML/CSV/Excel, Events/Interfaces, ControlAddIns/JS, Hintergrund-Tasks, Performance, Filter/Queries, Reports/PDF, Berechtigungen, Validierung, defensive AL-Fallen, Tooling | 12 Referenzdateien, ~475 KB |
| **`business-central-development`** | Kompakter AL-Leitfaden (Fork von Mindrally/skills, Apache-2.0) — **vier Upstream-Fehler korrigiert** (try/catch, Confirm ohne GuiAllowed, camelCase, ApplicationArea), Änderungen in `CHANGES.md` dokumentiert | 1 Datei |

Alle drei Skills ergänzen sich: `business-central` sagt **was der Standard hat**, `bc-al-cookbook`
sagt **wie man es baut**, `business-central-development` ist die **Kurzcheckliste**.

## Installation

Du brauchst eine der drei Varianten, nicht alle.

### A · Als Plugin über den Claude-Code-Marketplace (empfohlen, bekommt Updates)

In einer Claude-Code-Sitzung:

```
/plugin marketplace add seifamiri36-prog/claude-bc-skills
/plugin install bc-skills@claude-bc-skills
```

Oder im Terminal:

```bash
claude plugin marketplace add seifamiri36-prog/claude-bc-skills
claude plugin install bc-skills@claude-bc-skills
```

Die Skills heißen dann `bc-skills:business-central`, `bc-skills:bc-al-cookbook` und
`bc-skills:business-central-development`. Updates: `/plugin marketplace update claude-bc-skills`.

### B · Mit dem `skills`-CLI (legt die Skills direkt in den Skill-Ordner)

```bash
# global, für alle Projekte:
npx skills add seifamiri36-prog/claude-bc-skills -g -a claude-code

# nur für das aktuelle Projekt (.claude/skills/):
npx skills add seifamiri36-prog/claude-bc-skills -a claude-code

# nur einen Skill:
npx skills add seifamiri36-prog/claude-bc-skills --skill bc-al-cookbook -g -a claude-code
```

Das Werkzeug unterstützt auch andere Agenten (Cursor, Codex, OpenCode, …) über `-a`.

### C · Von Hand

```bash
git clone https://github.com/seifamiri36-prog/claude-bc-skills
cp -r claude-bc-skills/skills/* ~/.claude/skills/
```

Prüfen: in einer neuen Claude-Code-Sitzung `/skills` eingeben (oder einfach eine BC-Frage stellen).

## Benutzung

Die Skills triggern von selbst, sobald Business Central, AL, OData, eine ERP-App oder eine
konkrete AL-Technik zur Sprache kommt. Beispiele:

```
Welche Felder hat die Tabelle "Job Task" im Standard?
Gibt es im Standard ein Feld für einen Leistungszeitraum am Verkaufskopf?
Welche Ereignisse feuert "Purch.-Post" nach dem Buchen? Ich will mich daran hängen.
Wie rufe ich aus AL eine REST-API mit OAuth2 Client Credentials auf?
Wie lese ich ein Blob-Feld auf einer API-Page aus?
Entwirf mir eine Bauleiter-App, die Tagesrapporte in unser Business Central schreibt.
```

Die Nachschlagedateien kannst du auch ohne Claude benutzen:

```bash
cd skills/business-central/references
grep "^Sales Header|" bc28-standard-datenmodell.txt              # alle Felder einer Tabelle
grep -i "|.*unit of measure" bc28-standard-datenmodell.txt        # Feld dem Namen nach
grep "^1|18$" bc28-objektinventar.txt                            # ist Table 18 belegt?
grep -F ' "Purch.-Post"|' bc28-ereignisse.txt | grep '|OnAfter'  # Andockstellen
```

## Herkunft, Belegkraft, Grenzen

Dieses Material ist **in einem Projekt gewachsen**, nicht am Reißbrett entstanden. Das ist seine
Stärke (jede Warnung hat einen Schadensfall hinter sich) und seine Grenze:

- **Die Extrakte zeigen BC 28.3, AT-Lokalisierung, einen Stand vom August/September 2026.**
  Felder und Ereignisse kommen und gehen zwischen Versionen — vor dem Bau gegen die installierte
  Version gegenprüfen. Neuerzeugung für andere Versionen: `references/standard-nachschlagen.md`
  (SQL-Befehl) und `scripts/Baue-Ereignisindex.py`.
- **FlowFields haben keine SQL-Spalte** und fehlen deshalb im Datenmodell-Extrakt. Ein
  Null-Treffer auf einem FlowField ist kein Abwesenheitsbeweis.
- **Der Ereignisindex sagt, was deklariert ist — nicht, ob es in deinem Pfad feuert.**
- **Das Cookbook beschreibt, was in einer Demo funktioniert hat — nicht, was Microsoft
  zusichert.** Für Plattform-Zusicherungen gilt die Herstellerdoku; das Cookbook sagt das selbst
  und markiert unbelegte Stellen ausdrücklich (`UNBELEGT`).
- Inhalt, Beispiele und Relevanz-Bewertungen tragen eine **Bau-Branchen-Brille** (Leistungsverzeichnis,
  Rapport, Aufmaß, ÖNORM). Das Muster überträgt sich auf andere Branchen; die Beispiele nicht 1:1.

Die Projektfassung dieser Skills (mit Projektregeln, eigenen Objekt-IDs, Container-Namen) ist
nicht öffentlich; diese Fassung wurde deterministisch daraus erzeugt und auf Projektinterna geprüft.

## Mitmachen

Widerlegte Aussagen, neue Fallstricke, Extrakte für andere BC-Versionen oder Lokalisierungen:
Issue oder Pull Request. Regel aus dem Cookbook: **Korrektur mit Datum und Beleg** (Demo-Ordner,
Microsoft-Learn-Seite oder Messung), nicht nur mit Meinung.

## Lizenz

Eigener Inhalt: **MIT** (siehe `LICENSE`). Drittquellen und ihre Bedingungen stehen in
`NOTICE.md` — insbesondere: das Cookbook ist eine Destillation von Erik Hougaards öffentlichen
Demo-Quellen (Attribution dort), `business-central-development` ist ein Apache-2.0-Fork, und die
Extrakte sind Metadaten (Namen, Typen, Signaturen) des Microsoft-Standards, kein Quellcode.

---

## English summary

Three Claude Code skills for Microsoft Dynamics 365 Business Central / AL, grown in a real BC 28.3
project (Austrian construction-industry extension). Content is in German.

- **`business-central`** — project guidance (AL extensions, APIs, satellite apps) **plus grep-able
  extracts of the BC 28.3 standard**: 1,364 tables / 23,370 fields, 14,183 standard object IDs,
  23,629 event hooks with signatures. Look names up instead of guessing them.
- **`bc-al-cookbook`** — 254 distilled AL patterns ("how do I do X in AL?") from Erik Hougaard's
  ~350 video demos, each with code essence, pitfalls and source folder.
- **`business-central-development`** — concise AL checklist, corrected fork of Mindrally/skills
  (four upstream errors fixed, documented in `CHANGES.md`).

Install: `/plugin marketplace add seifamiri36-prog/claude-bc-skills` then
`/plugin install bc-skills@claude-bc-skills`, or `npx skills add seifamiri36-prog/claude-bc-skills -g -a claude-code`,
or clone and copy `skills/*` into `~/.claude/skills/`. License: MIT for own content; see `NOTICE.md`
for third-party sources.
