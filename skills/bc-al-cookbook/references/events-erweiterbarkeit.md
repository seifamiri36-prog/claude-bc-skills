# Events, Interfaces, Enums & Erweiterbarkeit

_Destilliert aus Erik Hougaards Youtube-Video-Sources (Ordnername = Videothema)._
_Vollquellen: https://github.com/hougaard/Youtube-Video-Sources (lokal klonen; Ordnername = Videothema)_

Der Cluster ist Hougaards Werkzeugkasten für Erweiterbarkeit in AL: die Event-Seite (isolierte Events, SingleInstance-Zustand zwischen Events, Event-Recorder-Workflow, Global Triggers) und das Enum+Interface+Wire-up-Dreigespann für Plugin-Architekturen, bis hin zur vollständigen Rezeptur, ein Standard-Enum wie "Sales Line Type" so zu erweitern, dass der neue Wert auch wirklich benutzbar ist. Dazu die Sprachebene: Prozedur-Sichtbarkeiten, Namespaces, Preprocessor für doppelte ID-Ranges, this, xRec, Overloading — und mehrere ehrliche Fallen, die man erst glaubt, wenn man sie sieht (Optionsliterale werden praktisch nicht geprüft, Zuweisungssyntax ruft Prozeduren auf, lokale Variablen verdecken Built-ins). Für ein Bau-ERP am wertvollsten: die Upgrade-Codeunit mit Upgrade-Tag als Wiederhol-Sperre (exakt die Migrations-Verdopplungs-Fehlerklasse, die das Referenzprojekt real getroffen hat), Codeunit.Run als try/catch für Stapelbuchungen mit Fehlerspalte, das Ein-Zeilen-Event für Sachposten-Granularität je Belegzeile und parametrisierte Dialogseiten statt RunObject.

**Wertvollste Ordner:** UpgradeCodeunit · CodeunitRun · OptionOverEnums · Interface · One Mighty Little Event

## Themen (nach Praxis-Relevanz)

