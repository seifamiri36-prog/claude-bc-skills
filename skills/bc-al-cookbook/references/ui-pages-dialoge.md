# Pages, Dialoge & UX-Kniffe

_Destilliert aus Erik Hougaards Youtube-Video-Sources (Ordnername = Videothema)._
_Vollquellen: https://github.com/hougaard/Youtube-Video-Sources (lokal klonen; Ordnername = Videothema)_

Der Cluster zeigt, wie viel UX in Business Central ohne eine Zeile JavaScript geht: StyleExpr-Färbung, Seiten-Views mit eigenem Layout, Tree-Repeater, generische Factboxes, StandardDialog/Date-Time-Dialog als fertige Eingabedialoge, ShowMandatory-Ausdrücke und sogar Emoji-Captions als Farbcodierung. Wo der Client-Rahmen endet, greift Hougaard konsequent zum selben Meta-Muster: ein unsichtbares 1x1-Pixel-Control-Addin als JS-Brücke in den Parent-DOM (Drag&Drop, Subpage-zu-Header-Kommunikation, Vollbild, Fortschrittsbalken) — mächtig, aber an undokumentierte Webclient-DOM-Klassen gekettet und damit fragil. Zweites Meta-Muster: Seitenvariablen plus OnAfterGetRecord ersetzen Tabellenfelder (berechnete Spalten, Matrix-Zellen, Stil-Variablen); drittes: RecordRef/SystemId machen Parts generisch für beliebige Host-Seiten. Wichtigste Fallstricke: AL-zu-JS-Aufrufe aus laufenden Triggern werden gepuffert statt live ausgeführt, Visible-Variablen werden nur bei OnOpenPage ausgewertet, und ShowMandatory/MaskType sind rein optisch. Für ein Bau-ERP direkt verwertbar: Tree-Repeater für LV-Hierarchien, Multiselect-Lookup für Zeilenerfassung, generische Factboxes, bedingte TableRelations und StandardDialoge für Schnelleingaben.

**Wertvollste Ordner:** factbox · treecontrol · multiselectrecord · MatrixPage · PagesWithStyle

## Themen (nach Praxis-Relevanz)

- ●●●  **PagesWithStyle** — Zeilen einer Liste abhängig vom Datensatz einfärben: StyleExpr mit einer Text-Variable, die in OnAfterGetRecord UND OnAfterGetCurrRecord gesetzt wird. Das Arbeitspferd für jede Status-Visualisierung.
- ●●●  **ListInColumns** — Master-Detail auf EINER Seite: ein grid-Control legt Repeater und verlinkten Part nebeneinander (statt untereinander); der Part folgt der Zeilenauswahl über SubPageLink = field(...). Demo nutzt die virtuellen Tabellen AllObj/Field als Datenbank-Browser.
- ●●●  **BoundAction** — OData-Bound-Actions auf API-Pages: eine [ServiceEnabled]-Prozedur mit WebServiceActionContext wird per POST auf .../quotes({id})/Microsoft.NAV.convertToOrder aufrufbar — Prozesse (Angebot zu Auftrag) aus externen Apps auslösen, ohne Datenfelder zu simulieren.
- ●●●  **datetimedialog** — BC liefert einen fertigen Datum/Zeit-Auswahldialog als Systemseite 'Date-Time Dialog' mit — Caption(), SetDateTime()/GetDateTime() und UseDateOnly() statt Eigenbau.
- ●●●  **StandardDialog** — PageType=StandardDialog als schneller Eingabedialog ohne SourceTable: OK/Abbrechen kommen automatisch, Werte gehen per Setup-Methode hinein und nach RunModal über Getter wieder heraus — die Seiteninstanz lebt weiter.
- ●●●  **MandatoryFields** — Pflichtfeld-Optik per Ausdruck: ShowMandatory akzeptiert eine Boolesche Bedingung (roter Stern nur wenn relevant), BlankZero lässt die 0 leer aussehen — die tatsächliche Durchsetzung braucht separaten Code (OnModifyRecord/Validate).
- ●●●  **FocusDemo** — Feature-Toggle-Architektur: ein Boolean in der Setup-Tabelle schaltet eine komplette Customization — Sichtbarkeit der Felder über eine in OnOpenPage gesetzte Variable, und JEDE Logik (Events, Berechnungen) prüft denselben Schalter. So bleibt eine Erweiterung für Standardnutzer unsichtbar.
- ●●●  **Lookups** — Die zwei Lookup-Mechanismen nebeneinander: deklarativ die bedingte TableRelation (if Type = const(...)), imperativ der OnLookup-Trigger, der das Standard-Lookup komplett ersetzt und den Wert über den var-Text-Parameter zurückgibt.
- ●●●  **multiselectrecord** — Mehrfachauswahl aus einem Lookup übernehmen: Seite als PAGE-VARIABLE mit LookupMode=true modal ausführen, dann GetSelectionFilter() als Filterstring über alle markierten Datensätze iterieren — z.B. viele Artikel auf einmal als Belegzeilen anlegen.
- ●●●  **FaxtBoxes** — Klassische Beleg-Factbox: ListPart mit SourceTableView-Filter, per addfirst(factboxes) + SubPageLink angehängt; OnDrillDown auf der Belegnummer öffnet den Beleg — plus Scope=Repeater für Zeilen-Aktionen im Part.
- ●●●  **factbox** — EINE generische Factbox, die an beliebige Seiten andockt: Kindtabelle mit Schlüssel (ParentTable, ParentSystemId), Host-Seite übergibt sich per RecordRef an eine SetParent-Methode statt über SubPageLink. So wird dieselbe Beteiligten-/Team-Factbox auf Customer Card UND Posted Invoice wiederverwendet.
- ●●●  **treecontrol** — Eine List-Page als auf-/zuklappbaren Baum rendern — vier Repeater-Properties genügen, die Hierarchie kommt allein aus einem Integer-Feld 'Indentation' benachbarter Zeilen (wie im Kontenplan).
- ●●●  **MatrixPage** — Eine editierbare Matrix ohne Matrix-Control: virtuelle Integer-Tabelle als Zeilentreiber, N feste Spalten-Variablen, CaptionClass '3,'+Text für dynamische Spaltentitel, Links/Rechts-Aktionen verschieben ein LeftMostColumn-Offset, Zell-Eingaben landen in einem verschachtelten Dictionary.
- ●●○  **DragnDrop** — Drag&Drop-Umsortierung in einer BC-Liste: ein unsichtbares Control-Addin macht per JS die Grid-Zeilen des Webclients draggable, liest die Datensatz-ID aus dem title-Attribut der ID-Zelle und meldet Drag/Drop-Paar an AL, das über ein Sorting-Index-Feld umsortiert.
- ●●○  **SpinningWait** — Seite sofort rendern, schwer rechnen danach: usercontrol-Ready startet einen JS-Timer (Wait), dessen Callback-Event die teure Berechnung NACH dem ersten Paint ausführt — wahlweise als wiederholte Häppchen.
- ●●○  **progressbar2** — Grafischer Fortschrittsbalken als Control-Addin: HTML/CSS-Balken, Ready-Handshake per Event aus dem StartupScript, AL schiebt Werte über eine Prozedur nach — das Grundgerüst jedes eigenen Control-Addins.
- ●●○  **InDataSet** — Berechnete Anzeigespalte ohne Tabellenfeld: eine Seitenvariable als Repeater-Feld, je Zeile in OnAfterGetRecord befüllt — die leichte Alternative zu FlowFields für reine Anzeigen.
- ●●○  **ColorCodingGeneralJournal** — Farbcodierung von Zeilen über ein Enum, dessen Captions Emojis sind (🟥🟩🦄): eine schmale Spalte (Width=1) wird zur wählbaren, filterbaren Farbmarkierung — Farben, die StyleExpr nie könnte.
- ●●○  **SessionSettings** — Die laufende Benutzersession per Code umkonfigurieren: SessionSettings.Init() + LanguageId(...) + RequestSessionUpdate(true) wechselt Sprache/Region und startet die Session neu — z.B. für einen Sprachumschalt-Button.
- ●●○  **HidingFieldValues** — MaskType=Concealed zeigt Feldwerte als Punkte an — auch nachträglich per modify() auf Standardfeldern und FlowFields. Sichtschutz für sensible Werte (Löhne, EK-Preise) auf Bildschirmen mit Publikum.
- ●●○  **LineBreaks** — Mehrzeilige String-Literale mit @'...' (verbatim) und Zeichen aus Codepunkten über Index-Zuweisung auf Text[1] — die Basis für CSV-Parsing und Testdaten direkt im AL-Code.
- ●●○  **Dialogs** — Der klassische Fortschritts-Dialog: Label mit \\ als Zeilenumbruch und #n####-Platzhaltern, die per Window.Update(n, Wert) live aktualisiert werden — die einzige Fortschrittsanzeige, die während eines laufenden Server-Triggers wirklich tickt.
- ●●○  **CueGroup** — Eigene Kacheln (Cues) im Rollencenter: cuegroup auf einem CardPart mit Tabellen- UND Seitenvariablen-Feldern, OnDrillDown je Kachel, StyleExpr färbt Kacheln, und ein actions-Block in der cuegroup rendert Aktions-Kacheln; angehängt per addfirst(rolecenter).
- ●●○  **FullPageUserControl** — Ein Control-Addin auf volle Seitenhöhe bringen: VerticalStretch=true plus Startup-JS, das das eigene iframe (window.frameElement) auf die Höhe des umgebenden .control-addin-form-Divs setzt und bei resize nachzieht — Basis für Vollflächen-UIs (Pläne, Karten, Grafiken).
- ●●○  **PrettyCardPages** — Card-Layout-Grundgriffe: zwei Geschwister-Gruppen unter einer Obergruppe rendern als zwei Spalten; Importance=Promoted hält ein Feld auch bei eingeklappter Gruppe sichtbar, Importance=Additional versteckt es hinter 'Mehr anzeigen'; Visible=false macht Felder nur per Personalisierung zuschaltbar.
- ●●○  **Pizzazz** — views-Block auf List-Pages: vordefinierte gefilterte Sichten, die mit SharedLayout=false je View eigenes Layout bekommen (Spalten aus-/einblenden, moveafter) — gespeicherte Ansichten per Code statt per Personalisierung ausliefern.
- ●●○  **PlaceHolderText** — InstructionalText auf Feld-Controls erzeugt graue Platzhaltertexte im leeren Feld (Web-Formular-Optik); kombiniert mit ShowCaption=false entsteht ein modernes, label-loses Formular — auch per modify() auf Standardfeldern.
- ●●○  **SubPartToParent** — Subpage-zu-Header-Kommunikation, die AL offiziell nicht kann: je ein unsichtbares Twin-Control-Addin in Zeilen- und Kopfseite; das Zeilen-JS iteriert window.parent.frames, findet den Schwester-Frame und ruft dort eine Funktion, die das Event auf der Kopfseite auslöst — der Header reagiert live auf die Zeilenauswahl.
- ●○○  **promptdialog** — PageType=PromptDialog — der Copilot-Seitentyp: area(Prompt) für die Eingabezone, area(Content) für das Ergebnis (auch mit ListPart), systemaction(Generate) als Auslöser; SourceTable muss temporär sein.
- ●○○  **MessingWithDialogues** — Das unsichtbare 1x1-Pixel-Control-Addin als JS-Brücke — und der Kernbefund dazu: AL-zu-JS-Aufrufe aus einem laufenden Trigger werden gepuffert und erst nach Trigger-Ende beim Client ausgeführt, während Dialog.Update live aktualisiert.

