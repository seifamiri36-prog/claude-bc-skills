# Records, Filter, FlowFields & Queries

_Destilliert aus Erik Hougaards Youtube-Video-Sources (Ordnername = Videothema)._
_Vollquellen: https://github.com/hougaard/Youtube-Video-Sources (lokal klonen; Ordnername = Videothema)_

Der Cluster lehrt die Datenzugriffs-Schicht von AL jenseits des FindSet-Alltags: die Filtersprache als eigenes Werkzeug (FilterGroup(-1) fuer Feld-uebergreifendes ODER, %1-Substitution als einzig sichere Art, Werte in Filter zu bringen, @ fuer case-insensitive, Temp-Tabelle als Wildcard-Matcher), FlowFields als vollstaendiges Muster (alle sechs CalcFormula-Methoden, das Posten+Summe+DrillDown-Ledger-Muster, Business-Logik ueber Events auf der treibenden Tabelle statt nicht existenter FlowField-Trigger) und Queries als echte SQL-Joins samt programmatischem Abgriff via SaveAsCsv. Dazu Seitentechnik, die direkt in Belegliste-UIs traegt: Zweittabellen-Felder anzeigen UND editieren, Batch-Aktionen ueber die Benutzer-Auswahl (SetSelectionFilter statt auf Rec loopen), virtuelle Integer/Date-Tabellen als Quellen. Wiederkehrender Fallstrick: Filterstrings per Konkatenation bauen (Datums-Locale, Sonderzeichen) — die Demos zeigen mehrfach, warum nur typisierte %1-Platzhalter sicher sind.

**Wertvollste Ordner:** EditFlowField · UpdateBusinessLogicOnFlowField · OneListTwoTables · MessWithRec · setfiltersetrange

## Themen (nach Praxis-Relevanz)