- ●●●  **One Mighty Little Event** — Eine einzige Subscriber-Zeile ändert die Buchungsgranularität: das Feld "Additional Grouping Identifier" im Invoice Post. Buffer existiert genau dafür, dass Extensions die Zusammenfassung gleichartiger Verkaufszeilen im Hauptbuch aufbrechen — eindeutiger Schlüssel je Zeile ergibt einen Sachposten pro Belegzeile.
- ●●●  **CodeunitRun** — if not Codeunit.Run() then ... ist das try/catch für Stapelläufe: ein Error im OnRun rollt nur die Transaktion DIESES Aufrufs zurück, GetLastErrorText liefert die Meldung, die Schleife läuft weiter — das Grundmuster jeder fehlertoleranten Massenverarbeitung (Job-Queue-Stil) mit Fehlertext am Datensatz.
- ●●●  **RunObjectWithParameters** — Parametrisierte Seiten: die RunObject-Property einer Action kann keine Parameter übergeben — eine Page-VARIABLE kann es. Vor RunModal Setter-Prozeduren auf der Instanz aufrufen; der Zustand steht in OnInit/OnOpenPage und den Controls bereit. Für reine Filter genügt RunPageLink bzw. ein gefiltertes Record an Page.Run.
- ●●●  **eventrecorder** — Der Auffind-Workflow für Hooks: mit der Event-Recorder-Seite im Client aufzeichnen, welche Events während einer Benutzeraktion feuern, dann den passendsten OnBefore-Hook abonnieren — hier gefunden: OnBeforeReleaseSalesDoc, um Belegfreigabe nach fachlicher Regel zu blocken.
- ●●●  **Interface** — Das komplette Plugin-Dreigespann, mit dem eine Fremd-App per Enum + Interface erweiterbar wird: (1) Enumwert der Fremd-App anhängen, (2) deren Interface implementieren, (3) die Implementierung über ein Auswahl-Event mit var-Interface-Parameter und Handled-Flag einhängen. Braucht man genau dann, wenn das Enum der Fremd-App gehört und man dessen implements-Liste nicht erweitern kann.
- ●●●  **OptionOverEnums** — Das vollständige Rezept, ein Standard-Enum wie "Sales Line Type" um eine WIRKLICH benutzbare eigene Zeilenart zu erweitern: Enumwert allein genügt nicht — es braucht die Freischaltung im Options-Dropdown (Option Lookup Buffer), das Übersteuern der Standard-No.-Validierung und eine bedingte TableRelation samt Folgefeld-Logik.
- ●●●  **UpgradeCodeunit** — Datenmigration beim App-Upgrade: Codeunit mit Subtype=Upgrade und OnUpgradePerCompany, Upgrade-Tag als Wiederhol-Sperre, alte Tabelle per ObsoleteState stilllegen statt löschen — hier inklusive Typwechsel Date auf DateTime über eine Nachfolgetabelle.
- ●●○  **xRec** — xRec, Rec und CurrFieldNo im OnValidate: xRec trägt den Zustand, wie die Page den Datensatz eingelesen hat — damit lassen sich Alt-gegen-Neu-Vergleiche und Änderungsprotokolle bauen; CurrFieldNo verrät, WELCHES Feld die Validierung ausgelöst hat.
- ●●○  **This** — Das this-Schlüsselwort (ab Runtime 14/BC 25) gibt Codeunits, Pages, Reports und XmlPorts eine explizite Selbstreferenz: ein Objekt kann SICH SELBST als Parameter an einen Helper übergeben (Callback-/Visitor-Muster), und Parametertypen dürfen konkrete Page-/Report-/XmlPort-Typen sein.
- ●●○  **ProcedureScope** — Die drei Prozedur-Sichtbarkeiten: local (nur dieses Objekt), internal (nur diese App), ohne Modifier public (jede App mit Dependency). internal ist der richtige Default für App-interne API — es verhindert, dass sich Fremd-Extensions auf Interna koppeln.
- ●●○  **overloading** — Prozedur-Überladung als Ersatz für optionale Parameter (die AL nicht kennt): schmale Overloads delegieren an den vollständigsten, statt Logik zu kopieren. Nebenmuster: Insert(true) VOR den Validates, damit die Nummernserie zieht, danach Modify(true).
- ●●○  **namespace** — Namespaces in AL (ab Runtime 12/BC 23): namespace-Deklaration je Datei, using für fremde Namespaces — Objektnamen müssen nur noch je Namespace eindeutig sein. Man KANN damit eine eigene Tabelle "Customer" neben Microsofts Customer stellen und per using/Qualifizierung unterscheiden.
- ●●○  **Preprocesor** — Ein Quellstand, zwei Objekt-ID-Welten: preprocessorSymbols in app.json plus #if um die OBJEKT-ID schalten zwischen On-Prem-Range (50xxx) und AppSource-Range (70xxxxxx) — beide Ranges stehen in idRanges. Dazu #region-Gliederung und zeilengenaues #pragma warning disable/restore.
- ●●○  **Select Enum** — Generischer Enum-Wert-Picker zur Laufzeit für jedes Enum-Feld jeder Tabelle: FieldRef liefert die Enum-Metadaten (EnumValueCount, GetEnumValueOrdinal, GetEnumValueNameFromOrdinalValue), die virtuelle Integer-Tabelle liefert die Listenzeilen. Aufruf: SetupPage(TableNo, FieldNo), LookupMode(true), RunModal, GetSelectedEnum.
- ●●○  **Enumify** — Migration Option-Feld zu Enum-Feld am selben Feld: der Typwechsel ist datenkompatibel, weil in der DB nur der Ordinalwert steht — solange die Enum-Ordinale exakt den alten OptionMembers-Positionen entsprechen, ist es ein reiner Metadatenwechsel ohne Datenmigration.
- ●●○  **globaltriggers** — GlobalTriggerManagement liefert tabellenübergreifende Datenbank-Trigger: EIN Subscriber bekommt jeden Insert (Modify/Delete/Rename analog) als RecordRef — die Grundlage von Änderungsprotokoll und Audit-Mechanismen, ohne je Tabelle einen Trigger zu schreiben.
- ●●○  **singleinstanceevents** — Zustand ZWISCHEN zwei getrennten Events transportieren: ein SingleInstance-Subscriber-Codeunit hält seine globalen Variablen die ganze Session — Event 1 legt ab, Event 2 liest. Nebenbefund mit Aha-Wert: Subscriber-Parameter werden per NAME gebunden, nicht per Position — das Demo vertauscht die Reihenfolge komplett und funktioniert.
- ●●○  **isolatedevents** — Initialisierungslogik sicher an das Öffnen der Company hängen: OnCompanyOpenCompleted ist ein isoliertes Event — jeder Subscriber läuft gekapselt, ein Error verhindert weder das Öffnen der Company noch die anderen Subscriber. Das Demo wirft absichtlich zufällig Fehler, der Client öffnet trotzdem.
- ●●○  **RuntimeDependencies** — Eine optionale Fremd-App OHNE Compile-Dependency ansprechen: RecordRef.Open(TabellenID) + FieldRef befüllen deren Parametertabelle, Codeunit.Run(CodeunitID, Variant-mit-RecordRef) startet deren Logik — die eigene App bleibt installierbar, auch wenn die Fremd-App fehlt. Gegenstück im Ordner DependencyAppSource: harte dependency in app.json (id/name/publisher/version) und direkte Symbolnutzung.
- ●○○  **Scope** — ⚠⚠ **BERICHTIGT 01.09.2026 (B) — DOKU-vs-DEMO-KONFLIKT, kein einfacher Fehler.** Hier stand: „Namensauflösung lokal > global > built-in: Variablen dürfen wie eingebaute Funktionen heißen (CompanyName, Today) und verdecken sie kommentarlos.“ **Microsoft sagt das GEGENTEIL:** *AL variables — Variable names*: „A variable can't have the same name as an AL method or a reserved word. This applies to both uppercase and lowercase spellings.“ **Die Demo (`Scope/HelloWorld.al` Z. 9–31) zeigt es dennoch kompilierend.** ⚠ **Die Handlungsanweisung ist in BEIDEN Fällen dieselbe: Variablen NIE wie eingebaute Funktionen benennen.** Gilt die Doku, bricht es spätestens beim nächsten Compiler; gilt die Demo, bedeutet dieselbe Schreibweise je nach Prozedur etwas anderes. **Und die Reihenfolge lokal > global > built-in ist NIRGENDS dokumentiert — sie darf nicht als Plattform-Zusicherung zitiert werden.**
- ●○○  **ObjectOrientedAL** — Codeunits als "Objekte": überladene New()-Factory-Prozeduren geben Codeunit-Instanzen zurück (Codeunit-Variablen sind Referenzen), Zustand liegt in einer privaten Var, Zugriff über Getter — OO-Stil ohne echte Klassen.
- ●○○  **WeirdOptions** — Warum Inline-Option-Parameter in Prozedursignaturen verboten gehören: ihr Typ ist anonym, und Optionsliterale beim Aufruf werden praktisch nicht geprüft — das Demo ruft mit komplett erfundenen Bezeichnern auf BEIDEN Seiten von :: auf und kompiliert laut Demo trotzdem. Lehre: Enums statt Options in Signaturen.
- ○○○  **SetterGetter** — AL-Kuriosum: eine Ein-Parameter-Prozedur lässt sich mit ZUWEISUNGS-Syntax aufrufen, eine parameterlose ohne Klammern — damit sind property-artige Setter/Getter möglich, die wie Variablenzugriffe aussehen.

---

## One Mighty Little Event

**Technik:** Eine einzige Subscriber-Zeile ändert die Buchungsgranularität: das Feld "Additional Grouping Identifier" im Invoice Post. Buffer existiert genau dafür, dass Extensions die Zusammenfassung gleichartiger Verkaufszeilen im Hauptbuch aufbrechen — eindeutiger Schlüssel je Zeile ergibt einen Sachposten pro Belegzeile.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** app.json: application/platform 17.0, runtime 6.0 — Muster vor BC 20 entstanden, Event-Name für BC 28 verifizieren

```al
codeunit 50129 "Make sure all is posted"
{
    // Verhindert das Zusammenfassen gleichartiger Zeilen zu EINER G/L-Zeile:
    // eindeutiger Gruppierungsschluessel je Zeile => 1 Sachposten pro Belegzeile
    [EventSubscriber(ObjectType::Table, Database::"Invoice Post. Buffer",
        'OnAfterInvPostBufferPrepareSales', '', true, true)]
    local procedure ForcePerLinePosting(var SalesLine: Record "Sales Line";
        var InvoicePostBuffer: Record "Invoice Post. Buffer")
    begin
        InvoicePostBuffer."Additional Grouping Identifier" :=
            Format(SalesLine."Line No.", 0, 2);
    end;
}
```

