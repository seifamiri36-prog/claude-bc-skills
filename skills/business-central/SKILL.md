---
name: business-central
description: Guidance for Microsoft Dynamics 365 Business Central (BC) ERP projects — AL-language extension development on the BC backend, and designing small role- or process-specific companion apps (mobile & desktop) that talk to BC via its APIs. Ships grep-able extracts of the BC 28 standard (1,364 tables / 23,370 fields, 14,183 standard object IDs, 23,629 event hooks) so standard table, field and event names are LOOKED UP instead of guessed. Use this whenever Business Central, BC, Dynamics 365 BC, AL language/extension, BC API/OData, or a Microsoft ERP integration comes up — and also whenever the user describes building a focused app that connects to an ERP backend for one role or workflow (e.g. "Baustellen-App", "Lager-App fürs ERP", "App für den Einkauf, die mit unserem Business Central spricht"), even if they never say "Business Central" or "AL" explicitly. Push to consult this skill for any ERP-adjacent app idea before assuming it's a generic web project.
---

# Business Central (BC) & AL-Entwicklung

Diese Skill hat zwei Aufgaben:

```
1  STANDARD-NACHSCHLAGEWERK   was BC von Haus aus hat - Tabellen, Felder, Objekt-IDs,
                             Ereignis-Andockstellen. Das ist der wertvollste Teil.
2  ONBOARDING + ARCHITEKTUR   wer neu auf BC/AL trifft, liest hier den Rahmen:
                             Extension-Modell, API-Anbindung, Satelliten-Apps.
```

⚠ **Projektregeln gewinnen.** Hat dein Projekt eine `CLAUDE.md` oder eine Arbeitsvereinbarung,
gilt sie bei jedem Widerspruch vor dieser Skill — sie kennt die Schadensfälle deines Projekts,
diese Skill nicht.

Sie deckt zwei zusammenhängende, aber unterschiedliche Arbeitsbereiche ab:

1. **Backend-Ebene**: Erweiterungen von Business Central selbst, geschrieben in AL.
2. **Frontend-Ebene**: kleine, rollen- oder prozessspezifische Satelliten-Apps (mobil & Desktop), die über APIs mit BC sprechen — statt einer einzigen monolithischen App für alles.

Der Kerngedanke: **ein BC-Backend, viele kleine fokussierte Apps**, jede zugeschnitten auf genau eine Rolle oder einen Prozess (z. B. Bauleiter, Einkauf, Lager), die automatisiert BC-Daten liefert und BC-Prozesse anstößt. Halte dieses Zielbild im Kopf, auch wenn eine einzelne Aufgabe nur einen Ausschnitt betrifft.

## Wie du an ein BC-Projekt herangehst

1. **Klären, auf welcher Ebene die Aufgabe liegt** — Backend (AL-Extension direkt in BC) oder Frontend (Satelliten-App gegen BC-APIs) oder beides. Das bestimmt, welche Referenzdatei relevant ist.
2. **BC-Version/Umgebung erfragen, statt zu raten** — On-Premises/Container vs. BC Online/SaaS, welche Ranges für Objekt-IDs bereits vergeben sind, welche BC-Version (Feature-Set ändert sich laufend). Bei Unsicherheit auf Microsoft Learn verweisen statt zu raten (siehe unten).
3. **Bei Satelliten-Apps: erst die Rolle/den Prozess scharf schneiden**, bevor Code entsteht. Eine App = ein Job-to-be-done. Siehe `references/satellite-app-architecture.md`.
4. **Bau-Branche als Referenzmuster, nicht als Vorgabe** — die Beispiele stammen aus einem realen Bau-ERP-Projekt. Übertrage das Muster (Rolle → App → BC-Daten/Aktionen) auf andere Branchen.

## Referenzdateien

Lies die passende Datei bei Bedarf — nicht alle auf einmal:

| Datei | Wann lesen |
|---|---|
| `references/al-extension-development.md` | Beim Anlegen/Ändern einer AL-Extension: Projektstruktur, Objekt-IDs, Objekttypen, Publishing (auch Mehrbenutzer-Container), Übersetzung, Berechtigungen an der Oberfläche |
| `references/bc-api-integration.md` | Wenn eine App/ein Service BC-Daten lesen oder BC-Prozesse per API auslösen soll — lokaler Container UND BC Online, inkl. Automation-API |
| `references/satellite-app-architecture.md` | Beim Entwurf der "Hub + kleine Apps"-Architektur, Rollenschnitt, Tech-Stack-Optionen |
| `references/construction-industry-example.md` | Konkretes Referenzbeispiel Bau-Branche — welche Rollen, welche Apps, welche BC-Daten |
| **`references/standard-nachschlagen.md`** | **Immer, sobald ein Standard-Tabellen-, Feld- oder Ereignisname vorkommt.** Sagt, wie man ihn in einer Sekunde belegt statt ihn zu raten |

