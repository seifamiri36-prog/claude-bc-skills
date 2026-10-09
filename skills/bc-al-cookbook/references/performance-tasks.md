# Performance, Hintergrund-Tasks & Datentypen

_Destilliert aus Erik Hougaards Youtube-Video-Sources (Ordnername = Videothema)._
_Vollquellen: https://github.com/hougaard/Youtube-Video-Sources (lokal klonen; Ordnername = Videothema)_

Der Cluster lehrt drei Dinge. Erstens, wie BC-Schreib- und String-Performance wirklich entsteht: der NST puffert aufeinanderfolgende Inserts zu SQL-Bulk-Inserts (und der Insert()-Rückgabewert zerstört das), TextBuilder schlägt +=, ModifyAll ist ein einzelnes UPDATE, und eine FEHLSCHLAGENDE TryFunction kostet Größenordnungen mehr als ein Evaluate mit Format 9. Zweitens das komplette Hintergrund-Handwerk: StartSession mit temporärem Parameter-Record und Log-Tabelle als Rückkanal, Job-Queue-taugliche Codeunits über TableNo=Job Queue Entry, ein selbstheilender Job-Restarter — plus die Falle, dass Time() in Hintergrund-Sessions Server-/UTC-Zeit liefert, während DateTime-Felder zeitzonenfest bleiben. Drittens Datentyp-Semantik mit Sprengkraft: TryFunctions rollen DB-Schreiber NICHT zurück, JsonObject ist Referenztyp (var irrelevant für Mutation), Date rechnet in Tagen aber Time/Duration in Millisekunden, und der Type-Helper-Codeunit parst kulturabhängige Zahlen wie '10.000,5' korrekt — direkt relevant für AT/DE-Importe.

**Wertvollste Ordner:** TryFunctionDatabase · BulkInsert · TheTimeProblem · MultiTasking · TypeHelper

## Themen (nach Praxis-Relevanz)