**Fallstricke:** Das Demo stammt aus der Invoice-Post.-Buffer-Ära; in neueren BC-Versionen ist der Buffer durch die interfacebasierte Invoice-Posting-Architektur ("Invoice Posting Buffer") ersetzt — das Äquivalent-Event im Zielrelease nachschlagen, nicht raten. Format(...,0,2) erzeugt einen sortierstabilen Schlüssel aus der Zeilennummer.

---

## CodeunitRun

**Technik:** if not Codeunit.Run() then ... ist das try/catch für Stapelläufe: ein Error im OnRun rollt nur die Transaktion DIESES Aufrufs zurück, GetLastErrorText liefert die Meldung, die Schleife läuft weiter — das Grundmuster jeder fehlertoleranten Massenverarbeitung (Job-Queue-Stil) mit Fehlertext am Datensatz.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
codeunit 50800 "Problematic Codeunit"
{
    trigger OnRun()
    begin
        Error('BIG PROBLEMS!!!');
    end;
}

// Fehlertolerante Stapelverarbeitung (z.B. Action auf einer Liste):
// var cu: Codeunit "Problematic Codeunit";
// begin
//     if Rec.FindSet() then
//         repeat
//             Rec.Modify();
//             Commit(); // PFLICHT: Codeunit.Run als Funktion braucht abgeschlossene Transaktion
//             if not cu.Run() then begin
//                 Rec."Name 2" := CopyStr(GetLastErrorText(), 1, MaxStrLen(Rec."Name 2"));
//                 Rec.Modify(); // Fehler am Datensatz persistieren statt Lauf abbrechen
//             end;
//         until Rec.Next() = 0;
// end;
```

**Fallstricke:** Ohne Commit vor dem Aufruf gibt es den Laufzeitfehler "Codeunit.Run in write transaction not allowed". Das nötige Commit macht die Schleife aber inkrementell-permanent: ein Abbruch mittendrin hinterlässt Teilstände — das Muster nur einsetzen, wo je-Datensatz-Fortschritt fachlich okay ist. Fehlertext immer mit CopyStr/MaxStrLen kappen.

---

## RunObjectWithParameters

**Technik:** Parametrisierte Seiten: die RunObject-Property einer Action kann keine Parameter übergeben — eine Page-VARIABLE kann es. Vor RunModal Setter-Prozeduren auf der Instanz aufrufen; der Zustand steht in OnInit/OnOpenPage und den Controls bereit. Für reine Filter genügt RunPageLink bzw. ein gefiltertes Record an Page.Run.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
page 50100 "Customer Card Info"
{
    PageType = Card;
    SourceTable = Customer;
    layout { area(content) { group(General) {
        field(Name; Rec.Name) { ApplicationArea = all; Editable = RememberParm2 > 200; }
    } } }
    var
        RememberParm1: Text;
        RememberParm2: Decimal;

    internal procedure SetupPage(Parm1: Text; Parm2: Decimal)
    begin
        RememberParm1 := Parm1;
        RememberParm2 := Parm2;
    end;
}

// Aufrufer (Action einer beliebigen Seite):
// trigger OnAction()
// var
//     ThePage: Page "Customer Card Info";
// begin
//     ThePage.SetupPage('Youtube', 123.345); // VOR RunModal
//     ThePage.RunModal();                    // Zustand ueberlebt bis in die Trigger
// end;
//
// Nur-Filter-Alternative: Customer.SetFilter(Address, '*Road*'); Page.Run(22, Customer);
```

**Fallstricke:** Das Demo loggt OnInit und OnOpenPage mit den Parametern — so macht man die Trigger-Reihenfolge und Zustands-Verfügbarkeit sichtbar, statt sie zu raten. Vorsicht bei Control-Properties an Zustandsvariablen (Editable = Var): solche Bindungen werden nicht bei jedem Roundtrip neu ausgewertet — was zur Laufzeit umschalten soll, gehört in Daten, nicht in Control-Metadaten.

---

## eventrecorder

**Technik:** Der Auffind-Workflow für Hooks: mit der Event-Recorder-Seite im Client aufzeichnen, welche Events während einer Benutzeraktion feuern, dann den passendsten OnBefore-Hook abonnieren — hier gefunden: OnBeforeReleaseSalesDoc, um Belegfreigabe nach fachlicher Regel zu blocken.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
codeunit 50112 "Release Guard"
{
    // Hook per Event-Recorder-Seite gefunden (zeichnet alle Events einer Aktion auf)
    [EventSubscriber(ObjectType::Codeunit, Codeunit::"Release Sales Document",
        'OnBeforeReleaseSalesDoc', '', true, true)]
    local procedure OnBeforeReleaseSalesDoc(var SalesHeader: Record "Sales Header"; PreviewMode: Boolean)
    begin
        if PreviewMode then
            exit; // Buchungsvorschau nicht blockieren
        if Date2DWY(SalesHeader."Posting Date", 1) = 7 then
            Error('Keine Buchungsdaten an einem Sonntag!');
    end;
}
```

**Fallstricke:** Den PreviewMode-Guard nicht vergessen, sonst bricht die Buchungsvorschau an der fachlichen Regel ab. Error in einem OnBefore-Event stoppt den gesamten Vorgang — hier gewollt, bei Seiteneffekt-Subscribern fatal. Date2DWY(...,1) liefert 1..7 mit 7 = Sonntag.

---

## Interface

**Technik:** Das komplette Plugin-Dreigespann, mit dem eine Fremd-App per Enum + Interface erweiterbar wird: (1) Enumwert der Fremd-App anhängen, (2) deren Interface implementieren, (3) die Implementierung über ein Auswahl-Event mit var-Interface-Parameter und Handled-Flag einhängen. Braucht man genau dann, wenn das Enum der Fremd-App gehört und man dessen implements-Liste nicht erweitern kann.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** Demo auf runtime 7.0 (BC 18); Interfaces ab runtime 5.0 (BC 16)

```al
// 1) Enum der Fremd-App um eigenen Wert erweitern
enumextension 50100 "My Destination" extends "Data Destination EFQ" { value(99; MongoDB) { Caption = 'MongoDB'; } }

// 2) Interface der Fremd-App implementieren
codeunit 50100 MongoDB implements DataProviderEFQ
{
    procedure Connect(): Boolean
    begin
        Error('MongoDB is not yet implemented!');
    end;
    procedure Insert(Ref: RecordRef; AddDateToPrimaryKey: Boolean; AddDate: Date): Boolean begin end;
    // ... ALLE Interface-Prozeduren muessen vorhanden sein
}

