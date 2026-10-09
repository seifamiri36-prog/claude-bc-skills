# Tooling, Umgebung, Telemetrie & KI in BC

_Destilliert aus Erik Hougaards Youtube-Video-Sources (Ordnername = Videothema)._
_Vollquellen: https://github.com/hougaard/Youtube-Video-Sources (lokal klonen; Ordnername = Videothema)_

Der Cluster lehrt den Werkzeugkasten UM den AL-Code herum: Umgebungs- und Tenant-Erkennung zur Laufzeit, Application-Insights-Telemetrie per KQL aus AL abfragen, die Anatomie der .app-Datei (ZIP mit 40-Byte-Header — Quellcodeschutz ist eine app.json-Entscheidung), AppSource-Abhaengigkeiten ueber NuGet-Symbolfeeds und die XLIFF-Uebersetzungspipeline inklusive de-AT. Dazu kommen drei komplementaere KI-Muster: ein roher HTTP-Client fuer OpenAI/Azure OpenAI (mit IsBlockedByEnvironment- und Markdown-Fence-Fallen), das Andocken an BCs eingebauten Entity-Text-Copilot per Facts-Dictionary, und ChatGPT-generierter AL-Code als warnendes Beispiel (kompiliert, ist aber subtil falsch). Der wertvollste Einzelfund fuer ein Bau-ERP ist der PageScriptingHelper: Page-Scripting-YAML-Testskripte automatisch aus echten Daten generieren — plus die Erkenntnis, dass Editable/Visible in "Page Control Field" Ausdruecke statt Literale sind. Etwa ein Drittel der Ordner ist reine Video-Kulisse (Hello-World-Geruest ohne extrahierbaren Mechanismus).

**Wertvollste Ordner:** BCALToolbox-master · PageScriptingHelper · AIPlayground · apptranslation · ReleaseManagement

## Themen (nach Praxis-Relevanz)

