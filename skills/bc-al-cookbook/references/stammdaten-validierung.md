# Validierung, Stammdaten, Nummern & Buchung

_Destilliert aus Erik Hougaards Youtube-Video-Sources (Ordnername = Videothema)._
_Vollquellen: https://github.com/hougaard/Youtube-Video-Sources (lokal klonen; Ordnername = Videothema)_

Der Cluster lehrt die komplette Mechanik hinter Feldeingabe und Buchung in BC: die exakte Feuerreihenfolge aller zehn Validierungs-Hooks (Page-Events/Ext-Trigger umschliessen die Tabellen-Kette, der letzte Schreiber gewinnt), dass TableRelation/OnValidate NUR bei Validate() greifen (direkte Zuweisung schreibt beliebige Daten), und wie Werte sauber in Belege und gebuchte Posten fliessen (Standard-Copy-Events, nummerngleiche Extension-Felder fuer TransferFields, OnBeforeInsertGlEntry als Stempel-Hook). Dazu die Zahlen-/Format-Fallen (Formatnummer 9 als kulturinvariantes Austauschformat, Code-Felder sortieren '10' vor '2', ClosingDate ueberlebt keine JSON-Runde) und die zwei Nummernvergabe-Wege (No. Series mit Setup-Tabelle vs. native NumberSequence ohne Locking). Fuer ein Bau-ERP direkt verwertbar sind vor allem die Dimension-Set-Manipulation aus Code, die Direktbuchung ins Hauptbuch und das Vertragsabrechnungs-Muster (ProcessingOnly-Report erzeugt Verkaufsrechnungen) als Blaupause fuer wiederkehrende/Teil-Rechnungen.

**Wertvollste Ordner:** Validate1 · FieldsTransfers · AddFieldToGLEntry · Dimensions · SubscriptionBilling

## Themen (nach Praxis-Relevanz)

