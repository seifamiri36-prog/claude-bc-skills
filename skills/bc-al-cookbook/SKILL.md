---
name: bc-al-cookbook
description: Nachschlagewerk mit destillierten AL-Code-Mustern aus ~350 Business-Central-Video-Demos (Erik Hougaards Youtube-Video-Sources). Nutze diesen Skill IMMER, wenn in AL/Business Central eine konkrete Technik gebraucht wird und die Frage „wie macht man X in AL?" lautet — z. B. HttpClient/REST/OAuth-Aufrufe, JSON/XML/CSV/Excel parsen oder erzeugen, Integration Events/Interfaces/Enums, ControlAddIns mit JavaScript (Charts, Kamera, Barcode, HTML-Rendering), Hintergrund-Tasks (StartSession, Job Queue, TaskScheduler), Performance-Muster (BulkInsert, Dictionary vs. List, TryFunction-Kosten), Filter/FlowFields/Queries, Report- und PDF-Tricks, Berechtigungen/IsolatedStorage/Passwörter, Dialoge/Progress/UX-Kniffe oder Validierungs- und Buchungsmuster. Auch nutzen, BEVOR etwas „von Hand" erfunden wird, das wie ein Standardproblem klingt — hier liegt sehr wahrscheinlich schon ein erprobtes Muster samt Fallstricken. Ergänzt die Skills business-central (Projekt-/Architekturwissen) und al-build (Bauen/Testen); dieser hier ist die Technik-Kartei.
---

# BC-AL-Cookbook — destillierte Muster aus Hougaards Video-Quellen

Quelle: Erik Hougaards öffentliches GitHub-Repo „Youtube-Video-Sources" — je Ordner
ein Demo-Projekt zu einem AL/BC-Thema, von NAV-2018-Zeiten bis BC 26. Die Muster
hier sind **destilliert** (Mechanismus + Fallstricke), nicht kopiert. Attribution:
Erik Hougaard (hougaard.com); nur als internes Nachschlagewerk verwenden.

> **Pflege:** Dieses Nachschlagewerk wird über sein GitHub-Repo gepflegt (Issues und Pull
> Requests willkommen). Wer eine Aussage widerlegt, korrigiert sie **mit Datum und Beleg** —
> siehe die Belegkraft-Regel unten. Stand der Mechanismus-Prüfung: 01.09.2026
> (22 Berichtigungen widersprochener Aussagen, 8 gezielte UNBELEGT-Marken).

## ⚠ Belegkraft: was dieser Skill ist — und was er NICHT ist

> **Jede Aussage hier stammt aus einer DEMO, nicht aus der Herstellerdoku.**
> Sie zeigt, **dass** etwas in einem Beispiel funktioniert hat — nicht, **warum**, und nicht,
> dass Microsoft es zusichert.
>
> ⚠⚠ **Und die härtere Möglichkeit, belegt am 01.09.2026:** Eine Aussage kann **auch in der
> Demo nicht stehen.** Die `%1`-Escaping-Behauptung in `records-filter-queries` war **beim
> Destillieren erfunden** — die Demo (fünf Zeilen) führt kein Escaping vor und erwähnt es
> nicht. **Nicht die Quelle ging zu weit; die Destillation hat etwas hinzugefügt.**
> **Deshalb gilt: Bei einer Aussage, auf die etwas gebaut wird, nicht nur die Herstellerdoku
> prüfen, sondern auch die QUELLDEMO** — sie liegt vollständig unter
> `<Ordner>` im Hougaard-Repo und ist meist wenige Zeilen
> lang. **Eine erfundene Erklärung sieht wie das Original aus.**

**Zwei belegte Fälle, in denen genau das schadete** *(beide aus einem realen Bau-ERP-Projekt, 31.08./01.09.2026)*:

```
1  Eine Projektregel verlangte "IsHandled ueberall", weil der Standard es 653-mal tut.
   Microsoft Learn nennt das Muster "low quality / last resort".
   -> Aus HAEUFIGKEIT im Bestand wurde faelschlich eine EMPFEHLUNG.

2  Dieser Skill behauptete (records-filter-queries), "%1" ESCAPE Sonderzeichen.
   In der MS-Doku zu SetFilter steht davon NICHTS - nur "insert values at
   run-time" und "data type of Value must match".
   -> Eine Demo-Beobachtung stand da als Plattform-Eigenschaft.
```

**Daraus die Nutzungsregel, und sie kostet je Fall eine Minute:**

