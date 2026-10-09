# Den BC-Standard nachschlagen statt raten

**Erhoben am 04.08.2026 aus einem lokalen BC-28.3-Container (AT-Lokalisierung, Demomandant `CRONUS AT`).**
Diese Datei sagt, **was ich vom Standard sehen kann, was nicht, und wie ich es in einer Sekunde
finde.**

> **Die ehrliche Vorbemerkung:** Ich kann den Standard **nicht auswendig**. 23.370 Felder passen
> in kein Gedächtnis, und alles, was ich „aus dem Kopf" über BC-Feldnamen sage, ist eine
> Vermutung. **Was hier steht, ist das Gegenteil davon: ein Nachschlagewerk, das jede Feldfrage
> mit einem `grep` beantwortet.** Das ist funktional besser als Auswendigwissen — es ist
> nachprüfbar.

---

## Was da liegt

| Datei | Inhalt | Größe |
|---|---|---|
| `bc28-standard-datenmodell.txt` | **1.364 Standardtabellen, 23.370 Felder** — `Tabelle\|Feld\|SQL-Typ\|Länge` | 1,1 MB |
| `bc28-objektinventar.txt` | **14.183 Standardobjekte** (IDs < 50000) — `Objekttyp\|Objekt-ID` | 116 KB |
| `bc28-ereignisse.txt` | **23.629 Ereignis-Andockstellen** — `Objekt\|Ereignis\|Art\|Datei\|Zeile\|Signatur` | 5,9 MB |

**Alle drei sind Extrakte, keine Kopien** — sie ersetzen den Container nicht, sie machen ihn
durchsuchbar, ohne ihn anzufassen (und ohne laufenden Container).

> ### ⚠ Warum die dritte Datei eine **andere Quelle** hat — und warum sie so spät kam
>
> Die ersten beiden kommen aus **SQL** (`sys.columns`, `sys.tables`). Die Datenbank kennt
> Tabellen und Felder. **Ereignisse kennt sie nicht — die sind Code, keine Daten.**
>
> ```
> bc28-standard-datenmodell.txt   SQL   -> Felder      sieht KEINE Ereignisse
> bc28-objektinventar.txt         SQL   -> Objekt-IDs  sieht KEINE Ereignisse
> bc28-ereignisse.txt             AL-QUELLTEXT (entpackter Standard)
> ```
>
> **Gemessen am 02.09.2026:** Beide SQL-Extrakte enthalten das Wort `IntegrationEvent`
> **null Mal**, und diese Anleitung erwähnte Ereignisse bis dahin ebenfalls **null Mal.**
> Für „welche Felder hat X" war Nachschlagen eine Sekunde; **für „woran kann ich mich
> hängen" gab es gar nichts** — und genau das ist die Frage, die eine Erweiterung stellt,
> die den Standard *erweitern statt verbiegen* soll.

---

## Die vier Fragen, die im Alltag wirklich vorkommen

### 1 · „Welche Felder hat Tabelle X?"

```bash
grep "^Sales Header|" bc28-standard-datenmodell.txt
grep "^Job Task|"     bc28-standard-datenmodell.txt
```

### 2 · „Gibt es ein Feld, das *irgendwie* so heißt?" — **die wichtigste**

```bash
grep -i "|.*leistungszeitraum" bc28-standard-datenmodell.txt     # -> nichts. Beweis, kein Gefuehl.
grep -i "|.*WIP"               bc28-standard-datenmodell.txt
```

> **Genau dafür ist das Ding gebaut.** Am 04.08. habe ich zwei Stunden gebraucht, um zu belegen,
> dass der Standardbeleg **kein** Feld für einen Leistungszeitraum hat. **Mit dieser Datei ist
> das eine Zeile.**

### 3 · „Wie heißt das Feld *genau*?"

BC-Feldnamen tragen Leerzeichen, Punkte und Umlaute — `"Bill-to Customer No."`,
`"Unit of Measure Code"`, `"WIP-Total"`. **Ein Tippfehler kostet einen Kompilierlauf.**