---

## PagesWithStyle

**Technik:** Zeilen einer Liste abhängig vom Datensatz einfärben: StyleExpr mit einer Text-Variable, die in OnAfterGetRecord UND OnAfterGetCurrRecord gesetzt wird. Das Arbeitspferd für jede Status-Visualisierung.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
pageextension 52600 "customer list" extends "Customer List"
{
    layout
    {
        modify(Name)
        {
            StyleExpr = MyStyle; // Style = X waere statisch fuer alle Zeilen
        }
    }
    trigger OnAfterGetRecord()
    begin
        SetMyStyle();
    end;

    trigger OnAfterGetCurrRecord()
    begin
        SetMyStyle();
    end;

    procedure SetMyStyle()
    begin
        case Rec."Gen. Bus. Posting Group" of
            'DOMESTIC': MyStyle := 'Unfavorable'; // rot
            'EU':       MyStyle := 'Favorable';   // gruen
            'EXPORT':   MyStyle := 'Ambiguous';   // gelb
        end;
    end;

    var
        MyStyle: Text;
}
```

**Fallstricke:** Beide Trigger setzen, sonst hinkt die Färbung der aktiven Zeile hinterher. Nur die festen Stilnamen (Favorable, Unfavorable, Ambiguous, Attention, AttentionAccent, Strong, Subordinate...) sind möglich — keine freien Farben.

---

## ListInColumns

**Technik:** Master-Detail auf EINER Seite: ein grid-Control legt Repeater und verlinkten Part nebeneinander (statt untereinander); der Part folgt der Zeilenauswahl über SubPageLink = field(...). Demo nutzt die virtuellen Tabellen AllObj/Field als Datenbank-Browser.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
page 50132 "Database Browser"
{
    ApplicationArea = all;
    PageType = List;
    SourceTable = AllObj;
    SourceTableView = where("Object Type" = const(Table));
    layout { area(Content) {
        grid(grid1) // grid = Spalten nebeneinander
        {
            group(g1)
            {
                repeater(Rep)
                {
                    field("Object ID"; Rec."Object ID") { }
                    field("Object Name"; Rec."Object Name") { }
                }
            }
            group(g2)
            {
                part(Fields; "Field Browser") // folgt der markierten Zeile
                {
                    SubPageLink = TableNo = field("Object ID");
                }
            }
        }
    } }
}
```

**Fallstricke:** Der als part eingebundene 'Field Browser' ist im Demo PageType=List (kein ListPart) — funktioniert im Webclient trotzdem; ein part darf sogar direkt im Content einer List-Seite unter dem Repeater stehen. Für ein Bau-ERP-Projekt das Grundmuster 'LV-Baum links, Positionen rechts'.

---

## BoundAction

