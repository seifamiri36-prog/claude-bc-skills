# BC-Skills für Claude Code — Handbuch

**Beschreibung und Betriebsanleitung** · Paket `claude-bc-skills` · Stand 09.10.2026 · Lizenz MIT
**Leserkreis:** Entscheider (Kapitel 0 genügt), Entwickler und Dienstleister (ab Kapitel 1)
**Repo:** https://github.com/seifamiri36-prog/claude-bc-skills

---

## 0 · Kurzfassung für Entscheider

**Worum es geht.** Immer mehr Entwicklung läuft mit KI-Assistenten wie *Claude Code*. Ein solcher
Assistent kennt Microsoft Dynamics 365 Business Central (BC) nur ungefähr: Er weiß, wie AL-Code
aussieht, aber nicht, welche 23.370 Felder der BC-Standard wirklich hat, an welchen Stellen eine
Erweiterung andocken darf oder welche Technik in der Praxis eine Falle ist. Ohne Nachhilfe **rät**
er — plausibel, und erfahrungsgemäß in etwa einem von zehn Fällen falsch.

**Was dieses Paket ist.** Drei *Skills* — Wissenspakete, die der Assistent automatisch lädt,
sobald es um Business Central geht. Sie machen aus „die KI rät" ein „die KI schlägt nach":

| Skill | In einem Satz | Umfang |
|---|---|---|
| `business-central` | **Das Nachschlagewerk**: alle Standard-Tabellen, -Felder, -Objekte und -Ereignisse eines BC 28.3 als durchsuchbare Dateien, plus der Projektrahmen (Extension, API, Satelliten-Apps) | 1.364 Tabellen · 23.370 Felder · 14.183 Objekte · 23.629 Ereignisse |
| `bc-al-cookbook` | **Die Technik-Kartei**: „Wie macht man X in AL?" — 254 geprüfte Muster mit Fallstricken, jedes mit Praxis-Relevanz bewertet | 12 Themenbereiche, ~475 KB |
| `business-central-development` | **Die Kurzcheckliste**: ein öffentlicher AL-Leitfaden, bei dem vier Fehler gefunden und belegt korrigiert wurden | 1 Datei |

**Was es bringt — drei belegte Fälle aus dem Projekt, in dem die Skills entstanden sind** (eine
BC-28.3-Erweiterung für die Baubranche in Österreich, lokaler Docker-Container, eigene Testsuite):

1. **Zwei Tage Arbeit, die es nicht gebraucht hätte.** Ein Berechtigungssatz wurde über zwei Tage
   selbst gebaut, den Microsoft fertig mitliefert. Seither gilt dort die Regel: *erst nachschlagen,
   dann bauen* — und genau dafür sind die Skills da.
2. **Zwei Stunden auf eine Zeile verkürzt.** Der Nachweis, dass der Standardbeleg kein Feld
   „Leistungszeitraum" hat, kostete zwei Stunden Suche. Mit dem Nachschlagewerk ist das ein
   einziger Suchbefehl mit Beleg.
3. **Fehler aus fremdem Material abgefangen.** Ein öffentlich verbreiteter AL-Leitfaden empfahl
   u. a. `try/catch` (gibt es in AL nicht) und `Confirm` ohne Schutz (stürzt in Hintergrundjobs
   ab). Vier solcher Aussagen wurden gegen Microsoft Learn geprüft und korrigiert.

**Was es kostet.** Nichts an Lizenzen (MIT). Installation: zwei Befehle. Pflege: Updates per
Befehl; eigene Nachschlagedateien für eine andere BC-Version lassen sich in etwa einer Stunde
erzeugen (Kapitel 7).

**Vertrauenswürdigkeit.** Das Material ist in einem Projekt gewachsen, nicht am Reißbrett
entstanden. Jede Aussage nennt ihre Quelle (Messung, Demo-Ordner, Microsoft-Learn-Seite); was
nicht belegt ist, ist als `UNBELEGT` markiert; und die eigenen Projektregeln eines Teams gehen
den Skills immer vor (Kapitel 6).

