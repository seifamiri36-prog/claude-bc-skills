# JSON, XML, CSV, Excel & Dateiformate

_Destilliert aus Erik Hougaards Youtube-Video-Sources (Ordnername = Videothema)._
_Vollquellen: https://github.com/hougaard/Youtube-Video-Sources (lokal klonen; Ordnername = Videothema)_

Der Cluster lehrt den kompletten Dateiformat-Werkzeugkasten von AL: JsonObject/JsonToken-Navigation samt generischer Rec↔Json-Konverter über RecordRef/FieldRef, drei XML-Parse-Strategien mit dem entscheidenden Evaluate-Format 9, und die Standard-Buffer-Tabellen (CSV Buffer, Excel Buffer) als fertige Importwege. Binärdaten laufen durchgängig über die Pipeline Temp Blob + Base64 Convert + Data Compression — vom Bild im JSON bis zum PDF-Zip aller Kundenbelege. Die Text-Werkzeuge (Split, TextBuilder, List als Stack) skalieren vom 80-Zeichen-Umbruch bis zum vollständigen MIME-E-Mail-Parser als Zustandsautomat. Roter Faden: Die System-App bringt fast alles fertig mit (CSV Buffer, Excel Buffer, Base64 Convert, Data Compression, Recurrence Schedule) — der eigentliche Lernwert sind die Fallstricke: TextEncoding vor Base64, CalcFields vor Blob-Streams, Quotes im CSV Buffer, locale-abhängiges Evaluate und FlowFields ohne CalcField.

**Wertvollste Ordner:** complexJSON · Process Large XML · CSV-Buffer · Excel Buffer · Zip

## Themen (nach Praxis-Relevanz)

- ●●●  **complexJSON** — Verschachteltes JSON aus einer Datensatz-Hierarchie (Job -> Tasks -> Budget/Ist) mit einem generischen Rec2Json-Serializer ueber RecordRef/FieldRef — jede Tabelle ohne Einzelmapping. Genau die Struktur Projekt -> LV-Positionen -> Plan/Ist.
- ●●●  **JsonTools** — Gegenrichtung zu complexJSON: generischer Json2Rec-Deserializer — JSON-Keys werden ueber ein Dictionary (bereinigter Feldname -> Feldnummer) auf FieldRefs gemappt, Rueckgabe des fertigen Records als Variant. Zeigt nebenbei AL-Prozedur-Overloading.
- ●●●  **Process Large XML** — XML-Datei in Records verwandeln — das Demo stellt bewusst drei Strategien nebeneinander: explizit mit Validate, case ueber Elementnamen, und vollgenerisch via RecordRef (FieldRef.Name = XML-Elementname). Direkt einschlaegig fuer ÖNORM-A2063-LV-Dateien.
- ●●●  **CSV-Buffer** — CSV-Import ohne eigene Parse-Logik ueber die Standardtabelle "CSV Buffer" (temporaer): LoadDataFromStream zerlegt in (Zeile, Spalte, Wert)-Tripel; Zellzugriff per Get(LineNo, FieldNo). Das Demo baut daraus Verkaufsrechnungen mit variabler Spaltenzahl je Zeile.
- ●●●  **Excel Buffer** — XLSX lesen ohne Fremdkomponente ueber die Standardtabelle "Excel Buffer": OpenBookStream + ReadSheet fuellen (Zeile, Spalte, Zellwert); dazu die Spaltenbuchstabe-zu-Nummer-Arithmetik (A=1, AA=27) und das Auffinden der letzten Datenzeile.
- ●●●  **Zip** — Alle Belege eines Kunden als PDF-Sammlung in einer ZIP-Datei ausliefern: Codeunit "Data Compression" als Zip-Archiv, Report.SaveAs rendert Belege in-memory als PDF, und die Report-ID kommt kundenkonfiguriert aus "Report Selections" statt hart verdrahtet.
- ●●●  **splittext** — Wortweiser Zeilenumbruch (Word-Wrap) idiomatisch mit Text.Split, List of [Text] und TextBuilder — das Standardproblem, lange Beschreibungstexte auf Belegzeilen fester Breite zu verteilen.
- ●●○  **JSON for Beginners** — Grundmechanik der AL-JSON-Typen: JsonObject/JsonArray/JsonValue bauen und die Token-Navigation beim Lesen (Get liefert immer JsonToken, erst IsObject/IsValue pruefen, dann casten).
- ●●○  **JsonBlob** — Binaerdaten (Blob-Feld) verlustfrei durch JSON transportieren: Blob -> Base64-Text als JSON-Wert und zurueck. Der einzige Weg, da JSON kein Binaerformat kennt.
- ●●○  **JPathSelectToken** — JSONPath-Abfragen mit Filterausdruecken direkt auf JsonToken.SelectToken — ein Einzeiler ersetzt die ganze foreach/IsObject/Get-Kaskade beim Suchen in API-Antworten.
- ●●○  **ExcelInMatrixPage** — Excel-Datei direkt im BC-Client anzeigen: List-Page ueber die virtuelle Integer-Tabelle als Zeilenquelle, Zellwerte als berechnete Feld-Ausdruecke aus einem page-weiten Excel Buffer, dynamische Spaltenueberschriften per CaptionClass und horizontales "Scrollen" ueber eine Offset-Variable.
- ●●○  **Base64** — Beliebige Bilder ohne Media-Feld im Client anzeigen: ControlAddIn mit JavaScript, das einen Base64-String als data-URI in ein img-Element setzt; AL fuettert es aus einem Blob via Base64 Convert.
- ●●○  **ImportAndParseEmail** — Vollstaendiger MIME-Parser fuer .eml-Dateien in reinem AL: Zustandsautomat (Outside/Header/Data), gefaltete Header-Zeilen, Boundary-Stack fuer verschachtelte Multiparts, Base64-Anhaenge direkt in Blob-Felder dekodiert.
- ●●○  **EditInExcel** — System-Codeunit "Recurrence Schedule": Wiederholungsregeln (taeglich/woechentlich mit Wochentagen) als konfigurierbares Objekt anlegen und die naechsten Termine iterativ berechnen — fertige Infrastruktur fuer wiederkehrende Wartungs-/Prueftermine.
- ●○○  **Base64 testing** — Base64 ist keine Zeichenkodierung: VOR dem Enkodieren entscheidet TextEncoding (UTF8/UTF16/Codepage) ueber die Bytes — Sonderzeichen wie Umlaute sind der Testfall. Nebenbei eine Vorlage fuer Facade+Implementation samt AAA-Testcodeunit mit Library Assert.