// 3) Implementierung ueber das Auswahl-Event der Fremd-App zuweisen
codeunit 50101 "Wire up"
{
    [EventSubscriber(ObjectType::Codeunit, Codeunit::"Cloud Replicator Engine EFQ",
        'OnSelectingCustomDestination', '', true, true)]
    local procedure Select(TableMap: Record "Replicator Table Mapping EFQ";
        var Destination: Interface DataProviderEFQ; var Handled: Boolean)
    var
        MongoDB: Codeunit MongoDB;
    begin
        if TableMap.Destination = TableMap.Destination::MongoDB then begin
            Destination := MongoDB; // Codeunit-Instanz an Interface-Var zuweisen
            Handled := true;
        end;
    end;
}
```

**Fallstricke:** Besitzt man das Enum selbst, ist enum-mit-implements plus DefaultImplementation der modernere Weg ohne Wire-up-Event — das Event-Muster ist die Bauform für FREMDE Enums. Für die eigene App heißt die Lehre umgekehrt: wer erweiterbar sein will, muss genau so ein OnSelecting-Event mit var-Interface + Handled publizieren.

---

## OptionOverEnums

**Technik:** Das vollständige Rezept, ein Standard-Enum wie "Sales Line Type" um eine WIRKLICH benutzbare eigene Zeilenart zu erweitern: Enumwert allein genügt nicht — es braucht die Freischaltung im Options-Dropdown (Option Lookup Buffer), das Übersteuern der Standard-No.-Validierung und eine bedingte TableRelation samt Folgefeld-Logik.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
enumextension 50135 "SL Type" extends "Sales Line Type" { value(50135; Job) { Caption = 'Job'; } }
codeunit 50135 Subscribers
{
    // 1) Wert im Type-Dropdown freischalten (LookupType 0 = Sales, RecRef 37 = Sales Line)
    [EventSubscriber(ObjectType::Table, Database::"Option Lookup Buffer", 'OnBeforeIncludeOption', '', true, true)]
    local procedure IncludeOption(LookupType: Option; Option: Integer; OptionLookupBuffer: Record "Option Lookup Buffer"; RecRef: RecordRef; var Handled: Boolean; var Result: Boolean)
    begin
        if (LookupType = 0) and (Option = 50135) and (RecRef.Number = 37) then begin
            Handled := true; Result := true;
        end;
    end;
    // 2) Standard-No.-Validierung fuer den neuen Typ uebersteuern
    [EventSubscriber(ObjectType::Table, Database::"Sales Line", 'OnBeforeValidateNo', '', true, true)]
    local procedure ValidateNo(CurrentFieldNo: Integer; var IsHandled: Boolean; var SalesLine: Record "Sales Line"; xSalesLine: Record "Sales Line")
    begin
        if SalesLine.Type = SalesLine.Type::Job then IsHandled := true;
    end;
}
// 3) Bedingte TableRelation + Folgefelder
tableextension 50135 MySales extends "Sales Line"
{
    fields
    {
        modify("No.")
        {
            TableRelation = if (Type = const(Job)) Job."No.";
            trigger OnAfterValidate()
            var Job: Record Job;
            begin
                if (Type = Type::Job) and Job.Get("No.") then Rec.Validate(Description, Job.Description);
            end;
        }
    }
}
```

**Fallstricke:** Ohne den Option-Lookup-Buffer-Subscriber existiert der Enumwert, taucht aber im Zeilen-Dropdown nie auf — die Freischaltung ist hartkodierte Magie (LookupType 0 = Sales, Tabelle 37). Und das Rezept endet vor der Buchung: eine Zeile dieses Typs BUCHEN braucht weitere Subscriber in der Posting-Kette. Enumwert-ID liegt hier bewusst in der eigenen Object-Range (50135).

---

## UpgradeCodeunit

**Technik:** Datenmigration beim App-Upgrade: Codeunit mit Subtype=Upgrade und OnUpgradePerCompany, Upgrade-Tag als Wiederhol-Sperre, alte Tabelle per ObsoleteState stilllegen statt löschen — hier inklusive Typwechsel Date auf DateTime über eine Nachfolgetabelle.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
table 50100 MyData // alte Tabelle bleibt im Code, aber stillgelegt
{
    ObsoleteState = Removed;
    ObsoleteReason = 'Replaced by MyData2';
    // Felder unveraendert stehen lassen
}

codeunit 50104 "Upgrade 1"
{
    Subtype = Upgrade;

    trigger OnUpgradePerCompany()
    var
        Old: Record MyData;
        New: Record MyData2;
        Tag: Codeunit "Upgrade Tag";
        MyTag: Label 'MYDATA_UPGRADE1';
    begin
        if Tag.HasUpgradeTag(MyTag) then
            exit; // Idempotenz-Wache: NIE doppelt migrieren
        if Old.FindSet() then
            repeat
                New.Init();
                New.Customer := Old.Customer;
                New.When := CreateDateTime(Old.When, 0T); // Typwechsel Date -> DateTime
                New.What := Old.What;
                New.Insert();
            until Old.Next() = 0;
        Tag.SetUpgradeTag(MyTag);
    end;
}
```

**Fallstricke:** Ohne die HasUpgradeTag-Wache läuft die Migration bei jedem weiteren Upgrade erneut und VERDOPPELT Daten — exakt diese Fehlerklasse ist in einem realen Projekt aufgetreten (Migrationsvorbereitung, 26.08.2026). Upgrade-Code läuft nur beim Versionssprung mit -upgrade, nicht beim Re-Publish derselben Version; OnUpgradePerCompany läuft je Mandant. Die als Removed markierte Alttabelle ist aus Upgrade-Code noch lesbar — genau dafür bleibt sie im Quelltext.

---

## xRec

**Technik:** xRec, Rec und CurrFieldNo im OnValidate: xRec trägt den Zustand, wie die Page den Datensatz eingelesen hat — damit lassen sich Alt-gegen-Neu-Vergleiche und Änderungsprotokolle bauen; CurrFieldNo verrät, WELCHES Feld die Validierung ausgelöst hat.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
table 50121 "Test Table"
{
    fields
    {
        field(1; "code"; Code[20]) { }
        field(2; "Text 1"; Text[200])
        {
            trigger OnValidate()
            begin
                // xRec = Zustand beim Einlesen durch die Page, Rec = neuer Zustand
                if GuiAllowed then
                    Message('alt=%1 neu=%2 (Feld %3)',
                        xRec."Text 1", Rec."Text 1", CurrFieldNo);
            end;
        }
    }
    keys { key(PK; "code") { Clustered = true; } }
}
```