---

## 1 · Was ein Skill ist — für Nicht-Techniker

*Claude Code* ist ein KI-Assistent, der direkt im Projektordner arbeitet: Er liest Code, schreibt
Code, baut und testet. Sein Allgemeinwissen endet beim Trainingsstand und ist bei Spezialthemen
wie Business Central lückenhaft.

Ein **Skill** ist ein Ordner mit einer Anleitung (`SKILL.md`: *wann* und *wie* benutzen) und
Referenzdateien (*was* nachschlagen). Der Assistent liest die Anleitung bei jedem Start, erkennt
am Gesprächsthema, dass ein Skill passt, und lädt dann gezielt die passende Referenzdatei.

Das Bild dazu: **ein Nachschlagewerk und eine Checkliste im Regal des Entwicklers, die die KI
selbst aufschlägt** — bevor sie etwas aus dem Gedächtnis behauptet.

Drei Eigenschaften, die für die Bewertung wichtig sind:

- **Lokal.** Skills liegen als Dateien auf dem Rechner des Entwicklers. Es wird kein KI-Modell
  trainiert, und die Skills enthalten keine Kundendaten (Kapitel 9).
- **Prüfbar.** Jede Aussage steht in einer Textdatei und nennt ihre Quelle.
- **Nachrangig.** Die Projektregeln eines Teams (z. B. eine `CLAUDE.md` im Repo) gewinnen bei
  jedem Widerspruch — sie kennen die Schadensfälle des eigenen Projekts, die Skills nicht.

---

## 2 · Die drei Skills im Überblick

| | `business-central` | `bc-al-cookbook` | `business-central-development` |
|---|---|---|---|
| **Frage, die er beantwortet** | *Was hat der Standard?* Welche Felder, Objekte, Ereignisse — und wie rahmt man ein BC-Projekt? | *Wie baut man das in AL?* Konkrete Technik mit Fallstricken | *Was muss ich beim AL-Schreiben beachten?* Kurzcheckliste |
| **Quelle** | Messungen an einem BC-28.3-Container (SQL) und am entpackten Standard-Quelltext | Erik Hougaards öffentliche Demo-Projekte (~350 Videos), destilliert und geprüft | Öffentlicher Leitfaden (Mindrally/skills, Apache-2.0), vier Korrekturen |
| **Belegkraft** | Messung = Beleg (mit dokumentierten Grenzen) | Demo = „hat in einem Beispiel funktioniert", nicht „Microsoft sichert zu" | Gegen Microsoft Learn geprüft |
| **Größe** | 7,0 MB (davon 6,9 MB Extrakte) | 0,5 MB | 20 KB |

Die drei ergänzen sich und überschneiden sich nicht: `business-central` sagt, **was** da ist,
`bc-al-cookbook` sagt, **wie** man es baut, `business-central-development` ist die **Checkliste**
beim Schreiben.

---

## 3 · Die Skills im Detail

### 3.1 `business-central` — Projektrahmen und Standard-Nachschlagewerk

```
business-central/
├── SKILL.md                            Rolle, Rangordnung, Einstieg
├── scripts/Baue-Ereignisindex.py       erzeugt den Ereignisindex aus dem Standard-Quelltext
└── references/
    ├── standard-nachschlagen.md        ⭐ Bedienung der Extrakte, Grenzen, Neuerzeugung
    ├── bc28-standard-datenmodell.txt   1.364 Tabellen · 23.370 Felder
    ├── bc28-objektinventar.txt         14.183 Standardobjekte nach Typ und ID
    ├── bc28-ereignisse.txt             23.629 Ereignis-Andockstellen mit Signatur
    ├── al-extension-development.md     Extension-Modell, IDs, Publishing, UI-Rechte
    ├── bc-api-integration.md           Standard-API, API-Pages, Automation-API
    ├── satellite-app-architecture.md   „ein BC-Hub, viele kleine Apps"
    └── construction-industry-example.md  Rollen → Apps → BC-Daten (Bau)
```