```bash
grep -i "unit of measure" bc28-standard-datenmodell.txt | head
```

### 4 · „Ist diese Objekt-ID im Standard belegt?"

```bash
grep "^1|18$"  bc28-objektinventar.txt      # Typ 1 = Table, ID 18
```

### 5 · „Woran kann ich mich hängen?" — **die Frage jeder Erweiterung**

```bash
# Alle Ereignisse einer Buchungscodeunit:
grep -F ' "Purch.-Post"|' bc28-ereignisse.txt            # 496 Stueck
grep -F ' "Item Jnl.-Post Line"|' bc28-ereignisse.txt    # 369

# Ein Ereignis dem Namen nach, ueber den ganzen Standard:
grep -i '|OnAfterPostPurchaseDoc|' bc28-ereignisse.txt

# Was feuert VOR dem Buchen, was danach?
grep -F ' "Purch.-Post"|' bc28-ereignisse.txt | grep '|OnBefore' | wc -l
```

**Der Name des Objekts steht mit Anführungszeichen, genau wie AL ihn schreibt** — die
Zeile ist damit kopierfertig für das Abo:

```
codeunit 90 "Purch.-Post"|OnAfterPostPurchaseDoc|IntegrationEvent|Purchases/Posting/PurchPost.Codeunit.al|8993|var PurchaseHeader: Record "Purchase Header"; ...
```

```al
[EventSubscriber(ObjectType::Codeunit, Codeunit::"Purch.-Post", 'OnAfterPostPurchaseDoc', '', false, false)]
```

> ⚠ **Und die Grenze, die dazugehört:** Der Index sagt, welche Ereignisse **deklariert**
> sind — **nicht, ob eines im konkreten Ablauf auch feuert.** Ein Abo auf ein existierendes
> Ereignis, das in deinem Pfad nie ausgelöst wird, **kompiliert sauber und tut nichts.**
> Das ist die teurere der beiden Fehlerarten: ein falscher Name bricht den Bau und wird
> gefunden, ein falscher *Zeitpunkt* wird es nicht.

---

## Die Objekttyp-Nummern — **geeicht, nicht gedeutet**

Die Nummern stehen roh in der Metadatentabelle. **Geeicht an einer eigenen Extension**, deren Bestand aus dem Quelltext bekannt war
(Zählung vom 04.08.2026 inklusive der damals eigenen Objekte; die öffentliche Datei
enthält nur noch die Standard-IDs):

| Typ | Objekte gesamt | eigene Extension (50000–50999) | Dateien im Quelltext | Eichung |
|---|---|---|---|---|
| **1** | 2.324 | 30 | 30 `*.Table.al` | ✅ **Table** |
| **3** | 782 | 4 | 4 `*.Report.al` | ✅ **Report** |
| **5** | 4.235 | 33 | 32 `*.Codeunit.al` | ✅ **Codeunit** *(±1)* |
| **8** | 4.180 | 55 | 55 `*.Page.al` | ✅ **Page** |
| 6 · 9 · 14 · 15 · 16 · 17 · 20 · 21 · 22 | — | — | — | **ungeeicht — nicht deuten** |

> **Drei exakte Treffer sind der Beleg.** Die übrigen Nummern stehen in der Datei und bleiben
> ohne Etikett, bis jemand sie genauso eicht. **Eine geratene Zuordnung wäre schlimmer als
> keine.**

---

## ⛔ Was ich **nicht** sehe — und das gehört genauso dazu

```
Objektnamen von Seiten, Codeunits, Reports   das Metadata-Blob ist binaer (0x02457D5B...)
AL-Quelltext des Standards                    liefert Microsoft nicht mit, nur Symbole
Prozedursignaturen des Standards              stecken in den .app-Symbolen, nicht in SQL
```

**Für Objektnamen und Signaturen bleibt: die offizielle Doku, `Ctrl+Klick` in VS Code mit
geladenen Symbolen, oder `learn.microsoft.com`.** Diese Datei hilft dort nicht — **und tut auch
nicht so.**

---

## ⚠ Ein Fehler beim Erheben, der als Warnung hierher gehört