**Fallstricke:** xRec ist nur im UI-Kontext verlässlich: bei programmgesteuertem Validate ist xRec = Rec und CurrFieldNo = 0 — Geschäftslogik darf sich nie ALLEIN auf xRec stützen (sonst verhält sich Code aus Job Queue/API anders als im Client). GuiAllowed-Guard, damit Hintergrundläufe nicht an Dialogen sterben.

---

## This

**Technik:** Das this-Schlüsselwort (ab Runtime 14/BC 25) gibt Codeunits, Pages, Reports und XmlPorts eine explizite Selbstreferenz: ein Objekt kann SICH SELBST als Parameter an einen Helper übergeben (Callback-/Visitor-Muster), und Parametertypen dürfen konkrete Page-/Report-/XmlPort-Typen sein.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 14.0 / application 25.0 (BC 25) — auf BC 28 verfügbar

```al
// runtime >= 14.0 (BC 25)
page 50100 MyPage
{
    trigger OnOpenPage()
    var
        Verify: Codeunit Helper;
    begin
        Verify.VerifyPage(this); // Seite reicht sich selbst weiter
        this.Update();           // explizite Selbstreferenz statt implizitem Aufruf
    end;
}

codeunit 50101 Helper
{
    procedure VerifyPage(p: Page MyPage) // konkreter Seitentyp als Parametertyp
    begin
    end;

    procedure Verify(c: Codeunit SomeCodeunit)
    begin
    end;
}
```

**Fallstricke:** Auf Seiten existieren this UND CurrPage nebeneinander — this ist die Objektinstanz, CurrPage das UI-Handle (in XmlPorts heißt es currXMLport); das Demo ruft absichtlich beides. Der Empfänger muss den konkreten Objekttyp im Parameter deklarieren — ein generisches "irgendeine Page" gibt es nicht.

---

## ProcedureScope

**Technik:** Die drei Prozedur-Sichtbarkeiten: local (nur dieses Objekt), internal (nur diese App), ohne Modifier public (jede App mit Dependency). internal ist der richtige Default für App-interne API — es verhindert, dass sich Fremd-Extensions auf Interna koppeln.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
codeunit 50100 Procedures
{
    var
        Tmp: Record Customer temporary; // Objekt-Zustand, allen Prozeduren gemeinsam

    internal procedure Process() // internal: aus der ganzen EIGENEN App aufrufbar
    var
        C: Record Customer;
    begin
        Tmp.DeleteAll();
        if C.FindSet() then
            repeat
                SubProcess();
            until C.Next() = 0;
    end;

    local procedure SubProcess() // local: nur innerhalb dieser Codeunit
    begin
        Tmp.Insert();
    end;

    procedure Test() // ohne Modifier: PUBLIC — API fuer Fremd-Apps
    begin
    end;
}
```

**Fallstricke:** Public ist der stillschweigende Default — wer nichts hinschreibt, publiziert API; nachträglich internal zu machen ist ein Breaking Change für alle Abhängigen. Die geteilte temporary-Var als Zwischenspeicher funktioniert, ist aber verdeckter Zustand: DeleteAll am Prozedurstart nicht vergessen.

---

## overloading

**Technik:** Prozedur-Überladung als Ersatz für optionale Parameter (die AL nicht kennt): schmale Overloads delegieren an den vollständigsten, statt Logik zu kopieren. Nebenmuster: Insert(true) VOR den Validates, damit die Nummernserie zieht, danach Modify(true).

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
codeunit 50214 Overloading
{
    procedure CreateCustomer(var Customer: Record Customer)
    begin
        Customer.Init();
        Customer.Insert(true);
    end;

    procedure CreateCustomer(NewName: Text; var Customer: Record Customer)
    begin
        CreateCustomer(NewName, '', '', Customer); // Default-Kette statt Copy-Paste
    end;

    procedure CreateCustomer(NewName: Text; PostingGrp: Code[20]; PhoneNo: Text; var Customer: Record Customer)
    begin
        Customer.Init();
        Customer.Insert(true); // erst Insert: Nummernserie vergibt "No."
        Customer.Validate(Name, NewName);
        Customer.Validate("Phone No.", PhoneNo);
        if PostingGrp <> '' then
            Customer.Validate("Customer Posting Group", PostingGrp);
        Customer.Modify(true);
    end;
}
```

**Fallstricke:** Im Original heißt der Parameter "Name" wie das Tabellenfeld — Customer.Validate(Name, Name) kompiliert, und dasselbe Token bedeutet zweimal etwas anderes; Parameter nie wie Felder benennen. Overloads unterscheiden sich nur über die Parameterliste, nicht über den Rückgabetyp.

---

## namespace

**Technik:** Namespaces in AL (ab Runtime 12/BC 23): namespace-Deklaration je Datei, using für fremde Namespaces — Objektnamen müssen nur noch je Namespace eindeutig sein. Man KANN damit eine eigene Tabelle "Customer" neben Microsofts Customer stellen und per using/Qualifizierung unterscheiden.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 12.0 / application 23.0 (BC 23) — auf BC 28 Standardpraxis

```al
namespace Hougaard.Apps.ToolBox;

using Microsoft.Sales.Customer;
using Microsoft.Sales.Posting;

// Eigene Objekte duerfen Standardnamen tragen — der Namespace unterscheidet:
// table 50100 Customer { ... }  // koexistiert mit Microsoft...Customer

tableextension 50100 CustomerTableExt extends Customer
{
    fields
    {
        field(50100; Name; Text[500]) // Demo: gleicher FELDNAME wie im Standard!
        {
            Caption = 'Long Name';
        }
    }
}
```

**Fallstricke:** Können heißt nicht sollen: das Demo legt sogar ein zweites Feld "Name" neben das Standard-"Name" — jeder unqualifizierte Zugriff wird damit zur Leserätsel-Quelle, Kollisionen erzeugen Mehrdeutigkeit statt klarer Compilerfehler. Praxisregel: Namespaces konsequent nutzen, Standard-Objekt- und Feldnamen trotzdem meiden.

---

## Preprocesor

