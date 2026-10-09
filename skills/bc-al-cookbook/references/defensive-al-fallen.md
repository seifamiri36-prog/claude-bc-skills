# Defensive AL, Sprach-Fallen & Kuriosa

_Destilliert aus Erik Hougaards Youtube-Video-Sources (Ordnername = Videothema)._
_Vollquellen: https://github.com/hougaard/Youtube-Video-Sources (lokal klonen; Ordnername = Videothema)_

Der Cluster lehrt zwei Dinge: wie AL STILL scheitert und wie man Fehler aktiv zum Werkzeug macht. Die stillen Fallen sind Rueckgabewert-Semantik statt Exceptions (HttpClient liefert false, Next(-1) liefert Schrittzahl, SetRange interpretiert keine Filterausdruecke) und Auswertungsregeln, die keiner erwartet (kein garantiertes Short-Circuit, case-Labels sind sequentiell ausgewertete Ausdruecke, and-vor-or-Praezedenz). Die Werkzeug-Seite ist das moderne ErrorInfo-Oekosystem: sammelbare Fehler fuer Alles-auf-einmal-Validierung, Fehlerdialoge mit Fix-Buttons und Feld-Navigation, plus Confirm Management fuer UI-lose Kontexte. Dazu kommen drei Einzeljuwelen mit direktem Bau-ERP-Wert: upperlimit() im CalcFormula (Stichtagssalden), der Schleifen-Bug beim Aendern des gefilterten Feldes (Batch-Rechnungsversand!) und mehrere Report-Layouts per rendering-Block.

**Wertvollste Ordner:** Upperlimit · TwoErrorsInOne · ActionErrors · confirmmanagement · SubtleBug

## Themen (nach Praxis-Relevanz)