Formate der Extrakte: `Tabelle|Feld|SQL-Typ|Länge` · `Objekttyp|Objekt-ID` ·
`Objekt|Ereignis|Art|Datei|Zeile|Signatur`.

**Die drei Extrakte** — der wertvollste Teil des Pakets:

| Datei | Was drin ist | Woher | Grenze, die dazugehört |
|---|---|---|---|
| `bc28-standard-datenmodell.txt` | Jede Tabelle der Base Application mit jedem Feld, SQL-Typ und Länge | SQL `sys.columns` eines BC-28.3-Containers (AT-Lokalisierung, Demomandant CRONUS) | **FlowFields haben keine SQL-Spalte** und fehlen deshalb. Ein Null-Treffer auf einem FlowField ist kein Abwesenheitsbeweis. |
| `bc28-objektinventar.txt` | Jede Standard-Objekt-ID (< 50000) nach Typ | SQL `[Application Object Metadata]`, `COUNT(DISTINCT)` | Sagt **nichts** darüber, ob eine ID im **eigenen** Bereich frei ist — eigene IDs prüft man gegen Quelltext **und** Container. |
| `bc28-ereignisse.txt` | Jedes `IntegrationEvent`/`BusinessEvent`/`InternalEvent` mit Objekt, Datei, Zeile, Signatur | Python-Skript über den entpackten Standard-Quelltext (8.094 AL-Dateien) | Sagt, was **deklariert** ist — nicht, ob es im eigenen Ablauf auch **feuert**. Apps ohne Quelltext fehlen. |

**Die fünf Alltagsfragen**, jede ein Suchbefehl von einer Sekunde:

```bash
grep "^Sales Header|"              bc28-standard-datenmodell.txt   # 1 Welche Felder hat Tabelle X?
grep -i "|.*leistungszeitraum"     bc28-standard-datenmodell.txt   # 2 Gibt es ein Feld, das so heißt? (nichts = Beweis)
grep -i "unit of measure"          bc28-standard-datenmodell.txt   # 3 Wie heißt das Feld GENAU?
grep "^1|18$"                      bc28-objektinventar.txt         # 4 Ist Table 18 im Standard belegt?
grep -F ' "Purch.-Post"|' bc28-ereignisse.txt | grep '|OnAfter'   # 5 Woran kann ich mich hängen?
```

Die Zeile aus dem Ereignisindex ist **kopierfertig für das Abo** — der Objektname trägt seine
Anführungszeichen genau wie AL sie schreibt:

```
codeunit 90 "Purch.-Post"|OnAfterPostPurchaseDoc|IntegrationEvent|Purchases/Posting/PurchPost.Codeunit.al|8993|var PurchaseHeader: Record "Purchase Header"; ...
```

**Eichung statt Deutung.** Die Objekttyp-Nummern (1, 3, 5, 8 …) stehen roh in der Datenbank.
Vier davon wurden an einer echten Extension geeicht (Tabellen, Reports, Pages exakt, Codeunits
±1) und nur die vier tragen ein Etikett. Die übrigen Nummern bleiben bewusst ungedeutet.
*Eine geratene Zuordnung wäre schlimmer als keine.*

**Was das Nachschlagewerk nicht sieht** (und auch nicht so tut): Objektnamen von Pages, Codeunits
und Reports (das Metadaten-Blob ist binär), den AL-Quelltext des Standards, Prozedursignaturen
außerhalb von Ereignissen. Dafür bleiben Microsoft Learn, `Ctrl+Klick` in VS Code mit geladenen
Symbolen und der entpackte Quelltext.

### 3.2 `bc-al-cookbook` — die Technik-Kartei