1. **Für WIE man etwas baut** — Skill nehmen, er ist dafür gemacht.
2. ⚠ **Für WAS die Plattform zusichert** — **Herstellerdoku**, immer. Besonders bevor eine
   Aussage in eine **Regel**, eine **Auflage** oder einen **Kommentar am Code** wandert.
3. **Wer hier eine Verhaltensbehauptung findet und sie braucht**, schreibt beim Übernehmen
   dazu, **woher sie stammt** — *„Demo"* oder *„MS-Doku, geprüft am …"*. **Der Unterschied ist
   nicht Pedanterie: Eine Regel mit richtigem Ziel und unbelegter Begründung fällt, sobald
   jemand die Begründung prüft — und nimmt das richtige Ziel mit.**

## So benutzt du diesen Skill

1. **Thema einordnen** → passende Referenzdatei aus der Tabelle unten lesen.
2. **Muster übernehmen und anpassen** — die Snippets sind die Essenz, kein
   Copy-Paste-Fertigcode. Objekt-IDs/Namespaces ans Zielprojekt anpassen
   (eigener ID-Bereich laut `app.json`, eigenes Präfix, eigene Projektstruktur).
3. **Bei Detailfragen den Original-Fundus greppen** — die vollständigen Quellen
   liegen öffentlich unter https://github.com/hougaard/Youtube-Video-Sources
   (lokal klonen; 1.455 Quelldateien, grep-bar; Ordnername = Videothema). Die BC-Version eines
   Demos steht in dessen `app.json` unter `runtime`/`application` — Muster aus
   alten Ordnern vor Übernahme gegen den heutigen Standard prüfen.
4. **Projektregeln schlagen Muster:** steht in der `CLAUDE.md` deines Projekts eine Regel,
   die einem Muster hier widerspricht (z. B. keine DB-Writes in TryFunctions, FlowFields
   vor dem Lesen `CalcFields`), gilt die Projektregel.

## Referenzdateien (references/)

| Datei | Inhalt — wann lesen |
|---|---|
| `http-integration.md` | HttpClient, REST, OAuth2/S2S, Azure Functions/Blob, SharePoint, Webhooks/Power Automate, Webscraping, externe APIs |
| `json-xml-dateien.md` | JSON lesen/schreiben/JPath, große XML-Streams, CSV-Buffer, Excel-Buffer, Zip, Base64, E-Mail-Import |
| `events-erweiterbarkeit.md` | Integration Events, isolierte/SingleInstance-Events, Interfaces, Enum-Erweiterung, Preprocessor, Namespaces, Upgrade-Codeunits |
| `ui-pages-dialoge.md` | Page-Typen, FactBoxes, Matrix/Tree, Dialoge, Progress, Pflichtfelder, Lookups, Styles, Fokus/Shortcuts |
| `controladdins-js.md` | ControlAddIn-Gerüst, JS↔AL-Kommunikation, Charts, Kamera/GPS/Barcode, HTML-Rendering, Höhen-Hacks |
| `performance-tasks.md` | BulkInsert, Dictionary/List, TryFunction-Kosten, StartSession/TaskScheduler/Job Queue, temporäre Tabellen, Variants |
| `records-filter-queries.md` | Filtertricks, FilterGroups, FlowField-Filter-Syntax, RecordRef, Duplikatsuche, Fuzzy-Vergleich, Query-Objekte, virtuelle Tabellen |
| `reports-belege.md` | Report-Extensions, Request-Page-Tricks, PDF drucken/kombinieren, Report als E-Mail-Body, Excel-Report, Headlines |
| `sicherheit-berechtigungen.md` | Permission-Sets aus AL, indirekte Rechte, IsolatedStorage, Passwort-Handling, Change-Log-Grenzen, Ransomware-LEHREN (defensiv) |
| `stammdaten-validierung.md` | Validate-Ketten, Nummernserien, Datums-/Format-Fallen, Dimensionen, ins Hauptbuch buchen aus Code, Config Packages |
| `defensive-al-fallen.md` | Sprach-Fallen (Case, Kurzschluss, Upperlimit), Transaktionen, ChangeCompany, robuste Fehlerbehandlung, versteckte Plattform-Grenzen |
| `tooling-ki.md` | Telemetrie, Snapshots-Debugging, Umgebungs-Info, Sandbox-Hygiene, Übersetzung (XLF), Copilot/KI-Anbindung, Designer |

Jede Referenzdatei nennt je Muster den **Quellordner** — bei Zweifeln dort die
vollständige Demo lesen statt raten.