- ●●●  **FilterGroup** — FilterGroup(-1) ist die Cross-Column-Gruppe: Filter auf VERSCHIEDENEN Feldern werden ODER- statt UND-verknuepft (wie die Mehrspalten-Suche des Clients); normale Gruppen wirken weiterhin als UND dazu.
- ●●●  **EditFlowField** — 'FlowField editieren' richtig geloest: der Wert lebt als sum() ueber eine Posten-Tabelle, Aenderungen entstehen als NEUE Eintraege ueber die DrillDown-Seite (Ledger-Muster); die Posten-Tabelle setzt Defaults in OnInsert.
- ●●●  **MessWithRec** — Batch-Aktion auf einer Liste: CurrPage.SetSelectionFilter(NewRec) holt genau die vom Benutzer MARKIERTEN Zeilen in eine Kopie (CopyFilters fuer 'alle sichtbaren') — und die Schleife laeuft ueber die Kopie, nie ueber Rec selbst.
- ●●●  **OneListTwoTables** — Felder einer ZWEITEN Tabelle in einer Liste anzeigen UND editieren: globale Record-Variable, in OnAfterGetRecord UND OnAfterGetCurrRecord nachladen (SetAutoCalcFields fuer deren FlowFields), Schreiben im Feld-OnValidate selbst per Validate+Modify.
- ●●●  **virtualfields** — Drei Wege, ein Fremdtabellen-Feld in einer Liste zu zeigen, direkt nebeneinander: Funktionsaufruf im Feldausdruck, Puffer-Variable aus OnAfterGetRecord, Lookup-FlowField — nur das FlowField kann der Benutzer filtern und sortieren.
- ●●●  **AddKeysToStandardTables** — Eine tableextension kann sekundaere Schluessel auch auf Feldern der BASIS-Tabelle anlegen — der schnellste legale Fix fuer lahme Filter auf Standardfeldern, ganz ohne Basis-App anzufassen.
- ●●●  **UpdateBusinessLogicOnFlowField** — FlowFields haben keine Trigger ⚠ **UNBELEGT (Prüfung 01.09.2026, D+B):** Diese Aussage trägt **weder die Demo noch die MS-Doku** — sie ist nicht widerlegt, sondern **unbelegt**. ⚠ **Ein Arbeitspaket in `PLAN-A-Musterzuordnung` baut darauf: vor dem Bau am Bestand MESSEN, nicht übernehmen.** ⚠ **Indirekt gestützt, aber nicht gesagt:** MS führt nur, dass FlowFields **keine physischen Felder** sind („FlowFields are not physical fields that are stored in the database“, AS0036) und zur Laufzeit berechnet werden (AL0910). Ein Satz „keine Trigger“ steht nirgends. *(AP-5 Kostensicht, ●●●)* — 'reagiere, wenn sich der Saldo aendert' heisst: Event auf der TREIBENDEN Posten-Tabelle abonnieren, dort CalcFields auf das FlowField, dann handeln (hier: Kunde bei Kreditlimit-Ueberschreitung sperren).
- ●●●  **query** — Ein Query-Objekt ist ein echter SQL-Join in einem Roundtrip: verschachtelte dataitems mit DataItemLink, SqlJoinType steuert Inner-/LeftOuterJoin; Konsum im Code per Open/Read/Close statt verschachtelter FindSet-Schleifen.
- ●●●  **LookupFlowFields** — Fremdfeld ohne eine Zeile Trigger-Code in Belegzeilen ziehen: Lookup-FlowField per tableextension auf der Sales Line (Item-Attribut ueber "No."), dann direkt in der Subform anzeigen — Editable=false und DrillDownPageId inklusive.
- ●●●  **setfiltersetrange** — Filterwerte nie als String zusammenbauen: %1-Platzhalter in SetFilter substituieren typisiert (Datum bleibt Datum, kein Locale-Parsing) und escapen Sonderzeichen in Benutzereingaben.
- ●●○  **Search App with RecordRefs** — Tabellen-generische Suche ueber konfigurierbare Tabellen: RecordRef/KeyRef/FieldRef fuer PK-Zugriff ohne Tabellenkenntnis, Format(RecordRef) als Ganze-Zeile-Text fuer Notnagel-Volltext, Feldtyp RecordId als generischer Zeiger im Ergebnis, RecordRef-als-Variant an Page.Run zum Oeffnen der richtigen Karte.
- ●●○  **AtFiltering** — SetRange behandelt seinen Wert als DATEN (keine Filtersprache), SetFilter parst ihn als Ausdruck — und das @-Praefix macht einen Filter case-insensitive, statt Varianten mit Pipes aufzuzaehlen.
- ●●○  **ELI5FlowFields** — Zwei wenig bekannte CalcFormula-Details: das Vorzeichen laesst sich direkt in der Formel drehen (CalcFormula = -sum(...)) und ein Lookup darf in eine voellig UNVERKNUEPFTE Tabelle greifen (Vendor ueber gleichlautende Nummer).
- ●●○  **FlowFields** — Alle sechs CalcFormula-Methoden als Referenz nebeneinander: lookup, exist, sum, count, average, max — je mit where(field/const)-Verknuepfung auf die treibende Tabelle.
- ●●○  **DateFilters** — Eigene Datumsfilter-Token (wie 'heute','lw') fuer ALLE Datumsfilterfelder des Clients definieren: Event OnResolveDateFilterToken der Codeunit "Filter Tokens" abonnieren.
- ●●○  **Virtual Tables** — Die virtuellen Tabellen Integer und Date taugen als SourceTable fuer Seiten: Integer als Zeilengenerator fuer Listen ohne physische Tabelle (Werte aus Dictionary o.ae.), Date liefert fertige Tages-/Wochen-/Monats-/Quartalsperioden frei Haus.
- ●●○  **filterSyntaxInFlowFields** — In CalcFormula-where-Klauseln gibt es zwei legale Filter-Schreibweisen: filter('<>Finished') als String und filter(<> Finished) als Symbol — beide kompilieren, koennen sich aber unterschiedlich verhalten.
- ●●○  **TextSearch** — BC 25 bringt optimierte Volltextsuche: das &&-Praefix im SetFilter nutzt den Suchindex statt LIKE-Scan. Messung des Autors auf der Customer List: '@erik*' 39 ms gegen '&&Erik*' 13-17 ms.
- ●●○  **WildcardMatchingStrings** — AL hat keine eingebaute Wildcard-Pruefung auf Strings — eine TableType=Temporary-Tabelle plus SetFilter macht die komplette BC-Filtersprache (auch Dezimalbereiche wie '120..125') zum In-Memory-Pattern-Matcher.
- ●●○  **QuerySaveAs** — Query-Ergebnisse (auch von Standard-Queries) programmatisch abgreifen: SaveAsCsv in einen TempBlob-Stream, Kopfzeile liefert die Spaltennamen, Zeilen per Split zerlegen und per Evaluate-Kaskade typisiert z.B. in JSON heben.
- ●●○  **FindingDuplicates** — Dubletten-Warnung beim Erfassen: OnBeforeValidate auf Name/Adresse, case-insensitive Contains-Filter ('@*wert*') gegen den Bestand, eigene Nummer per '<>%1' ausschliessen; GuiAllowed() schuetzt Webservice-Aufrufe vor Dialogen.
- ●●○  **Query Strings** — Eigene URL-Query-Parameter im Web Client lesen (Deep-Links mit Kontext): ein unsichtbares 1x1-Pixel-ControlAddIn liest im StartupScript window.location.search und meldet den Wert per Event an AL zurueck.
- ●●○  **FuzzyTextCompare** — Fuzzy-Vergleich zweier Texte: Die Standard-Codeunit "Type Helper" bringt TextDistance (Edit-Distanz) fertig mit — vor jedem Eigenbau pruefen; das Demo baut zusaetzlich einen eigenen Aehnlichkeits-QUOTIENTEN (Treffer/Laenge) fuer 'wie aehnlich' statt 'wie viele Edits'.
- ●●○  **QueryCategory** — Eine einzige Property macht eine Query fuer Endanwender nutzbar: QueryCategory = 'Customer List' haengt sie ohne jede weitere Verdrahtung in das Ansichten-/Analyse-Menue der genannten Listenseite.
- ●○○  **sorting** — Find('=') / Find('<') / Find('>') positionieren relativ zu den Feldwerten im Record-PUFFER entlang des aktuellen Schluessels — SetCurrentKey aendert also nicht nur die Reihenfolge von Next(), sondern auch die Positionierungssemantik von Find.
- ●○○  **QueryInSearch** — Was eine Query in der Tell-Me-Suche auffindbar macht: UsageCategory (plus Caption) ist der Schalter. QueryType=API macht sie zum Webservice und NICHT suchbar; Access=Public oder Description aendern an der Sichtbarkeit nichts.
- ●○○  **DecodingRecordID** — Das Hex-Layout eines als varbinary gespeicherten RecordID-Felds entschluesseln: Bytes 1-4 sind die Tabellennummer little-endian, danach folgen die PK-Werte mit Typ-/Laengenmarkern als UTF-16LE-Zeichen — noetig nur, wenn man solche Spalten direkt per SQL liest.
- ○○○  **BinaryKeys** — HMAC-Ketten mit BINAEREM Schluessel (AWS Signature V4: Schluessel der Stufe n = Digest der Stufe n-1) scheitern an Cryptography Management, weil GenerateHash den Schluessel als Text nimmt — der Hex-String wird als Zeichen gehasht, nicht als Bytes.

---

## FilterGroup

**Technik:** FilterGroup(-1) ist die Cross-Column-Gruppe: Filter auf VERSCHIEDENEN Feldern werden ODER- statt UND-verknuepft (wie die Mehrspalten-Suche des Clients); normale Gruppen wirken weiterhin als UND dazu.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
trigger OnOpenPage()
var
    Grp: Integer;
begin
    Grp := Rec.FilterGroup();      // aktuellen Stand merken
    Rec.FilterGroup(-1);           // Cross-Column: ODER ueber Felder
    Rec.SetFilter(Name, '@*ski*');
    Rec.SetFilter(Contact, '@*bond*'); // Name ODER Contact passt
    Rec.FilterGroup(Grp);          // zurueck; Gruppe 0 = UND dazu
    Rec.SetFilter(Address, '@*queen*'); // UND Address passt