**Technik:** Ein Quellstand, zwei Objekt-ID-Welten: preprocessorSymbols in app.json plus #if um die OBJEKT-ID schalten zwischen On-Prem-Range (50xxx) und AppSource-Range (70xxxxxx) — beide Ranges stehen in idRanges. Dazu #region-Gliederung und zeilengenaues #pragma warning disable/restore.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** Demo auf runtime 7.0 (BC 18); Preprocessor-Direktiven brauchen runtime >= 6.0

```al
// app.json: "preprocessorSymbols": ["appsource"],
//           "idRanges": [ 50100..50149, 70050100..70050149 ]
#if appsource
table 70050100 Preprocessor
#else
table 50100 Preprocessor
#endif
{
    fields
    {
        #region Fields
        field(1; Pre; Code[20]) { Caption = 'Pre'; }
#pragma warning disable AL0468 // Bezeichner > 30 Zeichen, bewusst
        field(3; Preprocessoriscoolandfuntoplaywith; Integer) { }
#pragma warning restore
        #endregion
    }
    keys { key(PK; Pre) { Clustered = true; } }
}

// Nicht definierte Symbole sind schlicht false — kein Fehler:
#if something
//   ...
#else
//   Message('Something else!');
#endif
```

**Fallstricke:** Das Symbol steht im app.json des jeweiligen BUILDS — man braucht zwei Build-Pipelines, nicht zwei Branches. Tippfehler im Symbolnamen sind still: #if TippFehler ist einfach false, keine Warnung. Aus dem pragma-Schwesterordner: AA0139 (möglicher Text-Overflow) lässt sich mit disable/restore exakt um die eine beabsichtigte Zeile legen statt projektweit.

---

## Select Enum

**Technik:** Generischer Enum-Wert-Picker zur Laufzeit für jedes Enum-Feld jeder Tabelle: FieldRef liefert die Enum-Metadaten (EnumValueCount, GetEnumValueOrdinal, GetEnumValueNameFromOrdinalValue), die virtuelle Integer-Tabelle liefert die Listenzeilen. Aufruf: SetupPage(TableNo, FieldNo), LookupMode(true), RunModal, GetSelectedEnum.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
page 50131 "Select an Enum"
{
    PageType = List;
    SourceTable = Integer; // virtuelle Tabelle als Zeilenlieferant
    layout
    {
        area(Content)
        {
            repeater(rep)
            {
                field(value; EnumValue(Rec.Number)) { Caption = 'Value'; ApplicationArea = all; }
            }
        }
    }
    var
        Ref: RecordRef;
        F: FieldRef;

    procedure SetupPage(TableNo: Integer; FieldNo: Integer)
    begin
        Ref.Open(TableNo);
        F := Ref.Field(FieldNo);
        SetRange(Number, 1, F.EnumValueCount()); // Index ist 1-basiert
        CurrPage.Caption('Select ' + F.Caption());
    end;

    local procedure EnumValue(Number: Integer): Text
    begin
        exit(F.GetEnumValueNameFromOrdinalValue(F.GetEnumValueOrdinal(Number)));
    end;

    procedure GetSelectedEnum(): Integer
    begin
        exit(F.GetEnumValueOrdinal(Rec.Number)); // Index -> Ordinal
    end;
}
```

**Fallstricke:** Index und Ordinal sind zwei Welten: Ordinale dürfen Lücken haben (Enumextensions!), deshalb immer über GetEnumValueOrdinal mappen statt Rec.Number direkt zu verwenden. Die Funktion liefert den NAMEN, nicht die übersetzte Caption. Bei Wiederverwendung der Page-Variable vor jedem RunModal Clear(p) — der Demo-Aufrufer macht es vor.

---

## Enumify

**Technik:** Migration Option-Feld zu Enum-Feld am selben Feld: der Typwechsel ist datenkompatibel, weil in der DB nur der Ordinalwert steht — solange die Enum-Ordinale exakt den alten OptionMembers-Positionen entsprechen, ist es ein reiner Metadatenwechsel ohne Datenmigration.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
enum 54800 RainbowColors
{
    // Ordinale muessen den alten Option-Positionen 1:1 entsprechen
    // (alt: OptionMembers = Red,Orange,Yellow,Green,Blue,Indigo)
    value(0; Red) { }
    value(1; Orange) { }
    value(2; Yellow) { }
    value(3; Green) { }
    value(4; Blue) { }
    value(5; Indigo) { }
    value(6; Violet) { } // neue Werte gefahrlos hinten anfuegen
}

table 54800 "Rainbow Component"
{
    fields
    {
        // vorher: field(3; Color; Option) { OptionMembers = Red,...,Indigo; }
        field(3; Color; Enum RainbowColors) { Caption = 'Color'; }
    }
}
```

**Fallstricke:** Wer beim Umstellen Werte umsortiert oder einschiebt, verfälscht Bestandsdaten still — die DB kennt nur Zahlen. Das Enum ist danach ein eigenes Objekt mit ID und (Extensible=true) von Fremd-Apps erweiterbar — bewusst entscheiden.

---

## globaltriggers

**Technik:** GlobalTriggerManagement liefert tabellenübergreifende Datenbank-Trigger: EIN Subscriber bekommt jeden Insert (Modify/Delete/Rename analog) als RecordRef — die Grundlage von Änderungsprotokoll und Audit-Mechanismen, ohne je Tabelle einen Trigger zu schreiben.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: application 23.0, runtime 12.0

```al
codeunit 50120 "Global Triggers"
{
    // Feuert fuer jede Tabelle, deren Trigger-Maske aktiviert ist
    [EventSubscriber(ObjectType::Codeunit, Codeunit::GlobalTriggerManagement,
        'OnAfterOnGlobalInsert', '', true, true)]
    local procedure OnGlobalInsert(RecRef: RecordRef)
    begin
        // Audit: RecRef.Number / RecRef.RecordId protokollieren
    end;

    // Ohne Aktivierung der Maske kommt fuer eigene Tabellen NICHTS an
    // (Setup-Event von GlobalTriggerManagement; exakte Signatur im Ziel-BC nachschlagen):
    [EventSubscriber(ObjectType::Codeunit, Codeunit::GlobalTriggerManagement,
        'OnAfterGetDatabaseTableTriggerSetup', '', true, true)]
    local procedure Setup(TableId: Integer; var OnDatabaseInsert: Boolean;
        var OnDatabaseModify: Boolean; var OnDatabaseDelete: Boolean; var OnDatabaseRename: Boolean)
    begin
        if TableId = Database::Customer then
            OnDatabaseInsert := true;
    end;
}
```