- ●●●  **TypeHelper** — Der System-Codeunit "Type Helper" parst und formatiert kulturabhängig (.NET-Formatstrings + CultureName) — der korrekte Weg, um Zahlen wie '10.000,5' aus deutsch-/österreichischen Quellen als Decimal zu lesen, wo das normale Evaluate scheitert oder falsch rundet.
- ●●●  **TryFunctionDatabase** — Die gefährlichste TryFunction-Eigenschaft: ein per TryFunction ABGEFANGENER Fehler rollt laufende Schreibtransaktionen NICHT zurück — Modify() vor dem Fehler bleibt in der DB stehen. Wer Try mit Rollback will, nimmt if Codeunit.Run(...).
- ●●●  **SlowToTryFunction** — Ein FEHLSCHLAGENDER TryFunction-Aufruf ist um Größenordnungen teurer als ein fehlschlagendes Evaluate (Exception-Maschinerie je Aufruf) — in Parse-Schleifen über Importdaten Evaluate mit Format 9 als Prüfer verwenden.
- ●●●  **BulkInsert** — BC bündelt aufeinanderfolgende Insert()-Aufrufe automatisch zu SQL-Bulk-Inserts — aber nur, solange der Code das Ergebnis nicht sofort braucht. Den Rückgabewert von Insert() abzufragen erzwingt Einzel-INSERTs und zerstört die Optimierung.
- ●●●  **MultiTasking** — Das komplette StartSession-Muster: Eingabe über einen TableType=Temporary-Parameter-Record, Rückkanal über eine echte Log-Tabelle mit GUID-Korrelation, plus DebugMode-Schalter, der denselben Code synchron über Codeunit.Run laufen lässt.
- ●●●  **JobRestarter** — Selbstheilende Job Queue: ein eigener, wiederkehrend geplanter Wächter-Job filtert Einträge mit Status=Error und startet sie per JQ.Restart() neu; WELCHE Jobs er bewacht, steuert sein Parameter String als Objekt-ID-Filter.
- ●●●  **Temporary Tables** — Die drei Temporär-Mechanismen in AL: temporary-Record-Variable einer echten Tabelle, Seite mit SourceTableTemporary=true (per Page.Run mit dem gefüllten Temp-Record verbunden) und TableType=Temporary als Tabellenobjekt, das nie in SQL existiert.
- ●●●  **BatchPostAndEmail** — Standard-Stapelbuchung erweitern statt nachbauen: reportextension auf "Batch Post Sales Orders" hängt eine eigene Option auf die Request Page und hookt sich mit OnAfterAfterGetRecord je Beleg ein.
- ●●●  **TheTimeProblem** — Time() und CurrentDateTime() liefern die Zeit der SESSION-Zeitzone: im Web-Client die des Benutzers, in TaskScheduler-/StartSession-/Job-Queue-Sessions die des Servers (SaaS: UTC). Derselbe Codeunit schreibt je nach Startweg verschiedene Uhrzeiten.
- ●●○  **Optimize your string operations** — TextBuilder statt +=-Konkatenation in Schleifen — jede +=-Operation kopiert den kompletten String (O(n²)); TextBuilder.Append ist amortisiert konstant. Zweite Lehre der Demo: für Base64 den System-Codeunit "Base64 Convert" nehmen statt Eigenbau.
- ●●○  **TypeConversion** — Die eingebauten Arithmetik-Regeln der Datums-/Zeittypen: Date rechnet in TAGEN, Time und Duration in MILLISEKUNDEN — Differenzen und Additionen mischen Integer und Zeittypen implizit, jeweils in der Einheit des Typs.
- ●●○  **Variants** — Variant-Parameter machen Prozeduren typoffen für beliebige Records: mit IsRecord prüfen, per RecordRef.GetTable an die Metadaten, und ein Record-Variant lässt sich direkt an Codeunit.Run und Page.RunModal weiterreichen — eine Log-/Utility-Funktion für alle Tabellen.
- ●●○  **VariableSizedRecords** — Schemafreier Dokument-Store in BC (Azure-Table-Storage-Stil): Entity+Document-Tabellen, JSON-Payload hybrid gespeichert — klein in Text-Feldern (eine Leseoperation, filterbar), gross im Blob; generische Listenseite mit Spalten-Slots, deren Überschriften zur Laufzeit via CaptionClass + OnResolveCaptionClass aufgelöst werden.
- ●●○  **Batch Jobs** — ProcessingOnly-Report als Gratis-Batch-UI: Request Page mit RequestFilterFields und eigenen Optionen kommt geschenkt, in OnPreDataItem übergibt man den vom Benutzer vorgefilterten Record an die eigentliche Verarbeitungs-Codeunit.
- ●●○  **ToVarOrNotToVar** — var entscheidet bei Werttypen (Text, Integer, Record) über Kopie vs. Durchgriff — JsonObject/JsonArray sind aber REFERENZtypen: der Callee verändert das Objekt des Aufrufers auch OHNE var. Bei IntegrationEvents bestimmen var-Parameter, ob Subscriber Werte zurückgeben können.
- ●●○  **JobQueueFriendlyCodeunit** — Job-Queue-taugliche Codeunit: TableNo = "Job Queue Entry" macht Parameter String und Kategorie zur Konfiguration — und ein leerer Entry (Object ID to Run = 0) verrät, dass die Codeunit direkt statt vom Scheduler aufgerufen wurde.
- ●●○  **DeleteRecords** — Selektives Löschen WÄHREND einer FindSet-Iteration funktioniert, weil BC das Resultset liest, bevor gelöscht wird — und FindSet(true) ist zum Löschen nicht nötig (der Parameter steuert Sperrverhalten, nicht Erlaubnis).
- ●●○  **ModifyAll** — ModifyAll ohne Validierung ist EIN SQL-UPDATE über den Filter; mit Validate-Parameter oder bei mehreren Feldern wird zeilenweise gearbeitet — ab zwei Feldern ist die eigene FindSet(true)-Schleife billiger als zwei ModifyAll.
- ●●○  **TryFunction** — Das Grundmuster für werfende Konvertierungen: [TryFunction]-Prozedur kapselt JsonValue.AsDecimal() u.ä. in ein Boolean, Ergebnis kommt über var-Parameter zurück, GetLastErrorText() liefert die Ursache.
- ●●○  **CalcTime** — AL hat CalcDate, aber kein CalcTime — Eigenbau parst Ausdrücke wie '1W4H' oder '-1H30M' zu einer Duration; Time-Werte rechnet man als Integer-Millisekunden relativ zur Konstante 000000T. Nebenbei: AL kann Prozedur-Überladung (zwei CalcTime mit verschiedenen Signaturen).
- ●●○  **Global Local** — Ein Seitenfeld, das an eine Prozedur gebunden ist, wird bei JEDEM UI-Roundtrip für jede sichtbare Zeile neu ausgewertet — die Demo macht das mit Random() sichtbar (Werte springen beim Scrollen). Teure Logik gehört nicht in prozedur-gebundene Felder.
- ●○○  **MedusaRecords** — Absturz-Forensik für Operationen, die eine Session einfrieren/töten (hier: die virtuelle Tabelle "Report Data Items" je Report lesen): jede riskante Prüfung in eine Wegwerf-Session isolieren und VOR dem Zugriff einen Schuld-Marker mit Commit setzen — stirbt die Session, bleibt der Marker als Beweis.

---

## TypeHelper

**Technik:** Der System-Codeunit "Type Helper" parst und formatiert kulturabhängig (.NET-Formatstrings + CultureName) — der korrekte Weg, um Zahlen wie '10.000,5' aus deutsch-/österreichischen Quellen als Decimal zu lesen, wo das normale Evaluate scheitert oder falsch rundet.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
var
    TypeHelper: Codeunit "Type Helper";
    V: Variant;
    d: Decimal;
    Culture: Text;
begin
    Culture := TypeHelper.LanguageIDToCultureName(1030); // 'da-DK'
    // de-AT waere Language-ID 3079

    V := d;  // Variant VORHER auf den Zieltyp setzen!
    TypeHelper.Evaluate(V, '10.000,5', 'G', Culture);
    d := V;  // 10000.5

    Message(TypeHelper.FormatDecimal(d, 'G', Culture));
    // Bonus: TypeHelper.UrlEncode(t) fuer Query-Strings