end;
```

**Fallstricke:** FilterGroup immer merken und zuruecksetzen; Filter in Gruppe -1 sind im Filterbereich des Clients fuer den Benutzer unsichtbar. ⚠ **UNBELEGT (Prüfung 01.09.2026, D+B):** Diese Aussage trägt **weder die Demo noch die MS-Doku** — sie ist nicht widerlegt, sondern **unbelegt**. ⚠ **Ein Arbeitspaket in `PLAN-A-Musterzuordnung` baut darauf: vor dem Bau am Bestand MESSEN, nicht übernehmen.** *(AP-Bezug: FilterGroup)*

> ⚠ **Lücken-Vermerk (P, 31.08.2026):** Dieser Eintrag behandelt NUR `FilterGroup(-1)`
> (Cross-Column-ODER). Die **SubPageLink-Gruppe `FilterGroup(4)`** — nötig, wenn eine
> Teilseite den vom Parent gesetzten Link-Filter lesen/ändern muss (unser K5-Fall) —
> kommt weder in den 12 Referenzen noch im Vollfundus vor (je 0 Treffer, gemessen).
> Präzedenz dafür liegt im BC-Standard: `IncomingDocAttachFactBox:288-295`.
> Merke: gleicher Funktionsname, verschiedene Gruppen-Nummern = verschiedene Gegenstände
> (0=Benutzer/Code-Default · 2=Seitenansicht · 4=SubPageLink · -1=Cross-Column).

---

## EditFlowField

**Technik:** 'FlowField editieren' richtig geloest: der Wert lebt als sum() ueber eine Posten-Tabelle, Aenderungen entstehen als NEUE Eintraege ueber die DrillDown-Seite (Ledger-Muster); die Posten-Tabelle setzt Defaults in OnInsert.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
table 50100 "Box Entry"
{
    fields
    {
        field(1; "Entry No."; Integer) { }
        field(2; CustomerNo; Code[20]) { }
        field(3; Type; Option) { OptionMembers = ,Adjustment,Sale,Return; }
        field(5; Quantity; Decimal) { }
    }
    trigger OnInsert()
    begin
        if Rec.Date = 0D then
            Rec.Date := Today();
    end;
}

field(50100; BoxesOnHand; Decimal)
{
    FieldClass = FlowField;
    CalcFormula = sum("Box Entry".Quantity where(CustomerNo = field("No.")));
}
// Kartenfeld: DrillDown = true; DrillDownPageId = 50100;
// "Editiert" wird durch neue Posten in der DrillDown-Liste.
```

**Fallstricke:** Ohne Editable=false ist ein FlowField auf der Seite tippbar — bei Lookup-FlowFields schreibt eine Eingabe sogar in die QUELLTABELLE zurueck. Fuer Bestandsgroessen deshalb immer Posten+Summe statt editierbarem Feld.

---

## MessWithRec

**Technik:** Batch-Aktion auf einer Liste: CurrPage.SetSelectionFilter(NewRec) holt genau die vom Benutzer MARKIERTEN Zeilen in eine Kopie (CopyFilters fuer 'alle sichtbaren') — und die Schleife laeuft ueber die Kopie, nie ueber Rec selbst.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
action(Verarbeiten)
{
    trigger OnAction()
    var
        NewRec: Record Customer;
    begin
        CurrPage.SetSelectionFilter(NewRec); // nur markierte Zeilen
        // Alternative: NewRec.CopyFilters(Rec); // alles im Seitenfilter
        if NewRec.FindSet() then
            repeat
                NewRec."Name 2" := NewRec.Name; // Fancy Processing
                NewRec.Modify();
            until NewRec.Next() = 0;
        // Wuerde man auf Rec loopen, stuende Rec danach auf dem letzten
        // Datensatz im Filter - die Seite springt und filtert sichtbar um.
    end;
}
```

**Fallstricke:** Der Autor kommentiert es selbst im Code: nach einem Loop auf Rec ist Rec 'the last record within the current filters' — Cursor und Filter der Seite sind dann verstellt.

---

## OneListTwoTables

**Technik:** Felder einer ZWEITEN Tabelle in einer Liste anzeigen UND editieren: globale Record-Variable, in OnAfterGetRecord UND OnAfterGetCurrRecord nachladen (SetAutoCalcFields fuer deren FlowFields), Schreiben im Feld-OnValidate selbst per Validate+Modify.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
page 50100 OneListTwoTables
{
    SourceTable = "Sales Header";
    // ... in der repeater:
    field(CustomerBalanceLCY; Customer."Balance (LCY)") { BlankZero = true; }
    field(CustomerPaymentTermsCode; Customer."Payment Terms Code")
    {
        trigger OnValidate()
        begin
            Customer.Validate("Payment Terms Code"); // Zweittabelle selbst
            Customer.Modify();                       // validieren + speichern
        end;
    }
    trigger OnAfterGetRecord() begin RefreshLine(); end;
    trigger OnAfterGetCurrRecord() begin RefreshLine(); end;
    procedure RefreshLine()
    begin
        Customer.SetAutoCalcFields("Balance (LCY)");
        if not Customer.Get(Rec."Sell-to Customer No.") then
            Clear(Customer);
    end;
    var
        Customer: Record Customer;
}
```

**Fallstricke:** Clear() beim Get-Fehlschlag ist Pflicht, sonst zeigt die Zeile die Werte des Vorgaengers; beide Trigger noetig (Scrollen vs. Fokuswechsel). SetAutoCalcFields erspart je Zeile den expliziten CalcFields-Roundtrip.

---

## virtualfields

**Technik:** Drei Wege, ein Fremdtabellen-Feld in einer Liste zu zeigen, direkt nebeneinander: Funktionsaufruf im Feldausdruck, Puffer-Variable aus OnAfterGetRecord, Lookup-FlowField — nur das FlowField kann der Benutzer filtern und sortieren.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
// 1: Funktionsaufruf je Zeile (flexibel, nicht filterbar)
field(V1; GetVendorName(Rec)) { }
// 2: Variable, gefuellt im Trigger (nicht filterbar)
field(V2; VendorNameTxt) { }
trigger OnAfterGetRecord()
begin
    if Vendor.Get(Rec."No.") then
        VendorNameTxt := Vendor.Name
    else
        VendorNameTxt := '';