- ●●●  **dontshortcut** — Statuswechsel an Belegen NIE per Validate(Status) abkuerzen, sondern die Standard-Prozess-Codeunit rufen (hier Release Sales Document.Reopen) — nur sie fuehrt Nebenpruefungen aus und feuert die Events, auf die andere Extensions hoeren.
- ●●●  **SubtleBug** — Der klassische Schleifen-Bug: FindSet ueber einen Filter, dessen Feld der Schleifenkoerper selbst aendert — der Datensatz faellt aus dem aktiven Set und Next() ueberspringt den Folgesatz. Demo: Batch-Rechnungsversand per E-Mail mit Report.SaveAs als PDF.
- ●●●  **Upperlimit** — Der CalcFormula-Filtermodifikator upperlimit(field(...)) nimmt nur die OBERE Grenze des uebergebenen Filters — der Mechanismus hinter 'Balance at Date': Saldo BIS Stichtag statt Bewegung im Zeitraum.
- ●●●  **TwoErrorsInOne** — Sammelbare Fehler: [ErrorBehavior(ErrorBehavior::Collect)] laesst mehrere Error(ErrorInfo)-Aufrufe mit Collectible(true) weiterlaufen statt abzubrechen — der Aufrufer liest alle mit GetCollectedErrors(). Damit zeigt eine Validierung ALLE Probleme auf einmal statt eines pro Anlauf.
- ●●●  **hiddengems** — Der rendering-Block gibt EINEM Report mehrere Layouts (Word + RDLC), zwischen denen der Benutzer zur Laufzeit waehlt; DefaultRenderingLayout bestimmt den Standard. Zweites Gem im Ordner: Interfaces koennen auch riesige Standard-Codeunit-Oberflaechen (Sales-Post, 48 Methoden) abbilden — leere Stubs kompilieren.
- ●●●  **ActionErrors** — Aktionierbare Fehler: ErrorInfo bekommt Navigation (PageNo/FieldNo/RecordId + AddNavigationAction springt zum fehlerhaften Feld) und Fix-Buttons (AddAction ruft eine Codeunit-Prozedur mit ErrorInfo-Parameter). Kontext rettet man ueber eine SingleInstance-Codeunit ueber den Rollback hinweg.
- ●●●  **confirmmanagement** — Plain Confirm() crasht in UI-losen Kontexten (Job Queue, Web Service, API, Background Session). Codeunit "Confirm Management" mit GetResponseOrDefault liefert dort statt des Crashs den Default zurueck.
- ●●●  **ErrorWithoutErrors** — HttpClient wirft keine Exceptions: Transportfehler (DNS, Timeout, Unsinn-URL) kommen als false-Rueckgabe, HTTP-Fehlerstatus (404/500) dagegen als true mit IsSuccessStatusCode=false. Robuste HTTP-Aufrufe pruefen BEIDE Ebenen.
- ●●○  **ELI5-Defensive-AL** — Defensives AL in drei Schichten: TryFunction als Fanggriff um crashende Plattformfunktionen (DMY2Date), deklarative Absicherung per TableRelation+NotBlank, und Boundary-Checks mit MaxStrLen beim Zuweisen fremder Texte.
- ●●○  **SintacticSugar** — Prozeduren direkt am Tabellenobjekt wirken wie Instanzmethoden: innen ist Rec der Record des Aufrufers. Records sind ausserdem als Rueckgabetyp erlaubt — damit werden Muster wie Clone() moeglich.
- ●●○  **ErrorJobQueue** — Was mit Error() in einer Job-Queue-Codeunit passiert: der Lauf wird zurueckgerollt, der Eintrag geht auf Status Error, die Meldung landet im Job Queue Log Entry, und 'Maximum No. of Attempts to Run' steuert automatische Wiederholungen.
- ●●○  **ChangeCompany** — Rec.ChangeCompany(Name) liest (und schreibt) Daten einer anderen Firma derselben Datenbank, ohne die Session zu wechseln — die Company-Tabelle liefert die Firmenliste zum Durchlaufen.
- ●●○  **theworstprogram** — Drei stille AL-Fallen in fuenf Zeilen: SetRange interpretiert keine Filterausdruecke (der String '10000...30000' wird als woertlicher Wert gesucht), Schleifen ohne FindSet starten auf undefinierter Position, und Next(-1) laeuft rueckwaerts und gibt die tatsaechlich gegangene Schrittzahl zurueck.
- ●●○  **weirdpagerror** — Selbstaktualisierende Seite ohne Benutzerinteraktion: BC hat keinen nativen Page-Timer, ein JS-ControlAddIn mit StartTimer/TimerTic-Trigger pollt zyklisch (hier: Extension-Deployment-Status) und zieht die Anzeige per CurrPage.Update(false) nach. Ausloeser des Videos: ein offen gelassener Dialog vor Page.Run erzeugt einen kryptischen Seitenfehler.
- ●●○  **ThePestkyBug** — Division durch null als Datenfehler: ein Guard-freier Divisor drei Aufrufebenen unter einem OnBeforeValidate-Trigger crasht erst zur Laufzeit mit 'Division by zero' — ohne Hinweis auf die Stelle. Divisoren aus Parametern/Daten immer pruefen.
- ●●○  **InOneLine** — Fluent-Chaining auf Text-Methoden: Split() liefert List of [Text], darauf laesst sich direkt Get() und wieder Split() ketten — Substring-Extraktion in einer Zeile statt StrPos/CopyStr-Arithmetik.
- ●○○  **HowMuchALonAsingleLine** — Operator-Praezedenz in booleschen Ketten: and bindet staerker als or — eine lange ungeklammerte Kette zerfaellt in (A and B and ...) or (C and D) und feuert anders als gelesen.
- ●○○  **TwoWeirdPatterns** — AL wertet boolesche Ketten vollstaendig aus — kein garantiertes Short-Circuit. Das Set-Idiom `false in [C1(), C2(), C3()]` ist ein kompaktes 'mindestens eine Bedingung false', ruft aber IMMER alle Funktionen auf (im Video per Sleep gemessen).
- ●○○  **TheCaseWithCaseStatements** — AL-case ist keine Sprungtabelle: Labels duerfen beliebige Ausdruecke und Funktionsaufrufe sein und werden der Reihe nach ausgewertet wie eine if-else-Kette — bis zum ersten Treffer.

---

## dontshortcut