end;
```

**Fallstricke:** TypeHelper.Evaluate arbeitet über einen Variant, der VOR dem Aufruf bereits den Zieltyp tragen muss (V := d) — sonst weiss die Funktion nicht, in was sie parsen soll. LanguageIDToCultureName übersetzt Windows-Language-IDs in .NET-Culture-Namen.

---

## TryFunctionDatabase

**Technik:** Die gefährlichste TryFunction-Eigenschaft: ein per TryFunction ABGEFANGENER Fehler rollt laufende Schreibtransaktionen NICHT zurück — Modify() vor dem Fehler bleibt in der DB stehen. Wer Try mit Rollback will, nimmt if Codeunit.Run(...).

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 15 / BC 26 — Verhalten gilt unverändert auf BC 28

```al
[TryFunction]
procedure TryUpdate()
var
    d, z: Decimal;
begin
    Rec.FindFirst();
    Rec.Name := 'Test 102';
    Rec.Modify();      // ueberlebt den gefangenen Fehler!
    d := 10 / z;       // Division durch 0 -> gefangen
end;

// Aufrufer:
if not TryUpdate() then
    Message('Fehler gefangen — aber Modify() ist geschrieben');

// Alternative MIT Rollback (eigene Transaktion):
codeunit 50100 "Try"
{
    trigger OnRun()
    var d, z: Decimal;
    begin
        d := 10 / z;
    end;
}
// if not Codeunit.Run(Codeunit::"Try") then ... // rollt zurueck
```

**Fallstricke:** Kein automatischer Rollback bei gefangenem Fehler — wer in einer TryFunction schreibt, muss den Zustand selbst reparieren; in Buchungsnähe deshalb Codeunit.Run als Try-Ersatz (verlangt aber, dass keine eigene Schreibtransaktion offen ist — sonst Commit-Zwang beachten).

---

## SlowToTryFunction

**Technik:** Ein FEHLSCHLAGENDER TryFunction-Aufruf ist um Größenordnungen teurer als ein fehlschlagendes Evaluate (Exception-Maschinerie je Aufruf) — in Parse-Schleifen über Importdaten Evaluate mit Format 9 als Prüfer verwenden.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 16 / BC 27

```al
// LANGSAM bei Fehlschlag (10.000x auf 'ABC' -> Sekunden):
[TryFunction]
local procedure TryIsDate(T: JsonToken; var OutDate: Date)
begin
    OutDate := T.AsValue().AsDate();
end;

// SCHNELL (gleiche Schleife -> Millisekunden):
local procedure IsDate(T: JsonToken; var OutDate: Date): Boolean
begin
    exit(Evaluate(OutDate, T.AsValue().AsText(), 9));
end;
// Format 9 = XML/invariant — Pflicht fuer JSON/XML-Werte
```

**Fallstricke:** Evaluate ohne Format 9 parst regional (die Demo zeigt beide Messages nebeneinander) — JSON/XML-Datumswerte immer mit 9. Die Kosten entstehen nur im FEHLERfall; erfolgreiche Tries sind billig — kritisch also genau bei Validierungsschleifen über schmutzige Daten.

---

## BulkInsert

**Technik:** BC bündelt aufeinanderfolgende Insert()-Aufrufe automatisch zu SQL-Bulk-Inserts — aber nur, solange der Code das Ergebnis nicht sofort braucht. Den Rückgabewert von Insert() abzufragen erzwingt Einzel-INSERTs und zerstört die Optimierung.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 8 / BC 19

```al
var
    B: Record Bulk;
    i: Integer;
begin
    for i := 1 to 10000 do begin
        B.Init();
        B.PK := i;
        B.Data := '...';
        B.Insert();   // NST puffert -> Bulk-Insert an SQL
        // NICHT: if not B.Insert() then Error('...');
        //  -> Rueckgabewert erzwingt sofortiges Einzel-INSERT,
        //     der Bulk-Puffer ist tot
    end;
    Commit();
end;
```

**Fallstricke:** Bulk-Puffer stirbt auch bei: AutoIncrement-Feldern, Blob/Media-Feldern, Lesezugriff auf dieselbe Tabelle zwischen den Inserts. Die auskommentierte if-not-Insert-Zeile im Original ist genau der Demo-Punkt. Für Massenimporte (Aufmaßzeilen!) das Prüfmuster nach die Schleife legen, nicht je Zeile.

---

## MultiTasking

**Technik:** Das komplette StartSession-Muster: Eingabe über einen TableType=Temporary-Parameter-Record, Rückkanal über eine echte Log-Tabelle mit GUID-Korrelation, plus DebugMode-Schalter, der denselben Code synchron über Codeunit.Run laufen lässt.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 14 / BC 25

```al
table 50100 "StartSession Parameter"
{
    TableType = Temporary; // nie in SQL — reiner Parameter-Container
    fields { field(1; CustomerNo; Code[20]) { } field(3; LogId; Guid) { } }
}

codeunit 50100 "The Works"
{
    TableNo = "StartSession Parameter";
    trigger OnRun()
    var
        Log: Record "Session Log";
    begin
        // ... Arbeit ...
        Log.Id := Rec.LogId;
        Log.SessionId := SessionId();
        Log.Insert();   // Ergebnis via echte Tabelle zurueck
    end;
}