end;
// 3: FlowField (filterbar, sortierbar, DB-seitig berechnet)
field(50100; VendorName; Text[100])
{
    FieldClass = FlowField;
    CalcFormula = lookup(Vendor.Name where("No." = field("No.")));
    Editable = false;
}
```

**Fallstricke:** Variante 1 und 2 koennen Fallback-Texte ('<no vendor>') und beliebige Logik liefern, tauchen aber nie im Filterbereich auf; Variante 3 ist die einzige mit Server-seitigem Join.

---

## AddKeysToStandardTables

**Technik:** Eine tableextension kann sekundaere Schluessel auch auf Feldern der BASIS-Tabelle anlegen — der schnellste legale Fix fuer lahme Filter auf Standardfeldern, ganz ohne Basis-App anzufassen.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** Lief hier schon auf runtime 7.0 (BC18) — kein neues Feature, nur ein unbekanntes.

```al
tableextension 50138 "My Sales Invoice" extends "Sales Invoice Header"
{
    fields
    {
        field(50138; MyField; Code[20]) { Caption = 'My Field'; }
    }
    keys
    {
        key(ExtDocKey; "External Document No.") { } // Index auf Basis-Feld
    }
}
```

**Fallstricke:** Jeder zusaetzliche Schluessel kostet Schreibperformance auf der Tabelle — gezielt fuer gemessene Filter-Hotspots einsetzen, nicht auf Vorrat.

---

## UpdateBusinessLogicOnFlowField

**Technik:** FlowFields haben keine Trigger ⚠ **UNBELEGT (Prüfung 01.09.2026, D+B):** Diese Aussage trägt **weder die Demo noch die MS-Doku** — sie ist nicht widerlegt, sondern **unbelegt**. ⚠ **Ein Arbeitspaket in `PLAN-A-Musterzuordnung` baut darauf: vor dem Bau am Bestand MESSEN, nicht übernehmen.** ⚠ **Indirekt gestützt, aber nicht gesagt:** MS führt nur, dass FlowFields **keine physischen Felder** sind („FlowFields are not physical fields that are stored in the database“, AS0036) und zur Laufzeit berechnet werden (AL0910). Ein Satz „keine Trigger“ steht nirgends. *(AP-5 Kostensicht, ●●●)* — 'reagiere, wenn sich der Saldo aendert' heisst: Event auf der TREIBENDEN Posten-Tabelle abonnieren, dort CalcFields auf das FlowField, dann handeln (hier: Kunde bei Kreditlimit-Ueberschreitung sperren).

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
codeunit 50123 CreditWatch
{
    [EventSubscriber(ObjectType::Codeunit, Codeunit::"Gen. Jnl.-Post Line",
        'OnAfterCustLedgEntryInsert', '', true, true)]
    local procedure OnLedgerInsert(var CustLedgerEntry: Record "Cust. Ledger Entry")
    var
        Cust: Record Customer;
    begin
        if Cust.Get(CustLedgerEntry."Customer No.") then begin
            Cust.CalcFields("Balance (LCY)"); // FlowField frisch rechnen
            if Cust."Balance (LCY)" > Cust."Credit Limit (LCY)" then begin
                Cust.Blocked := Cust.Blocked::Invoice;
                Cust.Modify(true);
            end;
        end;
    end;
}
```

**Fallstricke:** Der Subscriber laeuft MITTEN im Buchungsprozess — ein Error hier rollt die ganze Buchung zurueck; Logik defensiv halten. Das FlowField im Subscriber explizit CalcFields'en, der Puffer kommt ungerechnet an.

---

## query

**Technik:** Ein Query-Objekt ist ein echter SQL-Join in einem Roundtrip: verschachtelte dataitems mit DataItemLink, SqlJoinType steuert Inner-/LeftOuterJoin; Konsum im Code per Open/Read/Close statt verschachtelter FindSet-Schleifen.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
query 50100 "Sales Docs"
{
    elements
    {
        dataitem(SH; "Sales Header")
        {
            column(No; "No.") { }
            dataitem(SL; "Sales Line")
            {
                DataItemLink = "Document Type" = SH."Document Type",
                               "Document No." = SH."No.";
                SqlJoinType = LeftOuterJoin; // Koepfe auch OHNE Zeilen
                column(Description; Description) { }
                column(Amount; Amount) { }
            }
        }
    }
}

Q.Open();
while Q.Read() do
    ProcessRow(Q.No, Q.Description, Q.Amount);
Q.Close();
```

**Fallstricke:** ⚠⚠ **BERICHTIGT 01.09.2026 (B): Hier stand „Ohne SqlJoinType ist der Join inner — Belege ohne Zeilen verschwinden stillschweigend aus dem Ergebnis“. DAS IST DAS GEGENTEIL DER DOKU.** MS *Linking and Joining Data Items to Define the Query Dataset*: „By default, the SqlJoinType property is `LeftOuterJoin`, so if you omit this property, a `LeftOuterJoin` is performed.“ **Ohne Angabe bleiben Köpfe ohne Zeilen also gerade ERHALTEN** (die Spalten der unteren Tabelle sind dann null). ⚠ Die Falle liegt damit **umgekehrt**: wer einen INNER JOIN will, muss ihn hinschreiben — sonst zählt er Köpfe ohne Zeilen mit.

---

## LookupFlowFields

**Technik:** Fremdfeld ohne eine Zeile Trigger-Code in Belegzeilen ziehen: Lookup-FlowField per tableextension auf der Sales Line (Item-Attribut ueber "No."), dann direkt in der Subform anzeigen — Editable=false und DrillDownPageId inklusive.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
tableextension 50100 "My Sales Line" extends "Sales Line"
{
    fields
    {
        field(50100; VendorItemNo; Text[50])
        {
            Caption = 'Vendor Item No.';
            FieldClass = FlowField;
            Editable = false;
            CalcFormula = lookup(Item."Vendor Item No." where("No." = field("No.")));
        }
    }
}
pageextension 50100 "My Sales Line" extends "Sales Order Subform"
{
    layout
    {
        addafter(Description)
        {
            field(VendorItemNo; Rec.VendorItemNo)
            {
                ApplicationArea = all;
                DrillDownPageId = 30; // Item List
            }
        }
    }
}
```

**Fallstricke:** Der Lookup greift hier stumpf ueber "No." — bei Zeilen vom Typ G/L oder Ressource zeigt das Feld Unsinn oder leer; sauber waere eine zusaetzliche where-Bedingung auf den Zeilentyp (die CalcFormula-where kann auch const-Filter auf Type tragen).

---

## setfiltersetrange