**Technik:** Statuswechsel an Belegen NIE per Validate(Status) abkuerzen, sondern die Standard-Prozess-Codeunit rufen (hier Release Sales Document.Reopen) — nur sie fuehrt Nebenpruefungen aus und feuert die Events, auf die andere Extensions hoeren.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
action(ReopenAction)
{
    trigger OnAction()
    var
        ReleaseSalesDoc: Codeunit "Release Sales Document";
    begin
        // RICHTIG: der Standard-Prozessweg
        ReleaseSalesDoc.Reopen(Rec);

        // FALSCH (der Shortcut aus dem Video):
        // Rec.Validate(Status, Rec.Status::Open);
        // Rec.Modify(true);
    end;
}
```

**Fallstricke:** Der Shortcut kompiliert sauber und funktioniert scheinbar — er ueberspringt aber Warehouse-Pruefungen, Genehmigungslogik und OnBeforeReopen/OnAfterReopen-Events. Fuer eigene Belege heisst das: einen eigenen Release/Reopen-Codeunit als einzigen Statuswechsel-Weg bauen, nie Feldzuweisung im UI-Code.

---

## SubtleBug

**Technik:** Der klassische Schleifen-Bug: FindSet ueber einen Filter, dessen Feld der Schleifenkoerper selbst aendert — der Datensatz faellt aus dem aktiven Set und Next() ueberspringt den Folgesatz. Demo: Batch-Rechnungsversand per E-Mail mit Report.SaveAs als PDF.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 12.0 / BC23 (AllowInCustomizations ab BC23)

```al
PSH.SetRange("No. Printed", 0);
if PSH.FindSet() then
    repeat
        // Report erhoeht "No. Printed" -> Satz faellt aus dem Filter
        // -> Next() ueberspringt den NAECHSTEN Satz!
        PSH2 := PSH;                     // kopiert Felder, NICHT die Filter
        PSH2.SetRange("No.", PSH."No."); // Ein-Beleg-Filter fuer den Report
        Ref.GetTable(PSH2);
        Clear(TempBlob);                 // fehlt im Original: Blob sonst wiederverwendet
        TempBlob.CreateOutStream(OutS);
        if Report.SaveAs(Report::"Sales Invoice NA", '', ReportFormat::Pdf, OutS, Ref) then begin
            TempBlob.CreateInStream(InS);
            EmailMsg.Create(PSH."Sell-to E-Mail", 'Your Invoice', 'Here you go!');
            EmailMsg.AddAttachment('Invoice ' + PSH."No." + '.pdf', 'application/pdf', Base64.ToBase64(InS));
            Email.Send(EmailMsg, "Email Scenario"::"Sales Invoice");
        end;
    until PSH.Next() = 0;
// Fix: erst alle "No." in eine List of [Code[20]] sammeln, dann je No. verarbeiten
```

**Fallstricke:** Der Bug ist unsichtbar: kein Fehler, nur jede zweite Rechnung wird verschickt. Record-Zuweisung (PSH2 := PSH) kopiert Felder und Position, aber keine Filter. ⚠ **UNBELEGT (Prüfung 01.09.2026, D+B):** Diese Aussage trägt **weder die Demo noch die MS-Doku** — sie ist nicht widerlegt, sondern **unbelegt**. ⚠ **Ein Arbeitspaket in `PLAN-A-Musterzuordnung` baut darauf: vor dem Bau am Bestand MESSEN, nicht übernehmen.** ⚠ **Und die MS-Doku zeigt hier sogar in die Gegenrichtung:** `Record.Copy` kopiert laut Doku ausdrücklich **auch die Filter** („copies the current record's field values, **filters**, sorting, marks …“), und für Filter allein gibt es `CopyFilters`. Über das ZUWEISUNGSZEICHEN `:=` sagt Microsoft **nichts**. *(AP-4 Menge/Vertrag, ●●●)* PDF-Anhang geht ueber Base64.ToBase64(InStream) an EmailMsg.AddAttachment. Nebengem in test.al: `AllowInCustomizations = Never` versteckt ein Feld komplett vor Personalisierung (ab BC23).

---

## Upperlimit

**Technik:** Der CalcFormula-Filtermodifikator upperlimit(field(...)) nimmt nur die OBERE Grenze des uebergebenen Filters — der Mechanismus hinter 'Balance at Date': Saldo BIS Stichtag statt Bewegung im Zeitraum.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 10.0 / BC21; Modifikator existiert seit langem, kaum dokumentiert

```al
tableextension 66100 "My COA" extends "G/L Account"
{
    fields
    {
        field(66100; MyBalance; Decimal)
        {
            FieldClass = FlowField;
            // Date Filter '01.01..31.03' -> summiert wird ..31.03 (alles bis Stichtag)
            CalcFormula = sum("G/L Entry".Amount where(
                "G/L Account No." = field("No."),
                "Posting Date" = field(upperlimit("Date Filter"))));
        }
    }
}
```

**Fallstricke:** Ohne upperlimit ergibt derselbe FlowField die Periodenbewegung (Net Change) ⚠ **UNBELEGT (Prüfung 01.09.2026, D+B):** Diese Aussage trägt **weder die Demo noch die MS-Doku** — sie ist nicht widerlegt, sondern **unbelegt**. ⚠ **Ein Arbeitspaket in `PLAN-A-Musterzuordnung` baut darauf: vor dem Bau am Bestand MESSEN, nicht übernehmen.** *(AP-5 Kostensicht — hier hängen ZAHLEN dran: wer sich irrt, meldet Periodenbewegung als Saldo oder umgekehrt.)* — zwei fachlich voellig verschiedene Zahlen, ein Wort Unterschied. Funktioniert nur in CalcFormula-where, nicht mit SetFilter im Code. Leerer Date Filter = keine Obergrenze = Gesamtsumme. Fuer das Referenzprojekt direkt verwendbar: kumulierte Aufmass-/Leistungssummen zum Stichtag als FlowField statt Handschleife.

---

## TwoErrorsInOne

**Technik:** Sammelbare Fehler: [ErrorBehavior(ErrorBehavior::Collect)] laesst mehrere Error(ErrorInfo)-Aufrufe mit Collectible(true) weiterlaufen statt abzubrechen — der Aufrufer liest alle mit GetCollectedErrors(). Damit zeigt eine Validierung ALLE Probleme auf einmal statt eines pro Anlauf.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** app.json runtime 8.0/BC19 (ErrorInfo ab BC19); ErrorBehavior::Collect offiziell erst ab BC20.x-Runtime

```al
[ErrorBehavior(ErrorBehavior::Collect)]
procedure ValidateAll()
var
    E: ErrorInfo;