// Aufrufer:
Parm.CustomerNo := 'hello';
Parm.LogId := CreateGuid();
if DebugMode then
    Codeunit.Run(Codeunit::"The Works", Parm) // synchron debugbar
else
    StartSession(SessionNo, Codeunit::"The Works", CompanyName(), Parm);
```

**Fallstricke:** Die Kind-Session hat eine eigene Transaktion — Ergebnisse kommen NUR über die Datenbank zurück, nicht über var-Parameter. Der Debugger hängt sich nicht an StartSession-Sessions — deshalb der DebugMode-Schalter als fester Bestandteil des Musters. TableType=Temporary als Objekt kostet kein SQL-Schema.

---

## JobRestarter

**Technik:** Selbstheilende Job Queue: ein eigener, wiederkehrend geplanter Wächter-Job filtert Einträge mit Status=Error und startet sie per JQ.Restart() neu; WELCHE Jobs er bewacht, steuert sein Parameter String als Objekt-ID-Filter.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
codeunit 54600 "Job Queue Restarter"
{
    TableNo = "Job Queue Entry";
    trigger OnRun()
    var
        JQ: Record "Job Queue Entry";
    begin
        JQ.SetRange(Status, JQ.Status::Error);
        // Parameter String des Waechter-Eintrags = Filter,
        // z.B. '50100|50200'
        JQ.SetFilter("Object ID to Run", Rec."Parameter String");
        if JQ.FindSet() then
            repeat
                JQ.Restart();
            until JQ.Next() = 0;
    end;
}
```

**Fallstricke:** Ohne Filter startet der Wächter ALLE Error-Jobs neu — auch die, die aus gutem Grund tot sind. Kein Backoff im Muster: ein permanent fehlschlagender Job wird endlos wiederbelebt; Zähler/Maximalversuche selbst ergänzen.

---

## Temporary Tables

**Technik:** Die drei Temporär-Mechanismen in AL: temporary-Record-Variable einer echten Tabelle, Seite mit SourceTableTemporary=true (per Page.Run mit dem gefüllten Temp-Record verbunden) und TableType=Temporary als Tabellenobjekt, das nie in SQL existiert.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
// 1) Temp-Variable einer echten Tabelle (nur RAM, kein SQL):
var
    TempCust: Record Customer temporary;
begin
    TempCust.Init();
    TempCust."No." := '10000';
    TempCust.Insert();
    // 2) Seite auf den RAM-Bestand:
    Page.Run(50110, TempCust);
end;

page 50110 "Temp Customer"
{
    PageType = List;
    SourceTable = Customer;
    SourceTableTemporary = true; // zeigt den uebergebenen Bestand
}

// 3) Tabellenobjekt ohne SQL-Schema:
table 50100 "New Table"
{
    TableType = Temporary;
    fields { field(1; "Funky Field"; Code[13]) { } }
}
```

**Fallstricke:** Page.Run(Id, TempRec) verbindet die SourceTableTemporary-Seite mit GENAU dieser Record-Instanz samt Inhalt — der klassische Weg für Vorschau-/Staging-Listen. Temp-Inserts feuern keine DB-Trigger-Kaskaden und brauchen kein Commit. TableType=Temporary eignet sich als Parameter-/Puffertyp ohne Schema-Kosten.

---

## BatchPostAndEmail

**Technik:** Standard-Stapelbuchung erweitern statt nachbauen: reportextension auf "Batch Post Sales Orders" hängt eine eigene Option auf die Request Page und hookt sich mit OnAfterAfterGetRecord je Beleg ein.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 7.1 / BC 18 — reportextension ab BC 18

```al
reportextension 50100 "Batch Post" extends "Batch Post Sales Orders"
{
    dataset
    {
        modify("Sales Header")
        {
            trigger OnAfterAfterGetRecord()
            begin
                // je zu buchendem Beleg: eigene Logik,
                // z.B. Beleg fuer Mailversand vormerken
            end;
        }
    }
    requestpage
    {
        layout
        {
            addafter(PrintDoc)
            {
                field(eMail; eMail)
                {
                    ApplicationArea = all;
                    Caption = 'Email invoices';
                }
            }
        }
    }
    var
        eMail: Boolean;
}
```

**Fallstricke:** Der Trigger heißt wirklich OnAfterAfterGetRecord — Report-Extensions setzen Before/After-Präfixe VOR den Standard-Triggernamen. Die Request-Page-Option transportiert nur den Wunsch; das Mailen selbst muss NACH der Buchung ansetzen (Subscriber auf Posting-Events), sonst mailt man Ungebuchtes.

---

## TheTimeProblem

**Technik:** Time() und CurrentDateTime() liefern die Zeit der SESSION-Zeitzone: im Web-Client die des Benutzers, in TaskScheduler-/StartSession-/Job-Queue-Sessions die des Servers (SaaS: UTC). Derselbe Codeunit schreibt je nach Startweg verschiedene Uhrzeiten.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
codeunit 53400 "Update Time"
{
    trigger OnRun()
    var
        kt: Record "Time Keeper";
    begin
        kt.Get();
        kt.Time1 := Time();            // Time-Feld: roher Wert
        kt.Time2 := CurrentDateTime(); // DateTime-Feld: UTC + Anzeige-TZ
        kt.Modify();
    end;
}

// Vordergrund:  Codeunit.Run(53400);
//   -> beide Felder zeigen Benutzerzeit
// Hintergrund:  TaskScheduler.CreateTask(53400, 0);
//   -> Time1 zeigt SERVER-Zeit (falsch fuer den Benutzer),
//      Time2 stimmt weiter (DateTime speichert UTC,
//      Client rendert in Benutzer-Zeitzone)
```