**Technik:** Filterwerte nie als String zusammenbauen: %1-Platzhalter in SetFilter substituieren typisiert (Datum bleibt Datum, kein Locale-Parsing) und escapen Sonderzeichen in Benutzereingaben.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
GL.SetFilter("Posting Date", '5/5/22..6/6/22');             // BAD: locale-abhaengig geparst
GL.SetFilter("Posting Date", Format(D) + '|' + Format(D2));  // semi-BAD: Format() locale-abhaengig
GL.SetFilter("Posting Date", '%1..%2', D, D2);               // richtig: typisierte Substitution
GL.SetRange("Posting Date", D);                              // Gleichheit ohne jedes Parsing
GL.SetFilter(Description, '%1', UserInput);                  // Wert als Parameter statt im String
```

⚠⚠ **BERICHTIGT 01.09.2026 (B): Hier stand `// %1 ESCAPED *, |, .. im Eingabetext`.
DAS WAR ERFUNDEN.** Die Demo (`setfiltersetrange/HelloWorld.al`, **fünf Zeilen**) zeigt in
dieser Zeile `SetFilter(Description,'%1','sdfgsdfg')` — einen Wert **ohne jedes
Sonderzeichen**. **Von Escaping ist dort keine Rede, und es wird auch nichts vorgeführt.**
Die Microsoft-Doku zu `SetFilter` sagt dazu ebenfalls nichts (geprüft 01.09.: *Record.SetFilter
Method*, *Filtering records with SetRange, SetFilter…* — nur *„insert values at run-time"* und
*„the data type of Value must match the data type of Field"*).

> **Nicht die Quelle hat zu viel behauptet — meine Destillation hat etwas HINZUGEFÜGT, das in
> der Quelle nicht steht.** Das ist die gefährlichere Richtung: Eine Sekundärquelle, die zu
> weit geht, kann man an ihrem Original prüfen. Eine erfundene Erklärung sieht wie das
> Original aus.

**Was BELEGT bleibt** (und es ist der eigentliche Wert dieses Musters): **typisierte
Substitution** — `Format(Date)` hängt an den Regional Settings, `%1` nicht. Das steht in der
Demo (drei Varianten BAD/semi-BAD/Not-Bad) **und** bei Microsoft (*„data type of Value must
match the data type of Field"*).

**Fallstricke:** Format(Date) haengt an den Regional Settings von Server/Benutzer — derselbe Code filtert je Umgebung anders. Der Autor stuft die drei Varianten selbst als BAD/semi-BAD/Not-Bad ein.

⚠ **NACHTRAG aus der Praxis, 01.09.2026 — die Regel gilt fuer WERTE, nicht fuer MUSTER:**
`%1` mit einem Wildcard AUSSERHALB des Platzhalters zu mischen ist eine ANDERE Konstruktion
als die hier empfohlene, und sie ist uns einmal teuer geworden:

```al
Position.SetFilter(Gliederungsnummer, '%1*', Nummer + '.');   // <- 0 von 18 erkannt
Position.SetFilter(Gliederungsnummer, Gruppe.Gliederungsnummer + '.*');  // <- wirkt
```

**Am Pilotlauf gemessen** (`DGBJobTaskMgt`, Kommentar an der Fundstelle): Mit `'%1*'` wurde
**keine** der neun ULG als positionstragend erkannt — 0 statt 9 Buchungsaufgaben, der ganze
Aufgabenbaum kippte zu Summenknoten. Die Daten waren dabei in Ordnung (25 von 25 mit
korrektem Praefix und Elternverweis).

⚠ **Der Mechanismus ist NICHT bewiesen** — und seit der Berichtigung oben **weniger bekannt
als vorher.** Gemessen ist die WIRKUNG (0 von 18). Die Erklärung, die ich zuerst anbot
(`%1` escaped den Wert, und ein escapter Wert verträgt sich nicht mit einem Wildcard daneben),
**stützte sich auf eine Behauptung, die weder in der Demo noch beim Hersteller steht** —
ich hatte sie selbst erfunden. **Damit ist die Ursache wieder offen, nicht eingegrenzt.**

> **Eine falsche Erklärung ist schlimmer als keine: Sie beendet die Suche.**

**Merke:** `%1` fuer **Werte** — ja, und zwar immer. `%1` als Baustein eines **Musters**
(`'%1*'`, `'%1..'`, `'@%1'`) — **erst messen.** Wer die Regel als *„immer %1"* liest, baut
genau die Zeile wieder ein, die hier einen Pilotlauf gekostet hat.

---

## Search App with RecordRefs

**Technik:** Tabellen-generische Suche ueber konfigurierbare Tabellen: RecordRef/KeyRef/FieldRef fuer PK-Zugriff ohne Tabellenkenntnis, Format(RecordRef) als Ganze-Zeile-Text fuer Notnagel-Volltext, Feldtyp RecordId als generischer Zeiger im Ergebnis, RecordRef-als-Variant an Page.Run zum Oeffnen der richtigen Karte.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
Ref.Open(Setup."Table No.");
KRef := Ref.KeyIndex(1);          // Primaerschluessel generisch
FRef := KRef.FieldIndex(1);
FRef.SetRange(SearchTerm);
if Ref.FindFirst() then
    StoreResult(Ref.RecordId)      // field(15; "Record ID"; RecordId)
else if Ref.FindSet(false, false) then
    repeat // Poor-Man-Volltext ueber die ganze Zeile:
        if Format(Ref).ToLower().Contains(SearchTerm.ToLower()) then
            StoreResult(Ref.RecordId);
    until (Ref.Next() = 0) or LimitReached();
Ref.Close();

// Treffer oeffnen:
Ref.Open(Setup."Table No.");
Ref.Get(Result."Record ID");
RefVari := Ref;
Page.Run(Setup."Card Page", RefVari);
```

**Fallstricke:** Format(RecRef) je Zeile ist ein Full-Scan — das Demo baut deshalb ein Full Text Search Limit ein. TableRelation auf AllObjWithCaption macht Tabellen-/Seitennummern im Setup nachschlagbar.

---

## AtFiltering

**Technik:** SetRange behandelt seinen Wert als DATEN (keine Filtersprache), SetFilter parst ihn als Ausdruck — und das @-Praefix macht einen Filter case-insensitive, statt Varianten mit Pipes aufzuzaehlen.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
Rec.SetRange(Name, 'test|Test|TEST');  // WOERTLICH: sucht den String samt Pipes
Rec.SetFilter(Name, 'test|Test|TEST'); // Ausdruck: drei Alternativen
Rec.SetFilter(Name, '@test');          // @ = case-insensitive, ersetzt alle drei
```

**Fallstricke:** Umgekehrt nutzbar: SetRange ist das Mittel der Wahl, um nach Werten zu filtern, die Filter-Sonderzeichen (*, |, ..) enthalten.

---

## ELI5FlowFields

**Technik:** Zwei wenig bekannte CalcFormula-Details: das Vorzeichen laesst sich direkt in der Formel drehen (CalcFormula = -sum(...)) und ein Lookup darf in eine voellig UNVERKNUEPFTE Tabelle greifen (Vendor ueber gleichlautende Nummer).

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
tableextension 50100 CustomerTable extends Customer
{
    fields
    {
        field(50100; MyFlow; Decimal)
        {
            FieldClass = FlowField;
            Editable = false;
            // Minus direkt in der Formel: Kreditoren-Betraege positiv zeigen
            CalcFormula = -sum("Detailed Vendor Ledg. Entry".Amount
                where("Vendor No." = field("No.")));
            // auch moeglich: lookup(Vendor.Name where("No." = field("No.")))
        }
    }
}
field(MyFlow; Rec.MyFlow)
{
    ApplicationArea = all;
    DrillDownPageId = "Vendor Card"; // Drilldown-Ziel frei waehlbar
}
```

**Fallstricke:** DrillDownPageId auf dem Seitenfeld ueberschreibt den Standard-Drilldown des FlowFields — der Sprung kann in eine ganz andere Tabelle fuehren als die CalcFormula.

---

## FlowFields

**Technik:** Alle sechs CalcFormula-Methoden als Referenz nebeneinander: lookup, exist, sum, count, average, max — je mit where(field/const)-Verknuepfung auf die treibende Tabelle.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
field(2; Name; Text[250])          { FieldClass = FlowField;
    CalcFormula = lookup(Customer.Name where("No." = field("Customer No."))); }
field(3; "Has Invoices"; Boolean)  { FieldClass = FlowField;
    CalcFormula = exist("Sales Invoice Header" where("Sell-to Customer No." = field("Customer No."))); }
field(4; Total; Decimal)           { FieldClass = FlowField;
    CalcFormula = sum("Cust. Ledger Entry"."Sales (LCY)" where("Document Type" = const(Invoice), "Customer No." = field("Customer No."))); }
field(5; Cnt; Integer)             { FieldClass = FlowField;
    CalcFormula = count("Cust. Ledger Entry" where("Document Type" = const(Invoice), "Customer No." = field("Customer No."))); }
field(6; Avg; Decimal)             { FieldClass = FlowField;
    CalcFormula = average("Cust. Ledger Entry"."Sales (LCY)" where(...)); }
field(7; MaxAmt; Decimal)          { FieldClass = FlowField;
    CalcFormula = max("Cust. Ledger Entry"."Sales (LCY)" where(...)); }
```

**Fallstricke:** Im Code sind FlowFields 0/leer bis CalcFields/SetAutoCalcFields laeuft — nur Seiten rechnen sie automatisch. exist/count brauchen keine Zielspalte, nur die Tabelle.

---

## DateFilters

**Technik:** Eigene Datumsfilter-Token (wie 'heute','lw') fuer ALLE Datumsfilterfelder des Clients definieren: Event OnResolveDateFilterToken der Codeunit "Filter Tokens" abonnieren.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** Demo auf BC18 (runtime 7.0); Event existiert weiterhin.

```al
codeunit 50100 DateFilters
{
    [EventSubscriber(ObjectType::Codeunit, Codeunit::"Filter Tokens", 'OnResolveDateFilterToken', '', true, true)]
    local procedure MyFilters(DateToken: Text; var FromDate: Date; var ToDate: Date; var Handled: Boolean)
    begin
        if DateToken.ToLower() = 'party' then begin
            FromDate := Today() + 10;
            ToDate := FromDate;
            Handled := true;
        end;
    end;
}
```

**Fallstricke:** Wirkt ueberall, wo der Client Datumsfilter parst — der Benutzer tippt das Token einfach ins Filterfeld.

---

## Virtual Tables

**Technik:** Die virtuellen Tabellen Integer und Date taugen als SourceTable fuer Seiten: Integer als Zeilengenerator fuer Listen ohne physische Tabelle (Werte aus Dictionary o.ae.), Date liefert fertige Tages-/Wochen-/Monats-/Quartalsperioden frei Haus.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
page 52300 "Integer Page"
{
    PageType = List;
    SourceTable = Integer; // virtuell: kompletter int-Bereich!
    SourceTableView = where(Number = filter('-7..40'));
    layout { area(Content) { repeater(Rep) {
        field(Number; GetValue(Rec.Number)) { Caption = 'Wert'; ApplicationArea = all; }
    } } }
    procedure GetValue(i: Integer): Text
    begin
        if Dict.ContainsKey(i) then
            exit(Dict.Get(i));
    end;
    var
        Dict: Dictionary of [Integer, Text];
}

page 52301 "Date Virtual"
{
    PageType = List;
    SourceTable = Date; // fertige Periodenzeilen
    SourceTableView = where("Period Type" = const(Month));
}
```

**Fallstricke:** Integer ohne SourceTableView-Begrenzung heisst Milliarden Zeilen — den Bereich IMMER einschraenken. Negative Zahlen sind erlaubt.

---

## filterSyntaxInFlowFields

**Technik:** In CalcFormula-where-Klauseln gibt es zwei legale Filter-Schreibweisen: filter('<>Finished') als String und filter(<> Finished) als Symbol — beide kompilieren, koennen sich aber unterschiedlich verhalten.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
field(50100; Desc1; Text[100])
{
    FieldClass = FlowField;
    CalcFormula = lookup("Prod. Order Routing Line".Description
        where("Routing Status" = filter('<>Finished'))); // String: erst zur Laufzeit geparst
}
field(50101; Desc2; Text[100])
{
    FieldClass = FlowField;
    CalcFormula = lookup("Prod. Order Routing Line".Description
        where("Routing Status" = filter(<> Finished)));  // Symbol: compile-geprueft
}
```

**Fallstricke:** Die String-Variante entgeht der Compile-Pruefung — Tippfehler oder umbenannte Enum-Werte fallen erst zur Laufzeit (oder nie) auf. Bei Options/Enums immer die Symbol-Schreibweise nehmen.

---

## TextSearch

**Technik:** BC 25 bringt optimierte Volltextsuche: das &&-Praefix im SetFilter nutzt den Suchindex statt LIKE-Scan. Messung des Autors auf der Customer List: '@erik*' 39 ms gegen '&&Erik*' 13-17 ms.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** application 25.0, runtime 14.0 — erst ab BC 25.

```al
Rec.SetFilter(Name, '@erik*');  // klassisch case-insensitive: ~39 ms
Rec.SetFilter(Name, '&&Erik*'); // Optimized Text Search:      ~13-17 ms
if Rec.FindSet() then
    repeat
    until Rec.Next() = 0;
```

**Fallstricke:** Setzt das Textsuche-Feature auf dem Feld voraus (OptimizeForTextSearch); Semantik ist Suche, nicht exakter Wildcard-Match — Ergebnisse koennen von @-Filtern abweichen.

---

## WildcardMatchingStrings

**Technik:** AL hat keine eingebaute Wildcard-Pruefung auf Strings — eine TableType=Temporary-Tabelle plus SetFilter macht die komplette BC-Filtersprache (auch Dezimalbereiche wie '120..125') zum In-Memory-Pattern-Matcher.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
table 50100 StringMatch
{
    TableType = Temporary; // erzeugt KEINE SQL-Tabelle
    fields { field(1; Match; Text[2000]) { } field(2; MatchDec; Decimal) { } }
}

procedure MatchesPattern(Value: Text; Pattern: Text): Boolean
var
    m: Record StringMatch;
begin
    m.Match := CopyStr(Value, 1, MaxStrLen(m.Match));
    m.Insert();
    m.SetFilter(Match, Pattern); // z.B. '*B3*' oder '@*chair*'
    exit(not m.IsEmpty());
end;
```

**Fallstricke:** Funktioniert fuer beliebige Feldtypen (das Demo prueft auch einen Decimal gegen einen Bereichsfilter); dank TableType=Temporary ohne Schema-Deployment-Kosten.

---

## QuerySaveAs

**Technik:** Query-Ergebnisse (auch von Standard-Queries) programmatisch abgreifen: SaveAsCsv in einen TempBlob-Stream, Kopfzeile liefert die Spaltennamen, Zeilen per Split zerlegen und per Evaluate-Kaskade typisiert z.B. in JSON heben.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
Blob.CreateOutStream(OutS);
Sep[1] := 1;                    // Steuerzeichen als Trenner: kollidiert nie mit Daten
q.SaveAsCsv(OutS, 1, Sep);
Blob.CreateInStream(InS);
InS.ReadText(Line);
FieldNames := Line.Split(Sep);  // Kopfzeile = Spaltennamen
while InS.ReadText(Line) > 0 do begin
    Parts := Line.Split(Sep);
    Clear(DataEntry);
    for i := 1 to Parts.Count do
        if Evaluate(DT, Parts.Get(i)) then
            DataEntry.Add(FieldNames.Get(i), DT)
        else if Evaluate(Dec, Parts.Get(i)) then
            DataEntry.Add(FieldNames.Get(i), Dec)
        else if Evaluate(B, Parts.Get(i)) then
            DataEntry.Add(FieldNames.Get(i), B)
        else
            DataEntry.Add(FieldNames.Get(i), Parts.Get(i));
    Data.Add(DataEntry);
end;
```

**Fallstricke:** Die Evaluate-Kaskade RAET Typen — '1.5' wird Decimal, auch wenn Text gemeint war; die Reihenfolge DateTime vor Decimal vor Boolean ist bewusst gewaehlt. Sep[1] := 1 (Char-Zuweisung an Textposition) ist der Trick fuer einen kollisionsfreien Trenner.

---

## FindingDuplicates

**Technik:** Dubletten-Warnung beim Erfassen: OnBeforeValidate auf Name/Adresse, case-insensitive Contains-Filter ('@*wert*') gegen den Bestand, eigene Nummer per '<>%1' ausschliessen; GuiAllowed() schuetzt Webservice-Aufrufe vor Dialogen.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
modify(Name)
{
    trigger OnBeforeValidate()
    var
        Dup: Record Customer;
    begin
        if not GuiAllowed() then
            exit;
        Dup.SetFilter(Name, '@*' + Rec.Name + '*');
        Dup.SetFilter("No.", '<>%1', Rec."No.");
        Dup.SetCurrentKey(Name);
        if Dup.FindFirst() then
            Message('Kunde %1 (%2) existiert schon!', Dup.Name, Dup."No.");
    end;
}
```

**Fallstricke:** Die String-Konkatenation '@*'+Name+'*' bricht, sobald der Name Filterzeichen (*, |, Klammern) enthaelt — fuer Benutzereingaben eigentlich %1-Substitution noetig (siehe setfiltersetrange). Nur Warnung, kein Error: bewusst nicht blockierend.

---

## Query Strings

**Technik:** Eigene URL-Query-Parameter im Web Client lesen (Deep-Links mit Kontext): ein unsichtbares 1x1-Pixel-ControlAddIn liest im StartupScript window.location.search und meldet den Wert per Event an AL zurueck.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
controladdin urlhack
{
    MinimumHeight = 1; MaximumHeight = 1;
    MinimumWidth = 1; MaximumWidth = 1;
    StartupScript = 'startup.js';
    Scripts = 'script.js';
    event GetDemo(Demo: Text);
}

// startup.js:
// var p = new URLSearchParams(window.location.search);
// if (p.has('Demo'))
//     Microsoft.Dynamics.NAV.InvokeExtensibilityMethod("GetDemo", [p.get('Demo')]);

usercontrol(url; urlhack)
{
    ApplicationArea = all;
    trigger GetDemo(Demo: Text)
    begin
        Message('Wert aus URL = %1', Demo);
    end;
}
```

**Fallstricke:** Der Event feuert asynchron nach dem Seitenaufbau — Logik, die den Parameter braucht, gehoert in den Trigger, nicht in OnOpenPage.

---

## FuzzyTextCompare

**Technik:** Fuzzy-Vergleich zweier Texte: Die Standard-Codeunit "Type Helper" bringt TextDistance (Edit-Distanz) fertig mit — vor jedem Eigenbau pruefen; das Demo baut zusaetzlich einen eigenen Aehnlichkeits-QUOTIENTEN (Treffer/Laenge) fuer 'wie aehnlich' statt 'wie viele Edits'.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
var
    TypeHelper: Codeunit "Type Helper";
    Distance: Integer;
    Ratio: Decimal;
begin
    Distance := TypeHelper.TextDistance(A, B); // Levenshtein aus dem Standard
    // Eigenbau-Quotient des Demos: Zeichen-Treffer mit Positionstoleranz
    // diff := StrLen(kurz) div 3 + Abs(l1 - l2);  // erlaubter Versatz
    // Ratio := hit / StrLen(lang);                // 1.0 = identisch
```

**Fallstricke:** TextDistance liefert eine absolute Zahl — fuer 'Duplikat ja/nein' braucht man eine laengennormierte Schwelle, genau dafuer existiert die Eigenbau-Prozedur im Demo.

---

## QueryCategory

**Technik:** Eine einzige Property macht eine Query fuer Endanwender nutzbar: QueryCategory = 'Customer List' haengt sie ohne jede weitere Verdrahtung in das Ansichten-/Analyse-Menue der genannten Listenseite.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
query 50100 "Sales of some sort"
{
    QueryCategory = 'Customer List'; // Name der Ziel-Listenseite(n)
    QueryType = Normal;
    elements
    {
        dataitem(SH; "Sales Header")
        {
            column(No; "No.") { }
            dataitem(SL; "Sales Line")
            {
                DataItemLink = "Document Type" = SH."Document Type",
                               "Document No." = SH."No.";
                column(Amount; Amount) { }
            }
        }
    }
}
```

**Fallstricke:** Mehrere Seiten per kommagetrennter Liste moeglich; der Benutzer bekommt so Join-Sichten, die eine normale Listenseite nie zeigen koennte.

---

## sorting

**Technik:** Find('=') / Find('<') / Find('>') positionieren relativ zu den Feldwerten im Record-PUFFER entlang des aktuellen Schluessels — SetCurrentKey aendert also nicht nur die Reihenfolge von Next(), sondern auch die Positionierungssemantik von Find.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)

```al
C."No." := '30000';
C.Find('=');       // positioniert nach PK auf den Pufferwert
C.Next();          // Next folgt der aktuellen Sortierung (PK)

C.SetCurrentKey(Name);
C."No." := '30000';
C.Find('=');       // jetzt zaehlen die Felder des NAME-Schluessels
C.Next();          // Next laeuft in Namensreihenfolge weiter
```

**Fallstricke:** Nach SetCurrentKey muessen die Felder des neuen Schluessels im Puffer gesetzt sein, sonst positioniert Find woanders als erwartet — die klassische Quelle 'falscher Nachbar bei Next()'.

---

## QueryInSearch

**Technik:** Was eine Query in der Tell-Me-Suche auffindbar macht: UsageCategory (plus Caption) ist der Schalter. QueryType=API macht sie zum Webservice und NICHT suchbar; Access=Public oder Description aendern an der Sichtbarkeit nichts.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)