begin
    E := ErrorInfo.Create('Fehler 1');
    E.Collectible(true);
    E.DetailedMessage('Interne Detailinfo');
    Error(E);                    // bricht NICHT ab, wird gesammelt

    E := ErrorInfo.Create('Fehler 2');
    E.Collectible(true);
    Error(E);                    // ebenfalls gesammelt
end;

[TryFunction]
procedure TryValidateAll()
begin
    ValidateAll();
end;

// Aufrufer:
if not TryValidateAll() then begin
    Errors := GetCollectedErrors();      // List of [ErrorInfo]
    Message('%1 Fehler gesammelt', Errors.Count());
end;
```

**Fallstricke:** Ohne Collectible(true) stoppt Error() sofort — beides muss zusammenkommen. Am Ende des Collect-Scopes wirft die Runtime doch einen (Sammel-)Fehler, deshalb die TryFunction-Huelle beim Aufrufer. DetailedMessage und CustomDimensions(Dictionary) haengen Telemetrie-Kontext an, den der Endbenutzer nie sieht. Verbosity steuert das Telemetrie-Level je Fehler.

---

## hiddengems

**Technik:** Der rendering-Block gibt EINEM Report mehrere Layouts (Word + RDLC), zwischen denen der Benutzer zur Laufzeit waehlt; DefaultRenderingLayout bestimmt den Standard. Zweites Gem im Ordner: Interfaces koennen auch riesige Standard-Codeunit-Oberflaechen (Sales-Post, 48 Methoden) abbilden — leere Stubs kompilieren.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 9.0 / application 20 — rendering-Block ab BC20.x

```al
report 50100 "Item Report"
{
    ApplicationArea = All;
    UsageCategory = ReportsAndAnalysis;
    DefaultRenderingLayout = "word.docx";
    dataset
    {
        dataitem(Item; Item) { }
    }
    rendering   // mehrere Layouts an EINEM Report
    {
        layout("word.docx")
        {
            Type = Word;
            LayoutFile = 'word.docx';
        }
        layout("rdlc.rdlc")
        {
            Type = RDLC;
            LayoutFile = 'rdlc.rdlc';
        }
    }
}
```

**Fallstricke:** Sobald ein rendering-Block existiert, ist DefaultRenderingLayout Pflicht. Die Layoutwahl passiert ueber die Request-Page bzw. die Report-Layout-Verwaltung — kein Code noetig. Fuer ein Bau-ERP (LV-PDF): RDLC- und Word-Variante desselben Reports parallel ausliefern und per Musterprobe vergleichen, ohne den Report zu duplizieren.

---

## ActionErrors

**Technik:** Aktionierbare Fehler: ErrorInfo bekommt Navigation (PageNo/FieldNo/RecordId + AddNavigationAction springt zum fehlerhaften Feld) und Fix-Buttons (AddAction ruft eine Codeunit-Prozedur mit ErrorInfo-Parameter). Kontext rettet man ueber eine SingleInstance-Codeunit ueber den Rollback hinweg.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 11.0 / BC22; ErrorInfo-Actions ab ~BC20/21

```al
trigger OnAction()
var
    e: ErrorInfo;
    Helpful: Codeunit Helpful;
begin
    e.Message := 'Adresse fehlt';
    e.PageNo := Page::"Customer Card";
    e.FieldNo := Rec.FieldNo(Address);
    e.RecordId := Rec.RecordId;
    e.AddNavigationAction('Zum Feld springen');
    e.AddAction('Automatisch beheben', Codeunit::Helpful, 'BeHelpful');
    Helpful.SetContext(Rec.SystemId);   // Kontext ueber den Fehler retten
    Error(e);
end;