---

## complexJSON

**Technik:** Verschachteltes JSON aus einer Datensatz-Hierarchie (Job -> Tasks -> Budget/Ist) mit einem generischen Rec2Json-Serializer ueber RecordRef/FieldRef — jede Tabelle ohne Einzelmapping. Genau die Struktur Projekt -> LV-Positionen -> Plan/Ist.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 9.0 / application 20.0

```al
procedure Tasks2Json(JobNo: Code[20]): JsonArray
var
    Task: Record "Job Task";
    JA: JsonArray;
    JO: JsonObject;
begin
    Task.SetRange("Job No.", JobNo);
    if Task.FindSet() then
        repeat
            JO := Rec2Json(Task);
            JO.Add('Budget', PlanningLines2Json(Task)); // Unter-Arrays anhaengen
            JA.Add(JO);
        until Task.Next() = 0;
    exit(JA);
end;

procedure Rec2Json(Rec: Variant): JsonObject
var
    Ref: RecordRef;
    FRef: FieldRef;
    Out: JsonObject;
    i: Integer;
begin
    Ref.GetTable(Rec);
    for i := 1 to Ref.FieldCount() do begin
        FRef := Ref.FieldIndex(i);
        case FRef.Class of
            FRef.Class::Normal:
                Out.Add(JsonName(FRef.Name), Format(FRef.Value, 0, 9));
            FRef.Class::FlowField:
                begin
                    FRef.CalcField(); // sonst liefert der FlowField 0
                    Out.Add(JsonName(FRef.Name), Format(FRef.Value, 0, 9));
                end;
        end;
    end;
    exit(Out);
end;
```

**Fallstricke:** FlowFields brauchen FRef.CalcField() vor dem Lesen, sonst still 0. Feldnamen muessen JSON-tauglich gemacht werden (im Original: jedes Zeichen < '0' wird '_', Doppel-_ zusammengezogen, Raender getrimmt). Format(Value,0,9) liefert das invariante Format; Date/Time/DateTime/Boolean besser typisiert ueber JsonValue.SetValue, sonst werden sie Strings.

---

## JsonTools

**Technik:** Gegenrichtung zu complexJSON: generischer Json2Rec-Deserializer — JSON-Keys werden ueber ein Dictionary (bereinigter Feldname -> Feldnummer) auf FieldRefs gemappt, Rueckgabe des fertigen Records als Variant. Zeigt nebenbei AL-Prozedur-Overloading.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 8.0 / application 19.0

