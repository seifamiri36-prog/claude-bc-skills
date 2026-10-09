# AL-Extension-Entwicklung

Business Central wird nicht direkt verändert, sondern über **Extensions** erweitert — eigenständige Pakete aus AL-Objekten, die installiert/deinstalliert werden können, ohne den BC-Standardcode anzufassen.

## Projektstruktur

Ein typisches AL-Projekt (angelegt in VS Code mit der "AL Language"-Extension von Microsoft):

```
mein-projekt/
├── app.json              # App-Manifest: ID, Name, Publisher, Version, Abhängigkeiten, Objekt-ID-Range
├── .vscode/
│   └── launch.json       # Verbindung zum BC-Sandbox-Container / BC-Online-Sandbox
├── src/
│   ├── Tables/
│   ├── TableExtensions/
│   ├── Pages/
│   ├── PageExtensions/
│   ├── Codeunits/
│   ├── Enums/
│   ├── Reports/
│   ├── Queries/
│   └── PermissionSets/
└── Translations/
    └── de-AT.xlf          # Übersetzungsdatei je Zielsprache
```

`app.json` ist das Herzstück — u. a.:
- `id`: eindeutige GUID der Extension
- `idRange`: der reservierte Objekt-ID-Bereich (z. B. `[70000000, 70099999]` bei AppSource-Apps oder ein projektintern abgestimmter Bereich bei On-Prem-Extensions)
- `dependencies`: andere Extensions, auf denen aufgebaut wird
- `application`/`platform`: Mindest-BC-Version

## Objekt-ID-Ranges — der klassische Anfängerfehler

Jedes AL-Objekt (Table, Page, Codeunit, …) braucht eine numerische ID **innerhalb des in `app.json` reservierten Bereichs**. Zwei Extensions mit überlappenden Ranges kollidieren beim gemeinsamen Deployment. Vor Projektstart klären:
- Ist es eine AppSource-App (Microsoft vergibt den Range) oder eine Extension pro Kunde (Range wird selbst gewählt/dokumentiert)?
- Gibt es beim Kunden bereits andere Extensions, deren Ranges zu respektieren sind?

## Die wichtigsten Objekttypen

| Objekttyp | Zweck |
|---|---|
| `table` | Neue Datenstruktur |
| `tableextension` | Felder an ein Standard-Table anhängen (z. B. `Customer`) |
| `page` | Neue UI (Card, List, Worksheet, …) |
| `pageextension` | Standard-UI erweitern (neue Felder/Actions auf einer bestehenden Page) |
| `codeunit` | Geschäftslogik, Event-Subscriber, Prozeduren |
| `enum` / `enumextension` | Aufzählungstypen bzw. deren Erweiterung |
| `permissionset` | Berechtigungen, die die Extension mitbringt — nicht vergessen, sonst können Nutzer die neuen Objekte nicht sehen |
| `query` | Read-only-Datenzugriff über mehrere Tabellen, oft Basis für Reports/APIs |
| `report` | Auswertungen/Dokumente |
| `xmlport` | Im/Export strukturierter Daten (seltener bei neuen Projekten, meist durch API ersetzt) |

Faustregel: **`*extension`-Objekte statt Kopieren/Verändern von Standardobjekten** — das ist der ganze Sinn des Extension-Modells und hält Updates von Microsoft kompatibel.

## Events statt Codeänderung

Wo möglich, Geschäftslogik über **Event-Subscriber** (`[EventSubscriber(...)]`) an Standard-Events von BC andocken, statt Standardcode zu verändern (der ohnehin nicht direkt änderbar ist). Das ist der AL-typische Weg, "in" bestehende Prozesse einzuhaken.

## Publishing & Testen

**Der Lehrbuchweg ist `F5`/`Ctrl+F5` aus VS Code.** Er setzt voraus, dass genau eine Person
mit genau einem Arbeitsbaum gegen genau eine Umgebung baut. **Sobald das nicht mehr stimmt,
trägt er nicht** — etwa wenn mehrere Sessions oder Arbeitsbäume einen Container teilen.