```al
query 50131 "Query in Search"
{
    UsageCategory = ReportsAndAnalysis; // DAS macht sie in Tell-Me sichtbar
    Caption = 'Query in Search';        // unter diesem Namen findbar
    QueryType = Normal;
    elements { dataitem(Customer; Customer) { column(No; "No.") { } column(Name; Name) { } } }
}
```

**Fallstricke:** Vier-Varianten-Experiment des Autors: API-Queries tauchen trotz UsageCategory nicht in der Suche auf — wer beides will, braucht zwei Query-Objekte.

---

## DecodingRecordID

**Technik:** Das Hex-Layout eines als varbinary gespeicherten RecordID-Felds entschluesseln: Bytes 1-4 sind die Tabellennummer little-endian, danach folgen die PK-Werte mit Typ-/Laengenmarkern als UTF-16LE-Zeichen — noetig nur, wenn man solche Spalten direkt per SQL liest.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)

```al
// '12000000 02 7B FF 43003000300030003100300000000000'
//  12000000 LE = 0x12 = Tabelle 18 (Customer)
//  43 00 30 00 ... = 'C','0','0','0','1','0' (UTF-16LE)
TableNo := GetByte(Hex, 1) + GetByte(Hex, 3) * 256
         + GetByte(Hex, 5) * 65536 + GetByte(Hex, 7) * 16777216;
Char1 := GetByte(Hex, 15) + GetByte(Hex, 17) * 256; // je 4 Hexzeichen = 1 Zeichen
```