```al
procedure Json2Rec(JO: JsonObject; TableNo: Integer): Variant
var
    Ref: RecordRef;
    FR: FieldRef;
    FieldHash: Dictionary of [Text, Integer];
    i: Integer;
    JsonKey: Text;
    T: JsonToken;
    RecVar: Variant;
begin
    Ref.Open(TableNo);
    for i := 1 to Ref.FieldCount() do begin
        FR := Ref.FieldIndex(i);
        FieldHash.Add(JsonName(FR.Name), FR.Number);
    end;
    Ref.Init();
    foreach JsonKey in JO.Keys() do
        if JO.Get(JsonKey, T) and T.IsValue() then begin
            FR := Ref.Field(FieldHash.Get(JsonKey));
            case FR.Type of
                FieldType::Code, FieldType::Text:
                    FR.Value := T.AsValue().AsText();
                FieldType::Integer:
                    FR.Value := T.AsValue().AsInteger();
                FieldType::Date:
                    FR.Value := T.AsValue().AsDate();
                else
                    Error('%1 nicht unterstuetzt', FR.Type);
            end;
        end;
    RecVar := Ref;
    exit(RecVar);
end;
// Aufrufer: Cust := JsonTools.Json2Rec(JsonObj, Cust);  (Variant -> Record)
```

**Fallstricke:** Unbekannte JSON-Keys lassen FieldHash.Get() hart fehlschlagen — produktiv FieldHash.ContainsKey/TryGet vorschalten. FR.Value := ... umgeht alle OnValidate-Trigger (bewusst entscheiden ob Validate noetig). Zwei Prozeduren mit gleichem Namen und verschiedener Signatur sind in AL erlaubt (Overload-Kaskade Variant -> TableNo).

---

## Process Large XML

**Technik:** XML-Datei in Records verwandeln — das Demo stellt bewusst drei Strategien nebeneinander: explizit mit Validate, case ueber Elementnamen, und vollgenerisch via RecordRef (FieldRef.Name = XML-Elementname). Direkt einschlaegig fuer ÖNORM-A2063-LV-Dateien.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 5.0, BC16

```al
procedure Import()
var
    InS: InStream;
    FileName: Text;
    XmlDoc: XmlDocument;
    Root: XmlElement;
    Node: XmlNode;
    E: XmlElement;
    Data: Record "XML Data";
begin
    if not UploadIntoStream('Upload XML', '', '', FileName, InS) then
        exit;
    if not XmlDocument.ReadFrom(InS, XmlDoc) then
        Error('Cannot parse XML');
    XmlDoc.GetRoot(Root);
    foreach Node in Root.GetChildElements('Record') do begin
        E := Node.AsXmlElement();
        Data.Init();
        Data.RowID := GetInteger(E, 'RowID');
        Data.Company := CopyStr(GetText(E, 'Company'), 1, MaxStrLen(Data.Company));
        Data.Insert(true);
    end;
end;

local procedure GetText(E: XmlElement; Name: Text): Text
var
    N: XmlNode;
begin
    foreach N in E.GetChildElements(Name) do
        exit(N.AsXmlElement().InnerText); // "FirstOrDefault"-Idiom
end;
// GetInteger analog: if Evaluate(V, ...InnerText, 9) then exit(V);
```

**Fallstricke:** Evaluate(..., Text, 9) erzwingt das XML-invariante Format (Dezimalpunkt, ISO-Datum) — ohne die 9 platzt der Import je nach Windows-Region. Das foreach-mit-exit-Idiom liefert das erste Kindelement oder den Default. Der Autor bricht absichtlich mit error('Select method 1, 2 or 3 in code first') ab — die drei Varianten stehen untereinander im Code und sind nicht gleichzeitig lauffaehig. Generische Variante 3 traegt nur, wenn Feldnamen exakt den Elementnamen entsprechen.

---

## CSV-Buffer

**Technik:** CSV-Import ohne eigene Parse-Logik ueber die Standardtabelle "CSV Buffer" (temporaer): LoadDataFromStream zerlegt in (Zeile, Spalte, Wert)-Tripel; Zellzugriff per Get(LineNo, FieldNo). Das Demo baut daraus Verkaufsrechnungen mit variabler Spaltenzahl je Zeile.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 6.0, BC17