**Quelle.** Erik Hougaard (hougaard.com) veröffentlicht zu seinen Business-Central-Videos die
Demo-Projekte auf GitHub (`hougaard/Youtube-Video-Sources`, 372 Ordner, 1.455 Dateien;
Ordnername = Videothema).

**Destillation, nicht Kopie.** Jedes der 254 Muster beschreibt in eigenen Worten den
Mechanismus, bringt eine gekürzte Code-Essenz, die **Fallstricke** und den Quellordner — und
eine **Praxis-Relevanz** von ●○○ bis ●●● (bewertet aus Sicht eines Bau-ERP-Projekts), nach der
die Themen je Datei sortiert sind.

**Die zwölf Themenbereiche:**

| Datei | Inhalt |
|---|---|
| `http-integration.md` | HttpClient, REST, OAuth2/S2S, Azure Functions/Blob, SharePoint, Webhooks, externe APIs |
| `json-xml-dateien.md` | JSON/JPath, große XML-Streams, CSV-Buffer, Excel-Buffer, Zip, Base64, E-Mail-Import |
| `events-erweiterbarkeit.md` | Integration Events, SingleInstance, Interfaces, Enum-Erweiterung, Upgrade-Codeunits |
| `ui-pages-dialoge.md` | Page-Typen, FactBoxes, Matrix, Dialoge, Progress, Pflichtfelder, Lookups, Styles |
| `controladdins-js.md` | ControlAddIn-Gerüst, JS↔AL, Charts, Kamera/GPS/Barcode, HTML-Rendering |
| `performance-tasks.md` | BulkInsert, Dictionary/List, TryFunction-Kosten, StartSession/TaskScheduler/Job Queue |
| `records-filter-queries.md` | Filtertricks, FilterGroups, FlowField-Filter, RecordRef, Duplikate, Query-Objekte |
| `reports-belege.md` | Report-Extensions, Request-Page, PDF drucken/kombinieren, Report als E-Mail, Excel-Report |
| `sicherheit-berechtigungen.md` | Permission-Sets aus AL, indirekte Rechte, IsolatedStorage, Passwörter, Change-Log-Grenzen |
| `stammdaten-validierung.md` | Validate-Ketten, Nummernserien, Datumsfallen, Dimensionen, Buchen aus Code |
| `defensive-al-fallen.md` | Sprachfallen (Case, Kurzschluss, Upperlimit), Transaktionen, ChangeCompany, Plattformgrenzen |
| `tooling-ki.md` | Telemetrie, Snapshot-Debugging, Sandbox-Hygiene, XLF-Übersetzung, Copilot-Anbindung |

**Die Belegkraft-Regel — der wichtigste Absatz des Cookbooks.** Eine Demo zeigt, **dass** etwas
in einem Beispiel funktioniert hat — nicht **warum**, und nicht, dass Microsoft es zusichert. Am
01.09.2026 wurde das Cookbook deshalb einer Mechanismus-Prüfung unterzogen: **22 widersprochene
Aussagen berichtigt, 8 Stellen als `UNBELEGT` markiert.** Ein Fall zeigt, warum das nötig war:
Die Behauptung, `%1` in `SetFilter` „escape" Sonderzeichen, stand im Cookbook — **aber nicht in
der Demo** (fünf Zeilen, kein Escaping) und nicht in der Microsoft-Doku. Sie war beim
Destillieren hinzugekommen. Seither gilt: *Für WIE man etwas baut — Cookbook. Für WAS die
Plattform zusichert — Herstellerdoku, immer.*

### 3.3 `business-central-development` — der korrigierte Leitfaden

Ein kompakter englischer AL-Leitfaden aus dem öffentlichen Repo *Mindrally/skills*
(Apache-2.0). Vier Aussagen waren **falsch für AL** und wurden gegen Microsoft Learn korrigiert:

| # | Upstream behauptete | Richtig ist | Beleg |
|---|---|---|---|
| 1 | „try-catch blocks" | AL hat kein try/catch — `[TryFunction]` (Rückgabewert auswerten!) oder `if not Codeunit.Run()`; **keine DB-Schreibzugriffe in TryFunctions** | MS Learn *Try methods*; On-Prem-Vorgabe `DisableWriteInsideTryFunctions` |
| 2 | `Confirm` ohne Vorbehalt | Jeder Dialog hinter `if GuiAllowed() then` — in Job Queue und Webservice wirft `Confirm` einen Fehler | MS Learn *Job queue* |
| 3 | „camelCase for private" | PascalCase durchgehend; 3 von 23.370 Standardfeldern beginnen klein | gemessen am Datenmodell-Extrakt |
| 4 | Page-Beispiel ohne `ApplicationArea` | Ohne `ApplicationArea` ist das Feld im SaaS-Client unsichtbar; Linter PTE0008/AS0062 | MS Learn *ApplicationArea* |

Die Änderungen stehen in `CHANGES.md`, das unveränderte Original liegt als
`UPSTREAM-ORIGINAL.md` daneben. ⚠ **Ein Update aus dem Upstream überschreibt die Korrekturen** —
nach einem solchen Update gegen das Original diffen und die Korrekturen neu einspielen.

### 3.4 Empfohlener Begleiter: `al-build` (nicht im Paket)

Build- und Test-Gate für AL-Projekte von Flemming Bakkensen (MIT,
`FBakkensen/bc-agentic-dev-tools-marketplace`). Nützlich u. a. `Wait-BCAppsSynced` (Sync-Barriere
nach dem Publish) und `Get-JUnitTestCounts` (Testzahlen nur aus JUnit-XML). ⚠ Vor dem Einsatz
lesen: `commit-bc-container.ps1` **löscht** nach dem Docker-Commit den Quellcontainer, und der
Containername wird aus dem Git-Branch abgeleitet. Installation:
`/plugin marketplace add FBakkensen/bc-agentic-dev-tools-marketplace`.

---

## 4 · Installation

Einen der drei Wege wählen — **nicht mehrere**, sonst liegen die Skills doppelt vor (Kapitel 8).

**Weg A — als Plugin (empfohlen; Updates per Befehl).** In einer Claude-Code-Sitzung:

```
/plugin marketplace add seifamiri36-prog/claude-bc-skills
/plugin install bc-skills@claude-bc-skills
```

Dasselbe im Terminal:

```bash
claude plugin marketplace add seifamiri36-prog/claude-bc-skills
claude plugin install bc-skills@claude-bc-skills
```

Die Skills heißen dann `bc-skills:business-central`, `bc-skills:bc-al-cookbook` und
`bc-skills:business-central-development`.

**Weg B — mit dem `skills`-CLI direkt in den Skill-Ordner** (kein Plugin, keine Namenspräfixe;
funktioniert auch für Cursor, Codex, OpenCode u. a. über `-a`):

```bash
npx skills add seifamiri36-prog/claude-bc-skills -g -a claude-code        # global
npx skills add seifamiri36-prog/claude-bc-skills -a claude-code           # nur dieses Projekt
npx skills add seifamiri36-prog/claude-bc-skills --skill bc-al-cookbook -g -a claude-code
```

**Weg C — von Hand:**

```bash
git clone https://github.com/seifamiri36-prog/claude-bc-skills
cp -r claude-bc-skills/skills/* ~/.claude/skills/
```

**Prüfen**, in einer *neuen* Sitzung:

```
/plugin list                      → bc-skills@claude-bc-skills … enabled   (nur Weg A)
/skills                           → die drei Skills erscheinen
Welche Felder hat "Job Task"?     → die Antwort nennt bc28-standard-datenmodell.txt als Quelle
```

---

## 5 · Tägliche Nutzung

Die Skills triggern **von selbst**, sobald Business Central, AL, OData, eine ERP-App oder eine
konkrete AL-Technik zur Sprache kommt. Niemand muss sie aufrufen. Typische Fragen:

```
Welche Felder hat "Sales Header" im Standard? Gibt es eines für den Leistungszeitraum?
Woran kann ich mich in "Purch.-Post" nach dem Buchen hängen? Mit Signatur bitte.
Ist Table 18 im Standard belegt?
Wie rufe ich aus AL eine REST-API mit OAuth2 Client Credentials auf — mit Fallstricken?
Wie lese ich ein Blob-Feld auf einer API-Page aus?
Entwirf eine Bauleiter-App, die Tagesrapporte in unser Business Central schreibt.
```

**Die Reihenfolge beim Planen** — der Skill allein reicht nicht, die Reihenfolge zählt. Wer ein
vorhandenes ERP anpasst, dessen teuerste Fehlerklasse ist nicht falscher Code, sondern *richtiger
Code an der falschen Stelle*:

1. `bc-al-cookbook` — Referenzdatei des Themas (Muster + Fallstricke)
2. Nachschlagewerk + entpackter Standard-Quelltext — den **Mechanismus** lesen, nicht das Feld raten
3. Microsoft Learn — offizielle Doku und Grenzen

**Die Nachschlagedateien gehen auch ohne Claude** — jeder Editor, jedes `grep`, jedes
`Select-String` (siehe 3.1).

---

## 6 · Rangordnung und Grenzen — welche Quelle wofür

| Frage | Verbindliche Quelle | Skill-Rolle |
|---|---|---|
| Was darf ich wie bauen? (Coderegeln des Teams) | `CLAUDE.md` / Arbeitsvereinbarung im eigenen Repo | nachrangig |
| Hat der Standard Feld/Tabelle X? | `bc28-standard-datenmodell.txt` (grep) | **maßgeblich** (Grenze: FlowFields) |
| Ist Standard-ID X belegt? | `bc28-objektinventar.txt` | **maßgeblich** für < 50000 |
| Ist **meine** ID X frei? | eigener Quelltext **und** Container | Skill **ungeeignet** |
| Woran andocken? | `bc28-ereignisse.txt`, dann den Quelltext lesen | maßgeblich für *deklariert*, nicht für *feuert* |
| Wie baut man Technik Y? | `bc-al-cookbook` | maßgeblich für *wie* |
| Sichert die Plattform Verhalten Z zu? | Microsoft Learn | Skill **nicht ausreichend** (Demo ≠ Zusicherung) |
| Was ist installiert / was läuft? | Container, Publish, Test, Klick | Skill sagt dazu nichts |

Die Extrakte zeigen **BC 28.3, AT-Lokalisierung, Stand August/September 2026**. Felder und
Ereignisse kommen und gehen zwischen Versionen — vor dem Bau gegen die installierte Version
gegenprüfen oder eigene Extrakte erzeugen (Kapitel 7).

---

## 7 · Pflege und Aktualisierung

**Updates holen.** Weg A: `/plugin marketplace update claude-bc-skills`. Weg B: den
`npx skills add`-Befehl erneut ausführen. Weg C: `git pull` und erneut kopieren.

**Eigene Extrakte für eine andere BC-Version oder Lokalisierung** (ca. 1 Stunde inkl. Prüfung).
Die Befehle stehen vollständig in `references/standard-nachschlagen.md`, Abschnitt „Neu erzeugen":

| Datei | Werkzeug | Prüfzahl danach |
|---|---|---|
| `bc28-standard-datenmodell.txt` | `docker exec <container> sqlcmd …` (SQL im Dokument; Fallstricke: `-s'|'`, `-h -1`; Basis-App-GUID und Mandantenpräfix anpassen) | `grep "^Sales Header|"` liefert Treffer |
| `bc28-objektinventar.txt` | SQL `COUNT(DISTINCT [Object ID])` — ⚠ nicht Zeilen zählen (Fassungen ≠ Objekte) | Eichung: Typ 1/3/5/8 gegen eigene `*.Table.al` usw. |
| `bc28-ereignisse.txt` | `python scripts/Baue-Ereignisindex.py <Quelltext-Ordner>` | **„Indexzeilen OHNE Objektnamen: 0"** — sonst Index unbrauchbar |