**Fallstricke:** In AL selbst braucht man das nie: Format(Rec.RecordId) und Evaluate(RecIdVar, Text) serialisieren einen RecordId verlustfrei als Text (Ordner RecordID zeigt den Roundtrip).

---

## BinaryKeys

**Technik:** HMAC-Ketten mit BINAEREM Schluessel (AWS Signature V4: Schluessel der Stufe n = Digest der Stufe n-1) scheitern an Cryptography Management, weil GenerateHash den Schluessel als Text nimmt — der Hex-String wird als Zeichen gehasht, nicht als Bytes.

**Praxis-Relevanz (Bau-ERP):** ○○○ (0/3)  ·  **Version:** Stand BC18; neuere System-App-Versionen haben erweiterte Crypto-Ueberladungen — vor Verlass nachpruefen.

```al
// Stufe 1 stimmt (Text-Schluessel):
KeyDate := Lowercase(CryptoMgt.GenerateHash(DateToSign, KeyInitial, Alg::HMACSHA256));
// Stufe 2 MUESSTE das binaere Digest als Schluessel nehmen:
KeyRegion := Lowercase(CryptoMgt.GenerateBase64KeyedHash(
    AwsRegion, HexToBase64(KeyDate), Alg::HMACSHA256));
// Workaround-Idee: Hex -> Bytes -> Base64 und GenerateBase64KeyedHash,
// im Demo aber unbestaetigt — Soll- und Ist-Digest weichen ab.
```

**Fallstricke:** Ein Problem-Demo, kein Loesungs-Demo: der Autor schreibt selbst 'not really know if it is ok' und die Message zeigt Soll gegen Ist. Lehre: vor AWS-SigV4-artigen Integrationen pruefen, ob die verfuegbare Crypto-API binaere Schluessel durchreichen kann.

---

## Übersprungen (bewusst)

- ELI5Records (ELI5-Grundlagen ohne Aha)
- ELI5_Filters (Grundlagen, Datei mit Syntaxfehler)
- Filters (gleicher FilterGroup(-1)-Trick wie FilterGroup)
- LookingForRecords (trivialer Upsert)
- Find the right way (FindSet-Standardidiom)
- RecordID (nur Format/Evaluate-Roundtrip, in DecodingRecordID vermerkt)