```al
// Page: SourceTable = "CSV Buffer"; SourceTableTemporary = true;
var
    InS: InStream;
    FileName: Text;
begin
    if UploadIntoStream('CSV File', '', '', FileName, InS) then begin
        Rec.LoadDataFromStream(InS, ',');
        Message('Lines = %1', Rec.GetNumberOfLines());
    end;
end;

procedure GetText(LineNo: Integer; FieldNo: Integer): Text
begin
    if Rec.Get(LineNo, FieldNo) then
        exit(Rec.Value.TrimEnd('"').TrimStart('"')); // Quotes selbst entfernen
end;

// Variable Spaltenzahl (Artikel/Menge-Paare bis Zeilenende):
local procedure CreateLines(LineNo: Integer)
var
    FieldNo: Integer;
    Done: Boolean;
begin
    FieldNo := 3;
    repeat
        if Rec.Get(LineNo, FieldNo) then
            CreateLine(LineNo, FieldNo) // Feld = Artikel, Feld+1 = Menge
        else
            Done := true;
        FieldNo += 2;
    until Done;
end;
```

**Fallstricke:** CSV Buffer entfernt Anfuehrungszeichen NICHT — jeder Wert muss manuell getrimmt werden (im Demo sogar per OnAfterGetRecord fuer die Anzeige). Zeilen mit unterschiedlich vielen Spalten sind kein Problem: Get() als Existenzprobe nutzen. Typkonvertierung (Datum, Dezimal) laeuft ueber Evaluate — locale-abhaengig, das Test-CSV nutzt US-Datumsformat.

---

## Excel Buffer

**Technik:** XLSX lesen ohne Fremdkomponente ueber die Standardtabelle "Excel Buffer": OpenBookStream + ReadSheet fuellen (Zeile, Spalte, Zellwert); dazu die Spaltenbuchstabe-zu-Nummer-Arithmetik (A=1, AA=27) und das Auffinden der letzten Datenzeile.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 6.0, BC17

```al
var
    Buffer: Record "Excel Buffer" temporary;
    InS: InStream;
    FileName: Text;
    Row, LastRow: Integer;
begin
    if UploadIntoStream('Excel', '', '', FileName, InS) then begin
        Buffer.OpenBookStream(InS, 'Sheet1'); // Sheetname muss exakt stimmen
        Buffer.ReadSheet();
        Buffer.SetRange("Column No.", 4);     // letzte Zeile ueber Pflichtspalte
        Buffer.FindLast();
        LastRow := Buffer."Row No.";
        Buffer.Reset();
        for Row := 9 to LastRow do begin      // Daten beginnen unter den Kopfzeilen
            Data.Init();
            Data.Primary := GetText(Buffer, 'D', Row);
            Data."Date Data" := GetDate(Buffer, 'F', Row);
            Data.Insert();
        end;
    end;
end;

procedure GetText(var Buffer: Record "Excel Buffer" temporary; Col: Text; Row: Integer): Text
begin
    if Buffer.Get(Row, GetColumnNumber(Col)) then
        exit(Buffer."Cell Value as Text");
end;

procedure GetColumnNumber(ColumnName: Text): Integer
var
    Idx, Factor, Pos: Integer;
begin
    Factor := 1;
    for Pos := StrLen(ColumnName) downto 1 do
        if ColumnName[Pos] >= 65 then begin
            Idx += Factor * ((ColumnName[Pos] - 65) + 1);
            Factor *= 26;
        end;
    exit(Idx);
end;
```

**Fallstricke:** Alles kommt als "Cell Value as Text" — Datum/Dezimal per Evaluate, und das ist locale-abhaengig (Excel-Datumsanzeige vs. Serverregion pruefen). Leere Zellen existieren gar nicht als Datensatz: Get() schlaegt fehl, Helfer muessen den Default liefern. Excel-Spalten sind Basis-26 OHNE Null — daher das (dividend-1) mod 26 in der Rueckrichtung. Reale Dateien haben Kopf-/Deckzeilen: Startzeile ist Fachwissen, nicht Zeile 1.

---

## Zip

**Technik:** Alle Belege eines Kunden als PDF-Sammlung in einer ZIP-Datei ausliefern: Codeunit "Data Compression" als Zip-Archiv, Report.SaveAs rendert Belege in-memory als PDF, und die Report-ID kommt kundenkonfiguriert aus "Report Selections" statt hart verdrahtet.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 6.0, BC17