Nach der Neuerzeugung: Datum und Zahlen in den Dateiköpfen, in `SKILL.md` und in
`standard-nachschlagen.md` nachziehen. Extrakte für andere Versionen sind als Beitrag willkommen.

**`business-central-development` nach einem Upstream-Update.** `diff SKILL.md UPSTREAM-ORIGINAL.md`
— fehlen die vier Korrekturen (3.3), neu einspielen.

**Beiträge.** Widerlegte Aussagen, neue Fallstricke, andere Lokalisierungen: Issue oder Pull
Request. Regel aus dem Cookbook: **Korrektur mit Datum und Beleg** (Demo-Ordner,
Microsoft-Learn-Seite oder Messung), nicht nur mit Meinung.

---

## 8 · Störungen und bekannte Fallen

| Symptom | Ursache | Abhilfe |
|---|---|---|
| Skill triggert nicht | Sitzung wurde vor der Installation gestartet; oder Plugin deaktiviert | Neue Sitzung; `/plugin list` prüfen; `/reload-plugins` |
| Skills erscheinen doppelt (`business-central` und `bc-skills:business-central`) | Weg A **und** Weg B/C benutzt | Einen Weg entfernen (`/plugin uninstall …` oder Ordner aus `~/.claude/skills` löschen) |
| `grep "^1|18$"` findet nichts, obwohl die Zeile da ist | Datei mit CRLF-Zeilenenden (`$` trifft vor `\r` nicht) | Repo liefert LF (`.gitattributes`); bei Handkopien: `dos2unix` oder `-replace "`r`n","`n"` |
| `Invalid column name` bei einer SQL-Messung, obwohl der Feldname stimmt | Erweiterungsfelder liegen in der `$ext`-Begleittabelle; FlowFields haben keine Spalte | Spaltennamen aus `sys.columns` holen, nicht aus dem AL-Quelltext ableiten |
| Eigene ID laut Inventar „frei", Publish meldet Kollision | Das Inventar enthält nur Standard-IDs und ist ein Schnappschuss | Eigene IDs **nur** gegen Quelltext und Container prüfen |
| Korrekturen in einem Skill sind nach einem Update verschwunden | Upstream-Update hat die Datei überschrieben | Nur aus **diesem** Repo installieren; bei `business-central-development` gegen `UPSTREAM-ORIGINAL.md` diffen |
| Ereignisindex nach Neuerzeugung leer oder voller Zeilen ohne Objektnamen | Quelltext-Ordner leer, oder Objektkopf nicht erkannt | Standard neu entpacken; Selbstprüfung des Skripts lesen (muss 0 melden) |

---

## 9 · Sicherheit, Datenschutz, Lizenz

**Was in den Skills steht — und was nicht.** Keine Kundendaten, keine Passwörter, keine
Produktivdaten. Die Extrakte sind **Metadaten des Microsoft-Standards** (Namen, Typen, Längen,
IDs, Signaturen) aus einem Demomandanten (CRONUS). Beispielcode stammt aus öffentlichen Demos
oder ist neutralisiert.

**Lizenzlage:**

| Teil | Quelle | Lage |
|---|---|---|
| Eigene Texte, Messungen, Skripte | Seif Amiri | MIT (`LICENSE`) |
| `bc-al-cookbook` | Hougaard, `Youtube-Video-Sources` | Quell-Repo ohne explizite Lizenz. Die Destillation ist eigene Formulierung mit gekürzten, umgeschriebenen Code-Essenzen und Attribution; die Demos selbst werden nicht weitergegeben |
| `business-central-development` | Mindrally/skills | Apache-2.0: Fork erlaubt, Änderungen dokumentiert (`CHANGES.md`), Lizenztext liegt bei |
| `bc28-*.txt` | Microsoft BC 28.3 (Metadaten) | Namen/Typen/Signaturen sind die öffentliche Erweiterungsschnittstelle, die Microsoft über Symbole und Learn bereitstellt; **kein Quellcode** enthalten. Dieses Repo steht in keiner Verbindung zu Microsoft |