- ●●●  **Validate1** — Die vollstaendige Feuerreihenfolge bei Feldeingabe auf einer Page, per Message in jedem Hook sichtbar gemacht. Braucht man immer, wenn mehrere Schichten (Basis-App, Extension, Subscriber) am selben Feld haengen und man wissen muss, wer wen ueberschreibt.
- ●●●  **SubscriptionBilling** — Komplette Mini-Vertragsabrechnung: Contract/Contract-Line-Tabellen mit DateFormula als Abrechnungstakt und Preistabelle je (Item, Frequenz), abgerechnet durch einen ProcessingOnly-Report, der je faellige Zeile Verkaufsrechnungen aus Code erzeugt. Direkte Blaupause fuer wiederkehrende bzw. Abschlags-/Teilrechnungen.
- ●●●  **AddFieldToGLEntry** — Eigenes Feld auf dem Sachposten fuehren: tableextension auf "G/L Entry" mit eigenem Key, Subscriber auf Gen. Jnl.-Post Line OnBeforeInsertGlEntry stempelt den Wert bei JEDER Buchung, und ein Backfill mit Permissions-Attribut versorgt Altposten. Blaupause fuer Kostengliederung/Bauperioden auf FiBu-Ebene.
- ●●●  **PostToTheGLFromCode** — Direkt aus Code ins Hauptbuch buchen, ohne Journal-Batch: Gen. Journal Line nur im Speicher fuellen (nie einfuegen) und je Zeile Codeunit "Gen. Jnl.-Post Line".RunWithCheck aufrufen. Grundlage fuer jede automatische Buchungslogik.
- ●●●  **Postingdescription** — Aussagekraeftige Buchungstexte ohne Basiscode-Eingriff: Subscriber auf OnBeforeReleaseSalesDoc setzt die Posting Description (z. B. aus der ersten Artikelzeile), bevor der Beleg freigegeben und spaeter gebucht wird — der Text landet so in den Sachposten.
- ●●●  **Dimensions** — Der kanonische Weg, einem Beleg aus Code Dimensionen hinzuzufuegen: Dimension-Set-IDs sind unveraenderlich — man holt das bestehende Set als temporaere Records, mischt seine Aenderungen hinein, laesst sich eine NEUE Set-ID geben und aktualisiert die Shortcut-Dimensionen.
- ●●●  **AutoDimension** — Dimensionswerte automatisch je Stammsatz pflegen: Trigger auf der Stammtabelle (hier Job) legt den passenden Dimension Value ('PROJECT' = Job-Nr.) an bzw. haelt dessen Namen synchron. Genau das Muster fuer eine Baustellen-/Projekt-Dimension.
- ●●●  **FieldsTransfers** — Felder zwischen Stammdaten, Belegen und gebuchten Belegen fliessen lassen: erstens ueber die dafuer gebauten Standard-Copy-Events statt eigenem Get, zweitens — der grosse Aha — landet ein Extension-Feld automatisch im gebuchten Beleg, wenn es in beiden Tabellen-Extensions DIESELBE Feldnummer und denselben Typ traegt (TransferFields kopiert nummerngleich).
- ●●●  **NineIsAMagicNumber** — Formatnummer 9 ist das XML-/kulturinvariante Format fuer Evaluate und Format: Dezimalpunkt statt regionsabhaengigem Trenner. Pflicht fuer jeden Maschinen-Datenaustausch (CSV, XML, JSON, API), sonst parst derselbe Code je Server-Region verschieden.
- ●●●  **Number Series** — Das klassische Nummernserien-Muster fuer eigene Stammtabellen: Setup-Tabelle mit TableRelation auf "No. Series", im OnInsert der Stammtabelle GetNextNo, wenn keine Nummer mitgegeben wurde. Dazu IncStr() zum Hochzaehlen von Nummern in Strings.
- ●●○  **ClosingDates** — ClosingDate() erzeugt das Ultimo-Datum (C31.12.) — ein eigener Wertebereich im Date-Typ, der NACH dem normalen Tag sortiert und fuer Jahresabschlussbuchungen reserviert ist. Das Demo zeigt die Serialisierungs-Falle bei JSON.
- ●●○  **DateTime** — Zeitzonen-Arithmetik mit dem Type Helper: drei verschiedene Offsets (benannte Zone, User-Einstellung, Client) als Duration holen und per Plus/Minus auf DateTime rechnen. Noetig, weil BC DateTime als UTC speichert und je Client-Zeitzone anzeigt.
- ●●○  **pesky unicode** — Zeichenweise Eingabe-Validierung: Text-Indexing s[i] liefert den Zeichencode als Integer, Set-Ranges wie ['A'..'Z'] pruefen Zeichenklassen. Faengt unsichtbare Unicode-Zeichen aus Copy-Paste, bevor sie in Schluesselfeldern landen.
- ●●○  **NumberSequence** — Der eingebaute NumberSequence-Datentyp (SQL-Sequenz) als schnelle Alternative zur Nummernserie: Exists/Insert/Next/Range ohne Setup-Tabelle und ohne Tabellen-Locking — fuer hochfrequente interne Nummern (Logeintraege, Rapportzeilen).
- ●●○  **Trim** — Page-Extension-OnBeforeValidate als Normalisierungspunkt: der Wert wird bereinigt (Trim, URL-Normalisierung), BEVOR die Tabellenvalidierung ihn sieht — direkte Anwendung der Validate1-Reihenfolge.
- ●●○  **CombineField** — Ein berechnetes Kombifeld aus mehreren Quellfeldern: AL hat keine Computed Columns, also braucht JEDES Quellfeld seinen eigenen OnAfterValidate-Hook, der das Zielfeld neu aufbaut.
- ●●○  **CodeFields** — Zwei Code-Feld-Wahrheiten: Zuweisung Text->Code macht implizit ToUpper()+Trim(); und Code/Text sortiert als String ('10' vor '2'). Der Laengen-Praefix-Trick erzwingt numerische Sortierung in einem Textfeld — relevant fuer Positionsnummern.
- ●●○  **ClearInit** — Init() vs. Clear() auf Records: Init setzt Nicht-Schluesselfelder auf ihren InitValue (bzw. leer), laesst Primaerschluesselfelder aber unangetastet; ⚠⚠ **BERICHTIGT 01.09.2026 (B): Hier stand „Clear leert alles und ignoriert InitValue“. DAS IST DAS GEGENTEIL DER DOKU.** MS *System.Clear Method* (Remarks): „For a composite data type, such as a record or an array, all elements are cleared. Furthermore, **all fields in a record will be initialized with the InitValue Property of the field**.“ **Clear beachtet InitValue also gerade.** Die Init-Hälfte bleibt richtig (*Record.Init*: „Primary key and timestamp fields aren't initialized“). ⚠ Der Unterschied zwischen Init und Clear liegt damit **nicht** bei InitValue, sondern bei Filtern, Key und Company — und beim Primärschlüssel. Wichtig vor jedem Insert in Schleifen.
- ●●○  **BadDataNoProblem** — TableRelation und OnValidate greifen ausschliesslich bei Validate() bzw. UI-Eingabe — direkte Feldzuweisung plus Modify() schreibt jeden beliebigen Wert in die Datenbank. Erklaert, wie 'unmoegliche' Daten entstehen, und ist zugleich das bewusste Werkzeug fuer Migrationen.
- ●●○  **Validate2** — Zweite und dritte App haengen sich an dieselben Validierungs-Hooks (Event-Subscriber bzw. tableextension-modify-Trigger). Zeigt, was passiert, wenn mehrere Extensions dasselbe Feld validieren.
- ●●○  **RandomData** — Realistische Massen-Demodaten per REST (randomuser.me) und Rest-Client-Codeunit: Kunden mit Insert(true) bei leerer Nummer anlegen (Nummernserie zieht), dann Validate-Kette, CopyStr/MaxStrLen als Laengenschutz gegen API-Daten, Commit je Datensatz.
- ●●○  **Create Config Packages** — RapidStart-Konfigurationspakete programmatisch erzeugen: Config. Package plus Config. Package Table aus Code anlegen, inklusive der Schalter "Exclude Config. Tables" und "Skip Table Triggers" — reproduzierbares Setup fuer Kunden-Onboarding statt Klickarbeit.
- ●○○  **CustomTransformationRule** — Die Transformationsregeln des Data-Exchange-Frameworks (Bankimport, Feld-Mapping) sind event-erweiterbar: eigenen Regelcode im Setup anlegen und die Logik per OnTransformation-Subscriber liefern.
- ●○○  **FormatRecord** — Format() funktioniert auch auf einem ganzen Record und liefert dessen Primaerschluesselwerte als Text — praktisch fuer Logs und Fehlermeldungen. Nur die Standardformate 0-2 und 9 sind fuer Records gueltig.
- ●○○  **Constants** — AL kennt kein const-Schluesselwort: Locked Labels dienen als Text-Konstanten, eine SingleInstance-Codeunit mit Accessor-Prozeduren und Lazy-Cache liefert auch komplexe Konstanten (z. B. JsonObject) app-weit.

---

## Validate1

**Technik:** Die vollstaendige Feuerreihenfolge bei Feldeingabe auf einer Page, per Message in jedem Hook sichtbar gemacht. Braucht man immer, wenn mehrere Schichten (Basis-App, Extension, Subscriber) am selben Feld haengen und man wissen muss, wer wen ueberschreibt.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 8.0 / BC19; Reihenfolge gilt unveraendert auf BC28

```al
// Reihenfolge bei Eingabe im Client (jeder Hook kann Rec ueberschreiben):
//  1. Page  OnBeforeValidateEvent   (Event)
//  2. PageExt  OnBeforeValidate     (modify-Trigger)
//  3. Table OnBeforeValidateEvent   (Event)
//  4. TableExt OnBeforeValidate     (modify-Trigger)
//  5. Table  OnValidate             (Feld-Trigger)
//  6. TableExt OnAfterValidate
//  7. Table OnAfterValidateEvent
//  8. Page   OnValidate             (Feld-Trigger)
//  9. PageExt OnAfterValidate
// 10. Page  OnAfterValidateEvent
codeunit 56100 Hooks
{
    [EventSubscriber(ObjectType::Table, Database::"Validate Table", 'OnBeforeValidateEvent', 'Validate This', true, true)]
    local procedure T_Before(var Rec: Record "Validate Table"; var xRec: Record "Validate Table"; CurrFieldNo: Integer)
    begin
    end;

    [EventSubscriber(ObjectType::Page, Page::"Validate Test", 'OnAfterValidateEvent', 'Validate This', true, true)]
    local procedure P_After(var Rec: Record "Validate Table"; var xRec: Record "Validate Table")
    begin
    end; // Page-Events haben KEIN CurrFieldNo in der Signatur
}
```

**Fallstricke:** Die Page-vor-Tabelle-Intuition ist nur halb richtig: Page-BEFORE-Hooks laufen vor der Tabellen-Kette, der Page-OnValidate-TRIGGER aber erst danach. Jeder der zehn Hooks darf Rec veraendern — der letzte gewinnt still; wer die Reihenfolge nicht kennt, sucht Phantom-Ueberschreiber. Rec.Validate() aus Code startet nur bei Schritt 3 (die Page-Hooks fehlen dann komplett).

---

## SubscriptionBilling

**Technik:** Komplette Mini-Vertragsabrechnung: Contract/Contract-Line-Tabellen mit DateFormula als Abrechnungstakt und Preistabelle je (Item, Frequenz), abgerechnet durch einen ProcessingOnly-Report, der je faellige Zeile Verkaufsrechnungen aus Code erzeugt. Direkte Blaupause fuer wiederkehrende bzw. Abschlags-/Teilrechnungen.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 11.0 / BC22

```al
report 54100 ContractBilling
{
    ProcessingOnly = true; // Report als Batch-Engine: gratis Request-Page mit Filtern
    dataset
    {
        dataitem(Contract; Contract)
        {
            RequestFilterFields = "Contract No.", "Customer No.";
            trigger OnAfterGetRecord()
            begin
                CreateInvoice(Contract);
            end;
        }
    }
}

// Kern von CreateInvoice — Beleg aus Code:
if Lines.LastBillingDate < Today() then begin
    Lines.LastBillingDate := CalcDate(Lines.Frequency, Today()); // DateFormula!
    if not HeaderCreated then begin
        SH.Init();
        SH."Document Type" := SH."Document Type"::Invoice;
        SH.Insert(true);                                  // erst Insert -> Nummernserie
        SH.Validate("Sell-to Customer No.", Contract."Customer No.");
        SH.Modify(true);
        HeaderCreated := true;
    end;
    SL.Init();
    SL."Document Type" := SH."Document Type"; SL."Document No." := SH."No.";
    LineNo += 10000; SL."Line No." := LineNo; SL.Insert(true);
    SL.Validate(Type, SL.Type::Item); SL.Validate("No.", Lines."Item No.");
    SL.Validate(Quantity, 1); SL.Validate("Unit Price", Lines.Price); SL.Modify(true);
end;
```

**Fallstricke:** Reihenfolge ist heilig: Header Insert(true) VOR Validate(Sell-to...), Zeile Insert VOR den Validates von Type/No./Preis. Demo-Bug als Lehrstueck: Lines.LastBillingDate wird gesetzt, aber nie Lines.Modify() gerufen — der Fortschritt geht verloren und die Zeile wird beim naechsten Lauf erneut fakturiert (genau die Fehlerklasse 'verdrahtet, aber nicht wirksam'). DateFormula-Feld + CalcDate ist das saubere Muster fuer Abrechnungstakte; Description als FlowField-Lookup auf Item spart Redundanz.

---

## AddFieldToGLEntry

**Technik:** Eigenes Feld auf dem Sachposten fuehren: tableextension auf "G/L Entry" mit eigenem Key, Subscriber auf Gen. Jnl.-Post Line OnBeforeInsertGlEntry stempelt den Wert bei JEDER Buchung, und ein Backfill mit Permissions-Attribut versorgt Altposten. Blaupause fuer Kostengliederung/Bauperioden auf FiBu-Ebene.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
tableextension 51200 "My G/L Entry" extends "G/L Entry"
{
    fields { field(51200; AccountingPeriod; Integer) { } }
    keys { key(AP; AccountingPeriod) { } } // eigener Key -> filterbar/summierbar
}

codeunit 51200 "Odd Accounting"
{
    Permissions = tabledata "G/L Entry" = RM; // noetig: Sachposten sind sonst nicht modifizierbar

    [EventSubscriber(ObjectType::Codeunit, Codeunit::"Gen. Jnl.-Post Line", 'OnBeforeInsertGlEntry', '', true, true)]
    local procedure Stamp(var GLEntry: Record "G/L Entry")
    begin
        GLEntry.AccountingPeriod := CalcPeriod(GLEntry."Posting Date");
    end;

    internal procedure UpdateAccountingPeriods() // Backfill fuer Altbestand
    var
        Entry: Record "G/L Entry";
    begin
        if Entry.FindSet() then
            repeat
                Entry.AccountingPeriod := CalcPeriod(Entry."Posting Date");
                Entry.Modify();
            until Entry.Next() = 0;
    end;
}
```

**Fallstricke:** OnBeforeInsertGlEntry ist DER Hook, um eigene Felder auf Sachposten zu stempeln — nach dem Insert ist der Posten praktisch unantastbar. Das Permissions = tabledata ... = RM erhoeht die Rechte nur innerhalb dieser Codeunit (endet an der Objektgrenze — Lehre aus dem eigenen Gedaechtnis bestaetigt sich hier). Backfill per FindSet/Modify ohne SetLoadFields ist bei grossen Bestaenden langsam.

---

## PostToTheGLFromCode

**Technik:** Direkt aus Code ins Hauptbuch buchen, ohne Journal-Batch: Gen. Journal Line nur im Speicher fuellen (nie einfuegen) und je Zeile Codeunit "Gen. Jnl.-Post Line".RunWithCheck aufrufen. Grundlage fuer jede automatische Buchungslogik.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
var
    GLPost: Codeunit "Gen. Jnl.-Post Line";
    Line: Record "Gen. Journal Line";
begin
    Line.Init(); // NICHT einfuegen — reine Parameterhuelle
    Line."Posting Date" := Today();
    Line."Document Type" := Line."Document Type"::" ";
    Line."Document No." := 'X000004';
    Line."Account Type" := Line."Account Type"::"G/L Account";
    Line."Account No." := '10910';
    Line.Description := 'Direktbuchung';
    Line.Amount := 70;
    // Variante A: Gegenkonto je Zeile
    // Line."Bal. Account Type" := Line."Bal. Account Type"::"G/L Account";
    // Line."Bal. Account No." := '10920';
    GLPost.RunWithCheck(Line);

    // Variante B: mehrere Zeilen ohne Gegenkonto —
    // muessen sich innerhalb der Transaktion auf 0 saldieren
end;
```

**Fallstricke:** RunWithCheck prueft die EINZELNE Zeile (Datum, Dimensionen, Konto), nicht die Balance — die Bilanzwache ist die Transaktions-Konsistenzpruefung beim Commit. ⚠ **UNBELEGT (Prüfung 01.09.2026, D+B):** Diese Aussage trägt **weder die Demo noch die MS-Doku** — sie ist nicht widerlegt, sondern **unbelegt**. ⚠ **Ein Arbeitspaket in `PLAN-A-Musterzuordnung` baut darauf: vor dem Bau am Bestand MESSEN, nicht übernehmen.** ⚠ **Hier haengt eine BUCHUNG dran (AP-3 Ruecklass/USt).** Wer sich auf eine unbelegte Aussage ueber die Pruefreihenfolge beim Buchen verlaesst, merkt den Irrtum erst an einer schiefen Bilanz. Das Demo bucht absichtlich 70/-30/-41 (Summe -1): jede Zeile laeuft durch, der Commit knallt. Journal Template/Batch bleiben leer, die Buchung taucht in keinem Journal auf — Nachvollziehbarkeit selbst bauen (Document No. diszipliniert vergeben).

---

## Postingdescription

**Technik:** Aussagekraeftige Buchungstexte ohne Basiscode-Eingriff: Subscriber auf OnBeforeReleaseSalesDoc setzt die Posting Description (z. B. aus der ersten Artikelzeile), bevor der Beleg freigegeben und spaeter gebucht wird — der Text landet so in den Sachposten.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
codeunit 50100 Subscribers
{
    [EventSubscriber(ObjectType::Codeunit, Codeunit::"Release Sales Document", OnBeforeReleaseSalesDoc, '', true, true)]
    local procedure SetPostingDescription(var SalesHeader: Record "Sales Header")
    var
        SL: Record "Sales Line";
    begin
        SL.SetRange("Document Type", SalesHeader."Document Type");
        SL.SetRange("Document No.", SalesHeader."No.");
        SL.SetRange(Type, SL.Type::Item);
        if SL.FindFirst() then
            SalesHeader."Posting Description" := SL.Description;
    end;
}
```

**Fallstricke:** Release ist der richtige Zeitpunkt: frueher (Eingabe) wird der Text noch ueberschrieben, spaeter (Buchung) gibt es weniger saubere Hooks. ⚠ **UNBELEGT (Prüfung 01.09.2026, D+B):** Diese Aussage trägt **weder die Demo noch die MS-Doku** — sie ist nicht widerlegt, sondern **unbelegt**. ⚠ **Ein Arbeitspaket in `PLAN-A-Musterzuordnung` baut darauf: vor dem Bau am Bestand MESSEN, nicht übernehmen.** *(AP-3 Ruecklass/USt: Postingdescription)* Der Subscriber schreibt nur ins var-Rec — kein Modify noetig, der Release-Code persistiert. Wer direkt-bucht (ohne Release-Schritt), beachte: Release laeuft im Buchungsprozess implizit mit.

---

## Dimensions

**Technik:** Der kanonische Weg, einem Beleg aus Code Dimensionen hinzuzufuegen: Dimension-Set-IDs sind unveraenderlich — man holt das bestehende Set als temporaere Records, mischt seine Aenderungen hinein, laesst sich eine NEUE Set-ID geben und aktualisiert die Shortcut-Dimensionen.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
procedure UpdateDimSetOnSalesHeader(var SH: Record "Sales Header"; var ToAddDims: Record "Dimension Set Entry" temporary)
var
    DimMgt: Codeunit DimensionManagement;
    NewDimSet: Record "Dimension Set Entry" temporary;
begin
    DimMgt.GetDimensionSet(NewDimSet, SH."Dimension Set ID");
    if ToAddDims.FindSet() then
        repeat
            if NewDimSet.Get(SH."Dimension Set ID", ToAddDims."Dimension Code") then begin
                NewDimSet.Validate("Dimension Value Code", ToAddDims."Dimension Value Code");
                NewDimSet.Modify();
            end else begin
                NewDimSet := ToAddDims;
                NewDimSet."Dimension Set ID" := SH."Dimension Set ID";
                NewDimSet.Insert();
            end;
        until ToAddDims.Next() = 0;
    SH."Dimension Set ID" := DimMgt.GetDimensionSetID(NewDimSet); // neue oder existierende ID
    DimMgt.UpdateGlobalDimFromDimSetID(SH."Dimension Set ID", SH."Shortcut Dimension 1 Code", SH."Shortcut Dimension 2 Code");
end;

// Aufruf: temporaere Dim-Set-Entries fuellen, Prozedur rufen, Rec.Modify()
```

**Fallstricke:** Der haeufigste Fehler entfaellt hier bewusst: NIE direkt in "Dimension Set Entry" schreiben — GetDimensionSetID dedupliziert und legt nur bei Bedarf ein neues Set an. UpdateGlobalDimFromDimSetID nicht vergessen, sonst zeigen Shortcut-Dim-1/2 auf dem Beleg etwas anderes als das Set. Zeilen erben das Header-Set nur bei Neuanlage — bestehende Zeilen muss man selbst nachziehen.

---

## AutoDimension

**Technik:** Dimensionswerte automatisch je Stammsatz pflegen: Trigger auf der Stammtabelle (hier Job) legt den passenden Dimension Value ('PROJECT' = Job-Nr.) an bzw. haelt dessen Namen synchron. Genau das Muster fuer eine Baustellen-/Projekt-Dimension.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
tableextension 50100 MyJob extends Job
{
    trigger OnAfterModify()
    var
        DimValue: Record "Dimension Value";
    begin
        if Rec.Description = '' then
            exit;
        if not DimValue.Get('PROJECT', Rec."No.") then begin
            DimValue.Init();
            DimValue."Dimension Code" := 'PROJECT';
            DimValue.Code := Rec."No.";
            DimValue.Insert(true);
        end;
        DimValue.Validate(Name, CopyStr(Rec.Description, 1, MaxStrLen(DimValue.Name)));
        DimValue.Modify(true);
    end;
}
```

**Fallstricke:** OnAfterModify feuert nicht bei Insert — Neuanlagen brauchen zusaetzlich OnAfterInsert, sonst fehlt die Dimension bis zur ersten Aenderung. Und Modify(false)-Aufrufe aus Fremdcode umgehen den Trigger komplett. CopyStr gegen MaxStrLen: Job-Beschreibung ist laenger als Dimension-Value-Name.

---

## FieldsTransfers

**Technik:** Felder zwischen Stammdaten, Belegen und gebuchten Belegen fliessen lassen: erstens ueber die dafuer gebauten Standard-Copy-Events statt eigenem Get, zweitens — der grosse Aha — landet ein Extension-Feld automatisch im gebuchten Beleg, wenn es in beiden Tabellen-Extensions DIESELBE Feldnummer und denselben Typ traegt (TransferFields kopiert nummerngleich).

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
// 1) Standard-Event nutzen, wenn Kundendaten in den Beleg kopiert werden:
codeunit 50100 "Field Transfers"
{
    [EventSubscriber(ObjectType::Table, Database::"Sales Header",
        'OnAfterCopySellToCustomerAddressFieldsFromCustomer', '', true, true)]
    local procedure CopyMore(var SalesHeader: Record "Sales Header"; SellToCustomer: Record Customer)
    begin
        SalesHeader."Sell-to E-Mail" := SellToCustomer."E-Mail";
    end;
}

// 2) Feld bis in den gebuchten Beleg: gleiche Feldnummer in beiden Extensions
tableextension 50100 SH extends "Sales Header"
{
    fields { field(50100; MyField; Integer) { } }
}
tableextension 50102 SShip extends "Sales Shipment Header"
{
    fields { field(50100; MyField; Integer) { } }  // 50100 == 50100 -> TransferFields nimmt es mit
}
```

**Fallstricke:** Der TransferFields-Automatismus haengt an Feldnummer UND Typ — eine abweichende Nummer in der Shipment-Extension und das Feld kommt nie an, ohne Fehler. Fuer Zeilen gilt dasselbe Spiel (Sales Line -> gebuchte Zeilen). Alternative pro Feld: modify-Trigger mit eigenem Customer.Get, aber die Copy-Events sind der gewartete Weg.

---

## NineIsAMagicNumber

**Technik:** Formatnummer 9 ist das XML-/kulturinvariante Format fuer Evaluate und Format: Dezimalpunkt statt regionsabhaengigem Trenner. Pflicht fuer jeden Maschinen-Datenaustausch (CSV, XML, JSON, API), sonst parst derselbe Code je Server-Region verschieden.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
var
    d, d2 : Decimal;
begin
    // Komma ist im invarianten Format ungueltig -> Evaluate scheitert, d bleibt 0
    if Evaluate(d, '123456,789', 9) then;
    // Punkt parst korrekt, unabhaengig von der Region des Servers/Users
    if Evaluate(d2, '123678.789', 9) then;

    // Ausgaberichtung genauso:
    Message(Format(123456.789, 0, 9)); // '123456.789'
end;
```

**Fallstricke:** Das if...then; ohne else schluckt den Parse-Fehler still — d steht danach auf 0 und rechnet munter weiter; bei Importen den Rueckgabewert IMMER auswerten. Ohne die 9 haengt das Ergebnis an den Regional Settings der NST — der Klassiker, der lokal klappt und in der Cloud bricht. Fuer OENORM-A2063-Dateien (Dezimalwerte im XML) direkt einschlaegig.

---

## Number Series

**Technik:** Das klassische Nummernserien-Muster fuer eigene Stammtabellen: Setup-Tabelle mit TableRelation auf "No. Series", im OnInsert der Stammtabelle GetNextNo, wenn keine Nummer mitgegeben wurde. Dazu IncStr() zum Hochzaehlen von Nummern in Strings.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 6.0 / BC17. NoSeriesManagement ist ab BC24 obsolet — auf BC28 Codeunit "No. Series" (GetNextNo(SeriesCode)) verwenden, Muster bleibt identisch

```al
table 54301 "Dude Setup"
{
    fields
    {
        field(1; PKEY; Code[10]) { }
        field(2; "No. Series for Dude"; Code[20]) { TableRelation = "No. Series".Code; }
    }
    keys { key(PK; PKEY) { Clustered = true; } }
}

// In der Stammtabelle:
trigger OnInsert()
var
    Setup: Record "Dude Setup";
    NoMgt: Codeunit NoSeriesManagement; // BC24+: Codeunit "No. Series"
begin
    if No = '' then begin
        Setup.Get();
        No := NoMgt.GetNextNo(Setup."No. Series for Dude", WorkDate(), true);
    end;
end;

// Setup-Page legt den leeren Setup-Satz selbst an:
if Rec.IsEmpty() then
    Rec.Insert();
```

**Fallstricke:** Das if No = '' ist der Vertrag, der manuelles Vergeben weiter erlaubt — wer ihn weglaesst, ueberschreibt Import-Nummern. Setup.Get() ohne angelegten Setup-Satz wirft; daher das Insert-on-open-Muster auf der Setup-Page.

---

## ClosingDates

**Technik:** ClosingDate() erzeugt das Ultimo-Datum (C31.12.) — ein eigener Wertebereich im Date-Typ, der NACH dem normalen Tag sortiert und fuer Jahresabschlussbuchungen reserviert ist. Das Demo zeigt die Serialisierungs-Falle bei JSON.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
var
    D1, D2 : Date;
    JValue: JsonValue;
begin
    D1 := ClosingDate(Today()); // z. B. C29.08.26 — sortiert nach dem 29.08.
    JValue.SetValue(Format(D1));

    // JValue.AsDate() kommt mit dem C-Praefix nicht klar:
    // D2 := JValue.AsDate();   // <- funktioniert nicht
    Evaluate(D2, JValue.AsText()); // Evaluate versteht 'C...' wieder
end;
```

**Fallstricke:** Ultimo-Daten ueberleben keine typisierte JSON-/API-Runde — nur die Format/Evaluate-Textroute erhaelt das C. Wer G/L-Posten per API liest, verliert die Unterscheidung Abschluss- vs. Normalbuchung, wenn er das Datum als reines Date parst. Fuer AT-Jahresabschluss im Bau-ERP relevant, sobald Hauptbuch-Daten exportiert werden.

---

## DateTime

**Technik:** Zeitzonen-Arithmetik mit dem Type Helper: drei verschiedene Offsets (benannte Zone, User-Einstellung, Client) als Duration holen und per Plus/Minus auf DateTime rechnen. Noetig, weil BC DateTime als UTC speichert und je Client-Zeitzone anzeigt.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 16.0 / BC27

```al
var
    TypeHelper: Codeunit "Type Helper";
    OffsetZone, OffsetUser, OffsetClient : Duration;
    DT: DateTime;
begin
    TypeHelper.GetTimezoneOffset(OffsetZone, 'Pacific Standard Time');
    TypeHelper.GetUserTimezoneOffset(OffsetUser);      // BC-Benutzereinstellung
    TypeHelper.GetUserClientTypeOffset(OffsetClient);  // tatsaechlicher Client

    DT := CurrentDateTime();
    DT -= OffsetZone; // Duration-Arithmetik = Zeitzonen-Umrechnung
    // auch nuetzlich: TypeHelper.GetCurrUTCDateTimeISO8601()
end;
```

**Fallstricke:** Ein in die DB geschriebenes DateTime wird beim Anzeigen WIEDER in die User-Zeitzone gedreht — wer 'Ortszeit der Baustelle' fix speichern will, muss den Offset selbst herausrechnen und dokumentieren, was das Feld bedeutet. Die drei Offsets sind wirklich drei verschiedene Werte; fuer Rapport-Zeitstempel den Client-Offset nehmen.

---

## pesky unicode

**Technik:** Zeichenweise Eingabe-Validierung: Text-Indexing s[i] liefert den Zeichencode als Integer, Set-Ranges wie ['A'..'Z'] pruefen Zeichenklassen. Faengt unsichtbare Unicode-Zeichen aus Copy-Paste, bevor sie in Schluesselfeldern landen.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
tableextension 56700 Customer extends Customer
{
    fields
    {
        modify("No.")
        {
            trigger OnBeforeValidate()
            var
                i: Integer;
            begin
                for i := 1 to StrLen(Rec."No.") do
                    if not (Rec."No."[i] in ['A' .. 'Z', 'a' .. 'z', '0' .. '9']) then
                        Error('Only A-Z 0-9 allowed');
            end;
        }
    }
}

// Diagnose-Aktion: Zeichencodes sichtbar machen
for i := 1 to StrLen(Rec."No.") do
    str += Format(Rec."No."[i]) + ' - ';
```

**Fallstricke:** Der Ausloeser des Videos: aus Word/Websites kopierte Nummern enthalten unsichtbare Zeichen (NBSP, Zero-Width), die zwei optisch identische Schluessel zu verschiedenen Datensaetzen machen. Die Diagnose-Schleife mit Format(s[i]) ist das Werkzeug, um so etwas zu beweisen statt zu raten.

---

## NumberSequence

**Technik:** Der eingebaute NumberSequence-Datentyp (SQL-Sequenz) als schnelle Alternative zur Nummernserie: Exists/Insert/Next/Range ohne Setup-Tabelle und ohne Tabellen-Locking — fuer hochfrequente interne Nummern (Logeintraege, Rapportzeilen).

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 13.0 / BC24

```al
trigger OnOpenPage()
begin
    if not NumberSequence.Exists('youtube') then
        NumberSequence.Insert('youtube', 1234, 1, true); // Name, Start, Schrittweite

    // Einzelnummer:
    // Next := NumberSequence.Next('youtube');

    // Block von 5 Nummern am Stueck reservieren (liefert die ERSTE des Blocks):
    // BERICHTIGT 01.09.2026 (B): Hier stand "liefert die letzte des Blocks". WIDERLEGT.
    //   MS NumberSequence.Range(Text, Integer [, Boolean]): "RangeStart ... Returns the
    //   start of the range from the number sequence."
    //   Wer die letzte annimmt, vergibt die Nummern des Blocks DOPPELT.
    Message('Number %1', NumberSequence.Range('youtube', 5));
end;
```

**Fallstricke:** Sequenzen sind schnell, weil sie NICHT transaktional sauber sind: bei Rollback entstehen Luecken — fuer Belegnummern mit Lueckenlos-Anspruch (Rechnungen!) ungeeignet, dafuer ideal fuer interne IDs ohne Sperr-Contention auf der No.-Series-Zeile. Die Sequenz lebt in der Datenbank, nicht in der App — Deinstallation raeumt sie nicht auf.

---

## Trim

**Technik:** Page-Extension-OnBeforeValidate als Normalisierungspunkt: der Wert wird bereinigt (Trim, URL-Normalisierung), BEVOR die Tabellenvalidierung ihn sieht — direkte Anwendung der Validate1-Reihenfolge.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 13.0 / BC24 (.Trim/.TrimEnd sind Text-Methoden)

```al
pageextension 50100 Ext extends "Customer Card"
{
    layout
    {
        modify(Name)
        {
            trigger OnBeforeValidate()
            begin
                Rec.Name := Rec.Name.Trim(); // laeuft VOR Table-OnValidate
            end;
        }
        modify("Home Page")
        {
            trigger OnBeforeValidate()
            begin
                Rec."Home Page" := Rec."Home Page".Trim().TrimEnd('/') + '/contact.html';
            end;
        }
    }
}
```

**Fallstricke:** Die Normalisierung greift nur bei UI-Eingabe ueber DIESE Page — API, Import und Code-Validate laufen daran vorbei. Wer die Regel hart braucht, legt sie zusaetzlich (oder stattdessen) in den Tabellen-Trigger.

---

## CombineField

**Technik:** Ein berechnetes Kombifeld aus mehreren Quellfeldern: AL hat keine Computed Columns, also braucht JEDES Quellfeld seinen eigenen OnAfterValidate-Hook, der das Zielfeld neu aufbaut.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
tableextension 50100 GL extends "Gen. Journal Line"
{
    fields
    {
        field(50100; SharePointFolder; Text[30]) { }
        modify("Document No.")
        {
            trigger OnAfterValidate()
            begin
                UpdateCombined();
            end;
        }
        modify("Posting Date")
        {
            trigger OnAfterValidate()
            begin
                UpdateCombined();
            end;
        }
    }
    local procedure UpdateCombined()
    begin
        SharePointFolder := Rec."Document No." + ' ' + Format(Rec."Posting Date");
    end;
}
```

**Fallstricke:** Direkte Zuweisungen an die Quellfelder (ohne Validate) lassen das Kombifeld veralten — der klassische stille Drift. Format(Date) ohne Formatnummer im gespeicherten Wert ist locale-abhaengig; fuer stabile Schluessel Format(..., 0, 9) nehmen.

---

## CodeFields

**Technik:** Zwei Code-Feld-Wahrheiten: Zuweisung Text->Code macht implizit ToUpper()+Trim(); und Code/Text sortiert als String ('10' vor '2'). Der Laengen-Praefix-Trick erzwingt numerische Sortierung in einem Textfeld — relevant fuer Positionsnummern.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
// Implizite Code-Konvertierung:
var
    T: Text;
    C: Code[10];
begin
    T := ' 1 ';
    C := T;                        // C = '1'  (ToUpper + Trim automatisch)
end;

// Numerische Sortierung emulieren: 1. Zeichen = Laenge als Ziffer
// '5' -> '15', '10' -> '210'  =>  sortiert 5 vor 10
table 50132 "Code Table"
{
    fields
    {
        field(1; Primary; Text[20]) { }
        field(2; Display; Text[19])
        {
            trigger OnValidate()
            begin
                Primary := ' ' + Display;
                Primary[1] := StrLen(Display) + 48; // 48 = '0'
            end;
        }
    }
    keys { key(P; Primary) { } }
}
```

**Fallstricke:** String-Indexing schreibt direkt ins Feld (Primary[1] := ...) — Zeichen sind zuweisbare Integer. Der Trick traegt nur bis Laenge 9; darueber braucht das Praefix mehr Stellen. Fuer LV-Positionsnummern die Alternative bedenken: fuehrende Nullen beim Erfassen.

---

## ClearInit

**Technik:** Init() vs. Clear() auf Records: Init setzt Nicht-Schluesselfelder auf ihren InitValue (bzw. leer), laesst Primaerschluesselfelder aber unangetastet; ⚠⚠ **BERICHTIGT 01.09.2026 (B): Hier stand „Clear leert alles und ignoriert InitValue“. DAS IST DAS GEGENTEIL DER DOKU.** MS *System.Clear Method* (Remarks): „For a composite data type, such as a record or an array, all elements are cleared. Furthermore, **all fields in a record will be initialized with the InitValue Property of the field**.“ **Clear beachtet InitValue also gerade.** Die Init-Hälfte bleibt richtig (*Record.Init*: „Primary key and timestamp fields aren't initialized“). ⚠ Der Unterschied zwischen Init und Clear liegt damit **nicht** bei InitValue, sondern bei Filtern, Key und Company — und beim Primärschlüssel. Wichtig vor jedem Insert in Schleifen.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
table 50118 "Test Table"
{
    fields
    {
        field(1; Primary; Code[20]) { InitValue = 'ABC'; }   // PK
        field(3; Texti; Text[100]) { InitValue = 'Hello'; }
        field(4; ANumber; Decimal) { InitValue = 123.45; }
    }
    keys { key(PK; Primary) { } }
}

var
    x, y : Record "Test Table";
begin
    Clear(x);      // alles leer/0 — InitValue wird ignoriert
    y.Texti := '';
    y.Init();      // Texti='Hello', ANumber=123.45 — aber Primary bleibt '' (PK!)
end;
```

**Fallstricke:** Init() ueberschreibt bereits gesetzte Nicht-PK-Felder mit dem InitValue (die vorherige Zuweisung ist weg) und setzt den Primaerschluessel NIE — auch dessen InitValue verpufft. Wer in einer Schleife Record-Variablen wiederverwendet, braucht Clear+Init oder setzt den PK explizit, sonst schleppen sich PK-Reste aus dem Voraufruf mit.

---

## BadDataNoProblem

**Technik:** TableRelation und OnValidate greifen ausschliesslich bei Validate() bzw. UI-Eingabe — direkte Feldzuweisung plus Modify() schreibt jeden beliebigen Wert in die Datenbank. Erklaert, wie 'unmoegliche' Daten entstehen, und ist zugleich das bewusste Werkzeug fuer Migrationen.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
pageextension 50132 CustomerListExt extends "Customer List"
{
    trigger OnOpenPage()
    var
        Cust: Record Customer;
    begin
        Cust.FindFirst();
        // 'YOUTUBE' existiert nicht in der Tax-Area-Tabelle:
        Cust."Tax Area Code" := 'YOUTUBE'; // kein Validate -> TableRelation ungeprueft
        Cust.Modify(false);                // schreibt anstandslos
    end;
}
```

**Fallstricke:** BC prueft referentielle Integritaet NICHT auf Datenbankebene — TableRelation ist reine Validate-Zeit-Logik. Konsequenz fuer eigene Auswertungen: nie darauf vertrauen, dass ein Fremdschluesselwert existiert; und bei Datenimporten entscheidet die Wahl Validate vs. Zuweisung, welche Geschaeftslogik mitlaeuft.

---

## Validate2

**Technik:** Zweite und dritte App haengen sich an dieselben Validierungs-Hooks (Event-Subscriber bzw. tableextension-modify-Trigger). Zeigt, was passiert, wenn mehrere Extensions dasselbe Feld validieren.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
// App 2: Subscriber auf fremde Tabelle
codeunit 56200 "Validate Events 2"
{
    [EventSubscriber(ObjectType::Table, Database::"Validate Table", 'OnBeforeValidateEvent', 'Validate This', true, true)]
    local procedure B(var Rec: Record "Validate Table"; var xRec: Record "Validate Table"; CurrFieldNo: Integer)
    begin
        Rec."Validate This" := 'App2 war hier';
    end;
}

// App 3: modify-Trigger auf fremde Tabelle
tableextension 56300 "Validate ext3" extends "Validate Table"
{
    fields
    {
        modify("Validate This")
        {
            trigger OnBeforeValidate()
            begin
                Rec."Validate This" := 'App3 war hier';
            end;
        }
    }
}
```

**Fallstricke:** Innerhalb einer Hook-Stufe ist die Reihenfolge ZWISCHEN Apps nicht definiert (haengt an Abhaengigkeits-/Installationsreihenfolge). Zwei Apps, die denselben Hook beschreiben, ueberschreiben einander still — es gibt keinen Konflikt-Fehler, nur den letzten Schreiber.

---

## RandomData

**Technik:** Realistische Massen-Demodaten per REST (randomuser.me) und Rest-Client-Codeunit: Kunden mit Insert(true) bei leerer Nummer anlegen (Nummernserie zieht), dann Validate-Kette, CopyStr/MaxStrLen als Laengenschutz gegen API-Daten, Commit je Datensatz.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 13.0 / BC24 (Codeunit "Rest Client")

```al
Data := Rest.GetAsJson('https://randomuser.me/api/?results=1000').AsObject();
foreach T in JSONTools.GetArray(Data, 'results') do begin
    Person := T.AsObject();
    Customer.Init();
    Customer."No." := '';        // leer -> OnInsert vergibt Nummernserie
    Customer.Insert(true);
    Name := JSONTools.GetObj(Person, 'name');
    Location := JSONTools.GetObj(Person, 'location');
    Customer.Validate(Name, JSONTools.GetText(Name, 'first') + ' ' + JSONTools.GetText(Name, 'last'));
    Customer.City := CopyStr(JSONTools.GetText(Location, 'city'), 1, MaxStrLen(Customer.City));
    // Land per Wildcard-Filter suchen, sonst anlegen:
    Country.SetFilter(Name, '@*' + JSONTools.GetText(Location, 'country') + '*');
    if Country.FindFirst() then
        Customer.Validate("Country/Region Code", Country.Code);
    Customer.Modify(false);
    Commit();
end;
```

**Fallstricke:** Erst Insert(true), DANN Validate der Felder — viele Customer-Validierungen brauchen den existierenden Datensatz. Der @*...*-Filter ist die case-insensitive Contains-Suche. CopyStr mit MaxStrLen ist bei Fremddaten Pflicht (Feldlaengen-Falle). Das Commit je Satz macht den Lauf abbrechbar, verhindert aber sauberes Rollback.

---

## Create Config Packages

**Technik:** RapidStart-Konfigurationspakete programmatisch erzeugen: Config. Package plus Config. Package Table aus Code anlegen, inklusive der Schalter "Exclude Config. Tables" und "Skip Table Triggers" — reproduzierbares Setup fuer Kunden-Onboarding statt Klickarbeit.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 6.0 / BC17

```al
procedure CreateConfigPackage()
var
    ConfigPackage: Record "Config. Package";
begin
    ConfigPackage.Init();
    ConfigPackage.Validate(Code, 'YOUTUBE');
    ConfigPackage.Insert(true);
    ConfigPackage.Validate("Package Name", 'Youtube Video Example');
    ConfigPackage.Validate("Exclude Config. Tables", true);
    ConfigPackage.Validate("Product Version", 'YOU1.0');
    ConfigPackage.Modify(true);

    AddTable(ConfigPackage, Database::Customer);
    AddTable(ConfigPackage, Database::Item);
end;

procedure AddTable(CP: Record "Config. Package"; TableNo: Integer)
var
    ConfigTable: Record "Config. Package Table";
begin
    ConfigTable.Init();
    ConfigTable."Package Code" := CP.Code;
    ConfigTable.Validate("Table ID", TableNo);
    ConfigTable.Insert(true);
    ConfigTable.Validate("Skip Table Triggers", true);
    ConfigTable.Modify(true);
end;
```

**Fallstricke:** Auch hier das Insert-dann-Validate-Muster (Validate("Table ID") zieht Metadaten nach dem Insert). "Skip Table Triggers" entscheidet beim Import ueber Geschaeftslogik an/aus — bewusst setzen, das ist dieselbe Weiche wie Validate vs. Zuweisung aus BadDataNoProblem. Fuer ein Bau-ERP: Demo-/Startdaten als Paket ausliefern statt per Skript.

---

## CustomTransformationRule

**Technik:** Die Transformationsregeln des Data-Exchange-Frameworks (Bankimport, Feld-Mapping) sind event-erweiterbar: eigenen Regelcode im Setup anlegen und die Logik per OnTransformation-Subscriber liefern.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** runtime 5.0 (alt, Muster unveraendert gueltig)

```al
codeunit 50114 "Custom transformation"
{
    [EventSubscriber(ObjectType::Table, Database::"Transformation Rule", 'OnTransformation', '', false, false)]
    local procedure OnTransformation(TransformationCode: Code[20]; InputText: Text; var OutputText: Text)
    var
        i: Integer;
    begin
        case TransformationCode of
            'AAA': // Regel 'AAA' muss als Custom-Regel im Setup existieren
                begin
                    OutputText := '';
                    for i := 1 to StrLen(InputText) do
                        OutputText += InputText[StrLen(InputText) - i + 1];
                end;
        end;
    end;
}
```

**Fallstricke:** Der Subscriber wird fuer JEDE Custom-Regel gerufen — ohne das case-Gate auf den eigenen Code verfaelscht man fremde Regeln. Nuetzlich ueberall, wo Datenaustausch-Definitionen (CAMT-Import, Positionsdaten) ein Format brauchen, das die Standardregeln nicht koennen.

---

## FormatRecord

**Technik:** Format() funktioniert auch auf einem ganzen Record und liefert dessen Primaerschluesselwerte als Text — praktisch fuer Logs und Fehlermeldungen. Nur die Standardformate 0-2 und 9 sind fuer Records gueltig.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)

