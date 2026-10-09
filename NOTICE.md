# NOTICE — Herkunft und Drittquellen / Provenance and third-party sources

Eigener Inhalt dieses Repos steht unter MIT (`LICENSE`). Die folgenden Teile beruhen auf
Drittquellen; ihre Bedingungen bleiben unberührt.

## 1 · `skills/bc-al-cookbook` — Destillation aus Erik Hougaards „Youtube-Video-Sources"

- Quelle: https://github.com/hougaard/Youtube-Video-Sources (Erik Hougaard, hougaard.com) —
  öffentliche Demo-Projekte zu seinen Business-Central-Videos. Das Quell-Repo trägt **keine
  explizite Lizenz**.
- Was hier liegt: **keine Kopie.** Je Demo ein in eigenen Worten beschriebener Mechanismus, eine
  gekürzte und umgeschriebene Code-Essenz, Fallstricke aus eigener Prüfung und der Verweis auf den
  Quellordner. Die vollständigen Demos liegen nicht in diesem Repo; wer sie braucht, klont das
  Original.
- Attribution: Erik Hougaard. Wer die Quelle nutzt, respektiert seine Bedingungen; bei Zweifeln an
  der Weiterverwendung einzelner Snippets gilt das Original, nicht diese Destillation.

## 2 · `skills/business-central-development` — Fork von Mindrally/skills (Apache-2.0)

- Quelle: https://github.com/Mindrally/skills › `business-central-development/SKILL.md`,
  Apache License 2.0 (Kopie: `skills/business-central-development/LICENSE-Apache-2.0.txt`).
- Änderungen gegenüber dem Original: `skills/business-central-development/CHANGES.md`; das
  unveränderte Original liegt als `UPSTREAM-ORIGINAL.md` daneben (Apache-2.0 §4b: geänderte
  Dateien sind gekennzeichnet).

## 3 · `skills/business-central/references/bc28-*.txt` — Metadaten-Extrakte des BC-Standards

- `bc28-standard-datenmodell.txt` und `bc28-objektinventar.txt` wurden per SQL
  (`sys.columns`, `sys.tables`, `[Application Object Metadata]`) aus einem lokalen
  Business-Central-28.3-Container (AT-Lokalisierung, Demomandant CRONUS) erhoben.
- `bc28-ereignisse.txt` wurde aus dem entpackten AL-Quelltext der Base Application erzeugt
  (`scripts/Baue-Ereignisindex.py`): Objekt, Ereignisname, Art, Datei, Zeile, Signatur.
- Enthalten sind **Namen, Typen, Längen, IDs und Prozedursignaturen** — die öffentliche
  Erweiterungsschnittstelle, die Microsoft Entwicklern über Symbole und Microsoft Learn
  bereitstellt. **Kein Microsoft-Quellcode** ist enthalten. Microsoft Dynamics 365 Business
  Central ist ein Produkt und eine Marke der Microsoft Corporation; dieses Repo steht in keiner
  Verbindung zu Microsoft.

## 4 · Nicht enthalten, aber empfohlen

- `al-build` (Build-/Test-Gate für AL-Projekte) von Flemming Bakkensen, MIT:
  https://github.com/FBakkensen/bc-agentic-dev-tools-marketplace — eigenständig installieren.

---

**English:** Own content is MIT-licensed. The cookbook is a distillation (own wording, shortened
and rewritten code essences, pitfalls) of Erik Hougaard's public demo repository, which carries no
explicit license — attribution is given, the full demos are not redistributed. The
`business-central-development` skill is an Apache-2.0 fork of Mindrally/skills with documented
changes. The `bc28-*.txt` extracts contain metadata (names, types, IDs, signatures) of the
Microsoft Business Central standard, not Microsoft source code; this repository is not affiliated
with Microsoft.