**Fallstricke:** Genau das ist der Demo-Aufbau: ein Time-Feld und ein DateTime-Feld nebeneinander. DateTime wird als UTC gespeichert und je Session lokalisiert angezeigt — Time-Felder nicht. Fachliche Uhrzeiten (Rapport-Beginn!), die ein Hintergrundjob schreibt, deshalb nie aus Time() nehmen, sondern als DateTime führen oder die Zeitzone explizit umrechnen.

---

## Optimize your string operations

**Technik:** TextBuilder statt +=-Konkatenation in Schleifen — jede +=-Operation kopiert den kompletten String (O(n²)); TextBuilder.Append ist amortisiert konstant. Zweite Lehre der Demo: für Base64 den System-Codeunit "Base64 Convert" nehmen statt Eigenbau.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 5.0; TextBuilder ab runtime 4.0 verfügbar

```al
procedure BuildLargeText(Size: Integer): Text
var
    TB: TextBuilder;
    Ch: Text[1];
    i: Integer;
begin
    // NIE: Result += Ch in einer Schleife (O(n^2)-Stringkopien)
    for i := 1 to Size do begin
        Ch[1] := (i mod 32) + 64;
        TB.Append(Ch);
    end;
    exit(TB.ToText());
end;

procedure ToBase64(Value: Text): Text
var
    Base64Convert: Codeunit "Base64 Convert";
begin
    exit(Base64Convert.ToBase64(Value)); // Standard schlaegt Eigenbau
end;
```

**Fallstricke:** Die auskommentierten Zeilen im Original ("//ReturnValue += ..." ersetzt durch TB.Append) zeigen genau die Umbaustellen — die Kosten sitzen unauffällig in Hilfsfunktionen, die zeichenweise anhängen. Benchmark-Technik der Demo: Time()-Differenz um die Aktion, Dialog offen halten.

---

## TypeConversion

**Technik:** Die eingebauten Arithmetik-Regeln der Datums-/Zeittypen: Date rechnet in TAGEN, Time und Duration in MILLISEKUNDEN — Differenzen und Additionen mischen Integer und Zeittypen implizit, jeweils in der Einheit des Typs.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
var
    da, da2: Date;
    ti, ti2: Time;
    i: Integer;
    du: Duration;
    dt: DateTime;
begin
    da2 := da + 7;      // Date +/- Integer  = Tage
    i := da2 - da;      // Date - Date      = Integer (Tage)
    ti2 := ti + 60000;  // Time +/- Integer = Millisekunden
    du := ti - ti2;     // Time - Time      = Duration (ms, negativ moeglich)
    du := i;            // Integer -> Duration implizit: als MILLISEKUNDEN!
    da := DT2Date(dt);  // DateTime zerlegen: DT2Date / DT2Time
end;
```

**Fallstricke:** du := i interpretiert den Integer als Millisekunden — wer gerade noch in Tagen gerechnet hat (i = da2 - da), bekommt lautlos 7ms statt 7 Tagen. Die Einheiten wechseln je Typ, der Compiler warnt nicht.

---

## Variants

**Technik:** Variant-Parameter machen Prozeduren typoffen für beliebige Records: mit IsRecord prüfen, per RecordRef.GetTable an die Metadaten, und ein Record-Variant lässt sich direkt an Codeunit.Run und Page.RunModal weiterreichen — eine Log-/Utility-Funktion für alle Tabellen.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
procedure LogInformation(v: Variant)
var
    ref: RecordRef;
    c: Record Customer;
begin
    if not v.IsRecord then
        Error('Nur Records erlaubt');
    ref.GetTable(v);              // Variant -> RecordRef
    Message('Tabelle %1', ref.Number);

    // Variant direkt weiterreichen:
    Codeunit.Run(50138, v);       // Codeunit mit passendem TableNo
    // Page.RunModal(0, v);       // Default-Seite der Tabelle

    // Rueckweg nur nach Typpruefung:
    if ref.Number = Database::Customer then
        c := v;                   // kompiliert immer, prueft zur Laufzeit
end;
```

**Fallstricke:** Die Zuweisung Variant -> konkreter Record kompiliert IMMER und knallt erst zur Laufzeit bei falscher Tabelle — vorher ref.Number prüfen. Codeunit.Run mit Record-Variant verlangt ein passendes TableNo an der Ziel-Codeunit.

---

## VariableSizedRecords

**Technik:** Schemafreier Dokument-Store in BC (Azure-Table-Storage-Stil): Entity+Document-Tabellen, JSON-Payload hybrid gespeichert — klein in Text-Feldern (eine Leseoperation, filterbar), gross im Blob; generische Listenseite mit Spalten-Slots, deren Überschriften zur Laufzeit via CaptionClass + OnResolveCaptionClass aufgelöst werden.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
procedure SavePayload(var Doc: Record "Document Hgd"; O: JsonObject)
var
    AsText: Text;
    OutS: OutStream;