**Technik:** OData-Bound-Actions auf API-Pages: eine [ServiceEnabled]-Prozedur mit WebServiceActionContext wird per POST auf .../quotes({id})/Microsoft.NAV.convertToOrder aufrufbar — Prozesse (Angebot zu Auftrag) aus externen Apps auslösen, ohne Datenfelder zu simulieren.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
page 50300 ConvertQuoteToOrder
{
    PageType = API;
    APIPublisher = 'hougaard'; APIGroup = 'youtube'; APIVersion = 'v2.0';
    EntityName = 'quote'; EntitySetName = 'quotes';
    SourceTable = "Sales Header";
    SourceTableView = where("Document Type" = const(Quote));
    DelayedInsert = true;
    layout { area(content) { repeater(General) {
        field(no; Rec."No.") { }
    } } }

    [ServiceEnabled]
    procedure ConvertToOrder(var ActionContext: WebServiceActionContext)
    var
        SalesQuoteToOrder: Codeunit "Sales-Quote to Order";
    begin
        SalesQuoteToOrder.Run(Rec); // Rec = der adressierte Datensatz
        ActionContext.SetObjectType(ObjectType::Page);
        ActionContext.SetObjectId(Page::ConvertQuoteToOrder);
        ActionContext.AddEntityKey(Rec.FieldNo("No."), Rec."No.");
        ActionContext.SetResultCode(WebServiceActionResultCode::Created);
    end;
    // Aufruf: POST .../api/hougaard/youtube/v2.0/quotes({systemId})/Microsoft.NAV.convertToOrder
}
```

**Fallstricke:** Die committete Datei enthält Tippreste (x`x` nach der letzten Prozedur) und kompiliert so NICHT. Der Aktionsname im URL wird camelCase (convertToOrder). Direkt relevant für ein geplantes Sync-Gateway: Prozesse statt nur CRUD über die API.

---

## datetimedialog

**Technik:** BC liefert einen fertigen Datum/Zeit-Auswahldialog als Systemseite 'Date-Time Dialog' mit — Caption(), SetDateTime()/GetDateTime() und UseDateOnly() statt Eigenbau.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
trigger OnOpenPage()
var
    DateTimeDialog: Page "Date-Time Dialog"; // Standard-Systemseite
begin
    // DateTimeDialog.UseDateOnly();  // nur Datum abfragen
    DateTimeDialog.Caption('What date do you go on vacation?');
    DateTimeDialog.SetDateTime(CurrentDateTime());
    if DateTimeDialog.RunModal() = Action::OK then
        Message('You selected %1', DateTimeDialog.GetDateTime());
end;
```

**Fallstricke:** Caption ist hier eine Methode der Seiteninstanz (setzt den Dialogtitel). Vor dem Eigenbau eines Datumsdialogs immer prüfen, ob der Standard ihn schon mitbringt — gleiche Lehre wie beim Permission-Set-Fund.

---

## StandardDialog

**Technik:** PageType=StandardDialog als schneller Eingabedialog ohne SourceTable: OK/Abbrechen kommen automatisch, Werte gehen per Setup-Methode hinein und nach RunModal über Getter wieder heraus — die Seiteninstanz lebt weiter.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
page 51100 "Standard dialog test"
{
    PageType = StandardDialog;
    Caption = 'This is the caption';
    layout { area(Content) {
        field(x; x) { ApplicationArea = all; Caption = 'This is X'; }
        field(y; y) { ApplicationArea = all; Caption = 'This is Y'; }
    } }
    procedure Setup(_x: Text; _y: Text)
    begin
        x := _x;
        y := _y;
    end;
    procedure GetX(): Text begin exit(x); end;
    procedure GetY(): Text begin exit(y); end;
    var
        x: Text;
        y: Text;
}
// Aufrufer:
var
    SD: Page "Standard dialog test";
begin
    SD.Setup('Erik', 'Soccer');
    if SD.RunModal() = Action::OK then
        Message('%1 %2', SD.GetX(), SD.GetY()); // Variablen nach RunModal noch lesbar
end;
```

**Fallstricke:** Der Trick ist die Lebensdauer: Nach RunModal lassen sich die vom Benutzer editierten Seitenvariablen über Getter abholen — kein temporärer Record nötig. Ideal für Schnelleingaben (Aufmaß-Werte, Buchungsparameter).

---

## MandatoryFields

**Technik:** Pflichtfeld-Optik per Ausdruck: ShowMandatory akzeptiert eine Boolesche Bedingung (roter Stern nur wenn relevant), BlankZero lässt die 0 leer aussehen — die tatsächliche Durchsetzung braucht separaten Code (OnModifyRecord/Validate).

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
pageextension 50144 "Customer Card" extends "Customer Card"
{
    layout
    {
        modify("Credit Limit (LCY)")
        {
            ShowMandatory = Rec.Blocked = Rec.Blocked::" "; // Stern nur bei nicht gesperrten
            BlankZero = true; // sonst sieht "0" wie ausgefuellt aus
        }
    }
    trigger OnModifyRecord(): Boolean
    begin
        if Rec."Credit Limit (LCY)" = 0 then
            Error('You cannot create a customer without a credit limit!');
        exit(true);
    end;
}
```

**Fallstricke:** ShowMandatory ist REIN optisch — es verhindert nichts. Ohne BlankZero wirkt ein Decimal/Integer-Pflichtfeld nie leer. Fürs Bau-ERP: Rapport-Pflichtfelder je Zustand (z.B. nur bei Fremdgerät) elegant markierbar.

> ⚠ **Ergänzung (P, 31.08.2026, aus MS Learn + Produkt-Befund):** Die Tabellen-Eigenschaft
> `NotBlank` zeigt den roten Stern NUR an **Primärschlüssel-Feldern** — ein
> `NotBlank`-Feld außerhalb des PK ist eine **unsichtbare Pflicht** (schlägt erst beim
> Feld-Verlassen an, ohne Vorwarnung), und ein `TestField` im `OnInsert` meldet sich
> erst beim Einfügen. Deshalb zeigen sich Pflichtfelder scheinbar „der Reihe nach".
> Anzeige-Mittel ist `ShowMandatory` an der Page (belegt zulässig auch im Repeater,
> belegt folgenlos) — aber NIE an automatisch gefüllte Felder (Falschmeldung).
> **Vollständige Regel (P, Bestandsmessung 31.08.):** Ein `NotBlank`-Feld außerhalb
> des Primärschlüssels braucht `ShowMandatory` genau dann, wenn es NICHT von einem
> `SubPageLink` gesetzt wird — beide Bedingungen stehen im Quelltext, mechanisch
> prüfbar. Und die `TestField`-im-`OnInsert`-Pflichten bleiben von dieser Messung
> unsichtbar (Feldeigenschaft findet sie nicht — nur Aufrufanalyse, unscharf).

---

## FocusDemo

**Technik:** Feature-Toggle-Architektur: ein Boolean in der Setup-Tabelle schaltet eine komplette Customization — Sichtbarkeit der Felder über eine in OnOpenPage gesetzte Variable, und JEDE Logik (Events, Berechnungen) prüft denselben Schalter. So bleibt eine Erweiterung für Standardnutzer unsichtbar.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
table 72100 "Software Inc Setup"
{
    fields
    {
        field(1; "KEY"; Code[10]) { }
        field(10; "Subscription Customization"; Boolean) { } // der Modul-Schalter
    }
    keys { key(PK; "KEY") { Clustered = true; } }
}
pageextension 72100 "Item Card Focus" extends "Item Card"
{
    layout { addafter(Type) {
        field("Subscription Item"; Rec."Subscription Item") { ApplicationArea = all; Visible = ItemSub; }
    } }
    trigger OnOpenPage()
    var
        Setup: Record "Software Inc Setup";
    begin
        if Setup.Get() then
            ItemSub := Setup."Subscription Customization"; // nur beim Oeffnen gelesen
    end;
    var
        ItemSub: Boolean;
}
// Und jede Geschaeftslogik prueft den Schalter selbst:
if Setup.Get() then
    if Setup."Subscription Customization" then
        ; // ... Modul-Logik ...