codeunit 50100 Helpful
{
    SingleInstance = true;
    var
        RememberedId: Guid;
    procedure SetContext(g: Guid) begin RememberedId := g; end;
    procedure BeHelpful(e: ErrorInfo)   // Pflicht-Signatur: genau ein ErrorInfo
    var
        C: Record Customer;
    begin
        C.GetBySystemId(RememberedId);
        // ... Reparatur ausfuehren
    end;
}
```

**Fallstricke:** Error(e) rollt die Transaktion zurueck, der Button-Callback laeuft DANACH — ungesicherte Datenaenderungen sind weg; deshalb der SingleInstance-Trick (ueberlebt den Fehler innerhalb der Session). Die Callback-Prozedur muss public sein und exakt (e: ErrorInfo) als Signatur haben, sonst passiert beim Klick still nichts. RecordId+FieldNo machen aus der Meldung einen Sprung direkt ins Feld — Gold fuer Validierungsfehler in LV-Zeilen.

---

## confirmmanagement

**Technik:** Plain Confirm() crasht in UI-losen Kontexten (Job Queue, Web Service, API, Background Session). Codeunit "Confirm Management" mit GetResponseOrDefault liefert dort statt des Crashs den Default zurueck.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 9.0 / BC20; Confirm Management existiert seit NAV-Zeiten

```al
var
    ConfirmMgt: Codeunit "Confirm Management";
begin
    // FALSCH im Hintergrund: wirft 'callback functions are not allowed'
    // if Confirm('Weiter?', true) then ...

    // RICHTIG: mit UI fragt es, ohne UI kommt der Default (hier: true)
    if ConfirmMgt.GetResponseOrDefault('Weiter?', true) then
        DoTheWork();
end;
```

**Fallstricke:** Jeder Confirm/Dialog in Code, der je aus Job Queue oder API laufen kann, ist eine tickende Bombe — der Fehler kommt erst in Produktion. GetResponse (ohne OrDefault) liefert ohne UI immer false. Alternative fuer eigene Logik: GuiAllowed() pruefen. Fuer das Referenzprojekt: alle Buchungs-/Freigabepfade, die spaeter das Gateway oder die Job Queue ruft, muessen Confirm-frei sein.

---

## ErrorWithoutErrors

**Technik:** HttpClient wirft keine Exceptions: Transportfehler (DNS, Timeout, Unsinn-URL) kommen als false-Rueckgabe, HTTP-Fehlerstatus (404/500) dagegen als true mit IsSuccessStatusCode=false. Robuste HTTP-Aufrufe pruefen BEIDE Ebenen.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 11.0 / BC22

```al
var
    Client: HttpClient;
    Response: HttpResponseMessage;
begin
    if Client.Get(Url, Response) then begin
        if Response.IsSuccessStatusCode() then
            Message('OK %1', Response.HttpStatusCode())
        else
            Message('HTTP-Fehler %1', Response.HttpStatusCode()); // 404/500 ist KEIN false!
    end else
        Message('Transportfehler: %1', GetLastErrorText());
end;
```

**Fallstricke:** Wer nur den Boolean prueft, uebersieht jeden 4xx/5xx; wer nur IsSuccessStatusCode prueft, liest bei Transportfehler eine leere Response. GetLastErrorText() traegt nach einem false den Netzwerkfehler — direkt danach abholen, der naechste Aufruf ueberschreibt ihn.

---

## ELI5-Defensive-AL

**Technik:** Defensives AL in drei Schichten: TryFunction als Fanggriff um crashende Plattformfunktionen (DMY2Date), deklarative Absicherung per TableRelation+NotBlank, und Boundary-Checks mit MaxStrLen beim Zuweisen fremder Texte.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 16.0 / BC27; alle Techniken ab BC14 nutzbar

```al
[TryFunction]
local procedure TryCreateDate(d: Integer; m: Integer; y: Integer; var OutDate: Date)
begin
    OutDate := DMY2Date(d, m, y); // 29.02.2001 -> Laufzeitfehler, vom Try gefangen
end;

// Deklarativ statt imperativ absichern:
field(50100; ImportantAccount; Code[20])
{
    TableRelation = "G/L Account"."No." where("Account Type" = const(Total));
    NotBlank = true;
    trigger OnValidate()
    var
        GL: Record "G/L Account";
    begin
        GL.Get(ImportantAccount); // harte Zusicherung
        if GL."Account Type" <> GL."Account Type"::Total then
            Error('Not a total account type');
    end;
}