- ●●●  **apptranslation** — Die komplette Uebersetzungs-Pipeline: features:["TranslationFile"] in app.json laesst den Compiler eine .g.xlf erzeugen; je Zielsprache kommt eine Kopie mit target-language und <target>-Eintraegen ins Translations-Verzeichnis — der Ordner enthaelt 35 fertige Sprachdateien inklusive de-AT und de-CH.
- ●●●  **BCALToolbox-master** — Produktionsreife Helper-Bibliothek mit drei uebertragbaren Mustern: Facade(Public)+Impl(Internal)-Architektur je Modul, Fortschrittsdialog mit Restzeitschaetzung und 1-Sekunden-Drossel, und ein kompletter Excel-Import in vier Standard-Aufrufen.
- ●●●  **ReleaseManagement** — Geschaeftsregeln beim Freigeben von Belegen erzwingen: EventSubscriber auf OnBeforeReleaseSalesDoc der Codeunit "Release Sales Document" — ein error() darin blockiert die Freigabe komplett.
- ●●●  **PageScriptingHelper** — Page-Scripting-Testskripte (YAML fuer BCs Record/Replay-Testtool ab BC 24) automatisch aus vorhandenen DATEN generieren: Page Metadata + "Page Control Field" liefern die Steuerelemente, RecordRef/FieldRef die Werte, TextBuilder baut die Steps, Temp Blob + DownloadFromStream liefert die .yml aus.
- ●●○  **CoPilotInBC** — BCs eingebauten Entity-Text-Copilot (Marketingtext-Generator) auf eigene Seiten/Tabellen setzen: Factbox "Entity Text Factbox Part" andocken + SetContext, dann per OnRequestEntityContext-Subscriber ein Facts-Dictionary, Ton und Format liefern — das Prompting uebernimmt der Standard.
- ●●○  **AIPlayground** — Generischer LLM-Client in purem AL fuer Azure OpenAI, OpenAI und LM Studio hinter einem Enum: Provider-abhaengige Auth-Header, Chat-Completions-Payload aus JsonObject/JsonArray, TryFunction-Kapselung, JSON-Mode. Die Referenz, wenn ein LLM ohne Microsofts Copilot-Toolkit angebunden werden soll.
- ●●○  **Reuse old CAL code** — Alter CAL-Code laeuft fast unveraendert in AL weiter (Grossschreibung, IF-THEN-Stil, Arrays) — hier ein kompletter Code39-Barcode-Generator, der ein 24-bit-BMP byteweise per OutStream.WRITE in ein Blob-Feld schreibt, ganz ohne externe Bibliothek.
- ●●○  **EnvironmentInfo** — Zur Laufzeit erkennen, WO der Code laeuft (SaaS/OnPrem, Produktion/Sandbox) und WER der Tenant ist — fuer Feature-Gates, Telemetrie-Anreicherung und Schutz vor Testaktionen in Produktion.
- ●●○  **repos** — Azure Function (HTTP-Trigger, C#) als Fluchtluke fuer alles, was AL nicht kann — AL ruft sie als simplen HTTPS-POST mit JSON-Body auf; der Function-Key steckt bei AuthorizationLevel.Function als ?code= in der URL.
- ●●○  **Nuget** — Gegen AppSource-Apps (Continia, Avalara, WooCommerce ...) entwickeln, ohne .app-Symboldateien zu jagen: Abhaengigkeit einfach in app.json eintragen, die AL-Extension zieht die Symbole automatisch aus Microsofts NuGet-Feeds (MSSymbols/AppSourceSymbols).
- ●●○  **whatnewin2021w2** — Sammelbare Fehler: [ErrorBehavior(ErrorBehavior::Collect)] + ErrorInfo laesst eine Validierung ALLE Probleme einsammeln statt beim ersten abzubrechen — ideal fuer Zeilen-Validierung ganzer Belege.
- ●●○  **Whats New in v17 Dev** — Drei BC17-Perf-/Robustheitsfeatures in einem Demo: TableType=Temporary (Tabelle wird nie in SQL angelegt), SetLoadFields/Partial Records (nur benoetigte Spalten laden) und [CommitBehavior] (Commit in fremdem Code neutralisieren).
- ●●○  **telemetry** — Application-Insights-Telemetrie nicht nur schreiben, sondern aus AL heraus LESEN: REST-POST mit KQL-Query gegen api.applicationinsights.io, Ergebnis als tables[0].rows-Array parsen. Braucht man fuer In-App-Dashboards ueber die eigene Extension-Nutzung.
- ●●○  **AppDissect** — Anatomie einer .app-Datei: ZIP-Container mit 40-Byte-Praefix; nach dem Entpacken liegen NavxManifest.xml, SymbolReference.json und — bei offener resourceExposurePolicy — der komplette AL-Quellcode samt ControlAddIn-JavaScript lesbar da. Wichtig fuer beide Richtungen: fremde Apps analysieren und die eigene schuetzen.
- ●○○  **ALBuild** — Eine komplette BC-CI-Pipeline als deklarative Task-Liste (Eriks ALBuild.exe-Tool): die AUFGABENREIHENFOLGE ist das Lehrstueck — Version bumpen, Symbole aus dem Docker-Container ziehen, kompilieren, XLF maschinell uebersetzen, NOCHMAL kompilieren, Release kopieren, git commit+push.
- ●○○  **UsingTheDesigner** — Der In-Client-Designer (Drag&Drop im Web-Client) erzeugt eine echte pageextension, die man sich in VS Code herunterladen und ins eigene Projekt uebernehmen kann — schnellstes Scaffolding fuer Layout-Umbauten samt moveafter/modify-Syntax.
- ●○○  **ChatGPT** — Fallstudie: von ChatGPT generierte AL-Objekte (Tabelle + Card + List + Action) kompilieren sauber und sehen idiomatisch aus — enthalten aber subtile Fehler, die nur ein Fachkundiger sieht. Lehrt, WO man LLM-generierten AL-Code pruefen muss.
- ●○○  **WhatsNewInBC26** — BC26-Sprachzucker und der eingebaute Browser: ToText()-Instanzmethoden auf Decimal/DateTime statt Format(), this-Qualifizierer, und PageType=UserControlHost mit dem mitgelieferten WebPageViewer-Usercontrol — Webseite einbetten ohne eigenes ControlAddIn.
- ●○○  **Altpgen** — Dataverse/CDS-Proxytabellen in AL: TableType=CDS mit ExternalName/ExternalType je Feld mappt eine Dataverse-Entitaet (inkl. eigener Spalten wie new_youtube) — eine normale List-Page darauf liest live aus Dataverse. Die Dateien sind von Eriks Generator-Tool altpgen aus den CDS-Metadaten erzeugt.

---

## apptranslation

**Technik:** Die komplette Uebersetzungs-Pipeline: features:["TranslationFile"] in app.json laesst den Compiler eine .g.xlf erzeugen; je Zielsprache kommt eine Kopie mit target-language und <target>-Eintraegen ins Translations-Verzeichnis — der Ordner enthaelt 35 fertige Sprachdateien inklusive de-AT und de-CH.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** app.json application 19.0, runtime 8.0, features TranslationFile

```al
// app.json:  "features": ["TranslationFile"]
// -> Compiler erzeugt Translations\<app>.g.xlf (Quelle en-US)

// Uebersetzbar ist alles mit Caption/Label:
table 50101 "Translate example"
{
    fields
    {
        field(1; CustomerNo; Code[20]) { Caption = 'Customer No.'; }
    }
}
var
    ToTranslate: Label 'This message can be translated.', Comment = 'Kontext fuer den Uebersetzer';

// Je Sprache: Translations\<app>.g.de-AT.xlf mit
// <file source-language="en-US" target-language="de-AT">
//   <trans-unit id="Table 1621852298 - Field ... - Property ...">
//     <source>Customer No.</source><target>Debitorennr.</target>
```

**Fallstricke:** Die trans-unit-IDs sind Hashes aus Objekt-/Feldnamen — wer Objekte umbenennt, verwaist still alle vorhandenen Uebersetzungen. Das Comment-Attribut des Labels landet als <note> im XLF und ist die einzige Kontextinfo fuer Uebersetzer. ⚠⚠ **BERICHTIGT 01.09.2026 (B): Hier stand „Dateiname muss exakt <appname>.g.<kultur>.xlf lauten“. EINEN NAMENSZWANG GIBT ES NICHT.** MS *Working with translation files* (Abschnitt *The XLIFF file*): „There is **no enforced naming** on the file, but it's a good practice to name it `<extensionname>.<language>.xlf`.“ Das `g.`-Schema ist die **Erzeuger-Konvention des Compilers**, keine Vorgabe. ⚠ Was dort dagegen WIRKLICH steht und wichtiger ist: „Make sure to **rename the translation file** before building the extension next time, as it'll be **overwritten**.“ Die generierte `.g.xlf` wird bei jedem Bau neu geschrieben — eigene Übersetzungen gehören in eine umbenannte Datei.

---

## BCALToolbox-master

**Technik:** Produktionsreife Helper-Bibliothek mit drei uebertragbaren Mustern: Facade(Public)+Impl(Internal)-Architektur je Modul, Fortschrittsdialog mit Restzeitschaetzung und 1-Sekunden-Drossel, und ein kompletter Excel-Import in vier Standard-Aufrufen.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** app.json application/platform 18.0, runtime 7.0

```al
// Muster 1 — Facade delegiert an Impl (Access = Internal): stabile API, tauschbare Innereien.
// Muster 2 — Fortschrittsdialog, gedrosselt + Restzeit:
procedure UpdateWindow(Counter: Integer; NoOfRecords: Integer)
begin
    if CurrentDateTime < LastUpdate + 1000 then
        exit; // max. 1 Update/Sek. — sonst dominiert der Dialog die Laufzeit!
    Window.Update(20, ProgressBarText(Counter, NoOfRecords));
    LastUpdate := CurrentDateTime;
    EstimatedDuration := Round((CurrentDateTime - StartTime) * 100 / (Counter / NoOfRecords * 100), 100);
    Window.Update(23, Format(StartTime + EstimatedDuration, 0, '<Hours24>:<Minutes,2>:<Seconds,2>'));
end;

// Muster 3 — Excel-Datei in den Excel Buffer:
if not UploadIntoStream('Excel waehlen', '', '', FileName, InS) then
    Error('Keine Datei gewaehlt');
SheetName := TempExcelBuffer.SelectSheetsNameStream(InS); // fragt bei mehreren Sheets selbst nach
TempExcelBuffer.OpenBookStream(InS, SheetName);
TempExcelBuffer.ReadSheet(); // danach Buffer per Zeile/Spalte auslesen
```

**Fallstricke:** Jede UI-Prozedur prueft GuiAllowed und tut sonst NICHTS — dadurch laeuft derselbe Code unveraendert in Job Queue/Web-Service. Der GuiAllowed-Check ist per InternalEvent uebersteuerbar (fuer Tests mocken!). Excel-Helper erzwingt IsTemporary auf dem Buffer, sonst Error — schuetzt vor versehentlichem Schreiben in die echte Excel-Buffer-Tabelle. Bonus im Repo: .RuleSets mit AppSourceCop/PTE-Ruleset-Beispielen.

---

## ReleaseManagement

**Technik:** Geschaeftsregeln beim Freigeben von Belegen erzwingen: EventSubscriber auf OnBeforeReleaseSalesDoc der Codeunit "Release Sales Document" — ein error() darin blockiert die Freigabe komplett.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** app.json application 19.0, runtime 8.0

```al
codeunit 50144 "Sale Release Guard"
{
    [EventSubscriber(ObjectType::Codeunit, Codeunit::"Release Sales Document", 'OnBeforeReleaseSalesDoc', '', true, true)]
    local procedure BlockEarlyDelivery(var IsHandled: Boolean; var SalesHeader: Record "Sales Header"; PreviewMode: Boolean)
    begin
        if SalesHeader."Requested Delivery Date" < CalcDate('<14D>', Today()) then
            Error('Lieferung fruehestens in 14 Tagen moeglich.');
    end;
}
```

**Fallstricke:** Zwei Fallen im Original: (1) Ein leeres "Requested Delivery Date" (0D) ist ebenfalls kleiner als der Stichtag — Belege OHNE Datum waeren dauerhaft unfreigebbar; explizit auf 0D pruefen. (2) IsHandled := true wuerde die STANDARD-Freigabelogik ersetzen, nicht blockieren — zum Blockieren nur error() werfen, IsHandled nicht anfassen.

---

## PageScriptingHelper

**Technik:** Page-Scripting-Testskripte (YAML fuer BCs Record/Replay-Testtool ab BC 24) automatisch aus vorhandenen DATEN generieren: Page Metadata + "Page Control Field" liefern die Steuerelemente, RecordRef/FieldRef die Werte, TextBuilder baut die Steps, Temp Blob + DownloadFromStream liefert die .yml aus.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** app.json application 24.0, runtime 13.0 — Page Scripting existiert ab BC 24

```al
procedure GenerateScript(PageNo: Integer; RecVariant: Variant)
var
    MetaData: Record "Page Metadata";
    PageFields: Record "Page Control Field";
    Ref: RecordRef; FR: FieldRef;
    Script: TextBuilder; Blob: Codeunit "Temp Blob";
    InS: InStream; OutS: OutStream; FileName: Text;
begin
    MetaData.Get(PageNo);
    if MetaData.SourceTable = 0 then
        Error('Seite hat keine SourceTable');
    Ref.GetTable(RecVariant);
    if Ref.FindSet() then
        repeat
            // YAML: '- type: invoke ... action: Control_New' je Datensatz
            PageFields.SetRange(PageNo, MetaData.ID);
            if PageFields.FindSet() then
                repeat
                    FR := Ref.Field(PageFields.FieldNo);
                    // YAML: type: focus + type: input auf PageFields.ControlName
                    Script.AppendLine('    value: ' + Format(FR.Value, 0, 9));
                until PageFields.Next() = 0;
        until Ref.Next() = 0;
    Blob.CreateOutStream(OutS);
    OutS.WriteText(Script.ToText());
    Blob.CreateInStream(InS);
    FileName := 'script.yml';
    DownloadFromStream(InS, '', '', '', FileName);
end;
```

**Fallstricke:** Eriks eigener Kommentar im Code: PageFields.SetRange(Editable,'true') ist ein "MAJOR PROBLEM" — Editable/Visible in "Page Control Field" sind AL-AUSDRUECKE als Text, nicht die Literale 'true'/'false'; danach filtern geht schief. Primaerschluesselfelder muessen im Skript VOR den uebrigen Feldern befuellt werden (der Code macht zwei getrennte Durchlaeufe). Format(Value,0,9) fuer roundtrip-sichere Werte. Der Repeater-Name ist hart 'Control1' — echte Aufloesung fehlt.

---

## CoPilotInBC

**Technik:** BCs eingebauten Entity-Text-Copilot (Marketingtext-Generator) auf eigene Seiten/Tabellen setzen: Factbox "Entity Text Factbox Part" andocken + SetContext, dann per OnRequestEntityContext-Subscriber ein Facts-Dictionary, Ton und Format liefern — das Prompting uebernimmt der Standard.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json application 22.0, runtime 11.0 — API der fruehen Copilot-Welle, vor dem AOAI-Toolkit

```al
// 1) Factbox an die Seite haengen:
part(EntityTextFactBox; "Entity Text Factbox Part") { Caption = 'Marketing Text'; }
trigger OnAfterGetCurrRecord()
begin
    CurrPage.EntityTextFactBox.Page.SetContext(Database::Customer, Rec.SystemId,
        Enum::"Entity Text Scenario"::"Marketing Text", PlaceholderTxt);
end;

// 2) Fakten zuliefern:
[EventSubscriber(ObjectType::Codeunit, Codeunit::"Entity Text", OnRequestEntityContext, '', true, true)]
local procedure Supply(SourceScenario: Enum "Entity Text Scenario"; SourceSystemId: Guid;
    SourceTableId: Integer; var Facts: Dictionary of [Text, Text]; var Handled: Boolean;
    var TextFormat: Enum "Entity Text Format"; var TextTone: Enum "Entity Text Tone")
var
    Customer: Record Customer;
begin
    if SourceTableId <> Database::Customer then
        exit;
    Customer.GetBySystemId(SourceSystemId);
    Facts.Add('Customer Name', Customer.Name);
    Customer.CalcFields(Balance);
    Facts.Add('Current balance', Format(Customer.Balance));
    TextFormat := TextFormat::Paragraph;
    TextTone := TextTone::Inspiring;
    Handled := true;
end;
```

**Fallstricke:** Der Placeholder-Label braucht die [Create draft]()-Markdown-Syntax — der Klammerteil wird zum klickbaren Generieren-Link. Handled := true nicht vergessen, sonst faellt der Standard auf sein eigenes Kontextsammeln zurueck. Facts sind reine Key-Value-Texte — was rein soll (CalcFields!), muss man selbst berechnen.

---

## AIPlayground

**Technik:** Generischer LLM-Client in purem AL fuer Azure OpenAI, OpenAI und LM Studio hinter einem Enum: Provider-abhaengige Auth-Header, Chat-Completions-Payload aus JsonObject/JsonArray, TryFunction-Kapselung, JSON-Mode. Die Referenz, wenn ein LLM ohne Microsofts Copilot-Toolkit angebunden werden soll.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json application 26.0, runtime 15.0

```al
// Auth unterscheidet sich je Provider:
case CurrentProvider of
    CurrentProvider::AzureOpenAI:
        Headers.Add('api-key', _Key);
    CurrentProvider::ChatGPTOpenAI:
        Headers.Add('Authorization', 'bearer ' + _Key); // + 'model' im Payload!
end;
Client.Timeout(300000); // LLMs brauchen Zeit — Default-Timeout reicht nicht

if Client.Send(Request, Response) then begin
    if Response.IsBlockedByEnvironment() then
        Error('"Allow HttpClient Requests" ist fuer diese Extension abgeschaltet');
    Response.Content().ReadAs(ResponseTxt);
    if Response.IsSuccessStatusCode() then begin
        ResponseJson.ReadFrom(ResponseTxt);
        // Antwort: choices[0].message.content
    end;
end;

// JSON-Antworten robust parsen — Modelle wickeln JSON gern in ```json-Faences:
if Result.Contains('```json') then begin
    parts := Result.Split('```');
    JsonToken.ReadFrom(parts.Get(2).Substring(5));
end else
    JsonToken.ReadFrom(Result);
```

**Fallstricke:** Response.IsBlockedByEnvironment abfragen — sonst raetselt man, warum der Call in der Sandbox scheitert (Extension-HTTP-Schalter). response_format json_object kennt nur der Azure-Zweig; beim OpenAI-Zweig muss das model-Feld in den Payload (Default gpt-4o-mini). Payload via Temp Blob mit TextEncoding::UTF8 in den Content schreiben, sonst leiden Umlaute. System-/User-Messages sind Arrays von {type:'text',text:...}-Objekten, nicht nackte Strings.

---

## Reuse old CAL code

**Technik:** Alter CAL-Code laeuft fast unveraendert in AL weiter (Grossschreibung, IF-THEN-Stil, Arrays) — hier ein kompletter Code39-Barcode-Generator, der ein 24-bit-BMP byteweise per OutStream.WRITE in ein Blob-Feld schreibt, ganz ohne externe Bibliothek.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
// Kern: Bild byteweise in ein Blob-Feld rendern
table 50300 "Test Table BarCode"
{
    fields
    {
        field(1; BarCode; Code[20]) { }
        field(2; "BarCode Picture"; Blob) { Subtype = Bitmap; }
    }
}

// Aufrufer (Page-Action):
Rec.CalcFields("BarCode Picture");
Rec."BarCode Picture".CreateOutStream(OutS);
Barcode39.SetDPI(48, 9600, 900);
Barcode39.AddQuiet(true);
Barcode39.MkBarcode(Rec.BarCode, OutS, true);
Rec.Modify();

// Im Generator: BMP-Header + Pixel direkt schreiben
// OStrm.WRITE('B',1); OStrm.WRITE('M',1); OStrm.WRITE(54 + Rows*Cols*3, 4); ...
// je Pixel 3x OStrm.WRITE(CH,1) (BGR), Zeilen auf 4-Byte-Grenzen auffuellen
```

**Fallstricke:** BMP-Zeilen muessen auf Vielfache von 4 Bytes gepolstert werden (der Code rundet mit ROUND(J,4,'>')) — klassischer Stolperstein bei Handarbeit am Format. Blob braucht CalcFields vor CreateOutStream. Heute bringen BC-Standardmodule Barcode-Schriftarten mit; das Bitmap-Selbstbauen lohnt nur noch, wenn ein echtes Bild gebraucht wird (API, E-Mail, PDF-Einbettung).

---

## EnvironmentInfo

**Technik:** Zur Laufzeit erkennen, WO der Code laeuft (SaaS/OnPrem, Produktion/Sandbox) und WER der Tenant ist — fuer Feature-Gates, Telemetrie-Anreicherung und Schutz vor Testaktionen in Produktion.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json application 22.0, runtime 11.0

```al
procedure WhereAmI()
var
    EnvInfo: Codeunit "Environment Information";
    TenantInfo: Codeunit "Tenant Information";
    AadTenant: Codeunit "Azure AD Tenant";
begin
    if EnvInfo.IsSandbox() then
        ;// Test-Features nur hier freischalten
    if EnvInfo.IsOnPrem() then
        ;// Docker/OnPrem-Sonderweg
    // weitere Schalter: IsSaaS(), IsProduction(), IsSaaSInfrastructure(), IsFinancials()
    Message('%1 / %2', TenantInfo.GetTenantDisplayName(), TenantInfo.GetTenantId());
    Message('%1 / %2', AadTenant.GetAadTenantDomainName(), AadTenant.GetAadTenantId());
end;
```

**Fallstricke:** Drei verschiedene System-Codeunits fuer drei Fragen: "Environment Information" (Umgebungsart), "Tenant Information" (BC-Tenant), "Azure AD Tenant" (AAD-Domaene/-ID) — die Tenant-ID und die AAD-Tenant-ID sind NICHT dasselbe.

---

## repos

**Technik:** Azure Function (HTTP-Trigger, C#) als Fluchtluke fuer alles, was AL nicht kann — AL ruft sie als simplen HTTPS-POST mit JSON-Body auf; der Function-Key steckt bei AuthorizationLevel.Function als ?code= in der URL.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
procedure CallAzureFunction(Name: Text) Result: Text
var
    Client: HttpClient;
    Content: HttpContent;
    Response: HttpResponseMessage;
    Headers: HttpHeaders;
    Body: JsonObject;
begin
    Body.Add('name', Name);
    Content.WriteFrom(Format(Body));
    Content.GetHeaders(Headers);
    Headers.Remove('Content-Type');
    Headers.Add('Content-Type', 'application/json');
    // AuthorizationLevel.Function: Key als Query-Parameter ?code=...
    Client.Post('https://myapp.azurewebsites.net/api/Function1?code=' + FunctionKey, Content, Response);
    Response.Content().ReadAs(Result);
end;
```

**Fallstricke:** Die C#-Seite (Function1.cs) liest den Parameter wahlweise aus Query-String ODER JSON-Body (name ?? data?.name) — robustes Muster fuer Functions, die aus AL und Browser gleichermassen aufrufbar sein sollen. Im Ordner liegt nur die C#-Seite; die AL-Seite ist der Standard-HttpClient-Aufruf.

---

## Nuget

**Technik:** Gegen AppSource-Apps (Continia, Avalara, WooCommerce ...) entwickeln, ohne .app-Symboldateien zu jagen: Abhaengigkeit einfach in app.json eintragen, die AL-Extension zieht die Symbole automatisch aus Microsofts NuGet-Feeds (MSSymbols/AppSourceSymbols).

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json application 25.0, runtime 14.0 — NuGet-Symbolfeeds ab BC 24/25 nutzbar

```al
// app.json — mehr braucht es nicht, Symbole kommen per NuGet-Feed:
// "dependencies": [
//   { "id": "5fedf952-2450-4bce-b578-f3b7c13cd9a9", "name": "Avalara AvaTax",
//     "publisher": "Avalara", "version": "16.0.7.2" },
//   { "id": "8d4eab29-8c7f-4b6c-be9a-b7fdfb9da196", "name": "Continia Expense Management",
//     "publisher": "Continia Software", "version": "12.2.0.333892" }
// ]

// danach sind Fremd-Objekte direkt referenzierbar:
var
    AVADetailPosted: Record "AVA Detail Posted";
    WooSetup: Record "Woo Webstore Connector Setup";
```

**Fallstricke:** Die id/publisher/version-Tripel muessen exakt stimmen (aus AppSource bzw. vom Hersteller); die Feed-Aufloesung braucht die neuere AL-Extension und Internetzugang beim Symbol-Download. Fuer Nicht-AppSource-Apps (PTEs) funktioniert der Feed-Weg nicht — da bleibt manuelles Symbol-Publishing.

---

## whatnewin2021w2

**Technik:** Sammelbare Fehler: [ErrorBehavior(ErrorBehavior::Collect)] + ErrorInfo laesst eine Validierung ALLE Probleme einsammeln statt beim ersten abzubrechen — ideal fuer Zeilen-Validierung ganzer Belege.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** Features ab BC 19 (2021 Wave 2)

```al
[ErrorBehavior(ErrorBehavior::Collect)]
procedure ValidateAllLines(var Line: Record "My Line")
var
    Err: ErrorInfo;
begin
    if Line.FindSet() then
        repeat
            if Line.Quantity <= 0 then begin
                Err := ErrorInfo.Create(StrSubstNo('Zeile %1: Menge fehlt', Line."Line No."), true); // true = collectible
                Error(Err); // wird GESAMMELT, Ausfuehrung laeuft weiter
            end;
        until Line.Next() = 0;
    // Aufrufer prueft: if HasCollectedErrors() then GetCollectedErrors(true) durchgehen
end;
```

**Fallstricke:** Nur als collectible markierte ErrorInfo-Fehler werden gesammelt — ein nacktes Error('...') im selben Scope bricht weiterhin sofort ab. Der Demo-Code im Ordner ist nur ein unfertiges Fragment (haengendes err.), zeigt aber auch HttpHeaders.Keys als damals neue API.

---

## Whats New in v17 Dev

**Technik:** Drei BC17-Perf-/Robustheitsfeatures in einem Demo: TableType=Temporary (Tabelle wird nie in SQL angelegt), SetLoadFields/Partial Records (nur benoetigte Spalten laden) und [CommitBehavior] (Commit in fremdem Code neutralisieren).

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** BC 17-Featureset (Partial Records, TableType=Temporary, CommitBehavior)

```al
table 50129 "Very Temporary Table"
{
    TableType = Temporary; // existiert nie in SQL — sichere Buffer-Tabelle
    fields { field(1; Primary; Code[10]) { } }
    keys { key(PK; Primary) { Clustered = true; } }
}

codeunit 50121 "Test Stuff in v17"
{
    [CommitBehavior(CommitBehavior::Ignore)] // Commit() im Aufrufbaum wird ignoriert (::Error wuerde werfen)
    procedure ProcessSafely()
    var
        GL: Record "G/L Entry";
    begin
        GL.SetLoadFields("My ID"); // Partial Records: SQL laedt nur PK + diese Spalte
        if GL.FindSet() then
            repeat
            until GL.Next() = 0;
    end;
}
```

**Fallstricke:** SetLoadFields muss VOR FindSet stehen; Zugriff auf ein nicht geladenes Feld loest einen stillen Nachlade-Roundtrip (JIT-Load) aus und frisst den Gewinn wieder auf. TableType=Temporary schuetzt davor, dass jemand die Buffer-Tabelle versehentlich persistent verwendet — besser als die Konvention "nur temporary instanziieren".

---

## telemetry

**Technik:** Application-Insights-Telemetrie nicht nur schreiben, sondern aus AL heraus LESEN: REST-POST mit KQL-Query gegen api.applicationinsights.io, Ergebnis als tables[0].rows-Array parsen. Braucht man fuer In-App-Dashboards ueber die eigene Extension-Nutzung.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json application 21.0, runtime 10.0

```al
procedure QueryAppInsights(AppId: Text; ApiKey: Text; Kql: Text): JsonArray
var
    Client: HttpClient; Request: HttpRequestMessage; Response: HttpResponseMessage;
    Headers: HttpHeaders; Content: HttpContent; Body: JsonObject; Json: JsonObject; T: JsonToken; Txt: Text;
begin
    Request.Method := 'POST';
    Request.SetRequestUri('https://api.applicationinsights.io/v1/apps/' + AppId + '/query');
    Request.GetHeaders(Headers);
    Headers.Add('x-api-key', ApiKey);
    Body.Add('query', Kql); // z.B. 'traces | where timestamp > ago(1d) | project customDimensions.eventId, message'
    Content.WriteFrom(Format(Body));
    Content.GetHeaders(Headers);
    Headers.Remove('Content-Type');
    Headers.Add('Content-Type', 'application/json');
    Request.Content(Content);
    if not Client.Send(Request, Response) then
        Error('HTTP-Fehler');
    Response.Content().ReadAs(Txt);
    Json.ReadFrom(Txt);
    Json.Get('tables', T); T.AsArray().Get(0, T);
    T.AsObject().Get('rows', T);
    exit(T.AsArray()); // rows = Array von Zeilen-Arrays, Spaltenreihenfolge wie im KQL-project
end;
```

**Fallstricke:** Der Demo-Code hat den API-Key hart im Quelltext eines OEFFENTLICHEN Repos (mit Kommentarzeile daneben!) — Anti-Pattern, gehoert in Isolated Storage/Setup. Content-Type muss per Remove+Add gesetzt werden, sonst haengt 'text/plain; charset=utf-8' dran. BC-eigene Events landen in customDimensions, nicht in Top-Level-Spalten.

---

## AppDissect

**Technik:** Anatomie einer .app-Datei: ZIP-Container mit 40-Byte-Praefix; nach dem Entpacken liegen NavxManifest.xml, SymbolReference.json und — bei offener resourceExposurePolicy — der komplette AL-Quellcode samt ControlAddIn-JavaScript lesbar da. Wichtig fuer beide Richtungen: fremde Apps analysieren und die eigene schuetzen.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** Beispiel-App: Platform/Application 17.0, runtime 6.0 (Vor-resourceExposurePolicy-Aera mit ShowMyCode=True)

```al
// Kein AL noetig — Handgriff + Schutzschalter:
// 1. .app kopieren, die ersten 40 Bytes abschneiden, als .zip entpacken
// 2. Inhalt: NavxManifest.xml (alle Metadaten), SymbolReference.json,
//    src/**/*.al (Klartext-Quellcode!), addin/... (JS der ControlAddIns)
//
// Eigene App dichtmachen (app.json):
// "resourceExposurePolicy": {
//     "allowDebugging": false,
//     "allowDownloadingSource": false,
//     "includeSourceInSymbolFile": false
// }
```

**Fallstricke:** Die Default-Templates setzen alle drei Schalter auf true — wer ein kommerzielles Produkt so ausliefert, verschenkt den Quellcode. Die Dateinamen im Paket sind URL-encodiert (Leerzeichen als %2520 = doppelt encodiert). Aeltere Apps steuern das ueber showMyCode statt resourceExposurePolicy.

---

## ALBuild

**Technik:** Eine komplette BC-CI-Pipeline als deklarative Task-Liste (Eriks ALBuild.exe-Tool): die AUFGABENREIHENFOLGE ist das Lehrstueck — Version bumpen, Symbole aus dem Docker-Container ziehen, kompilieren, XLF maschinell uebersetzen, NOCHMAL kompilieren, Release kopieren, git commit+push.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** Ziel-Container BC 20 (URL http://bc20:7049/BC/)

```al
// pos.json (gekuerzt) — die Reihenfolge ist der Punkt:
// 1. DeployBasicDocker   (Testrunner in den Container, SchemaUpdateMode forcesync)
// 2. Git pull
// 3. UpdateVersion       (Build-Teil +1, Datum in Versionsteil 3 codiert)
// 4. DownloadSymbolsDocker (VOR dem Compile — gegen den Ziel-Container)
// 5. Compile             (erzeugt u.a. die .g.xlf)
// 6. Translate           (XLF maschinell fuellen)
// 7. Compile             (NOCHMAL — packt die Uebersetzungen mit ins .app)
// 8. Copy .app nach Release\
// 9. Git add / commit -m "ALBuild Version %VERSION%" / push
```

**Fallstricke:** Translate braucht einen Compile davor (erst dann existiert die .g.xlf) und einen danach (erst dann landen die Sprachdateien im Paket) — wer nur einmal kompiliert, liefert unuebersetzte Apps aus. Datum im Versionsteil macht jede Build-Nummer rueckverfolgbar. Das Tool selbst ist proprietaer; die Schrittfolge ist 1:1 auf eigene Skripte uebertragbar.

---

## UsingTheDesigner

**Technik:** Der In-Client-Designer (Drag&Drop im Web-Client) erzeugt eine echte pageextension, die man sich in VS Code herunterladen und ins eigene Projekt uebernehmen kann — schnellstes Scaffolding fuer Layout-Umbauten samt moveafter/modify-Syntax.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)

```al
pageextension 50100 ChangesToCustomerCard extends "Customer Card"
{
    layout
    {
        moveafter("IC Partner Code"; "Balance Due (LCY)");
        modify("Address 2") { Visible = false; }
        addafter("IC Partner Code")
        {
            field("Name 260182"; Rec."Name 2") { ApplicationArea = All; }
        }
        modify("Shipping Advice") { Visible = false; }
    }
    actions
    {
        modify("Prices and Discounts Overview")
        {
            Promoted = true;
            PromotedCategory = Category5;
            PromotedOnly = true;
        }
    }
}
```

**Fallstricke:** Der Designer generiert Zufalls-Suffixe an Feldnamen ("Name 260182", "Territory Code81265") — vor der Uebernahme ins Repo umbenennen, sonst leben die haesslichen Namen ewig. Designer-Aenderungen liegen bis zum Export als eigene Extension pro Profil im System und koennen mit Repo-Staenden kollidieren.

---

## ChatGPT

**Technik:** Fallstudie: von ChatGPT generierte AL-Objekte (Tabelle + Card + List + Action) kompilieren sauber und sehen idiomatisch aus — enthalten aber subtile Fehler, die nur ein Fachkundiger sieht. Lehrt, WO man LLM-generierten AL-Code pruefen muss.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)

```al
// ChatGPT-generiert — kompiliert, aber:
page 50101 "Customers List"
{
    PageType = List;
    SourceTable = Customers; // Eigentabelle "Customers" statt Standard-Customer angelegt
    CardPageId = 50100;      // numerische ID statt Seitenname — bricht still bei ID-Verschiebung
}

pageextension 50101 "Customers List Action" extends "Customer List"
{
    actions
    {
        addlast(Processing)
        {
            action("View Card")
            {
                trigger OnAction()
                begin
                    Page.RunModal(Page::"Customers List"); // heisst "View Card", oeffnet die LISTE
                end;
            }
        }
    }
}
```

**Fallstricke:** Typische LLM-Fehlerklassen sichtbar: semantische Verwechslung (Action-Name vs. Ziel), Parallelbau von Standardobjekten (eigene Customers-Tabelle neben Customer), IDs statt Namen, DataClassification pauschal ToBeClassified. Alles kompiliert — Review muss auf Semantik zielen, nicht auf Syntax.

---

## WhatsNewInBC26

**Technik:** BC26-Sprachzucker und der eingebaute Browser: ToText()-Instanzmethoden auf Decimal/DateTime statt Format(), this-Qualifizierer, und PageType=UserControlHost mit dem mitgelieferten WebPageViewer-Usercontrol — Webseite einbetten ohne eigenes ControlAddIn.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** Ordner zu BC 26 (application 26.0)

```al
trigger OnOpenPage()
var
    d: Decimal;
    dt: DateTime;
begin
    d := 123.456;
    dt := CurrentDateTime();
    Message('%1 / %2', d.ToText(), dt.ToText(true)); // Instanzmethoden statt Format()
end;

page 50100 EmbeddedWeb
{
    PageType = UserControlHost; // Seite besteht NUR aus dem Usercontrol
    layout
    {
        area(Content)
        {
            usercontrol(web; WebPageViewer) // Standard-Addin, kein eigenes JS noetig
            {
                trigger ControlAddInReady(CallbackUrl: Text)
                begin
                    this.CurrPage.web.Navigate('https://www.example.com');
                end;
            }
        }
    }
}
```

**Fallstricke:** Navigate erst im ControlAddInReady-Trigger aufrufen — vorher existiert das iframe nicht. UserControlHost verzichtet auf alle normalen Page-Chrome-Elemente; fuer eingebettete Dashboards/Dokuseiten gedacht.

---

## Altpgen

**Technik:** Dataverse/CDS-Proxytabellen in AL: TableType=CDS mit ExternalName/ExternalType je Feld mappt eine Dataverse-Entitaet (inkl. eigener Spalten wie new_youtube) — eine normale List-Page darauf liest live aus Dataverse. Die Dateien sind von Eriks Generator-Tool altpgen aus den CDS-Metadaten erzeugt.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** app.json application/platform 17.0, runtime 6.0

```al
table 50102 "CDS Account"
{
    ExternalName = 'account';
    TableType = CDS;
    fields
    {
        field(1; AccountId; GUID)
        {
            ExternalName = 'accountid';
            ExternalType = 'Uniqueidentifier';
            ExternalAccess = Insert; // nur beim Insert schreibbar
        }
        field(7; CustomerTypeCode; Option)
        {
            ExternalName = 'customertypecode';
            ExternalType = 'Picklist';
            OptionMembers = " ",Competitor,Consultant,Customer,Investor,Partner;
            OptionOrdinalValues = -1, 1, 2, 3, 4, 5; // Dataverse-Werte != AL-Ordinale!
        }
    }
}
// List-Page mit SourceTable="CDS Account" zeigt Live-Dataverse-Daten
// (CRM-Integration muss eingerichtet sein)
```

**Fallstricke:** OptionOrdinalValues mappt die Dataverse-Picklist-Zahlen auf AL-Options — von Hand fehleranfaellig, deshalb generieren lassen. Hunderte Felder je Entitaet: nur die benoetigten in die Proxytabelle uebernehmen. ExternalAccess steuert Schreibbarkeit je Feld.

---

## Übersprungen (bewusst)

- Getting Started (Hello-World-Geruest)
- LaunchJson (keine launch.json committed)
- cloudsandboxfor6bucks (Azure-VM-Thema, kein Code)
- vscodium (Editor-Thema, Hello World)
- sandboxcleanup (unfertiges Math-Fragment)
- snapshot2 (nur Lastcode fuers Snapshot-Debugging)
- codeunitstillinbaseapp (Hello World + using)
- WhatsNewinBC25 (leerer Trigger)
- WhatsNewInALBC22 (nur foreach-ueber-Text-Schnipsel)
- AL Code Actions (IDE-Refactoring-Wegwerfcode)
- AZ AL Tools Demo (Demo-Tabelle ohne Mechanismus)
- Agents (unfertiger Stub)
- BCURL (UWP-WebView-Testapp mit Build-Muell)