```

**Fallstricke:** Die Visible-Variable wird nur in OnOpenPage ausgewertet — Schalter-Änderung wirkt erst nach erneutem Öffnen der Seite (deckt sich mit der Praxiserfahrung: Visible/Editable werden nicht je Roundtrip neu ausgewertet). Setup.Get() kann fehlschlagen, deshalb überall if-geschützt. Vorlage für abschaltbare Module (z.B. 'Modul Baustelle').

---

## Lookups

**Technik:** Die zwei Lookup-Mechanismen nebeneinander: deklarativ die bedingte TableRelation (if Type = const(...)), imperativ der OnLookup-Trigger, der das Standard-Lookup komplett ersetzt und den Wert über den var-Text-Parameter zurückgibt.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
// Deklarativ in der Tabelle: bedingte TableRelation
field(4; "No."; Code[20])
{
    TableRelation = if (Type = const(Item)) Item."No."
    else if (Type = const(GL)) "G/L Account"."No.";
}
// Imperativ auf der Seite: OnLookup ersetzt das Standard-Lookup
field("Item No."; Rec."Item No.")
{
    ApplicationArea = All;
    trigger OnLookup(var Text: Text): Boolean
    var
        Item: Record Item;
    begin
        if Page.RunModal(Page::"Item List", Item) = Action::LookupOK then begin
            Text := Item."No."; // Rueckgabe ueber den var-Parameter
            exit(true);         // true = Wert uebernehmen
        end;
    end;
}
```

**Fallstricke:** Sobald OnLookup implementiert ist, ist das automatische TableRelation-Lookup weg — die Validierung gegen die TableRelation greift aber weiterhin. Muster für LV-Zeilen mit Typ Material/Lohn/Gerät, wo je Typ eine andere Stammtabelle gilt.

---

## multiselectrecord

**Technik:** Mehrfachauswahl aus einem Lookup übernehmen: Seite als PAGE-VARIABLE mit LookupMode=true modal ausführen, dann GetSelectionFilter() als Filterstring über alle markierten Datensätze iterieren — z.B. viele Artikel auf einmal als Belegzeilen anlegen.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
modify("No.")
{
    AssistEdit = true;
    trigger OnAssistEdit()
    var
        ItemList: Page "Item List";
        Item: Record Item;
        SL: Record "Sales Line";
        LineNo: Integer;
    begin
        ItemList.LookupMode := true; // Page-Variable, nicht Page.RunModal(Page::...)
        if ItemList.RunModal() = Action::LookupOK then begin
            SL.SetRange("Document No.", Rec."Document No.");
            SL.SetRange("Document Type", Rec."Document Type");
            if SL.FindLast() then
                LineNo := SL."Line No.";
            Item.SetFilter("No.", ItemList.GetSelectionFilter()); // ALLE markierten
            if Item.FindSet() then
                repeat
                    LineNo += 10000;
                    SL.Init();
                    SL."Document Type" := Rec."Document Type";
                    SL."Document No." := Rec."Document No.";
                    SL."Line No." := LineNo;
                    SL.Insert(true);
                    SL.Validate(Type, SL.Type::Item);
                    SL.Validate("No.", Item."No.");
                    SL.Validate(Quantity, 1);
                    SL.Modify(true);
                until Item.Next() = 0;
            CurrPage.Update(false); // sonst zeigt das Subform die neuen Zeilen nicht
        end;
    end;
}
```

**Fallstricke:** GetSelectionFilter gibt es nur auf der Seiteninstanz, deshalb die Page-Variable. Insert(true) VOR den Validates (Zeile muss existieren), dann Modify(true). CurrPage.Update(false) am Ende — false = Record nicht speichern, nur Anzeige auffrischen; dasselbe gilt generell, wenn Code Zeilen ändert, die eine Subpage anzeigt.

---

## FaxtBoxes

**Technik:** Klassische Beleg-Factbox: ListPart mit SourceTableView-Filter, per addfirst(factboxes) + SubPageLink angehängt; OnDrillDown auf der Belegnummer öffnet den Beleg — plus Scope=Repeater für Zeilen-Aktionen im Part.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
page 50100 "Our Factbox"
{
    PageType = ListPart;
    SourceTable = "Sales Header";
    SourceTableView = where("Document Type" = const(Order));
    Editable = false;
    layout
    {
        area(Content)
        {
            repeater(Rep)
            {
                field("No."; Rec."No.")
                {
                    trigger OnDrillDown()
                    begin
                        Page.RunModal(Page::"Sales Order", Rec); // Klick oeffnet den Beleg
                    end;
                }
                field(Amount; Rec.Amount) { }
            }
        }
    }
    actions
    {
        area(Processing)
        {
            action(Test)
            {
                Scope = Repeater; // erscheint im Zeilen-Kontext des Parts
                trigger OnAction() begin end;
            }
        }
    }
}
pageextension 50100 Ext extends "Customer Card"
{
    layout { addfirst(factboxes) {
        part(SalesOrders; "Our Factbox") { SubPageLink = "Sell-to Customer No." = field("No."); }
    } }
}
```

**Fallstricke:** Ohne den OnDrillDown-Trigger verlinkt eine eigene Factbox nirgendwohin — der Sprung zum Beleg muss selbst gebaut werden.

---

## factbox

**Technik:** EINE generische Factbox, die an beliebige Seiten andockt: Kindtabelle mit Schlüssel (ParentTable, ParentSystemId), Host-Seite übergibt sich per RecordRef an eine SetParent-Methode statt über SubPageLink. So wird dieselbe Beteiligten-/Team-Factbox auf Customer Card UND Posted Invoice wiederverwendet.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
table 50100 "Sales Team Member"
{
    fields
    {
        field(1; ParentTable; Integer) { }
        field(2; ParentSystemId; Guid) { }
        field(3; SalesPerson; Code[20]) { TableRelation = "Salesperson/Purchaser".Code; }
        field(4; Name; Text[100])
        {
            FieldClass = FlowField; Editable = false;
            CalcFormula = Lookup("Salesperson/Purchaser".Name where(Code = field(SalesPerson)));
        }
    }
    keys { key(PK; ParentTable, ParentSystemId, SalesPerson) { } }
}
// In der ListPart-Factbox:
procedure SetParent(Ref: RecordRef)
var
    SystemIdField: FieldRef;
begin
    PTable := Ref.Number;
    SystemIdField := Ref.Field(Ref.SystemIdNo);
    PSystemId := SystemIdField.Value;
    Rec.SetRange(ParentTable, PTable);
    Rec.SetRange(ParentSystemId, PSystemId);
    CurrPage.Update(false);
end;
// Auf JEDER Host-Seite identisch:
trigger OnAfterGetCurrRecord()
var
    Ref: RecordRef;
begin
    Ref.GetTable(Rec);
    CurrPage.Team.Page.SetParent(Ref);