begin
    AsText := Format(O);
    if StrLen(AsText) < 3072 then begin
        Doc.Storage := Doc.Storage::TextField;
        Doc.StorageText1 := CopyStr(AsText, 1, 2048);
        Doc.StorageText2 := CopyStr(AsText, 2049, 1024);
    end else begin
        Doc.Storage := Doc.Storage::BLOB;
        Doc.BlobStorage.CreateOutStream(OutS);
        OutS.Write(AsText);
    end;
end;

// Dynamische Spaltencaption: CaptionClass = 'DOC,' + FieldName
[EventSubscriber(ObjectType::Codeunit, Codeunit::"Caption Class",
    OnResolveCaptionClass, '', true, true)]
local procedure Resolve(CaptionArea: Text; CaptionExpr: Text;
    Language: Integer; var Caption: Text; var Resolved: Boolean)
begin
    if CaptionArea = 'DOC' then begin
        Caption := CaptionExpr;
        Resolved := true;
    end;
end;
```

**Fallstricke:** Tabellenobjekte können Prozeduren UND globale Variablen tragen — die Record-Instanz cached hier das geparste JsonObject samt LoadedRowKey (Lazy-Load je Zeile). Blob verlangt CalcFields vor CreateInStream. Sortieren/Filtern auf JSON-Inhalte geht nur über gespiegelte echte Felder (SortingField wird beim Schreiben aus dem JSON extrahiert und indiziert).

---

## Batch Jobs

**Technik:** ProcessingOnly-Report als Gratis-Batch-UI: Request Page mit RequestFilterFields und eigenen Optionen kommt geschenkt, in OnPreDataItem übergibt man den vom Benutzer vorgefilterten Record an die eigentliche Verarbeitungs-Codeunit.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
report 50100 "My Batch"
{
    ProcessingOnly = true;  // kein Layout, reine Verarbeitung
    UsageCategory = ReportsAndAnalysis;
    dataset
    {
        dataitem(Customer; Customer)
        {
            RequestFilterFields = "Customer Posting Group", "Customer Price Group";
            trigger OnPreDataItem()
            var
                Fancy: Codeunit FancyCo;
            begin
                Fancy.FancyFunc(Customer); // traegt die User-Filter
            end;
        }
    }
    requestpage
    {
        layout { area(content) { field(Test; Test) { ApplicationArea = all; } } }
    }
    var
        Test: Text;
}
// Start per Action: RunObject = Report "My Batch";
```

**Fallstricke:** In OnPreDataItem hat der Record die Filter, aber noch KEINEN Datensatz geladen — Verarbeitung je Zeile gehört in OnAfterGetRecord oder in die Codeunit, die selbst FindSet fährt. Requestpage-Variablen (Test) transportieren Optionen in die Verarbeitung.

---

## ToVarOrNotToVar

**Technik:** var entscheidet bei Werttypen (Text, Integer, Record) über Kopie vs. Durchgriff — JsonObject/JsonArray sind aber REFERENZtypen: der Callee verändert das Objekt des Aufrufers auch OHNE var. Bei IntegrationEvents bestimmen var-Parameter, ob Subscriber Werte zurückgeben können.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
// JsonObject ist Referenz — wirkt beim Aufrufer mit UND ohne var:
procedure ProcA(j: JsonObject)
begin
    j.Add('Field2', 'Another value'); // Aufrufer sieht die Aenderung!
end;

// Record OHNE var = vollstaendige Kopie (inkl. Filter/Marks):
// Aenderungen verpuffen, und die Kopie kostet.

// Events: ohne var koennen Subscriber NICHTS zurueckgeben —
// Rueckgabefaehige Parameter bewusst als var deklarieren:
[IntegrationEvent(false, false)]
local procedure OnAfterEncoding(t1: Text; t2: Text)
begin
end;
```

**Fallstricke:** JsonObject ohne var suggeriert eine Isolation, die nicht existiert — wer eine unabhängige Kopie will, muss über Format/ReadFrom klonen. Record-Parameter ohne var kopieren auch Filter und Marks mit — bei grossen Sets doppelt teuer. Event-Signaturen sind API: ein vergessenes var ist später ein Breaking Change.

---

## JobQueueFriendlyCodeunit

**Technik:** Job-Queue-taugliche Codeunit: TableNo = "Job Queue Entry" macht Parameter String und Kategorie zur Konfiguration — und ein leerer Entry (Object ID to Run = 0) verrät, dass die Codeunit direkt statt vom Scheduler aufgerufen wurde.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
codeunit 50133 "My JobQueue Job"
{
    TableNo = "Job Queue Entry";
    trigger OnRun()
    begin
        if Rec."Object ID to Run" = 0 then begin
            // Direktaufruf (Test/manuell):
            // Codeunit.Run(Codeunit::"My JobQueue Job", TempJQE)
        end else begin
            // laeuft in der Job Queue
        end;
        if Rec."Job Queue Category Code" = 'DOTHIS' then
            ; // Kategorie / "Parameter String" als Steuerdaten
    end;
}
```

**Fallstricke:** Dieselbe Codeunit läuft so im Scheduler UND im Test ohne Scheduler — den Unterschied am Entry erkennen statt an GuiAllowed raten. Parameter String ist das einzige freie Konfigurationsfeld je Eintrag.