> ### ⚑ Standard-Feldnamen werden nachgeschlagen, nicht erinnert
>
> Daneben liegen drei erzeugte Nachschlagedateien aus einem echten BC-28.3-Container (AT-Lokalisierung):
>
> ```
> references/bc28-standard-datenmodell.txt   1.364 Standardtabellen · 23.370 Felder
> references/bc28-objektinventar.txt         14.183 Standardobjekte nach Typ und ID
> references/bc28-ereignisse.txt             23.629 Ereignis-Andockstellen mit Signatur
> ```
>
> **Jede Frage der Art „welche Felder hat X", „gibt es ein Feld für Y" oder „woran kann ich mich hängen" ist damit ein `grep`:**
>
> ```bash
> grep "^Sales Header|" references/bc28-standard-datenmodell.txt
> grep -i "|.*leistungszeitraum" references/bc28-standard-datenmodell.txt   # nichts -> Beweis
> grep -F ' "Purch.-Post"|' references/bc28-ereignisse.txt | grep '|OnAfter'
> ```
>
> **Ein Feldname aus dem Gedächtnis ist eine Vermutung.** Der `grep` kostet eine Sekunde und
> liefert einen Beleg — Bedienung, Grenzen und Neuerzeugung stehen in
> `references/standard-nachschlagen.md`. ⚠ Die Extrakte zeigen den Stand EINER Version (28.3);
> vor dem Bau gegen die installierte Version gegenprüfen.

## Kurzüberblick AL-Extension-Entwicklung

- Jede AL-Extension ist ein eigenständiges VS-Code-Projekt mit `app.json` (App-ID, Name, Publisher, Version, Abhängigkeiten, **Objekt-ID-Range**).
- BC-Objekte (Table, Page, Codeunit, Enum, Report, Query, Permission Set, …) werden als `.al`-Dateien angelegt bzw. als `tableextension`/`pageextension` an Standardobjekte angehängt.
- Der Objekt-ID-Range in `app.json` muss vorab mit dem Kunden/AppSource-Prozess abgestimmt sein — Kollisionen mit anderen Extensions sind der klassische Anfängerfehler.
- Veröffentlichung/Testen erfolgt gegen einen BC-Sandbox-Container oder eine BC-Online-Sandbox. **F5/Ctrl+F5 aus VS Code ist der Lehrbuchweg — er trägt nur, solange eine Person mit einem Arbeitsbaum gegen eine Umgebung baut**; für geteilte Container siehe `references/al-extension-development.md`.
- Mehrsprachigkeit läuft über `.xlf`-Übersetzungsdateien, nicht über Hardcoded-Strings.

Details, Beispielstruktur und typische Stolperfallen: `references/al-extension-development.md`.

## Kurzüberblick BC-API-Integration

Business Central ist von Haus aus API-first aufgebaut — das ist die Grundlage für die Satelliten-App-Idee:

- **Standard-API v2.0** (OData v4) liefert Kernentitäten (Kunden, Verkaufsaufträge, Artikel, …) unter einem festen Endpunkt-Schema, ohne dass dafür AL-Code nötig ist.
- **Custom API-Pages** (`APIPage`-Objekte in AL) exponieren eigene/erweiterte Entitäten und eigene Aktionen (z. B. "Rapport abschließen" als aufrufbare Action), wenn die Standard-API nicht reicht.
- **Auth**: BC Online über Microsoft Entra ID (OAuth2); lokaler Container über Basic Auth (NavUserPassword) — die Referenzdatei unterscheidet beide Fälle ausdrücklich.
- **Push statt Poll**: Webhooks bzw. Power-Automate-Anbindung, wenn eine App auf BC-Änderungen reagieren soll, statt ständig zu pollen.
- `$filter`, `$expand`, `$select` (OData-Query-Optionen) sind der Standardweg, um Antworten für eine schlanke mobile App klein zu halten.

Details, Auth-Setup, Beispiel-Requests, Automation-API: `references/bc-api-integration.md`.

## Kurzüberblick Satelliten-App-Architektur

Statt eines BC-Rollencenters, das alle Rollen in einer UI zusammenpresst: pro Rolle/Prozess eine eigene, schlanke App.

- Jede App bekommt nur die BC-Entitäten und -Aktionen, die ihre Rolle wirklich braucht — kein Nachbau des ganzen BC-Menüs.
- Mobil vs. Desktop ist eine UX-Entscheidung pro Rolle (Bauleiter auf der Baustelle → mobil-first; Einkauf im Büro → eher Desktop/Web), nicht ein technischer Zwang, alles auf beiden zu bauen.
- Tech-Stack ist bewusst offen zu halten (React Native/Flutter/PWA für mobil, Web-App/Electron für Desktop) — die Wahl hängt vom jeweiligen Projekt ab, nicht von einer festen Vorgabe dieser Skill.
- Gemeinsamer Nenner aller Satelliten-Apps: eine dünne API-Schicht gegen BC, klar getrennt vom eigentlichen UI, damit neue Apps schnell entstehen können, ohne die BC-Anbindung jedes Mal neu zu bauen.

Details, Architekturskizze, Entscheidungsfragen: `references/satellite-app-architecture.md`.

## Wo weiter nachschlagen

AL/BC entwickelt sich schnell — bei Detailfragen (genaue Syntax, aktuelle API-Version, neue Objekttypen) lieber gezielt nachschlagen als aus dem Gedächtnis raten:

- Microsoft Learn — AL-Entwicklung: `learn.microsoft.com/dynamics365/business-central/dev-itpro/developer/`
- Microsoft Learn — BC API-Referenz: `learn.microsoft.com/dynamics365/business-central/dev-itpro/api-reference/v2.0/`
- Microsoft Learn — Webhooks/Automation-APIs: `learn.microsoft.com/dynamics365/business-central/dev-itpro/administration/automation-apis-using-webhooks`
- Schwester-Skill `bc-al-cookbook` (falls installiert): konkrete AL-Techniken („wie macht man X in AL?") mit Fallstricken.

Wenn eine Detailfrage über das hinausgeht, was in den Referenzdateien steht, sag das offen und schlage vor, die passende Learn-Seite zu prüfen, statt eine veraltete oder erfundene API-Form zu unterstellen.