end;
```

**Fallstricke:** Die SubPageLink-Variante (ParentTable = const(18), ParentSystemId = field(SystemId)) steht auskommentiert im Code — sie würde je Host-Seite eine hartkodierte Tabellennummer brauchen; der Methodenaufruf hält die Factbox wirklich generisch. CurrPage.Update(false) im SetParent nicht vergessen, sonst zeigt die Factbox veraltete Zeilen. InsertAllowed=false + eigene Add-Action mit Lookup ergibt saubere Bedienung.

---

## treecontrol

**Technik:** Eine List-Page als auf-/zuklappbaren Baum rendern — vier Repeater-Properties genügen, die Hierarchie kommt allein aus einem Integer-Feld 'Indentation' benachbarter Zeilen (wie im Kontenplan).

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
page 50142 "Tree test"
{
    PageType = List;
    SourceTable = "G/L Account";
    Editable = false;
    layout
    {
        area(Content)
        {
            repeater(rep)
            {
                IndentationColumn = Rec.Indentation; // Ebene je Zeile
                IndentationControls = Name;          // dieses Feld wird eingerueckt
                ShowAsTree = true;
                TreeInitialState = CollapseAll;
                field(Indentation; Rec.Indentation) { Visible = false; }
                field(Name; Rec.Name) { ApplicationArea = All; }
                field("No."; Rec."No.") { ApplicationArea = All; }
                field(Balance; Rec.Balance) { ApplicationArea = All; }
            }
        }
    }
}
```

**Fallstricke:** Der Baum ist reine Anzeige: Eltern-Kind ergibt sich nur aus der Einrückung AUFEINANDERFOLGENDER Zeilen — die Sortierung muss stimmen, es gibt keine echte Parent-Referenz. Für ein LV heißt das: Positionsnummern-Sortierung + Indentation-Feld pflegen.

---

## MatrixPage

**Technik:** Eine editierbare Matrix ohne Matrix-Control: virtuelle Integer-Tabelle als Zeilentreiber, N feste Spalten-Variablen, CaptionClass '3,'+Text für dynamische Spaltentitel, Links/Rechts-Aktionen verschieben ein LeftMostColumn-Offset, Zell-Eingaben landen in einem verschachtelten Dictionary.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
page 50800 "Matrix Page"
{
    PageType = List;
    SourceTable = Integer; // Zeilen = virtuelle Tabelle
    SourceTableView = where(Number = filter(> 0));
    layout { area(Content) { repeater(Rep) {
        field(Number; Rec.Number) { Caption = ' '; Editable = false; }
        field(c1; V1)
        {
            CaptionClass = '3,' + GiveMeTheColumnCaption(LeftMostColumn + 0); // dyn. Titel
            Width = 10;
            trigger OnValidate()
            begin
                StoreCell(Rec.Number, LeftMostColumn + 0, V1); // Dictionary of [Row, Dictionary of [Col, Wert]]
            end;
        }
        // c2..c5 analog mit V2..V5
    } } }
    actions { area(Processing) {
        action(Right)
        {
            ShortcutKey = RightArrow;
            trigger OnAction()
            begin
                LeftMostColumn += 5;
                CurrPage.Update(); // "scrollt" alle Spalten
            end;
        }
    } }
    trigger OnAfterGetRecord()
    begin
        V1 := CellValue(Rec.Number, LeftMostColumn + 0); // je Zeile neu befuellen
    end;
    var
        LeftMostColumn: Integer;
        V1: Integer;
        OverrideValues: Dictionary of [Integer, Dictionary of [Integer, Integer]];
}
```

**Fallstricke:** Im Original steckt ein Copy-Paste-Bug: die OnValidate-Trigger von c2 bis c5 schreiben alle V1 statt V2..V5 ins Dictionary — beim Nachbauen exakt prüfen. CaptionClass mit Prefix '3,' bedeutet 'nimm den Text dahinter wörtlich als Caption'. Muster passt auf Soll/Ist-je-Monat, Aufmaß-Spalten, Preisvergleich mehrerer Lieferanten.

---

## DragnDrop

**Technik:** Drag&Drop-Umsortierung in einer BC-Liste: ein unsichtbares Control-Addin macht per JS die Grid-Zeilen des Webclients draggable, liest die Datensatz-ID aus dem title-Attribut der ID-Zelle und meldet Drag/Drop-Paar an AL, das über ein Sorting-Index-Feld umsortiert.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
controladdin DragDrop
{
    Scripts = 'DropScript.js';
    StartupScript = 'DropStartup.js';
    RequestedHeight = 1; RequestedWidth = 1; // unsichtbarer Helfer
    event ControlReady();
    procedure DragDropEnable(IDField: Text);
    event DropEvent(DragID: Text; DropID: Text);
}
// List-Page (SourceTableView = sorting("Sorting Index")):
usercontrol(HTML; DragDrop)
{
    ApplicationArea = all;
    trigger ControlReady()
    begin
        CurrPage.HTML.DragDropEnable('pkey'); // Name der ID-Spalte
    end;
    trigger DropEvent(DragID: Text; DropID: Text)
    var
        drag: Record "Drop table";
        drop: Record "Drop table";
    begin
        drag.Get(DragID);
        drop.Get(DropID);
        if drag."Sorting Index" < drop."Sorting Index" then
            drag."Sorting Index" := drop."Sorting Index" + 1
        else
            drag."Sorting Index" := drop."Sorting Index" - 1;
        drag.Modify();
        CurrPage.Update(false);
    end;
}
// JS-Kern: rows von '.ms-nav-grid-data-table' draggable machen;
// ID = row.querySelector("[ariaLabel^='pkey']").getAttribute('title');
// Microsoft.Dynamics.NAV.InvokeExtensibilityMethod('DropEvent',[dragId,dropId]);
```

**Fallstricke:** Hängt an undokumentierten Webclient-DOM-Klassen (.ms-nav-grid-data-table) — jedes Client-Update kann es brechen; die ID-Spalte muss sichtbar im Grid stehen (JS liest ihr title-Attribut). Die ±1-Indexvergabe kollidiert bei wiederholtem Sortieren (kein Renumbering). Für LV-Positions-Umsortierung verlockend, aber als fragil einstufen.

---

## SpinningWait

**Technik:** Seite sofort rendern, schwer rechnen danach: usercontrol-Ready startet einen JS-Timer (Wait), dessen Callback-Event die teure Berechnung NACH dem ersten Paint ausführt — wahlweise als wiederholte Häppchen.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
page 50100 Spinner
{
    ApplicationArea = all;
    layout { area(Content) {
        usercontrol(Spin; WaitSpinner)
        {
            trigger Ready()
            begin
                if ControlReady then
                    exit; // Doppel-Init abfangen
                ControlReady := true;
                CurrPage.Spin.Wait(0); // JS-Timer -> Seite rendert ZUERST
            end;
            trigger Callback() // kommt vom JS-Timer zurueck
            var
                Customer: Record Customer;
            begin
                Customer.SetAutoCalcFields(Balance);
                if Customer.FindSet() then
                    repeat
                        Balance += Customer.Balance;
                    until Customer.Next() = 0;
                CurrPage.Spin.Wait(0); // optional: naechstes Haeppchen einplanen
            end;
        }
        field(Result; Balance) { Editable = false; }
    } }
    var
        ControlReady: Boolean;
        Balance: Decimal;
}
```

**Fallstricke:** Der Repo-Ordner ist unvollständig: controladdin 'WaitSpinner' und die JS-Dateien fehlen — nur die AL-Seite ist committet, das Add-in (Wait(ms) startet setTimeout, der Callback feuert) muss man nachbauen. Der ControlReady-Guard gegen Mehrfach-Init ist essenziell.

---

## progressbar2

**Technik:** Grafischer Fortschrittsbalken als Control-Addin: HTML/CSS-Balken, Ready-Handshake per Event aus dem StartupScript, AL schiebt Werte über eine Prozedur nach — das Grundgerüst jedes eigenen Control-Addins.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
controladdin MyProgressBar
{
    Scripts = 'script.js';
    StartupScript = 'startup.js';
    StyleSheets = 'progress.css';
    MinimumHeight = 50; MaximumHeight = 50;
    HorizontalStretch = true;
    event IAmReady();
    procedure SetProgress(Progress: Integer);
}
// startup.js:
//   addin.innerHTML = '<div id="myProgress"><div id="myBar">0%</div></div>';
//   Microsoft.Dynamics.NAV.InvokeExtensibilityMethod('IAmReady',[]);
// script.js:
//   function SetProgress(p){ var b=document.getElementById('myBar');
//     b.style.width=p+'%'; b.innerHTML=p+'%'; }
// AL-Seite:
usercontrol(bar; MyProgressBar)
{
    ApplicationArea = All;
    trigger IAmReady()
    begin
        CurrPage.bar.SetProgress(Rec.MyProgress); // Startwert erst NACH Ready
    end;
}
field(MyProgress; Rec.MyProgress)
{
    ApplicationArea = All;
    trigger OnValidate()
    begin
        CurrPage.bar.SetProgress(Rec.MyProgress);
    end;
}
```