---

## DeleteRecords

**Technik:** Selektives Löschen WÄHREND einer FindSet-Iteration funktioniert, weil BC das Resultset liest, bevor gelöscht wird — und FindSet(true) ist zum Löschen nicht nötig (der Parameter steuert Sperrverhalten, nicht Erlaubnis).

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 16 / BC 27

```al
var
    c: Record Customer;
begin
    c.SetFilter("No.", 'C00060..');
    if c.FindSet(false) then   // false reicht — Delete geht trotzdem
        repeat
            if c."No." = 'C00070' then
                c.Delete();    // Iteration laeuft sauber weiter
        until c.Next() = 0;
end;
// Alles im Filter loeschen: c.DeleteAll() — nie die Schleife
```

**Fallstricke:** Delete() ohne true feuert OnDelete (und damit Kaskaden-Löschungen abhängiger Tabellen) NICHT — Delete(true) für fachliches Löschen. Das ungenutzte zweite Record-Var im Original deutet das Alternativmuster an: mit einer Variablen iterieren, über eine Kopie löschen, wenn man dem Resultset nicht traut.

---

## ModifyAll

**Technik:** ModifyAll ohne Trigger ist EIN SQL-UPDATE über den Filter; mit `RunTrigger = true` oder bei mehreren Feldern wird zeilenweise gearbeitet — ab zwei Feldern ist die eigene FindSet(true)-Schleife billiger als zwei ModifyAll.
⚠ **BERICHTIGT 01.09.2026 (B): Hier stand „Validate-Parameter".** Der dritte Parameter heißt
`RunTrigger` und läuft `OnModify` (Tabelle), **nicht** `OnValidate` (Feld) — Microsoft:
*„The OnValidate field trigger is never run when ModifyAll is used."* **ModifyAll validiert
nie, mit keinem Parameterwert.** Wer Feldvalidierung braucht, nimmt `Validate` + `Modify` in
einer eigenen Schleife.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
// 1 SQL-UPDATE fuer alle gefilterten Zeilen:
Rec.ModifyAll(Name, '123 Best Street');

// Mit ONMODIFY je Zeile (laeuft intern als Schleife):
Rec.ModifyAll(Name, '123 Best Street', true);
// ⚠ BERICHTIGT 01.09.2026 (B): Hier stand "Mit OnValidate je Zeile".
// DAS IST FALSCH. Microsoft, Record.ModifyAll Method, woertlich:
//   "The OnValidate field trigger is NEVER run when ModifyAll is used."
//   RunTrigger: "If this parameter is true, the code in the OnModify Trigger
//                is executed."
// Der dritte Parameter laeuft den TABELLEN-Trigger OnModify, NICHT die
// FELD-Trigger OnValidate. Wer ModifyAll(..., true) fuer "mit Validierung"
// haelt, glaubt an eine Pruefung, die nicht stattfindet.
// ✓ Was STIMMT: die Aequivalenz zur Schleife - MS zeigt sie im Beispiel
//   ausdruecklich (Find('-') / repeat / Modify / until Next = 0).

// Zwei Felder: NICHT 2x ModifyAll (2 Durchlaeufe),
// sondern eine Schleife:
if Rec.FindSet(true) then
    repeat
        Rec.Validate(Name, '123 Best Street');
        Rec.Address := '234 Another Street';
        Rec.Modify(true);
    until Rec.Next() = 0;
```

**Fallstricke:** ModifyAll ohne true überspringt OnModify/OnValidate komplett (auch abhängige Felder und Modified-At-Logik) — schnell, aber fachlich blind. Zwei ModifyAll hintereinander iterieren die Menge zweimal.

---

## TryFunction

**Technik:** Das Grundmuster für werfende Konvertierungen: [TryFunction]-Prozedur kapselt JsonValue.AsDecimal() u.ä. in ein Boolean, Ergebnis kommt über var-Parameter zurück, GetLastErrorText() liefert die Ursache.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
trigger OnOpenPage()
var
    J: JsonObject;
    T: JsonToken;
    D: Decimal;
begin
    J.Add('amount', '1.00.00');
    if J.Get('amount', T) then
        if TryDecimal(T, D) then
            Message('Amount = %1', D)
        else
            Message('Keine Zahl (%1)', GetLastErrorText());
end;

[TryFunction]
local procedure TryDecimal(var T: JsonToken; var D: Decimal)
begin
    D := T.AsValue().AsDecimal();
end;
```

**Fallstricke:** TryFunctions dürfen keinen eigenen Rückgabewert deklarieren — der Boolean kommt vom Attribut, Nutzdaten nur über var-Parameter. Aufruf ohne if-Abfrage wirft den Fehler normal weiter.

---

## CalcTime

**Technik:** AL hat CalcDate, aber kein CalcTime — Eigenbau parst Ausdrücke wie '1W4H' oder '-1H30M' zu einer Duration; Time-Werte rechnet man als Integer-Millisekunden relativ zur Konstante 000000T. Nebenbei: AL kann Prozedur-Überladung (zwei CalcTime mit verschiedenen Signaturen).

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
procedure CalcTime(Expr: Text; StartDateTime: DateTime): DateTime
var
    i, OpInt: Integer;
    Op: Text;
    D: Duration;