// Boundary-Check bei Fremddaten:
CPG.Validate(ImportantAccount, CopyStr(x, 1, MaxStrLen(CPG.ImportantAccount)));
```

**Fallstricke:** TableRelation validiert NICHT bei programmatischer Zuweisung ohne Validate(). Das Muster `if not TGC.Get(...) then;` (leeres then) schluckt Fehler bewusst — lesbar als 'optional laden'. TryFunction rollt Schreibvorgaenge NICHT zurueck, sie faengt nur den Fehler. Ungueltige Datumsteile crashen DMY2Date zur Laufzeit — Datumsimporte immer per TryFunction pruefen.

---

## SintacticSugar

**Technik:** Prozeduren direkt am Tabellenobjekt wirken wie Instanzmethoden: innen ist Rec der Record des Aufrufers. Records sind ausserdem als Rueckgabetyp erlaubt — damit werden Muster wie Clone() moeglich.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 11.0 / BC22; Table-Methoden gehen seit BC14, Record-Rueckgabe seit ~BC19

```al
table 50109 MySugarTable
{
    fields { field(1; P; Code[30]) { } field(2; Description; Text[200]) { } }
    keys { key(PK; P) { Clustered = true; } }

    procedure MarkDone()
    begin
        Rec.Description := 'Done';   // aendert die VARIABLE des Aufrufers (in-memory)
    end;

    procedure Clone(): Record MySugarTable
    var
        NewRec: Record MySugarTable;
    begin
        NewRec := Rec;
        NewRec.P := IncStr(Rec.P);
        NewRec.Insert();
        exit(NewRec);                // Record als Rueckgabewert
    end;
}
// Aufrufer:  Sugar.MarkDone();  NewS := Sugar.Clone();
```

**Fallstricke:** Die Tabellenmethode aendert nur den Speicherzustand — ohne Modify() landet nichts in der DB. Ein Parameter darf sogar Rec heissen und beschattet das implizite Rec (kompiliert, verwirrt). Der Record-Rueckgabewert ist eine Kopie inklusive Filterzustand. Fuer ein Bau-ERP das Muster schlechthin: LVPosition.Clone(), Rapport.Abschliessen() als Methoden AN der Tabelle statt in Streu-Codeunits.

---

## ErrorJobQueue

**Technik:** Was mit Error() in einer Job-Queue-Codeunit passiert: der Lauf wird zurueckgerollt, der Eintrag geht auf Status Error, die Meldung landet im Job Queue Log Entry, und 'Maximum No. of Attempts to Run' steuert automatische Wiederholungen.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 10.0 / BC21

```al
codeunit 56800 ErrorJob
{
    trigger OnRun()
    begin
        Error('It''s not working!!!');
    end;
}
// Als Job Queue Entry einplanen:
// - Fehler bricht nur DIESEN Lauf ab (Transaktion des Laufs wird zurueckgerollt)
// - Meldung erscheint im Job Queue Log Entry / Fehlermeldungsfeld des Eintrags
// - nach den konfigurierten Wiederholversuchen bleibt der Eintrag auf Error stehen
```

**Fallstricke:** Niemand sieht den Fehler ausser im Log — es gibt keine Benutzer-Benachrichtigung; Monitoring (Log-Seite, Telemetrie, eigene Mail) muss man selbst bauen. Teilarbeit vor einem Commit ist weg, Teilarbeit nach einem Commit bleibt — Commits in Job-Queue-Code deshalb bewusst setzen. Ein absichtlicher Mini-Fehlerjob wie dieser ist der schnellste Test, ob das eigene Job-Queue-Monitoring wirklich anschlaegt.

---

## ChangeCompany

**Technik:** Rec.ChangeCompany(Name) liest (und schreibt) Daten einer anderen Firma derselben Datenbank, ohne die Session zu wechseln — die Company-Tabelle liefert die Firmenliste zum Durchlaufen.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 5.0 / BC17; Funktion existiert seit NAV

```al
var
    Company: Record Company;
    Customer: Record Customer;
begin
    Company.SetFilter(Name, '<>%1', CompanyName());
    if Company.FindSet() then
        repeat
            Customer.ChangeCompany(Company.Name);
            if Customer.FindFirst() then
                Message('%1: %2', Company.Name, Customer.Name);
        until Company.Next() = 0;