**Fallstricke:** Das Demo zeigt nur den Insert-Subscriber — der funktioniert im Video, weil Standardfeatures (z.B. Änderungsprotokoll) die Trigger-Maske bereits aktiviert haben. Wer sich darauf verlässt, wundert sich in einer sauberen DB über Stille: die Maske muss über das Setup-Event je Tabelle eingeschaltet werden. Performance: der Subscriber läuft danach in JEDEM Insert-Pfad der freigeschalteten Tabellen.

---

## singleinstanceevents

**Technik:** Zustand ZWISCHEN zwei getrennten Events transportieren: ein SingleInstance-Subscriber-Codeunit hält seine globalen Variablen die ganze Session — Event 1 legt ab, Event 2 liest. Nebenbefund mit Aha-Wert: Subscriber-Parameter werden per NAME gebunden, nicht per Position — das Demo vertauscht die Reihenfolge komplett und funktioniert.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
codeunit 50112 Publisher
{
    procedure DoWork()
    begin
        OnInit();
        OnTheFirstEvent('123', 123, CalcDate('-34D', Today()));
        OnTheSecondEvent(Time());
    end;

    [IntegrationEvent(false, false)]
    local procedure OnTheFirstEvent(NumberTxt: Text; Number: Integer; Date: Date) begin end;
    [IntegrationEvent(false, false)]
    local procedure OnTheSecondEvent(Time: Time) begin end;
    [IntegrationEvent(false, false)]
    local procedure OnInit() begin end;
}

codeunit 50144 Subs
{
    SingleInstance = true; // Instanz + Vars leben sessionlang

    // Bindung per PARAMETERNAME — Reihenfolge hier absichtlich anders als beim Publisher:
    [EventSubscriber(ObjectType::Codeunit, Codeunit::Publisher, 'OnTheFirstEvent', '', true, true)]
    local procedure First(Date: Date; Number: Integer; NumberTxt: Text)
    begin
        SavedDate := Date;
    end;

    [EventSubscriber(ObjectType::Codeunit, Codeunit::Publisher, 'OnTheSecondEvent', '', true, true)]
    local procedure Second(Time: Time)
    begin
        Message('%1', CreateDateTime(SavedDate, Time)); // Zustand aus Event 1
    end;

    [EventSubscriber(ObjectType::Codeunit, Codeunit::Publisher, 'OnInit', '', true, true)]
    local procedure Init()
    begin
        SavedDate := 0D; // expliziter Reset — SingleInstance vergisst nie von selbst
    end;

    var
        SavedDate: Date;
}
```

**Fallstricke:** SingleInstance-Zustand lebt bis Session-Ende — ohne eigenes Reset-Event (hier OnInit) arbeitet der zweite Durchlauf mit Datenleichen aus dem ersten. Und weil Parameter per Name gebunden werden, fällt eine vertauschte Reihenfolge beim Kompilieren nicht auf — ein umbenannter Parameter beim Publisher bricht dagegen alle Subscriber.

---

## isolatedevents

**Technik:** Initialisierungslogik sicher an das Öffnen der Company hängen: OnCompanyOpenCompleted ist ein isoliertes Event — jeder Subscriber läuft gekapselt, ein Error verhindert weder das Öffnen der Company noch die anderen Subscriber. Das Demo wirft absichtlich zufällig Fehler, der Client öffnet trotzdem.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: application 20.0, runtime 9.0

```al
codeunit 50100 "Company Open Init"
{
    // OnCompanyOpenCompleted ist ein ISOLATED Event:
    // ein Error im Subscriber verhindert das Oeffnen der Company NICHT
    [EventSubscriber(ObjectType::Codeunit, Codeunit::"Company Triggers",
        'OnCompanyOpenCompleted', '', true, true)]
    local procedure OnCompanyOpenCompleted()
    begin
        if Random(10) < 3 then
            Error('Init fehlgeschlagen'); // wird verschluckt, Client oeffnet trotzdem
    end;
}
```

**Fallstricke:** Die Kehrseite der Isolation: Fehler verschwinden lautlos — was hier scheitert, sieht niemand, und Schreibzugriffe des gescheiterten Subscribers werden zurückgerollt. Für Pflicht-Initialisierung (ohne die die App nicht funktioniert) ist das der falsche Ort.

---

## RuntimeDependencies

**Technik:** Eine optionale Fremd-App OHNE Compile-Dependency ansprechen: RecordRef.Open(TabellenID) + FieldRef befüllen deren Parametertabelle, Codeunit.Run(CodeunitID, Variant-mit-RecordRef) startet deren Logik — die eigene App bleibt installierbar, auch wenn die Fremd-App fehlt. Gegenstück im Ordner DependencyAppSource: harte dependency in app.json (id/name/publisher/version) und direkte Symbolnutzung.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** Demo auf runtime 13.0 (BC 24); Mechanismus versionsunabhängig

```al
// app.json: KEINE dependency — Kopplung nur zur Laufzeit ueber numerische IDs
var
    TempBlob: Codeunit "Temp Blob";
    OutS: OutStream;
    ParmVar: Variant;
    ParmRef: RecordRef;
    ParmField: FieldRef;
begin
    TempBlob.CreateOutStream(OutS);
    Report.SaveAs(Report::"Item List", '', ReportFormat::Pdf, OutS);

    ParmRef.Open(70319494); // Parametertabelle der Fremd-App, per ID
    ParmField := ParmRef.Field(1); // Guid-PK
    ParmField.Value := CreateGuid();
    ParmRef.Insert();
    ParmField := ParmRef.Field(2); // Blob-Feld
    TempBlob.ToFieldRef(ParmField); // Blob direkt in FieldRef schreiben
    ParmField := ParmRef.Field(3); // Dateiname
    ParmField.Value := 'youtube-item-list.pdf';
    ParmRef.Modify();

    ParmVar := ParmRef;
    Codeunit.Run(70319499, ParmVar); // Codeunit der Fremd-App, per ID