**Fallstricke:** Der Ready-Handshake ist Pflicht: AL-Aufrufe vor dem Startup-Event des Add-ins verpuffen. Taugt für Baufortschritt-Anzeigen auf Projekt-/Baustellenkarten — aber NICHT als Live-Fortschritt für Serverschleifen (siehe MessingWithDialogues).

---

## InDataSet

**Technik:** Berechnete Anzeigespalte ohne Tabellenfeld: eine Seitenvariable als Repeater-Feld, je Zeile in OnAfterGetRecord befüllt — die leichte Alternative zu FlowFields für reine Anzeigen.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
page 50100 "Customer List 2"
{
    PageType = List;
    SourceTable = Customer;
    layout { area(Content) { repeater(Rep) {
        field("No."; Rec."No.") { ApplicationArea = All; }
        field(AltAdr; AltAdr) // Variable als Spalte
        {
            ApplicationArea = all;
            Caption = 'Alt Adr';
        }
    } } }
    trigger OnAfterGetRecord()
    begin
        AltAdr := Rec.Address; // je Zeile berechnet
    end;
    var
        [InDataSet]
        AltAdr: Text;
}
```

**Fallstricke:** Die Variablen-Spalte ist weder sortier- noch filterbar (kein echtes Feld). [InDataSet] ist ein historisches Attribut aus C/AL-Zeiten — moderne Runtimes brauchen es für dieses Muster nicht mehr.

---

## ColorCodingGeneralJournal

**Technik:** Farbcodierung von Zeilen über ein Enum, dessen Captions Emojis sind (🟥🟩🦄): eine schmale Spalte (Width=1) wird zur wählbaren, filterbaren Farbmarkierung — Farben, die StyleExpr nie könnte.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
enum 50130 Color
{
    value(0; " ") { Caption = ' '; }
    value(1; Red) { Caption = '🟥'; }   // Emoji ALS Caption
    value(4; Green) { Caption = '🟩'; }
    value(8; Unicorn) { Caption = '🦄'; }
}
tableextension 50130 "My Color" extends "Gen. Journal Line"
{
    fields { field(50130; Color; Enum Color) { } }
}
pageextension 50130 Color extends "General Journal"
{
    layout { addafter("Posting Date") {
        field(Color; Rec.Color)
        {
            ApplicationArea = all;
            Width = 1; // schmale "Farbspalte"
        }
    } }
}
```

**Fallstricke:** Weil es ein echtes Tabellenfeld ist, kann man danach FILTERN und SORTIEREN — der eigentliche Gewinn gegenüber StyleExpr. Emojis funktionieren überall, wo das Enum gerendert wird (auch im Filterbereich). Für Rapport-/Journalzeilen-Markierung sofort brauchbar.

---

## SessionSettings

**Technik:** Die laufende Benutzersession per Code umkonfigurieren: SessionSettings.Init() + LanguageId(...) + RequestSessionUpdate(true) wechselt Sprache/Region und startet die Session neu — z.B. für einen Sprachumschalt-Button.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
action(SwitchLanguage)
{
    ApplicationArea = All;
    trigger OnAction()
    var
        s: SessionSettings;
    begin
        s.Init();                     // aktuelle Einstellungen laden!
        s.LanguageId(1030);           // 1030 = Daenisch; de-AT = 3079
        s.RequestSessionUpdate(true); // true = in User-Personalisierung speichern
    end;                              // Client laedt die Session neu
}
```

**Fallstricke:** Init() zuerst, sonst überschreibt man die übrigen Einstellungen mit Leerwerten. RequestSessionUpdate startet die Client-Session neu — ungespeicherte Eingaben sind weg. Der Verify-Teil des Demos zeigt daneben Codeunit "Type Helper".FormatUtcDateTime für zeitzonen-saubere Anzeige.

---

## HidingFieldValues

**Technik:** MaskType=Concealed zeigt Feldwerte als Punkte an — auch nachträglich per modify() auf Standardfeldern und FlowFields. Sichtschutz für sensible Werte (Löhne, EK-Preise) auf Bildschirmen mit Publikum.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: application 27.0 / runtime 16.0 — MaskType ist neu (BC27), auf dem das Referenzprojekt-Ziel BC28 verfügbar

```al
pageextension 50100 Ext extends "Customer Card"
{
    layout
    {
        addafter(Name)
        {
            field(Hidden; Rec."Name 2")
            {
                ApplicationArea = all;
                MaskType = Concealed; // Punkte statt Wert
            }
        }
        modify(BalanceAsVendor)
        {
            MaskType = Concealed; // geht auch auf bestehenden Feldern
        }
    }
}
```

**Fallstricke:** Rein optische Maskierung, KEIN Berechtigungsschutz — der Wert bleibt über andere Seiten, Personalisierung und APIs lesbar. Echten Schutz liefern nur Permissions.

---

## LineBreaks

**Technik:** Mehrzeilige String-Literale mit @'...' (verbatim) und Zeichen aus Codepunkten über Index-Zuweisung auf Text[1] — die Basis für CSV-Parsing und Testdaten direkt im AL-Code.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: application 26.0 / runtime 15.0 — @'…'-Verbatim-Strings brauchen neuere Runtime

```al
trigger OnOpenPage()
var
    CR: Text[1];
    NL: Text[1];
    csv: Text;
    Lines: List of [Text];
begin
    CR[1] := 13; // Zeichen aus Codepunkt
    NL[1] := 10;
    csv :=
@'1000,Hello,123
2000,More,234
3000,Last,345
';
    Lines := csv.Split(NL);
    Message('Line 2 = %1', Lines.Get(2).TrimEnd(CR)); // CR haengt sonst an!