```al
var
    Zip: Codeunit "Data Compression";
    TempBlob: Codeunit "Temp Blob";
    ReportSelection: Record "Report Selections";
    SalesInv: Record "Sales Invoice Header";
    Ref: RecordRef;
    InS: InStream;
    OutS: OutStream;
begin
    Zip.CreateZipArchive();

    // je Beleg (hier: gebuchte Rechnung):
    ReportSelection.SetRange(Usage, ReportSelection.Usage::"S.Invoice");
    ReportSelection.SetFilter("Report ID", '<>0');
    ReportSelection.FindFirst();               // konfigurierter Belegreport
    SalesInv.SetRange("No.", DocumentNo);
    Ref.GetTable(SalesInv);                    // Filter wandern in den RecordRef mit
    TempBlob.CreateOutStream(OutS);
    Report.SaveAs(ReportSelection."Report ID", '', ReportFormat::Pdf, OutS, Ref);
    TempBlob.CreateInStream(InS);
    Zip.AddEntry(InS, 'Invoice ' + DocumentNo + '.pdf');

    // Abschluss:
    Clear(TempBlob);
    TempBlob.CreateOutStream(OutS);
    Zip.SaveZipArchive(OutS);
    TempBlob.CreateInStream(InS);
    DownloadFromStream(InS, '', '', '', CustomerName + ' data.zip');
end;
```

**Fallstricke:** Report-ID nie hart verdrahten — "Report Selections" (Usage S.Invoice/S.Cr.Memo/...) liefert den beim Kunden eingerichteten Layout-Report. Ref.GetTable(Rec) uebernimmt die gesetzten Filter, dadurch druckt der Report genau EINEN Beleg. Je Eintrag einen frischen Temp Blob nehmen, sonst haengen alte Bytes im Stream. Fuer Zahlungen zeigt das Demo Report "Customer - Payment Receipt" direkt auf dem Ledger Entry.

---

## splittext

**Technik:** Wortweiser Zeilenumbruch (Word-Wrap) idiomatisch mit Text.Split, List of [Text] und TextBuilder — das Standardproblem, lange Beschreibungstexte auf Belegzeilen fester Breite zu verteilen.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 10.0 / application 21.0

```al
procedure WrapText(Input: Text; MaxLen: Integer) Lines: List of [Text]
var
    Words: List of [Text];
    Builder: TextBuilder;
    W: Integer;
begin
    Words := Input.Split(' ');
    for W := 1 to Words.Count() do begin
        if Builder.Length() > 0 then
            Builder.Append(' ');
        Builder.Append(Words.Get(W));
        if Builder.Length() > MaxLen then begin // Original prueft NACH dem Anfuegen!
            Lines.Add(Builder.ToText());
            Clear(Builder);
        end;
    end;
    if Builder.Length() > 0 then
        Lines.Add(Builder.ToText()); // Rest nicht vergessen
end;
```

**Fallstricke:** Das Original prueft die Laenge NACH dem Anfuegen — Zeilen werden dadurch MINDESTENS MaxLen lang (bis MaxLen + Wortlaenge), nicht hoechstens. Fuer Felder fester Laenge (z.B. Description Text[100]) muss die Pruefung VOR dem Anfuegen stehen: passt das Wort nicht mehr, erst Zeile abschliessen, dann anfuegen. Die reporttest.al im Ordner ist ein artfremder Rest (Pet-Feld am Customer).

---

## JSON for Beginners

**Technik:** Grundmechanik der AL-JSON-Typen: JsonObject/JsonArray/JsonValue bauen und die Token-Navigation beim Lesen (Get liefert immer JsonToken, erst IsObject/IsValue pruefen, dann casten).

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 5.0, BC16

```al
procedure BuildAndRead()
var
    Obj, Item: JsonObject;
    Arr: JsonArray;
    V: JsonValue;
    Tok, T2, T3: JsonToken;
begin
    V.SetValue(123.456);
    Obj.Add('Price', V);          // JsonValue traegt den Typ
    Item.Add('No', 20201110D);    // Date direkt -> typisierter JSON-Wert
    Arr.Add(Item);
    Arr.Add(100);                 // Arrays duerfen gemischt sein
    Obj.Add('Items', Arr);

    if Obj.Contains('Items') then begin
        Obj.Get('Items', Tok);
        foreach T2 in Tok.AsArray() do
            if T2.IsObject() then begin
                T2.AsObject().Get('No', T3);
                if T3.IsValue() then
                    Message('%1', CalcDate('+5D', T3.AsValue().AsDate()));
            end;
    end;
    // Serialisieren: Obj.WriteTo(txt);
end;
```

**Fallstricke:** Jeder Lesezugriff geht ueber JsonToken — vor AsObject()/AsValue() immer IsObject()/IsValue() pruefen, sonst Laufzeitfehler. Ein als Date geschriebener Wert kommt ueber AsValue().AsDate() typisiert zurueck (kein Evaluate noetig). WriteTo(Text) serialisiert; Format(Obj) geht auch.