### So lief es in einem Mehrbenutzer-Projekt (ein Container, mehrere Sessions)

```powershell
pwsh -File bc-extension/compile.ps1        # Produkt-App - containerlos gegen gecachte Symbole
pwsh -File bc-extension-test/compile.ps1   # Test-App - Produkt ZUERST bauen
```

```powershell
Publish-BcContainerApp -containerName <container> -appFile "<pfad zur .app>" `
                       -skipVerification -sync -install -upgrade
```

⚠ **Warum nicht `alc.exe` von Hand und nicht `F5`:** ein eigenes `compile.ps1` regelt den **Symbolcache
je Arbeitsbaum**. Geteilte Ausgabeordner haben dort zweimal *fremde* Symbole untergeschoben —
der Build war dann sauber und gehörte jemand anderem.

⚠ **`docker cp` funktioniert bei Hyper-V-Isolation NICHT.** Der Weg in den Container führt
ausschließlich über `Publish-BcContainerApp`.

### Drei Regeln, die je einen Schaden hinter sich haben

```
1  SPERRE + VERSIONSTAG VOR dem Publish.
   Ablauf: eine schriftliche Sperr-Vereinbarung im Repo. Parallele Sessions teilen EINEN
   Container - wer ohne Sperre published, ueberschreibt einen fremden Testlauf.

2  VERSIONSBUMP in DENSELBEN Commit wie die AL-Aenderung.
   Sonst belegt eine gleiche Versionsnummer nichts mehr: zwei verschiedene Staende
   tragen dieselbe Zahl, und ab da ist nicht mehr entscheidbar, was installiert ist.

3  EIN Publish beendet ALLE offenen Web-Client-Sitzungen.
   Deshalb: erst ALLES bauen und publishen, dann EINMAL anmelden, dann am Stueck
   testen. Wer zwischendrin published, testet danach in einer toten Sitzung -
   und eine tote Sitzung raeumt den Bildschirm nicht ab, sie zeigt alte Werte.