Details: `NOTICE.md`.

---

## 10 · Kennzahlen und Dateiinventar (Stand 09.10.2026)

| Kennzahl | Wert |
|---|---|
| BC-Version der Extrakte | 28.3 (AT-Lokalisierung) |
| Standardtabellen / Felder | 1.364 / 23.370 (04.08.2026) |
| Standardobjekte im Inventar | 14.183 (04.08.2026) |
| Ereignis-Andockstellen | 23.629 aus 8.094 AL-Dateien (02.09.2026) |
| Cookbook-Muster / Themenbereiche | 254 / 12 (aus 372 Demo-Ordnern, 1.455 Dateien) |
| Berichtigungen bei der Mechanismus-Prüfung | 22 + 8 UNBELEGT-Marken (01.09.2026) |
| Korrekturen am Fremd-Leitfaden | 4 (18.08.2026) |
| Paketgröße | ~7,5 MB |

```
claude-bc-skills/
├── HANDBUCH.md / .pdf                       dieses Dokument
├── README.md                                Kurzfassung + Installation (DE/EN)
├── LICENSE · NOTICE.md                      MIT, Drittquellen
├── .claude-plugin/marketplace.json          Marketplace-Manifest (Plugin-Quelle: ./)
├── .claude-plugin/plugin.json               Plugin-Manifest
└── skills/
    ├── business-central/                    SKILL.md, references/, scripts/
    ├── bc-al-cookbook/                      SKILL.md, references/ (12 Dateien)
    └── business-central-development/        SKILL.md, CHANGES.md, UPSTREAM-ORIGINAL.md, Apache-2.0
```

---

## 11 · Glossar

| Begriff | Bedeutung |
|---|---|
| **AL** | Programmiersprache für Business-Central-Erweiterungen |
| **Base Application** | Microsofts Standard-Anwendung in BC (Tabellen, Seiten, Buchungslogik) |
| **BC** | Microsoft Dynamics 365 Business Central (ERP) |
| **Claude Code** | KI-Entwicklungsassistent von Anthropic, arbeitet im Projektordner |
| **Container** | lokaler Docker-Container mit BC, gegen den gebaut und getestet wird |
| **Extension** | eigenständiges AL-Paket, das BC erweitert, ohne den Standard zu verändern |
| **Extrakt** | aus Container oder Quelltext erzeugte Textdatei zum Nachschlagen (Felder, Objekte, Ereignisse) |
| **FlowField** | berechnetes Feld ohne eigene Datenbankspalte — unsichtbar für SQL-Extrakte |
| **Integration Event** | von Microsoft vorgesehene Andockstelle, an die eine Extension eigene Logik hängt |
| **Marketplace** | Katalog, aus dem Claude Code Plugins installiert — hier: ein GitHub-Repo mit Manifest |
| **Objekt-ID** | Nummer jedes AL-Objekts; Standard < 50000, eigene Bereiche laut `app.json` |
| **Plugin** | installierbares Paket für Claude Code; kann Skills enthalten |
| **Skill** | Ordner mit `SKILL.md` und Referenzdateien, den Claude Code themenabhängig lädt |

---

## Anhang · Änderungsprotokoll

| Version | Datum | Änderung |
|---|---|---|
| 1.0.1 | 09.10.2026 | Handbuch (dieses Dokument) ergänzt |
| 1.0.0 | 09.10.2026 | Erste Fassung: drei Skills, README, NOTICE, Marketplace-Manifest |