end;
```

**Fallstricke:** Das Multiline-Literal enthält CRLF: nach Split auf LF bleibt an jeder Zeile ein unsichtbares CR hängen — TrimEnd(CR) nicht vergessen, sonst schlagen Vergleiche und Code-Zuweisungen still fehl. Relevant für ÖNORM-/CSV-Importtests.

---

## Dialogs

**Technik:** Der klassische Fortschritts-Dialog: Label mit \\ als Zeilenumbruch und #n####-Platzhaltern, die per Window.Update(n, Wert) live aktualisiert werden — die einzige Fortschrittsanzeige, die während eines laufenden Server-Triggers wirklich tickt.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
trigger OnAction()
var
    Window: Dialog;
    GL: Record "G/L Entry";
    DialogTextLbl: Label 'Stay calm,\\ AL is #1####### #2###### working...';
    i: Integer;
    Sum: Decimal;
begin
    Window.Open(DialogTextLbl); // \\ = Zeilenumbruch, #n#### = Update-Felder
    for i := 1 to 50 do begin
        Window.Update(1, i);    // schreibt in Feld #1
        if GL.FindSet() then
            repeat
                Sum += GL.Amount;
            until GL.Next() = 0;
        Window.Update(2, Sum);  // Feld #2
    end;
    Window.Close();
    Message('Total is %1', Sum);
end;
```

**Fallstricke:** Die Breite der #-Felder (#1#######) begrenzt die Anzeige. Dialog nach Gebrauch schließen — Update auf geschlossenem Dialog wirft Laufzeitfehler. Für ÖNORM-Importe und Massenbuchungen das Mittel der Wahl.

---

## CueGroup

**Technik:** Eigene Kacheln (Cues) im Rollencenter: cuegroup auf einem CardPart mit Tabellen- UND Seitenvariablen-Feldern, OnDrillDown je Kachel, StyleExpr färbt Kacheln, und ein actions-Block in der cuegroup rendert Aktions-Kacheln; angehängt per addfirst(rolecenter).

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
page 66100 "Cue Test"
{
    PageType = CardPart;
    SourceTable = Customer;
    layout { area(Content) {
        cuegroup(Kpis)
        {
            Caption = 'A nice caption';
            field(Number; Number) // Seitenvariable als Kachel
            {
                ApplicationArea = all;
                trigger OnDrillDown()
                begin
                    ; // eigene Navigation/Aktion
                end;
            }
            field(Balance; Rec.Balance)
            {
                ApplicationArea = all;
                StyleExpr = 'Unfavorable'; // rote Kachel
            }
        }
        cuegroup(Act)
        {
            Caption = 'Even more actions';
            actions
            {
                action(HelloWorld)
                {
                    ApplicationArea = all;
                    Image = TileBrickCustomer;
                    trigger OnAction() begin end;
                }
            }
        }
    } }
    var
        Number: Integer;
}
pageextension 66100 "My role" extends "Business Manager Role Center"
{
    layout { addfirst(rolecenter) { part(My; "Cue Test") { ApplicationArea = all; } } }
}
```

**Fallstricke:** Cues funktionieren auch mit reinen Seitenvariablen (in OnOpenPage befüllt) — es braucht keine FlowField-Cue-Tabelle für schnelle Kennzahlen. Für ein Bauleiter-Rollencenter (offene Rapporte, ungeprüfte Aufmaße) das Einstiegsmuster.

---

## FullPageUserControl

**Technik:** Ein Control-Addin auf volle Seitenhöhe bringen: VerticalStretch=true plus Startup-JS, das das eigene iframe (window.frameElement) auf die Höhe des umgebenden .control-addin-form-Divs setzt und bei resize nachzieht — Basis für Vollflächen-UIs (Pläne, Karten, Grafiken).

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
controladdin fullpagetest
{
    StartupScript = 'startup.js';
    VerticalStretch = true;
}
page 50112 Test
{
    PageType = Card;
    SourceTable = Customer;
    Editable = false;
    ApplicationArea = all;
    layout { area(Content) {
        usercontrol(test; fullpagetest) { }
    } }
}
// startup.js:
// var h = window.frameElement.closest('div[class~="control-addin-form"]');
// window.frameElement.style.height = (h.offsetHeight - 5) + 'px';
// window.frameElement.style.maxHeight = (h.offsetHeight - 5) + 'px';
// window.addEventListener('resize', function () {
//     var h2 = window.frameElement.closest('div[class~="control-addin-form"]');
//     window.frameElement.style.height = (h2.offsetHeight - 5) + 'px';
// }, true);
```

**Fallstricke:** VerticalStretch allein füllt die Seite nicht — erst der iframe-Hack über den undokumentierten DOM (Klasse 'control-addin-form') tut es; damit updateanfällig. PageType=Card + Editable=false, damit das Control den Content-Bereich allein bekommt.

---

## PrettyCardPages