end;
```

**Fallstricke:** ChangeCompany wechselt NUR die Datenquelle der einen Variable: CompanyName(), Setups, Nummernserien, Events und Trigger-Kontext bleiben in der aktuellen Firma — Insert(true) in der Fremdfirma feuert Trigger, die im falschen Setup-Kontext rechnen koennen. Berechtigungen werden je Firma geprueft. Fuer Konzern-Auswertungen (mehrere Bau-Gesellschaften) lesen ok, schreiben nur mit grosser Vorsicht.

---

## theworstprogram

**Technik:** Drei stille AL-Fallen in fuenf Zeilen: SetRange interpretiert keine Filterausdruecke (der String '10000...30000' wird als woertlicher Wert gesucht), Schleifen ohne FindSet starten auf undefinierter Position, und Next(-1) laeuft rueckwaerts und gibt die tatsaechlich gegangene Schrittzahl zurueck.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 10.0 / BC21

```al
CustomerToFind := '10000...30000';
Rec.SetRange(Name, CustomerToFind);
// (1) SetRange = exakter Match: gesucht wird der Name '10000...30000'.
//     Bereiche/Wildcards brauchen SetFilter:
//     Rec.SetFilter("No.", '10000..30000');
repeat
until Rec.Next(-1) = 1;
// (2) kein FindSet/FindFirst davor: Startposition undefiniert
// (3) Next(-1) liefert -1 (bewegt) oder 0 (Ende) - nie 1 -> Endlosschleife
Message('%1', Format(Rec, 40, 0)); // Format(Record) gibt den Primaerschluessel aus
```

**Fallstricke:** Die SetRange/SetFilter-Verwechslung ist die gefaehrlichste: kein Fehler, kein Treffer, Batchlauf verarbeitet still nichts. Next() vergleicht man gegen 0, nie gegen eine konkrete Schrittzahl. Format(Rec) auf einem Record ist ein legitimer Debug-Trick fuer den Primaerschluessel.

---

## weirdpagerror

**Technik:** Selbstaktualisierende Seite ohne Benutzerinteraktion: BC hat keinen nativen Page-Timer, ein JS-ControlAddIn mit StartTimer/TimerTic-Trigger pollt zyklisch (hier: Extension-Deployment-Status) und zieht die Anzeige per CurrPage.Update(false) nach. Ausloeser des Videos: ein offen gelassener Dialog vor Page.Run erzeugt einen kryptischen Seitenfehler.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 16.0 / BC27; ControlAddIn-Timer-Trick funktioniert seit BC14

```al
page 50100 "Deployment Watcher"
{
    PageType = StandardDialog;
    SourceTable = "Extension Deployment Status";
    SourceTableTemporary = true;   // reiner Anzeige-Puffer
    layout
    {
        area(Content)
        {
            usercontrol(Timer; "AL HTMLHelper")   // JS-Add-in mit setInterval
            {
                trigger ControlReady()
                begin
                    CurrPage.Timer.StartTimer();
                end;

                trigger TimerTic()
                var
                    ExtMgt: Codeunit "Extension Management";
                    Status: Record "Extension Deployment Status" temporary;
                begin
                    ExtMgt.GetAllExtensionDeploymentStatusEntries(Status);
                    Status.SetCurrentKey("Started On");
                    if Status.FindLast() then begin
                        Rec.DeleteAll();
                        Rec := Status;
                        Rec.Insert();
                        CurrPage.Update(false);   // Anzeige nachziehen, kein Commit
                    end;
                end;
            }
        }
    }
}
```

**Fallstricke:** start.al zeigt den Fehler: Dialog.Open() ohne Close() und danach Page.Run() -> Client-Fehler; Dialoge immer schliessen bevor eine Seite laeuft. Weitere Griffe im Original: Detailstatus als Stream lesen (GetDeploymentDetailedStatusMessageAsStream + TempBlob), rohe Fehlertexte per Contains() auf freundliche Meldungen mappen, Ergebnis per LogMessage mit CustomDimensions in die Publisher-Telemetrie schreiben.

---

## ThePestkyBug

**Technik:** Division durch null als Datenfehler: ein Guard-freier Divisor drei Aufrufebenen unter einem OnBeforeValidate-Trigger crasht erst zur Laufzeit mit 'Division by zero' — ohne Hinweis auf die Stelle. Divisoren aus Parametern/Daten immer pruefen.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 7.0 / BC18

```al
tableextension 50143 "Sales Lines Ext" extends "Sales Line"
{
    fields
    {
        modify(Quantity)
        {
            trigger OnBeforeValidate()
            begin
                Check(Quantity, 10, -10);   // p + u = 0 ...
            end;
        }
    }
    local procedure Check(q: Decimal; p: Decimal; u: Integer)
    begin
        if q > q / (p + u) then   // ... -> Laufzeitfehler mitten in der Validierung
            Message('bug');
    end;
}
```

**Fallstricke:** ⚠⚠ **BERICHTIGT 01.09.2026 (B): Hier stand „AL liefert dem Anwender keinen Stacktrace“. DAS IST WIDERLEGT.** Der Anwender bekommt ihn über **Copy details** im Fehlerdialog — MS *Understanding the error dialog*, Tabelle *Information in Copy details section*: „**AL call stack** — The AL stack trace in the session when the error occurred“. Richtig bleibt nur: der Dialog zeigt ihn nicht von selbst, der Anwender muss ihn über Copy details holen. Der Fehler erscheint zunächst als nackte Meldung beim Eintippen einer Menge. Lehre fuer Formelwerke (Kalkulation!): jede Division gegen 0 wachen. Nebenbei sichtbar: AL-Bezeichner sind case-insensitiv (Parameter q/Q gemischt kompiliert), und modify(Feld) in einer Tableextension kann OnBeforeValidate an Standardfelder haengen.

---

## InOneLine

**Technik:** Fluent-Chaining auf Text-Methoden: Split() liefert List of [Text], darauf laesst sich direkt Get() und wieder Split() ketten — Substring-Extraktion in einer Zeile statt StrPos/CopyStr-Arithmetik.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 10.0 / BC21

```al
T := 'Text[250]';
Output := T.Split('[').Get(2).Split(']').Get(1);   // -> '250'