```

⚠ **Vor dem Compile `git status` lesen.** Fremde Änderungen im Baum heißen: **der Build ist
nicht deiner.**

### Und was der Compiler NICHT meldet

- Ein falscher `LayoutFile`-Pfad wird **nicht** als Fehler gemeldet — der Compiler packt still
  ein leeres Gerüst ein. Gegenmittel: `-GenerateReportLayout No` erzwingt den Fehler.
- **„Kompiliert sauber“ ist kein Beleg für Verhalten.** In der Praxis sind mehrfach echte
  Fehler durchgerutscht, weil sauberes Kompilieren als Nachweis behandelt wurde.
  Oberflächenänderungen gelten erst als erledigt, wenn sie **angeklickt** wurden.

### Wenn du allein gegen eine Umgebung baust

Dann gilt oben der Lehrbuchweg (`BcContainerHelper` für den lokalen Container, BC-Online-Sandbox
aus dem Admin Center, `launch.json` + `F5`). **Kläre aber zuerst, ob mehrere Leute denselben
Container benutzen** — danach entscheidet sich, ob `F5` reicht oder ob es eine Sperre braucht.

## Übersetzung

Alle Label-Texte in AL werden über `Caption`/`Label`-Properties definiert; die tatsächlichen Übersetzungen liegen in `.xlf`-Dateien (eine je Zielsprache, generiert aus dem Projekt). Bei Kundenprojekten mit mehreren Sprachen (z. B. DE/EN in Österreich) das früh mitplanen, nicht am Ende nachziehen.

## Typische Stolperfallen

- Objekt-ID-Range nicht vorab reserviert → Kollisionen beim Zusammenspiel mehrerer Extensions.
- Permission Sets vergessen → Feature ist im Code fertig, aber für Nutzer unsichtbar.
- Direktes Ändern von Standardobjekten statt `*extension` → bricht bei jedem BC-Update.
- Business-Logik nur in der Page statt im Codeunit → nicht wiederverwendbar, nicht API-tauglich (siehe `bc-api-integration.md` — APIs sprechen i. d. R. mit Codeunits/Queries, nicht mit UI-Pages).

## Nachtrag 06.09.2026 — Berechtigungen an der OBERFLÄCHE: was das Attribut kann und was nicht

Gemessen an BC 28.3 (Base App, entpackter Quelltext, 8.094 AL-Dateien) und MS Learn
(`UIElementRemovalOption`).
Geltungsbereich: Base Application; andere Module nicht gezählt.

- **`AccessByPermission` nimmt GENAU EIN Objekt** — keine Komma-Liste. 2.127 Vorkommen im
  Standard, 10 davon mit Komma, alle der Form `System "Tools…"` (Systemrechte, keine
  tabledata-Listen). Folge: eine Kachel/ein Part, der beim Aufbau SIEBEN Tabellen liest, lässt
  sich mit dem Attribut nur als Stichprobe absichern. Der Standard tut stattdessen: **`ReadPermission`
  an der LESESTELLE, gibt 0 zurück statt zu scheitern** (`SalesCue.Table.al:402`,
  `ActivitiesMgt:287`) — und zwar an JEDER gelesenen Tabelle.
- **`DrillDownPageId` braucht kein `AccessByPermission`** (0 von 634 im Standard). Ein
  `AccessByPermission` am FlowField ist ein Lizenz-/Modulmarker, kein Leserechts-Wachposten
  (nur 2 von 98 nennen die CalcFormula-Quelle).
- **Aktionen mit `RunObject` auf ein Standardobjekt tragen `AccessByPermission` auf dessen
  Haupttabelle** (Standardmuster); für `Page.Run(Page::…)` aus Code gibt es das nicht — dort
  ist `ReadPermission` an der Aufrufstelle das Gegenstück.
- **`ApplicationArea` versteckt lautlos, sie blockiert nicht** — eine Aktion mit `All` auf eine
  Seite mit engerer Area öffnet bei abgeschaltetem Bereich eine spaltenlose Seite ohne Fehler.
- **Server-Schalter `UIElementRemovalOption`** (Vorgabe `LicenseFileAndUserPermissions`,
  *Dynamically updatable: No* → Dienstneustart): `AccessByPermission` wirkt nur unter
  `LicenseFile` oder `LicenseFileAndUserPermissions`. UI-Elemente mit `TableRelation`/`CalcFormula`
  werden AUTOMATISCH entfernt. ⚠ Die CRONUS-Demo-Rechtesätze lassen sich laut MS Learn meist
  NICHT so mit FOUNDATION kombinieren, dass die Entfernung vollständig greift — ein Klicktest mit
  Demo-Sätzen belegt das Feature nicht.
- **Prüfform vor dem Bau** (Projektregel): *Wer darf das lesen?* UND *Wie kommt der Anwender
  hin?* — Erreichbarkeit wird am SEITENAUFBAU gemessen, nicht an der Prozedur.

### Nachtrag 24.09.2026 — NotBlank ist keine Datensperre

MS Learn (NotBlank Property): «If a field is updated through application code, then the NotBlank property is not validated» — die Prüfung läuft nur bei Eingabe über die UI. An einem Feld mit `Editable = false` auf Tabellenebene kann NotBlank darum NIE greifen, und Code-Zuweisungen, Konfigurationspakete und RecordRef umgehen es immer. Beleg im Standard: `JobTask.Table.al` trägt NotBlank an «Job Task No.» — und wer die Aufgabe aus Code anlegt, prüft `Nr = ''` trotzdem selbst (eigene Prüfung in der anlegenden Codeunit). Datensperre heißt: TestField/Error im Trigger oder am Verbraucher, nie eine UI-Eigenschaft.