---

## JsonBlob

**Technik:** Binaerdaten (Blob-Feld) verlustfrei durch JSON transportieren: Blob -> Base64-Text als JSON-Wert und zurueck. Der einzige Weg, da JSON kein Binaerformat kennt.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 8.0 / application 19.0

```al
var
    Base64: Codeunit "Base64 Convert";
    J: JsonObject;
    T: JsonToken;
    InS: InStream;
    OutS: OutStream;
begin
    // Blob -> JSON
    Rec.CalcFields(Blob);              // Blob-Feld erst laden!
    Rec.Blob.CreateInStream(InS);
    J.Add('PK', Rec.PK);
    J.Add('Blob', Base64.ToBase64(InS));

    // JSON -> Blob
    J.Get('Blob', T);
    if T.IsValue() then begin
        Rec.Blob.CreateOutStream(OutS);
        Base64.FromBase64(T.AsValue().AsText(), OutS);
        Rec.Modify();
    end;
end;
```

**Fallstricke:** Rec.CalcFields(Blob) vor CreateInStream ist Pflicht — Blob-Felder werden nicht automatisch mitgeladen, der Stream ist sonst leer. Fuer den Datei-Umweg dient Codeunit "Temp Blob" als In-Memory-Container (OutStream schreiben, InStream lesen, DownloadFromStream).

---

## JPathSelectToken

**Technik:** JSONPath-Abfragen mit Filterausdruecken direkt auf JsonToken.SelectToken — ein Einzeiler ersetzt die ganze foreach/IsObject/Get-Kaskade beim Suchen in API-Antworten.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 12.0 / application 23.0 (BC23)

```al
local procedure SelectEmployeeSalary(Data: JsonToken; EmployeeId: Text) Salary: Decimal
var
    Query: Text;
    Tok: JsonToken;
begin
    Query := '$.company.employees[?(@.id==''' + EmployeeId + ''')].salary';
    if Data.SelectToken(Query, Tok) then
        Salary := Tok.AsValue().AsDecimal();
end;

// Aufruf:
// J.ReadFrom(JsonText);
// Betrag := SelectEmployeeSalary(J.AsToken(), 'John');
```

**Fallstricke:** ⚠⚠ **BERICHTIGT 01.09.2026 (B): Hier stand „SelectToken lebt auf JsonToken, nicht auf JsonObject — vorher J.AsToken()“. DAS IST WIDERLEGT.** MS dokumentiert `JsonObject.SelectToken(Text, var JsonToken)` als **eigene Methode**, „Available or changed with runtime version 1.0“ — ebenso auf `JsonValue` und `JsonArray`. Der `AsToken()`-Umweg der Demo funktioniert, ist aber **nicht nötig**. Filterausdruecke [?(@.feld==wert)] funktionieren (Newtonsoft-JPath unter der Haube). String-Quoting: '' im AL-Literal ergibt das einfache Anfuehrungszeichen im JPath. SelectToken gibt false zurueck, wenn nichts matcht — Rueckgabewert pruefen statt blind AsValue().

---

## ExcelInMatrixPage

**Technik:** Excel-Datei direkt im BC-Client anzeigen: List-Page ueber die virtuelle Integer-Tabelle als Zeilenquelle, Zellwerte als berechnete Feld-Ausdruecke aus einem page-weiten Excel Buffer, dynamische Spaltenueberschriften per CaptionClass und horizontales "Scrollen" ueber eine Offset-Variable.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 8.0 / application 19.0

```al
page 50410 "Excel Viewer"
{
    PageType = List;
    SourceTable = Integer;                        // virtuelle Zeilennummern
    SourceTableView = where(Number = filter(1 ..));
    Editable = false;
    layout { area(Content) { repeater(Rep) {
        field(Col1; GetExcelCell(Rec.Number, LeftMostColumn))
        { CaptionClass = '3,' + GetColumnHeading(LeftMostColumn); ApplicationArea = all; }
        field(Col2; GetExcelCell(Rec.Number, LeftMostColumn + 1))
        { CaptionClass = '3,' + GetColumnHeading(LeftMostColumn + 1); ApplicationArea = all; }
        // ... Col3..Col5 analog
    } } }
    actions { area(Processing) {
        action(Right) { trigger OnAction() begin LeftMostColumn += 1; end; }
        action(Load)  { trigger OnAction()
            begin // UploadIntoStream -> ExcelBuffer.OpenBookStream/ReadSheet
            end; }
    } }
    var
        ExcelBuffer: Record "Excel Buffer" temporary; // ueberlebt Roundtrips
        LeftMostColumn: Integer;

    local procedure GetExcelCell(Row: Integer; Col: Integer): Text
    begin
        if ExcelBuffer.Get(Row, Col) then
            exit(ExcelBuffer."Cell Value as Text");
    end;
}
```