**Der erste Zählversuch ergab 39.885 Objekte. Er war falsch.**

`Application Object Metadata` hält **jede Objektfassung je Paket und Emit-Version** — ich hatte
Zeilen gezählt statt Objekte. Aufgefallen ist es an einer Unmöglichkeit: *4.234 Tabellen in einem
200er-ID-Bereich.*

```sql
FALSCH:   SELECT COUNT(*)                    FROM [Application Object Metadata]
RICHTIG:  SELECT COUNT(DISTINCT [Object ID]) FROM [Application Object Metadata]
```

> **Die Zahl sah plausibel aus und war es nicht.** Wer aus dieser Tabelle zählt, zählt Fassungen,
> nicht Objekte.

---

## Neu erzeugen — für einen anderen Container oder eine andere Version

Die GUID `437dbf0e-84ff-417a-965d-ed2bb9650972` ist die **Basis-App**; der Mandantenpräfix
(`CRONUS AT$`) hängt an der Firma. Beides anpassen, dann:

```powershell
$dir = "$HOME\.claude\skills\business-central\references"

docker exec <container> sqlcmd -S localhost -d <mandanten-db> -h -1 -W -s'|' -l 60 -Q @"
SET NOCOUNT ON;
SELECT REPLACE(REPLACE(t.name,'CRONUS AT`$',''),'`$437dbf0e-84ff-417a-965d-ed2bb9650972','')
     + '|' + c.name + '|' + ty.name + '|' + CONVERT(varchar(10), c.max_length)
FROM sys.columns c
JOIN sys.tables t  ON t.object_id     = c.object_id
JOIN sys.types ty  ON ty.user_type_id = c.user_type_id
WHERE t.name LIKE 'CRONUS AT`$%437dbf0e-84ff-417a-965d-ed2bb9650972'
  AND c.name NOT LIKE '`$system%' AND c.name <> 'timestamp'
ORDER BY t.name, c.column_id
"@ | Where-Object { $_ -match '\|' } | Set-Content "$dir\bc28-standard-datenmodell.txt" -Encoding UTF8
```

**Zwei Fallstricke, beide teuer gelernt:**

```
-s'|'  und NICHT -s"<TAB>"   sqlcmd weist den Tabulator als Argument zurueck
-h -1                        sonst stehen Kopfzeilen und Trennlinien in der Datei
```

**Und `sys.columns` liest die Datenbank, nicht den Dienst** — es braucht also **keinen
Neustart**, aber es zeigt auch **keine FlowFields**: die haben keine Spalte. *(Dasselbe gilt für
`DateFormula`-Felder, die als Ziffer plus nicht druckbarem Einheitenbyte liegen.)*

### Und den Ereignis-Index neu erzeugen

Der kommt **nicht** aus SQL, sondern aus dem entpackten AL-Quelltext:

```bash
python scripts/Baue-Ereignisindex.py    # liegt in diesem Skill-Ordner
```

Er liest den entpackten Standard-Quelltext (Vorgabe `C:\bcsrcfull`, 8.094 `.al`-Dateien)
und schreibt die Datei hierher zurück. Quelle und Ziel lassen sich als Argumente übergeben.
**Er meldet seinen eigenen blinden Fleck mit** — die Zahl der Indexzeilen ohne
Objektnamen. Steht dort nicht `0`, ist der Index unbrauchbar geworden und die Ursache
gehört geprüft, nicht ignoriert.

⚠ **Das Verzeichnis mit dem entpackten Quelltext ist nicht dauerhaft.** Ist es geräumt, muss der Standard erst wieder
entpackt werden — der Index ist dann die einzige verbliebene Spur und älter als der
Container.

---

## Die Regel, für die das hier gebaut ist

> **Ein BC-Feldname, den ich aus dem Gedächtnis schreibe, ist eine Vermutung — und Vermutungen
> liegen erfahrungsgemäß bei 1 von 10.** Ein `grep` in diese Datei kostet eine Sekunde und
> liefert einen Beleg. **Es gibt keinen Grund, den teureren Weg zu gehen.**