end;
```

**Fallstricke:** Nackte Zahlen-IDs heißen: null Compilerprüfung — Feld-IDs und Semantik der Fremd-App sind ein stiller Vertrag, der bei deren Update bricht. Vor dem Aufruf prüfen, ob die App installiert ist, sonst Laufzeitfehler. Reihenfolge beachten: Insert des Parametersatzes vor dem Blob-Schreiben, dann Modify — wie im Demo.

---

## Scope

**Technik:** ⚠⚠ **BERICHTIGT 01.09.2026 (B) — DOKU-vs-DEMO-KONFLIKT, kein einfacher Fehler.** Hier stand: „Namensauflösung lokal > global > built-in: Variablen dürfen wie eingebaute Funktionen heißen (CompanyName, Today) und verdecken sie kommentarlos.“ **Microsoft sagt das GEGENTEIL:** *AL variables — Variable names*: „A variable can't have the same name as an AL method or a reserved word. This applies to both uppercase and lowercase spellings.“ **Die Demo (`Scope/HelloWorld.al` Z. 9–31) zeigt es dennoch kompilierend.** ⚠ **Die Handlungsanweisung ist in BEIDEN Fällen dieselbe: Variablen NIE wie eingebaute Funktionen benennen.** Gilt die Doku, bricht es spätestens beim nächsten Compiler; gilt die Demo, bedeutet dieselbe Schreibweise je nach Prozedur etwas anderes. **Und die Reihenfolge lokal > global > built-in ist NIRGENDS dokumentiert — sie darf nicht als Plattform-Zusicherung zitiert werden.**

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)

```al
pageextension 50100 CustomerListExt extends "Customer List"
{
    var
        CompanyName: Text; // globale Var verdeckt die Built-in-Funktion CompanyName()

    trigger OnOpenPage()
    begin
        Message('%1', CompanyName()); // mit Klammern: noch die Built-in
        Test();
    end;

    procedure Test()
    var
        CompanyName: Text; // lokale Var verdeckt Global UND Built-in
        Today: Date;       // verdeckt Today()
    begin
        Today := 20230101D;
        CompanyName := 'Local Var';
        Message('%1 %2', CompanyName, Today);
    end;
}
```

**Fallstricke:** Kompiliert praktisch ohne Widerstand und ändert still die Semantik — Reviews übersehen es, weil die Zeile korrekt aussieht. Built-in-Namen (Today, Time, CompanyName, WorkDate...) nie als Variablennamen vergeben.

---

## ObjectOrientedAL

**Technik:** Codeunits als "Objekte": überladene New()-Factory-Prozeduren geben Codeunit-Instanzen zurück (Codeunit-Variablen sind Referenzen), Zustand liegt in einer privaten Var, Zugriff über Getter — OO-Stil ohne echte Klassen.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)

```al
codeunit 50100 OOAL
{
    var
        _Data: JsonObject;

    procedure New(): Codeunit OOAL
    var
        Empty: JsonObject;
    begin
        exit(New(Empty)); // Overload-Kette
    end;

    procedure New(Data: JsonObject): Codeunit OOAL
    var
        O: Codeunit OOAL;
    begin
        O.SetData(Data);
        exit(O); // WICHTIG: explizit die initialisierte Instanz zurueckgeben
    end;

    procedure SetData(Data: JsonObject)
    begin
        _Data := Data.Clone().AsObject(); // Clone: Aufrufer haelt keine Referenz hinein
    end;

    procedure Data(): JsonObject
    begin
        exit(_Data);
    end;
}
```

**Fallstricke:** Der Original-Democode enthält die Falle selbst: er setzt _Data auf der AUFGERUFENEN Instanz und lässt das exit weg — zurück kommt die uninitialisierte implizite Rückgabevariable, also eine ANDERE, leere Instanz. Ohne explizites exit(O) ist jede Codeunit-Factory still kaputt. Und es gibt keinen echten Konstruktor: niemand hindert Aufrufer, die Codeunit roh zu deklarieren und Getter auf leerem Zustand zu rufen.

---

## WeirdOptions

**Technik:** Warum Inline-Option-Parameter in Prozedursignaturen verboten gehören: ihr Typ ist anonym, und Optionsliterale beim Aufruf werden praktisch nicht geprüft — das Demo ruft mit komplett erfundenen Bezeichnern auf BEIDEN Seiten von :: auf und kompiliert laut Demo trotzdem. Lehre: Enums statt Options in Signaturen.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** Demo auf application 21.0 / runtime 10.0 — Prüfverhalten des Compilers im Zielrelease gegentesten

```al
pageextension 50126 CustomerListExt extends "Customer List"
{
    trigger OnOpenPage();
    begin
        // Kompiliert laut Demo — saemtliche Bezeichner sind frei erfunden:
        test(randomjfkghlslghj::ghdfkzghndfkjghsdkfjgh, sjrgkdfkjghsdfk::ghdfjhg);
    end;

    procedure test(PostingMethod: Option OpenEntry,ClosedEntry;
                   SalesLineType: Option Item,GL,Resource)
    begin
    end;
}
```

**Fallstricke:** Was beim Callee ankommt, hat mit dem, was der Leser im Aufruf zu sehen glaubt, nichts zu tun; zwei Option-Parameter sind zudem untereinander zuweisungskompatibel — Vertauschen fällt nicht auf. In Signaturen konsequent Enums verwenden, Options nur noch als Legacy an Tabellenfeldern dulden.

---

## SetterGetter

**Technik:** AL-Kuriosum: eine Ein-Parameter-Prozedur lässt sich mit ZUWEISUNGS-Syntax aufrufen, eine parameterlose ohne Klammern — damit sind property-artige Setter/Getter möglich, die wie Variablenzugriffe aussehen.

**Praxis-Relevanz (Bau-ERP):** ○○○ (0/3)

```al
codeunit 50100 PropertyStyle
{
    var
        _test: Text;

    procedure Test(value: Text)
    begin
        _test := value;
    end;

    procedure Test2(): Text
    begin
        exit(_test);
    end;

    procedure Demo()
    begin
        Test := '3123123';    // Zuweisungs-Syntax ruft Test('3123123') auf!
        Message('%1', Test2); // klammerloser Aufruf von Test2()
    end;
}
```

**Fallstricke:** Für Leser nicht von einer Variablenzuweisung zu unterscheiden — in fremdem Code eine echte Fehllesequelle (deshalb kennen lohnt sich), im eigenen Code besser lassen. Das Original deklariert beim Setter zusätzlich einen Rückgabetyp ohne exit — der liefert stumm den Leerwert.

---

## Übersprungen (bewusst)

- EnumExtensions — nackte Enumextension, redundant zu OptionOverEnums
- namespaces — nur Hello-World-Codeunit
- pragma — im Preprocesor-Topic mitdestilliert
- DependencyAppSource — nur app.json-Eintrag, als Kontrast in RuntimeDependencies erwähnt