**Fallstricke:** CaptionClass = '3,' + <Text> ist der Mechanismus fuer zur Laufzeit berechnete Spaltenueberschriften — das Matrix-Pattern schlechthin. Die Integer-Tabelle braucht zwingend einen Filter im SourceTableView, sonst rendert die Liste ins Bodenlose (hier 1.. — Zeilen unterhalb der Daten erscheinen leer). Page-Variablen mit temporary-Record halten die geladene Datei ueber Aktionen hinweg; die Scroll-Aktionen aendern nur den Offset und der Roundtrip wertet Felder und Captions neu aus.

---

## Base64

**Technik:** Beliebige Bilder ohne Media-Feld im Client anzeigen: ControlAddIn mit JavaScript, das einen Base64-String als data-URI in ein img-Element setzt; AL fuettert es aus einem Blob via Base64 Convert.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
controladdin HTML
{
    StartupScript = 'startup.js';
    Scripts = 'scripts.js';
    RequestedHeight = 400;
    HorizontalStretch = true;
    event ControlReady();
    procedure AddImage(b64txt: Text);
}

// startup.js:
//   HTMLContainer = document.getElementById("controlAddIn");
//   Microsoft.Dynamics.NAV.InvokeExtensibilityMethod("ControlReady",[]);
// scripts.js:
//   function AddImage(b64txt) {
//     var image = new Image();
//     image.src = 'data:image/png;base64,' + b64txt;
//     HTMLContainer.appendChild(image); }

// Page (usercontrol(HTML; HTML) im Layout):
trigger OnValidate() // Base64-Text -> Blob -> zurueck ins Add-in
var
    Convert: Codeunit "Base64 Convert";
    InS: InStream;
    OutS: OutStream;
begin
    Rec.BLOB.CreateOutStream(OutS);
    Convert.FromBase64(Rec.base64, OutS);
    Rec.CalcFields(BLOB);
    Rec.BLOB.CreateInStream(InS);
    CurrPage.HTML.AddImage(Convert.ToBase64(InS));
end;
```

**Fallstricke:** Der Add-in-Container heisst im DOM fix "controlAddIn". AL ruft JS-Prozeduren ueber CurrPage.<UserControl-Name>.<Prozedur> auf; die Gegenrichtung laeuft ueber InvokeExtensibilityMethod-Events. Das Text[2000]-Feld fuer Base64 ist reine Demo-Groesse — echte Fotos sprengen das, produktiv Blob/Media als Quelle nehmen.

---

## ImportAndParseEmail

**Technik:** Vollstaendiger MIME-Parser fuer .eml-Dateien in reinem AL: Zustandsautomat (Outside/Header/Data), gefaltete Header-Zeilen, Boundary-Stack fuer verschachtelte Multiparts, Base64-Anhaenge direkt in Blob-Felder dekodiert.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 16.0 / application 27.0 (BC27, nahe am BC28-Stand)

```al
// Kern des Zustandsautomaten (LF: Text[2] = Char13+Char10, Tab: Char 9)
InS.Read(EmailTxt);
Lines := EmailTxt.Split(LF);

// 1) Header: Folgezeile mit Space/Tab gehoert zum vorigen Header (Folding)
if Line.StartsWith(' ') or Line.StartsWith(Tab) then
    Header.Value += ' ' + Line.Trim()
else begin
    HeaderKey := Line.Substring(1, Line.IndexOf(':') - 1);
    HeaderValue := Line.Substring(Line.IndexOf(':') + 1).Trim();
end;

// 2) boundary aus Content-Type; List of [Text] als STACK fuer Verschachtelung
Boundary.Add(GetHeaderDetail(HeaderValue, 'boundary'));

// 3) Zustaende:
//   '--'+Boundary            -> neuer Part (Header-Zustand)
//   Leerzeile im Part-Header -> Datenblock beginnt (TextBuilder sammelt)
//   '--'+Boundary / +'--'    -> Part fertig; '--...--' poppt den Stack:
//                               Boundary.RemoveAt(Boundary.Count);
if Encoding.ToLower() = 'base64' then
    Base64.FromBase64(DataBuilder.ToText().Trim(), OutS) // Anhang -> Blob
else
    OutS.WriteText(DataBuilder.ToText());