// klassisches Aequivalent:
// P1 := StrPos(T, '[');
// P2 := StrPos(T, ']');
// Output := CopyStr(T, P1 + 1, P2 - P1 - 1);
```

**Fallstricke:** List.Get() ist 1-basiert und wirft einen Laufzeitfehler, wenn das Trennzeichen fehlt (Split liefert dann nur 1 Element) — der Einzeiler hat keinerlei Fehlerbehandlung. Fuer Fremddaten die Kette in eine TryFunction packen oder vorher Contains() pruefen.

---

## HowMuchALonAsingleLine

**Technik:** Operator-Praezedenz in booleschen Ketten: and bindet staerker als or — eine lange ungeklammerte Kette zerfaellt in (A and B and ...) or (C and D) und feuert anders als gelesen.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** runtime 8.0 / BC19

```al
if true and false and true and (false and false) or true and true then
    Message('feuert trotzdem!');
// gelesen als: (true and false and true and (false and false)) or (true and true)
// -> false or true -> true

// Regel: gemischte and/or-Ketten IMMER klammern:
if (CondA and CondB) or (CondC and CondD) then ...;
```

**Fallstricke:** Der Bug ist unsichtbar, weil beide Lesarten kompilieren. Kombiniert mit der Nicht-Short-Circuit-Auswertung (siehe TwoWeirdPatterns) laufen zudem alle Teilausdruecke.

---

## TwoWeirdPatterns

**Technik:** AL wertet boolesche Ketten vollstaendig aus — kein garantiertes Short-Circuit. Das Set-Idiom `false in [C1(), C2(), C3()]` ist ein kompaktes 'mindestens eine Bedingung false', ruft aber IMMER alle Funktionen auf (im Video per Sleep gemessen).

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** runtime 10.0 / BC21

```al
// beide Varianten rufen ALLE drei Funktionen auf:
if not Condition1() or not Condition2() or not Condition3() then
    Message('teuer, wenn Condition2/3 lange rechnen');

if false in [Condition1(), Condition2(), Condition3()] then
    Message('kurios, aber gleich teuer');

// Short-Circuit gibt es nur durch Schachtelung:
if not Condition1() then
    exit;
if not Condition2() then
    exit;
```

**Fallstricke:** Teure oder nebenwirkende Bedingungen gehoeren nie in eine and/or-Kette oder in eine in-Liste — die Reihenfolge rettet nichts, alles laeuft. Der beliebte Fehler `if Rec.Get(x) and (Rec.Feld = y)` ist deshalb riskant; geschachtelte ifs sind der einzig sichere Weg.

---

## TheCaseWithCaseStatements

**Technik:** AL-case ist keine Sprungtabelle: Labels duerfen beliebige Ausdruecke und Funktionsaufrufe sein und werden der Reihe nach ausgewertet wie eine if-else-Kette — bis zum ersten Treffer.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** runtime 8.0 / BC19

```al
case age of
    test(0):
        Message('Welcome to the world');
    test(1):
        Message('Learn to walk');
    test(16):
        Message('Sweet sixteen');
    else
        Message('Anything else');
end;
// identisch zu: if age = test(0) then ... else if age = test(1) then ...
// jede Label-Funktion VOR dem Treffer wird tatsaechlich aufgerufen
```

**Fallstricke:** Seiteneffekte oder teure Aufrufe in case-Labels feuern fuer jede nicht passende Branch davor. Dass Funktionsaufrufe als Label ueberhaupt kompilieren, ueberrascht die meisten — nuetzlich fuer dynamische Grenzen, gefaehrlich fuer Performance.

---

## Übersprungen (bewusst)

- RobustCode (nur Hello-World-Geruest)
- shortcomingsintheplatform (nur Hello-World-Geruest)
- ELI5-Transactions (unfertiger Demo-Torso, kompiliert nicht)