```al
Rec.FindFirst();
Message(Format(Rec));        // Default: PK-Werte als Text
Message(Format(Rec, 0, 1));
Message(Format(Rec, 0, 2));
Message(Format(Rec, 0, 9));  // maschinenlesbare Variante
// Format(Rec, 0, 3..8) -> Laufzeitfehler (im Demo auskommentiert)
```

**Fallstricke:** Die Formatnummern 3-8 werfen fuer Records zur Laufzeit — der Compiler warnt nicht. Fuer Fehlermeldungen ist Format(Rec) die schnellste Art, den betroffenen Datensatz zu benennen, ohne Felder einzeln zu verketten.

---

## Constants

**Technik:** AL kennt kein const-Schluesselwort: Locked Labels dienen als Text-Konstanten, eine SingleInstance-Codeunit mit Accessor-Prozeduren und Lazy-Cache liefert auch komplexe Konstanten (z. B. JsonObject) app-weit.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** runtime 12.0 / BC23 (namespace-Syntax)

```al
codeunit 50100 "My Constants"
{
    SingleInstance = true;

    procedure Welcome(): Text
    begin
        exit(WelcomeLbl);
    end;

    procedure Data(): JsonObject
    begin
        if not DataCached then begin
            _Data.ReadFrom(JsonLbl);
            DataCached := true;
        end;
        exit(_Data);
    end;

    var
        DataCached: Boolean;
        _Data: JsonObject;
        JsonLbl: Label '{"hello":"Hello"}', Locked = true;
        WelcomeLbl: Label 'Hello YouTube', Locked = true;
}
```

**Fallstricke:** Locked = true ist der eigentliche Konstanten-Marker — ohne ihn wandert der Label-Text in die Uebersetzung und kann je Sprache abweichen. SingleInstance-Zustand lebt fuer die ganze Session: der JSON-Cache wird genau einmal geparst, aber auch nie invalidiert.

---

## Übersprungen (bewusst)

- validate3 — in Validate2-Topic destilliert
- AutoFormat — nur Hello-World-Geruest
- format — duenner Format-Einzeiler
- LineNumbers — nur Hello-World-Geruest
- StringFunctions — triviale Substring-Demo
- FunkyNumbers — Nischen-QuickBooks-Trick
- HexNumbers — IntToHex-Einzeiler
- TrueCase — bekanntes case-Idiom
- DateVsDateTime — triviale Duration-Demo
- Unicode stuff — Unicode-Spielerei
- generatedata — schlichter Insert-Loop