begin
    // wie CalcDate, aber fuer Zeit: '1W4H', '-1H30M', '1H2M13S'
    for i := 1 to StrLen(Expr) do
        if Expr[i] in ['A' .. 'Z', 'a' .. 'z'] then begin
            Evaluate(OpInt, Op);
            case Expr[i] of
                'W': D += OpInt * 7 * 24 * 60 * 60 * 1000;
                'D': D += OpInt * 24 * 60 * 60 * 1000;
                'H': D += OpInt * 60 * 60 * 1000;
                'M': D += OpInt * 60 * 1000;
                'S': D += OpInt * 1000;
            end;
            Op := '';
        end else
            Op += Expr[i];
    exit(StartDateTime + D);
end;
// Time-Variante: IntMs := StartTime - 000000T; rechnen;
// Ergebnis := 000000T + (IntMs mod (24*60*60*1000));
```

**Fallstricke:** Time ist zyklisch — Überlauf über Mitternacht per mod 86400000 selbst behandeln (der Autor markiert '-56H' mit '// Hmmm...'). Negative Operanden funktionieren gratis, weil Evaluate '-30' parst.

---

## Global Local

**Technik:** Ein Seitenfeld, das an eine Prozedur gebunden ist, wird bei JEDEM UI-Roundtrip für jede sichtbare Zeile neu ausgewertet — die Demo macht das mit Random() sichtbar (Werte springen beim Scrollen). Teure Logik gehört nicht in prozedur-gebundene Felder.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
page 50108 "Global vs Local"
{
    PageType = List;
    SourceTable = Customer;
    layout
    {
        area(Content)
        {
            repeater(Rep)
            {
                field(test; GlobalText(Rec)) // je Zeile, je Roundtrip!
                {
                    Caption = 'Global Text';
                    ApplicationArea = all;
                }
            }
        }
    }
    procedure GlobalText(Customer: Record Customer): Text
    begin
        test2(Customer); // mutiert nur die Kopie (kein var beim Feld-Aufruf)
        exit(Customer.Name + ' ' + Format(Random(100000)));
    end;
    procedure test2(var Customer: Record Customer)
    begin
        Customer.Name := 'Erik'; // sichtbar im Feld, nie in der DB
    end;
}
```

**Fallstricke:** Der Random-Wert ändert sich ohne Datenänderung — der Beweis, dass die Prozedur ständig neu läuft; DB-Abfragen oder CalcFields an dieser Stelle skalieren mit Zeilen × Roundtrips. Stattdessen: in OnAfterGetRecord in eine globale Variable rechnen und das Feld daran binden. Die Record-Kopie im Feld-Aufruf zeigt ausserdem: Mutationen dort betreffen nur die Anzeige.

---

## MedusaRecords

**Technik:** Absturz-Forensik für Operationen, die eine Session einfrieren/töten (hier: die virtuelle Tabelle "Report Data Items" je Report lesen): jede riskante Prüfung in eine Wegwerf-Session isolieren und VOR dem Zugriff einen Schuld-Marker mit Commit setzen — stirbt die Session, bleibt der Marker als Beweis.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** runtime 14 / BC 25

```al
codeunit 51100 MedusaDetector
{
    TableNo = AllObj;
    trigger OnRun()
    var
        RDI: Record "Report Data Items";
        Medusa: Record Medusa;
    begin
        Medusa.Init();
        Medusa.ReportID := Rec."Object ID";
        Medusa.Status := Medusa.Status::Medusa; // "schuldig, bis..."
        Medusa.Insert();
        Commit();  // Marker ueberlebt den Session-Tod
        RDI.SetRange("Report ID", Rec."Object ID");
        if RDI.FindSet() then
            repeat until RDI.Next() = 0;        // riskanter Zugriff
        Medusa.Status := Medusa.Status::"No Medusa"; // freigesprochen
        Medusa.Modify();
    end;
}
// Treiber: je Report eine eigene Session:
// StartSession(Sid, Codeunit::MedusaDetector, CompanyName, Reports);
```

**Fallstricke:** Ohne Commit vor dem riskanten Zugriff stirbt der Marker mit der Session — das Muster steht und fällt mit der Reihenfolge Insert→Commit→Risiko→Modify. Der Treiber startet eine Session je Report: Session-/Ressourcen-Limits im Blick behalten. Nebenbefund: es gibt Systemtabellen, deren blosses Iterieren die Session hängen kann.

---

## Übersprungen (bewusst)

- Process (Ordner existiert nicht — nur 'Process Large XML' vorhanden, gehoert zum XML-Cluster)
- ScheduledTasks (nur Hello-World-Stub)
- SessionTaskJobQueue (unvollstaendiger Code-Stub)
- ErrorJobQueue (nur Error()-Einzeiler)
- TryFunctionsAreExpensive (deckungsgleich mit SlowToTryFunction)
- ListvsDictionary (triviale Add/Get-Demo)
- SmarterDictionaries (Demo-Torso, misst leeres Objekt)
- ArraysOfEverything (nur Array-Deklaration)
- emptyvariables (Syntax-Kuriositaet ohne Praxiswert)