**Technik:** Card-Layout-Grundgriffe: zwei Geschwister-Gruppen unter einer Obergruppe rendern als zwei Spalten; Importance=Promoted hält ein Feld auch bei eingeklappter Gruppe sichtbar, Importance=Additional versteckt es hinter 'Mehr anzeigen'; Visible=false macht Felder nur per Personalisierung zuschaltbar.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
page 50123 "Pretty Customer Card"
{
    PageType = Card;
    SourceTable = Customer;
    layout { area(content) {
        group(GenGroup)
        {
            Caption = 'General';
            group(NameGroup) // zwei Geschwister-Gruppen -> zwei Spalten
            {
                Caption = 'Name';
                field("No."; Rec."No.")
                {
                    ApplicationArea = All;
                    Importance = Promoted;   // auch eingeklappt sichtbar
                }
                field("Name 2"; Rec."Name 2")
                {
                    ApplicationArea = All;
                    Importance = Additional; // erst unter "Mehr anzeigen"
                }
            }
            group(AddressGroup)
            {
                Caption = 'Address';
                field(Address; Rec.Address) { ApplicationArea = All; }
                field(City; Rec.City) { ApplicationArea = All; }
            }
        }
        field(GLN; Rec.GLN) { ApplicationArea = All; Visible = false; }
    } }
}
```

**Fallstricke:** Kuriosum im Original: mitten in der Card-Gruppe steht ein repeater(Rep) um ein einzelnes Feld — kompiliert anstandslos; die eigentliche Spaltenaufteilung machen aber die Geschwister-Gruppen.

---

## Pizzazz

**Technik:** views-Block auf List-Pages: vordefinierte gefilterte Sichten, die mit SharedLayout=false je View eigenes Layout bekommen (Spalten aus-/einblenden, moveafter) — gespeicherte Ansichten per Code statt per Personalisierung ausliefern.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: application 19.0 / runtime 8.0 — views gibt es seit BC15, läuft überall

```al
page 56800 "Customers with Pizzazz"
{
    PageType = List; SourceTable = Customer; UsageCategory = Lists; ApplicationArea = all;
    layout { area(content) { repeater(General) {
        field("No."; Rec."No.") { ApplicationArea = all; }
        field(Address; Rec.Address) { ApplicationArea = all; }
        field("Mobile Phone No."; Rec."Mobile Phone No.") { ApplicationArea = all; }
        field("Customer Price Group"; Rec."Customer Price Group") { ApplicationArea = all; Visible = false; }
    } } }
    views
    {
        view(Blocked)
        {
            Caption = 'Blocked Customers';
            Filters = where(Blocked = filter(All | Invoice | Ship));
            SharedLayout = false; // eigenes Layout je View
            layout
            {
                modify(Address) { Visible = false; }
                moveafter("No."; "Mobile Phone No.")
            }
        }
        view(PriceGroups)
        {
            Caption = 'Customers with price groups';
            Filters = where("Customer Price Group" = filter(<> ''));
            SharedLayout = false;
            layout { modify("Customer Price Group") { Visible = true; } }
        }
    }
}
```

**Fallstricke:** SharedLayout=false ist der Schlüssel — ohne ihn teilen alle Views ein Layout. Ein per Default unsichtbares Feld kann in einem View gezielt sichtbar geschaltet werden. Für Rollen-Sichten (Bauleiter sieht andere LV-Spalten als Abrechner) sofort nutzbar.

---

## PlaceHolderText

**Technik:** InstructionalText auf Feld-Controls erzeugt graue Platzhaltertexte im leeren Feld (Web-Formular-Optik); kombiniert mit ShowCaption=false entsteht ein modernes, label-loses Formular — auch per modify() auf Standardfeldern.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: application 24.0 / runtime 13.0 — InstructionalText direkt auf Feldern ist neuer als auf Gruppen

```al
page 50100 "My Card"
{
    SourceTable = Customer;
    PageType = Card;
    layout { area(Content) {
        field(Name; Rec.Name)
        {
            ApplicationArea = All;
            ShowCaption = false;        // Label weg ...
            InstructionalText = 'Name'; // ... Platzhalter im leeren Feld
        }
        field(Address; Rec.Address)
        {
            ApplicationArea = All;
            ShowCaption = false;
            InstructionalText = 'Address';
        }
    } }
}
// Nachtraeglich:
// pageextension ... { layout { modify("Address 2") { InstructionalText = 'Suite No.'; } } }
```

**Fallstricke:** Der Platzhalter verschwindet, sobald ein Wert drinsteht — ohne ShowCaption=false wirkt er doppelt zum Label. Nett für Erfassungsmasken (Rapport-Schnellerfassung), sparsam einsetzen: ausgefüllte Felder verlieren ihre Beschriftung.

---

## SubPartToParent

**Technik:** Subpage-zu-Header-Kommunikation, die AL offiziell nicht kann: je ein unsichtbares Twin-Control-Addin in Zeilen- und Kopfseite; das Zeilen-JS iteriert window.parent.frames, findet den Schwester-Frame und ruft dort eine Funktion, die das Event auf der Kopfseite auslöst — der Header reagiert live auf die Zeilenauswahl.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
controladdin InterPageCommunication
{
    RequestedHeight = 1; RequestedWidth = 1; // unsichtbar, in Kopf UND Zeilen einbetten
    MaximumHeight = 1; MaximumWidth = 1; MinimumHeight = 1; MinimumWidth = 1;
    Scripts = 'interpagecommunication.js';
    event PingFromSubPage(LineNo: Integer);
    procedure PingParentPage(LineNo: Integer);
}
pageextension 50100 Lines extends "Sales Order Subform"
{
    layout { addlast(content) { usercontrol(Comm; InterPageCommunication) { ApplicationArea = all; } } }
    trigger OnAfterGetCurrRecord()
    begin
        CurrPage.Comm.PingParentPage(Rec."Line No."); // Zeile meldet sich
    end;
}
pageextension 50101 Header extends "Sales Order"
{
    layout { addlast(content) {
        usercontrol(Comm; InterPageCommunication)
        {
            ApplicationArea = all;
            trigger PingFromSubPage(LineNo: Integer)
            begin
                if LineNo <> CurrentLineNo then
                    CurrentLineNo := LineNo; // hier reagieren (Summen etc.)
            end;
        }
    } }
    var
        CurrentLineNo: Integer;
}
// JS: iteriert window.parent.frames, ruft im Schwester-Frame RealPing(lineno)
// -> InvokeExtensibilityMethod('PingFromSubPage',[lineno])
```

**Fallstricke:** Frame-Iterations-Hack, undokumentiert — Sandbox-/Isolationsänderungen des Clients können ihn jederzeit killen. OnAfterGetCurrRecord feuert häufig: ohne Entprellung (CurrentLineNo-Vergleich) spammt der Header. Denkbar für 'Aufmaßzeile gewählt -> Kopf zeigt Positionssumme', aber nur als Nice-to-have einsetzen.

---

## promptdialog

**Technik:** PageType=PromptDialog — der Copilot-Seitentyp: area(Prompt) für die Eingabezone, area(Content) für das Ergebnis (auch mit ListPart), systemaction(Generate) als Auslöser; SourceTable muss temporär sein.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** app.json: application 23.0 / runtime 12.1 — PromptDialog ist der Copilot-Seitentyp ab BC23

```al
page 50100 "Prompt Dialog Test"
{
    PageType = PromptDialog;
    Extensible = false;
    PromptMode = Prompt; // oeffnet im Eingabe-Modus
    SourceTable = Item;
    SourceTableTemporary = true;
    layout
    {
        area(Prompt) // Eingabezone oben
        {
            field(P; P)
            {
                ShowCaption = false;
                MultiLine = true;
                ApplicationArea = All;
            }
        }
        area(Content) // Ergebniszone
        {
            part(Items; "Item SubList") { ApplicationArea = all; }
        }
    }
    actions { area(SystemActions) {
        systemaction(Generate) // der "Generieren"-Knopf
        {
            Caption = 'Do something!';
            trigger OnAction()
            begin
                ; // hier KI/Verarbeitung aufrufen
            end;
        }
    } }
    var
        P: Text;
}
```

**Fallstricke:** Eigene Areas (Prompt, SystemActions) und systemaction statt action — normale Page-Muster gelten hier nicht. SourceTableTemporary=true, sonst schreibt der Dialog echte Daten. Nur relevant, falls das Projekt einmal einen KI-Assistenten (z.B. LV-Positionsvorschläge) bekommt.

---

## MessingWithDialogues

**Technik:** Das unsichtbare 1x1-Pixel-Control-Addin als JS-Brücke — und der Kernbefund dazu: AL-zu-JS-Aufrufe aus einem laufenden Trigger werden gepuffert und erst nach Trigger-Ende beim Client ausgeführt, während Dialog.Update live aktualisiert.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)

```al
controladdin jshacks
{
    MaximumHeight = 1; MinimumHeight = 1;
    MaximumWidth = 1; MinimumWidth = 1;
    RequestedHeight = 1; RequestedWidth = 1; // unsichtbar
    Scripts = 'script.js';
    StartupScript = 'startup.js';
    procedure Update(i: Integer);
}
// script.js: function Update(i) { alert('hello' + i); }
// Auf der Seite:
usercontrol(hack; jshacks) { ApplicationArea = all; }
action(Test)
{
    trigger OnAction()
    var
        d: Dialog;
        i: Integer;
    begin
        d.Open('Progress #1##########');
        for i := 1 to 10 do begin
            Sleep(300);
            d.Update(1, i);          // live sichtbar
            CurrPage.hack.Update(i); // JS: kommt erst NACH Trigger-Ende, gesammelt
        end;
        d.Close();
    end;
}
```

**Fallstricke:** Wer ein Control-Addin als Fortschrittsanzeige für eine Serverschleife baut, sieht alle Aufrufe am Ende auf einmal — für Live-Fortschritt bleibt nur Dialog/#-Felder. Die 1x1-Pixel-Bauform ist zugleich das Grundmuster aller DOM-Hacks dieses Repos.

---

## Übersprungen (bewusst)

- CardList — Standard List/Card-Paar
- fullscreen — AL-Datei leer
- PageTypes — auskommentiertes Minimalbeispiel
- BlankFields — reine Feldtyp-Schau
- OpenPageTrigger — SingleInstance-Basiswissen
- CurrPageUpdate — Kern in multiselectrecord
- ShortCutKeys — Ein-Property-Demo
- Hack the Search dialog — fragiler DOM-Hack, Code defekt
- PrettyCardPages test.al — leerer Event-Stub