// Dateiname des Anhangs aus content-disposition (filename=...)
```

**Fallstricke:** Header-Folding (RFC 5322) nicht vergessen — mehrzeilige Header zerreissen sonst den Parser. Verschachtelte multipart-Container brauchen einen Boundary-STACK; List of [Text] mit RemoveAt(Count) als Pop. GetHeaderDetail schneidet mit Substring(10) hart ab — funktioniert nur, weil 'boundary=' und 'filename=' zufaellig beide 9 Zeichen haben; fuer andere Details bricht es. Im OnOpenPage klebt ein artfremder Barcode-Schnipsel (Interface "Barcode Font Provider" + Enum "Barcode Symbology" — als Nebenfund brauchbar).

---

## EditInExcel

**Technik:** System-Codeunit "Recurrence Schedule": Wiederholungsregeln (taeglich/woechentlich mit Wochentagen) als konfigurierbares Objekt anlegen und die naechsten Termine iterativ berechnen — fertige Infrastruktur fuer wiederkehrende Wartungs-/Prueftermine.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 10.0 / application 21.0

```al
var
    Recur: Codeunit "Recurrence Schedule";
    ID: Guid;
    Next: DateTime;
    i: Integer;
begin
    // woechentlich (Intervall 1), Montag + Donnerstag, ab heute bis 31.12.
    ID := Recur.CreateWeekly(0T, Today(), 20231231D, 1,
            true, false, false, true, false, false, false); // Mo,Di,Mi,Do,Fr,Sa,So
    Message(Recur.RecurrenceDisplayText(ID)); // lesbare Beschreibung der Regel

    Next := 0DT;
    for i := 1 to 10 do begin
        Next := Recur.CalculateNextOccurrence(ID, Next); // ab letztem Treffer
        // Next verwenden (DT2Date(Next) ...)
    end;
    // Alternative: ID := Recur.CreateDaily(0T, Today(), 20231231D, 3);
end;
```

**Fallstricke:** Der Ordnername "EditInExcel" fuehrt in die Irre — die app.json heisst "Recurrence" und der Code demonstriert ausschliesslich den Recurrence-Schedule-Codeunit. CalculateNextOccurrence iteriert vom zuletzt gelieferten DateTime aus — mit 0DT starten. Die sieben Booleans in CreateWeekly sind die Wochentage Mo–So in Reihenfolge; SetMinDateTime kann den Startpunkt verschieben.

---

## Base64 testing

**Technik:** Base64 ist keine Zeichenkodierung: VOR dem Enkodieren entscheidet TextEncoding (UTF8/UTF16/Codepage) ueber die Bytes — Sonderzeichen wie Umlaute sind der Testfall. Nebenbei eine Vorlage fuer Facade+Implementation samt AAA-Testcodeunit mit Library Assert.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** runtime 5.0, BC16, target OnPrem (DotNet)

```al
var
    Base64: Codeunit "Base64 Convert";
    B64, Txt: Text;
begin
    // 'ÆØÅæøå' UTF16-kodiert ergibt 'xgDYAMUA5gD4AOUA'
    B64 := Base64.ToBase64('ÆØÅæøå', TextEncoding::UTF16);

    // Zurueck NUR mit derselben Encoding-Angabe:
    Txt := Base64.FromBase64(B64, TextEncoding::UTF16); // korrekt
    // Base64.FromBase64(B64)  -> Default UTF8 = Zeichensalat
end;

// Teststruktur (Subtype = Test; TestPermissions = NonRestrictive):
[Test]
procedure StringToBase64UTF16Test()
var
    ConvertedText: Text;
begin
    // [WHEN] The string is converted
    ConvertedText := Base64Convert.ToBase64(SampleUTF16Txt, TextEncoding::UTF16);
    // [THEN] The converted value is correct
    Assert.AreEqual(Base64SampleUTF16Txt, ConvertedText, Err);
end;
```

**Fallstricke:** FromBase64 ohne TextEncoding-Parameter nimmt UTF8 an — UTF16-kodierte Daten kommen als Muell zurueck, ohne Fehler. Bei TextEncoding::Windows ist Codepage 1252 der Default. Das Demo klont Microsofts System-App-Implementierung mit DotNet Convert/Encoding — deshalb target OnPrem; in eigener Cloud-App immer die System-App-Codeunit "Base64 Convert" nehmen, nie DotNet.

---

## Übersprungen (bewusst)

- SplitTextInLines (Datei leer)
- testJsonAndDateTime (3-Zeilen-Demo: 0DT in JsonValue)

