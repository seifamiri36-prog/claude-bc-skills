# Reports, Belege, PDF & E-Mail

_Destilliert aus Erik Hougaards Youtube-Video-Sources (Ordnername = Videothema)._
_Vollquellen: https://github.com/hougaard/Youtube-Video-Sources (lokal klonen; Ordnername = Videothema)_

Der Cluster lehrt, dass BC-Reports keine starren Druckobjekte sind, sondern programmierbare Pipelines: Report.SaveAs in einen Stream ist das Universalscharnier, das denselben Report zu PDF-Anhang, HTML-Mailbody, Excel-Datei oder Base64-Web-Service-Antwort macht. Die ReportManagement-Events sind die zweite Achse: OnAfterSubstituteReport tauscht Standardbelege systemweit gegen eigene Kopien, OnAfterDocumentReady laesst AL das gerenderte Dokument komplett durch eigene Bytes ersetzen (beliebige PDFs ueber die BC-Druckstrecke), und ab BC 26 gibt OnPreRendering den Render-Payload als JsonObject frei. Drittens: Standard-Belegreports iterieren Puffer-Dataitems, an die ein reportextension nicht direkt herankommt — der List-of-Text-Sammeltrick mit Index-Synchronisation ist der dokumentierte Ausweg. Viertens zeigen Query-in-Report (Integer-Dataitem pumpt Query.Read) und der OmniReport (RecordRef + FilterPageBuilder) wie man Datenbeschaffung vom Report-Geruest entkoppelt.

**Wertvollste Ordner:** GenericReportService · ReportAsEmailBody · Customize standard reports · ReportExtentionInvoice · PrintPDF

## Themen (nach Praxis-Relevanz)

- ●●●  **GenericReportService** — Ein einziger Codeunit-Web-Service rendert JEDEN Report auf Abruf als PDF/Excel/XML und liefert ihn Base64-codiert zurueck — die generische Report-API fuer externe Systeme. Report.RunRequestPage(ReportNo) liefert das Parameter-XML, das man dem Aufruf mitgibt.
- ●●●  **ReportAsEmailBody** — Einen Beleg-Report als HTML rendern und direkt als E-Mail-BODY (nicht Anhang) verschicken: Report.SaveAs mit ReportFormat::Html in einen TempBlob, Text auslesen, EmailMsg.Create mit HTML-Flag true.
- ●●●  **Customize standard reports** — Standardreport systemweit durch eine eigene Kopie ersetzen, ohne eine einzige Aufrufstelle anzufassen: Report 1:1 mit eigener ID + eigenem RDLC-Layout kopieren und per ReportManagement::OnAfterSubstituteReport umleiten. Der klassische Weg fuer angepasste Belege (Rechnung, Mahnung).
- ●●●  **ReportExtentionInvoice** — Feld auf einem Standard-Belegreport ergaenzen, dessen Layout-Dataitem ein PUFFER ist (hier SalesInvLine in 'Sales Invoice NA'): Werte waehrend der echten Dataitems in eine List of [Text] einsammeln und im Puffer-Dataitem ueber dessen Number-Index wieder herausgeben. Drei gescheiterte Direktversuche sind im Code dokumentiert.
- ●●○  **reportclient** — Die .NET-Konsumentenseite des generischen Report-Web-Service: SOAP-Client mit Basic Auth ruft RunReport(ReportNo, ParameterXML) und decodiert das Base64-Ergebnis zur PDF-Datei — zeigt das exakte ReportParameters-XML-Format.
- ●●○  **QueryAsReport** — Eine Query wie einen Report auffindbar machen: UsageCategory = ReportsAndAnalysis bringt sie in 'Tell me', QueryCategory in Seitenlisten — dieselbe Query ist zugleich API-Query (Job -> Job Task -> Job Planning Line) mit RightOuterJoin und expliziten filter()-Elementen fuer Konsumenten.
- ●●○  **SendEmailToALCode** — AL-Code von aussen gezielt ausfuehren lassen (z. B. Power Automate nach E-Mail-Eingang): API-Page mit [ServiceEnabled]-Prozedur = gebundene OData-Aktion — POST auf .../calls(<SystemId>)/Microsoft.NAV.CallALCode fuehrt den AL-Code auf genau diesem Datensatz aus und kann ein Ergebnis zurueckschreiben.
- ●●○  **Obsolete Email** — Migrationsbild alte gegen neue E-Mail-API im selben File: neues Email-Modul (Email Message.Create + AddAttachment(Base64) + Email.Send) neben der obsoleten SMTP-Mail-Variante — inklusive des Musters, einen Report per Report.SaveAs als PDF in den Anhang-Stream zu rendern.
- ●●○  **HTML Email** — Report (Word-Layout) als HTML rendern und Platzhalter-Tokens im gerenderten HTML per String-Replace gegen echtes Markup tauschen — weil Word-Layouts kein **rohes HTML** durchreichen ⚠⚠ **BERICHTIGT 01.09.2026 (B): Hier stand „kein rohes HTML (Links!)“ — der Link-Teil ist WIDERLEGT.** MS *Using Hyperlinks in Word Layouts*: „In a Word report layout, you can set up hyperlinks on text and picture fields“ — über die Namenskonvention `<Name>_Url` / `<Name>_UrlText` an den Dataset-Spalten. **Links gehen also sehr wohl, nur nicht als HTML-Markup.** Für rohes HTML-Passthrough ist nichts dokumentiert; genau dafür behilft sich die Demo mit String-Replace nach dem Rendern. Dazu RecordRef+FieldRef.SetRange, um den Report auf den aktuellen Datensatz zu filtern.
- ●●○  **FancyReportRequestFieldsTheLazyWay** — Requestpage-Felder mit Lookup, Validierung und Captions GRATIS: statt Text-Variablen + eigenem OnLookup einfach Felder einer globalen Record-Variablen als field()-Quelle nehmen — Lookup = true erbt die TableRelation des Tabellenfelds.
- ●●○  **100 in 1 Reports** — Ein Report, viele Layouts: beim Start (OnInitReport) eine Layout-Auswahlseite zeigen und das gewaehlte Custom-Report-Layout per "Report Layout Selection".SetTempLayoutSelected nur fuer DIESEN Lauf aktivieren — z. B. ein Rechnungsreport mit Layout je Kundengruppe.
- ●●○  **ExcelReport** — Natives Excel-Layout als Report-Layouttyp (ab BC 20): DefaultLayout = Excel plus ExcelLayout-Arbeitsmappe; das Dataset (auch verschachtelte Dataitems per DataItemLink) landet als flache Tabelle im Daten-Blatt, Pivots/Formeln im Layout werten es aus.
- ●●○  **OmniReport** — EIN Report fuer beliebige Tabellen: Benutzer waehlt auf der Requestpage die Tabellennummer, filtert per FilterPageBuilder wie im Standard, und das Integer-Dataitem laeuft ueber einen RecordRef — Spalten via Ref.Field(n).Value.
- ●●○  **QueryInReport** — Eine Query (mit Joins/Aggregaten) als Datenquelle eines Reports nutzen: Integer-Dataitem als Pumpe, Q.Open in OnPreDataItem, Q.Read je OnAfterGetRecord, CurrReport.Break am Ende — Spalten referenzieren direkt Query-Felder.
- ●●○  **PrintPDF** — Ein beliebiges, fertiges PDF durch die BC-Druckinfrastruktur schicken (Cloud-Print, Druckerauswahl), ohne dass es je ein Report gerendert hat: Koeder-Report laedt das PDF hoch, ein SingleInstance-Codeunit haelt den Stream, und ReportManagement::OnAfterDocumentReady ersetzt das Rendering durch die eigenen Bytes.
- ●●○  **CombinePDFs** — Der neue OnPreRendering-Trigger (BC 25/26) gibt den Render-Payload als JsonObject frei, BEVOR das Layout rendert — der Einstiegspunkt, um Dokumente zu buendeln/anzureichern (PDF-Kombination) oder das Rendering zu inspizieren.
- ●○○  **OneClickTwoDownloads** — Zwei Dateidownloads aus EINER Benutzeraktion: Der Browser erlaubt pro Client-Interaktion nur einen Download — ein Mini-ControlAddIn, dessen JS sofort per InvokeExtensibilityMethod zurueckruft, erzeugt eine zweite Interaktion, in deren Trigger der zweite DownloadFromStream laeuft.
- ●○○  **Create your own headlines** — Eigene Rollencenter-Headline ohne Headline-Framework-Zeremonie: pageextension auf die Headline-Page, Textfeld vor Control1 einhaengen, Formatierung per <emphasize>-Tag, Klickziel via OnDrillDown+Hyperlink.

---

## GenericReportService

**Technik:** Ein einziger Codeunit-Web-Service rendert JEDEN Report auf Abruf als PDF/Excel/XML und liefert ihn Base64-codiert zurueck — die generische Report-API fuer externe Systeme. Report.RunRequestPage(ReportNo) liefert das Parameter-XML, das man dem Aufruf mitgibt.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** app.json: BC 18 / runtime 7.0 — funktioniert unveraendert bis BC 28

```al
codeunit 50144 "Report Web Service"
{
    procedure RunReport(ReportNo: Integer; Parameters: Text): Text
    var
        TempBlob: Codeunit "Temp Blob";
        Base64: Codeunit "Base64 Convert";
        OutS: OutStream;
        InS: InStream;
    begin
        TempBlob.CreateOutStream(OutS);
        Report.SaveAs(ReportNo, Parameters, ReportFormat::Pdf, OutS);
        TempBlob.CreateInStream(InS);
        exit(Base64.ToBase64(InS));
    end;
    // analog: ReportFormat::Excel, ReportFormat::Xml
}
// Parameter-XML eines Reports interaktiv abgreifen:
//   Message(Report.RunRequestPage(ReportNo));
// Publizieren: Tenant Web Service (ObjectType CodeUnit, ID 50144,
// ServiceName 'report') -> SOAP /WS/<Company>/Codeunit/report
```

**Fallstricke:** Das Parameters-XML muss exakt dem Format von Report.RunRequestPage entsprechen (inkl. DataItems-Views mit 'VERSION(1) SORTING(...)'); leerer Parameters-Text nimmt Defaults. Der Web Service wird im Repo per XML-Import (TenantWebService-Eintrag) publiziert, nicht per UI.

---

## ReportAsEmailBody

**Technik:** Einen Beleg-Report als HTML rendern und direkt als E-Mail-BODY (nicht Anhang) verschicken: Report.SaveAs mit ReportFormat::Html in einen TempBlob, Text auslesen, EmailMsg.Create mit HTML-Flag true.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** app.json: BC 23 / runtime 12.0 (namespace-Syntax); Email-Modul ab BC 17

```al
var
    Email: Codeunit Email;
    EmailMsg: Codeunit "Email Message";
    TempBlob: Codeunit "Temp Blob";
    InvHeader: Record "Sales Invoice Header";
    Ref: RecordRef;
    OutS: OutStream;
    InS: InStream;
    Body: Text;
begin
    InvHeader.SetRange("No.", '103001'); // auf EINEN Beleg filtern!
    Ref.GetTable(InvHeader);
    TempBlob.CreateOutStream(OutS);
    Report.SaveAs(Report::"Standard Sales - Invoice", '',
        ReportFormat::Html, OutS, Ref);
    TempBlob.CreateInStream(InS);
    InS.ReadText(Body);
    EmailMsg.Create('kunde@example.com',
        'Invoice from ' + CompanyName(), Body, true); // true = HTML-Body
    Email.Send(EmailMsg, "Email Scenario"::"Sales Invoice");
end;
```

**Fallstricke:** Ohne SetRange auf dem uebergebenen Record rendert der Report ALLE Belege in eine Mail. InStream.ReadText liest nur bis zum ersten Zeilenumbruch — traegt hier nur, weil das gerenderte HTML einzeilig ist; bei mehrzeiligem Inhalt in Schleife lesen. Email.Send mit Email Scenario waehlt das konfigurierte Absenderkonto.

---

## Customize standard reports

**Technik:** Standardreport systemweit durch eine eigene Kopie ersetzen, ohne eine einzige Aufrufstelle anzufassen: Report 1:1 mit eigener ID + eigenem RDLC-Layout kopieren und per ReportManagement::OnAfterSubstituteReport umleiten. Der klassische Weg fuer angepasste Belege (Rechnung, Mahnung).

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** runtime 5.0 (BC 16-Aera); der Event existiert unveraendert in BC 28 — heute ist reportextension oft die leichtere Alternative, Substitution bleibt fuer Layout-Totalumbauten

```al
// 1) Kopie des Standardreports mit eigener ID + eigenem Layout
report 54100 "Customer - Top 10 List (YT)"
{
    DefaultLayout = RDLC;
    RDLCLayout = './CustomerTop10List.yt.rdlc';
    // Dataset 1:1 vom Standard uebernommen, dann anpassen
}

// 2) Substitution — greift ueberall: Menue, Belegdruck, Report.Run
codeunit 54100 "Sub Reports YT"
{
    [EventSubscriber(ObjectType::Codeunit, Codeunit::ReportManagement,
        'OnAfterSubstituteReport', '', true, true)]
    local procedure SubstituteReport(ReportId: Integer; var NewReportId: Integer)
    begin
        if ReportId = Report::"Customer - Top 10 List" then
            NewReportId := Report::"Customer - Top 10 List (YT)";
    end;
}
```

**Fallstricke:** Mehrere Apps koennen denselben Report substituieren — nur setzen, wenn ReportId exakt passt, sonst ueberschreibt man fremde Umleitungen. Die Kopie muss das komplette Dataset des Originals mitbringen, damit vorhandene Kundenlayouts weiter funktionieren.

---

## ReportExtentionInvoice

**Technik:** Feld auf einem Standard-Belegreport ergaenzen, dessen Layout-Dataitem ein PUFFER ist (hier SalesInvLine in 'Sales Invoice NA'): Werte waehrend der echten Dataitems in eine List of [Text] einsammeln und im Puffer-Dataitem ueber dessen Number-Index wieder herausgeben. Drei gescheiterte Direktversuche sind im Code dokumentiert.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** app.json: BC 21 / runtime 10.0; 'Sales Invoice NA' ist die NA-Lokalisierung — dasselbe Puffer-Muster steckt aber auch in W1/AT-Belegreports

```al
reportextension 50100 "My Invoice" extends "Sales Invoice NA"
{
    dataset
    {
        modify("Sales Invoice Header")
        {
            trigger OnBeforeAfterGetRecord()
            begin
                Clear(D2List); // pro Beleg neu
            end;
        }
        modify("Sales Invoice Line")
        {
            trigger OnAfterAfterGetRecord()
            begin
                D2List.Add("Description 2"); // Wert einsammeln
            end;
        }
        modify("Sales Comment Line") // Kommentare erzeugen AUCH Pufferzeilen
        {
            trigger OnAfterAfterGetRecord()
            begin
                D2List.Add(''); // Index synchron halten!
            end;
        }
        modify(SalesInvLine) // das Puffer-Dataitem des Layouts
        {
            trigger OnAfterAfterGetRecord()
            begin
                Description2 := D2List.Get(Number);
            end;
        }
        add(SalesInvLine)
        {
            column(Description2; Description2) { }
        }
    }
    var
        Description2: Text;
        D2List: List of [Text];
}
```

**Fallstricke:** add() auf dem Puffer-Dataitem kann NICHT direkt auf Felder der Quelltabelle zeigen — weder "Sales Invoice Line"."Description 2" noch die Temp-Variable des Basisreports sind sichtbar (drei auskommentierte Fehlversuche im Original). JEDES Dataitem, das Pufferzeilen erzeugt (Kommentarzeilen!), muss einen Platzhalter in die Liste schieben, sonst verrutschen die Werte zeilenweise. Bonus im Original: rendering { layout(Excel) } als Reportextension, um das Dataset zum Debuggen nach Excel zu kippen.

---

## reportclient

**Technik:** Die .NET-Konsumentenseite des generischen Report-Web-Service: SOAP-Client mit Basic Auth ruft RunReport(ReportNo, ParameterXML) und decodiert das Base64-Ergebnis zur PDF-Datei — zeigt das exakte ReportParameters-XML-Format.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** .NET-5-Projekt gegen BC 18; Muster ist die Blaupause fuer ein .NET-Gateway, das BC-Belege rendert

```al
// C# (.NET, Connected Service auf den SOAP-Endpunkt):
var binding = new BasicHttpBinding();
binding.Security.Mode = BasicHttpSecurityMode.TransportCredentialOnly;
binding.Security.Transport.ClientCredentialType =
    HttpClientCredentialType.Basic;
binding.MaxReceivedMessageSize = 9999999; // Default 64KB ist zu klein!
var ep = new EndpointAddress(
    "http://bc:7047/BC/WS/CRONUS%20Canada%2C%20Inc./Codeunit/report");
var client = new report_PortClient(binding, ep);
client.ClientCredentials.UserName.UserName = "demo";
client.ClientCredentials.UserName.Password = "demo";

var result = await client.RunReportAsync(111,
  "<?xml version=\"1.0\" standalone=\"yes\"?>" +
  "<ReportParameters name=\"Customer - Top 10 List\" id=\"111\"><Options>" +
  "<Field name=\"NoOfRecordsToPrint\">3</Field></Options><DataItems>" +
  "<DataItem name=\"Customer\">VERSION(1) SORTING(Field1)</DataItem>" +
  "</DataItems></ReportParameters>");

File.WriteAllBytes("report111.pdf",
    Convert.FromBase64String(result.return_value));
```

**Fallstricke:** MaxReceivedMessageSize hochsetzen — ein Base64-PDF sprengt das SOAP-Default-Limit sofort. Der Company-Name im Endpunkt muss URL-encodiert sein. Das ReportParameters-XML holt man sich 1:1 aus Report.RunRequestPage im AL (siehe GenericReportService), nicht von Hand bauen.

---

## QueryAsReport

**Technik:** Eine Query wie einen Report auffindbar machen: UsageCategory = ReportsAndAnalysis bringt sie in 'Tell me', QueryCategory in Seitenlisten — dieselbe Query ist zugleich API-Query (Job -> Job Task -> Job Planning Line) mit RightOuterJoin und expliziten filter()-Elementen fuer Konsumenten.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: BC 23 / runtime 12.0; die Job/Job-Task/Planning-Hierarchie ist genau die Projekt-Baustellen-Struktur

```al
query 50100 JOBS
{
    QueryType = API;
    APIPublisher = 'hougaard';
    APIGroup = 'SOD';
    APIVersion = 'v2.0';
    EntityName = 'job';
    EntitySetName = 'jobs';
    UsageCategory = ReportsAndAnalysis; // Query erscheint in "Tell me"
    QueryCategory = 'test';
    elements
    {
        dataitem(job; Job)
        {
            filter(no__filter; "No.") { } // filterbar fuer API-Konsumenten
            column(description; Description) { }
            dataitem(task; "Job Task")
            {
                SqlJoinType = RightOuterJoin; // Kindzeilen fuehren den Join
                DataItemLink = "Job No." = job."No.";
                column(jobtaskno_; "Job Task No.") { }
                column(schedule_totalcost_; "Schedule (Total Cost)") { }
                dataitem(plan; "Job Planning Line")
                {
                    SqlJoinType = RightOuterJoin;
                    DataItemLink = "Job No." = task."Job No.",
                                   "Job Task No." = task."Job Task No.";
                    column(quantity; Quantity) { }
                }
            }
        }
    }
}
```

**Fallstricke:** Ohne explizite filter()-Elemente kann ein API-Konsument NICHT nach beliebigen Feldern filtern — was filterbar sein soll, muss deklariert werden. RightOuterJoin sorgt dafuer, dass die Zeilen der tiefsten Ebene fuehren (Planzeilen ohne vollstaendige Eltern erscheinen trotzdem).

---

## SendEmailToALCode

**Technik:** AL-Code von aussen gezielt ausfuehren lassen (z. B. Power Automate nach E-Mail-Eingang): API-Page mit [ServiceEnabled]-Prozedur = gebundene OData-Aktion — POST auf .../calls(<SystemId>)/Microsoft.NAV.CallALCode fuehrt den AL-Code auf genau diesem Datensatz aus und kann ein Ergebnis zurueckschreiben.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: BC 25 / runtime 14.0; [ServiceEnabled] gibt es seit BC 18

```al
page 50100 "Inbound API calls"
{
    PageType = API;
    APIPublisher = 'youtube';
    APIGroup = 'yt';
    APIVersion = 'v2.0';
    EntityName = 'call';
    EntitySetName = 'calls';
    SourceTable = "Inbound API Calls"; // eigene Tabelle, Id AutoIncrement
    DelayedInsert = true;
    ODataKeyFields = SystemId;

    layout { area(Content) { repeater(General) {
        field(id; Rec.SystemId) { }
        field(subject; Rec.Subject) { }
        field(returnValue; Rec."Return Value") { } } } }

    [ServiceEnabled] // gebundene Aktion:
    // POST .../api/youtube/yt/v2.0/companies(...)/calls(<SystemId>)
    //      /Microsoft.NAV.CallALCode
    procedure CallALCode(var ActionContext: WebServiceActionContext)
    begin
        Rec."Return Value" := 'Result of stuff happening!';
        Rec.Modify();
    end;
}
```

**Fallstricke:** Die Aktion ist an einen Datensatz GEBUNDEN — der Aufrufer muss erst per POST einen call-Datensatz anlegen (daher DelayedInsert + ODataKeyFields=SystemId) und dann die Aktion auf dessen SystemId feuern. Aktionsname im URL bekommt das Praefix Microsoft.NAV.

---

## Obsolete Email

**Technik:** Migrationsbild alte gegen neue E-Mail-API im selben File: neues Email-Modul (Email Message.Create + AddAttachment(Base64) + Email.Send) neben der obsoleten SMTP-Mail-Variante — inklusive des Musters, einen Report per Report.SaveAs als PDF in den Anhang-Stream zu rendern.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: BC 17 / runtime 6.0 — exakt der Versionsstand des API-Umbruchs; SMTP Mail in aktuellen Versionen entfernt

```al
// NEU (ab BC 17): System-Email-Modul
procedure NewSendMail()
var
    Msg: Codeunit "Email Message";
    Email: Codeunit Email;
    Base64: Codeunit "Base64 Convert";
    InS: InStream;
begin
    Msg.Create('to@example.com', 'Subject', 'Body');
    Msg.AddAttachment('doc.pdf', 'application/pdf', Base64.ToBase64(InS));
    Email.Send(Msg);
end;

// Report als PDF in einen Stream rendern (fuer den Anhang):
procedure SaveDocumentAsPDFToStream(var TempBlob: Codeunit "Temp Blob";
    ReportID: Integer): Boolean
var
    DocumentRef: RecordRef;
    OutS: OutStream;
begin
    DocumentRef.Open(Database::"Sales Invoice Header");
    TempBlob.CreateOutStream(OutS);
    exit(Report.SaveAs(ReportID, '', ReportFormat::Pdf, OutS, DocumentRef));
end;
```

**Fallstricke:** AddAttachment der neuen API nimmt Base64-TEXT, nicht den Stream selbst — daher der Umweg ueber Base64 Convert (es gibt auch eine Stream-Ueberladung in neueren Versionen). Die alte SMTP-Variante brauchte SMTPSetup.Get + TestField("User ID") als Vorflug-Pruefung.

---

## HTML Email

**Technik:** Report (Word-Layout) als HTML rendern und Platzhalter-Tokens im gerenderten HTML per String-Replace gegen echtes Markup tauschen — weil Word-Layouts kein **rohes HTML** durchreichen ⚠⚠ **BERICHTIGT 01.09.2026 (B): Hier stand „kein rohes HTML (Links!)“ — der Link-Teil ist WIDERLEGT.** MS *Using Hyperlinks in Word Layouts*: „In a Word report layout, you can set up hyperlinks on text and picture fields“ — über die Namenskonvention `<Name>_Url` / `<Name>_UrlText` an den Dataset-Spalten. **Links gehen also sehr wohl, nur nicht als HTML-Markup.** Für rohes HTML-Passthrough ist nichts dokumentiert; genau dafür behilft sich die Demo mit String-Replace nach dem Rendern. Dazu RecordRef+FieldRef.SetRange, um den Report auf den aktuellen Datensatz zu filtern.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 5.0; "SMTP Mail" ist seit BC 17 obsolet und spaeter entfernt — Versand auf das Email-Modul portieren

```al
var
    B: Codeunit "Temp Blob";
    Ref: RecordRef;
    FRef: FieldRef;
    OutS: OutStream;
    InS: InStream;
    Body: Text;
begin
    B.CreateOutStream(OutS);
    Ref.Open(Database::Customer);
    FRef := Ref.Field(1);
    FRef.SetRange(Rec."No."); // Report auf aktuellen Datensatz filtern
    Report.SaveAs(50147, '', ReportFormat::Html, OutS, Ref);
    B.CreateInStream(InS);
    InS.ReadText(Body);
    // Word-Layout kann kein rohes HTML -> Token ersetzen:
    Body := Body.Replace('%%%%HOMEPAGE%%%%',
        '<a href="https://' + Rec."Home Page" + '">Homepage</a>');
    // Body als HTML-Mail versenden (heute: Codeunit "Email Message" + Email)
end;
```

**Fallstricke:** Der Begleit-Report legt bewusst SAEMTLICHE Customer-Felder als Spalten an — Strategie: einmal alles ins Dataset, damit das Word-Layout frei waehlen kann. Das Original nutzt die obsolete Codeunit "SMTP Mail"; nur der Versand-Teil ist zu ersetzen, der Token-Trick bleibt gueltig. ReadText-Einzeilen-Falle wie bei ReportAsEmailBody.

---

## FancyReportRequestFieldsTheLazyWay

**Technik:** Requestpage-Felder mit Lookup, Validierung und Captions GRATIS: statt Text-Variablen + eigenem OnLookup einfach Felder einer globalen Record-Variablen als field()-Quelle nehmen — Lookup = true erbt die TableRelation des Tabellenfelds.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: BC 22 / runtime 11.0

```al
report 50100 Test
{
    ProcessingOnly = true;
    dataset { dataitem(Customer; Customer) {
        column(Balance_Customer; Balance) { } } }

    requestpage
    {
        layout { area(Content) {
            // Record-Variable als Feldquelle:
            field(x; I.Description)
            {
                ApplicationArea = All;
            }
            field(I; I."Sales Unit of Measure")
            {
                ApplicationArea = All;
                Lookup = true; // erbt die TableRelation des Item-Felds
            } } }

        trigger OnOpenPage()
        begin
            I.FindFirst(); // ohne Datensatz-Kontext bleibt die Var leer
        end;
    }
    var
        I: Record Item;
}
```

**Fallstricke:** Die Werte landen nur in der Record-Variablen (nichts wird gespeichert, kein Modify) — sie ist reines Transportmittel in den Report. Ohne FindFirst im OnOpenPage fehlt der Record-Kontext. SaveValues funktioniert mit Record-Feldern nicht wie mit einfachen Variablen.

---

## 100 in 1 Reports

**Technik:** Ein Report, viele Layouts: beim Start (OnInitReport) eine Layout-Auswahlseite zeigen und das gewaehlte Custom-Report-Layout per "Report Layout Selection".SetTempLayoutSelected nur fuer DIESEN Lauf aktivieren — z. B. ein Rechnungsreport mit Layout je Kundengruppe.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** runtime 5.0 (BC 16-Aera); ab BC 20 gibt es zusaetzlich rendering-Layouts mit eingebauter Auswahl, SetTempLayoutSelected existiert weiter

```al
report 50123 "Multi Report"
{
    dataset { dataitem(Customer; Customer) {
        column(No; "No.") { } /* ... alle Felder ... */ } }

    requestpage
    {
        layout { area(content) {
            field(LayoutCtl; Layout.Description)
            {
                Caption = 'Selected Layout';
                Editable = false;
            } } }
    }

    trigger OnInitReport()
    var
        RLS: Record "Report Layout Selection";
    begin
        Layout.SetRange("Report ID", 50123);
        if Page.RunModal(50123, Layout) = Action::LookupOK then
            RLS.SetTempLayoutSelected(Layout.Code) // nur dieser Lauf
        else
            Error('Please select a layout to continue!');
    end;

    var
        Layout: Record "Custom Report Layout";
}
```

**Fallstricke:** SetTempLayoutSelected wirkt nur temporaer fuer die Session/den Lauf — nichts wird persistiert. OnInitReport laeuft VOR der Requestpage, deshalb funktioniert der Auswahldialog dort. Basiert auf der Legacy-Tabelle "Custom Report Layout" (benutzerdefinierte RDLC/Word-Layouts).

---

## ExcelReport

**Technik:** Natives Excel-Layout als Report-Layouttyp (ab BC 20): DefaultLayout = Excel plus ExcelLayout-Arbeitsmappe; das Dataset (auch verschachtelte Dataitems per DataItemLink) landet als flache Tabelle im Daten-Blatt, Pivots/Formeln im Layout werten es aus.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: BC 20 / runtime 9.0 — die erste Version mit Excel-Layouts

```al
report 50100 "Test Excel"
{
    Caption = 'Testing Excel';
    DefaultLayout = Excel;
    ExcelLayout = 'SuperExcelLayout.xlsx'; // Mappe mit Pivots/Formeln
    dataset
    {
        dataitem(Customer; Customer)
        {
            column(No_Customer; "No.") { }
            column(Name_Customer; Name) { }
            column(SalesLCY_Customer; "Sales (LCY)") { }
            dataitem("Cust. Ledger Entry"; "Cust. Ledger Entry")
            {
                DataItemLink = "Customer No." = field("No.");
                column(PostingDate_CustLedgerEntry; "Posting Date") { }
                column(AmountLCY_CustLedgerEntry; "Amount (LCY)") { }
            }
        }
        dataitem(Vendor; Vendor)
        {
            column(No_Vendor; "No.") { }
            column(BalanceLCY_Vendor; "Balance (LCY)") { }
        }
    }
}
```

**Fallstricke:** Das Dataset wird zu EINEM flachen Datenblatt: Eltern-Spalten wiederholen sich je Kindzeile, und ein zweites Top-Level-Dataitem (Vendor) haengt seinen Zeilenblock mit leeren Customer-Spalten an — Pivots im Layout muessen danach filtern. Erster Lauf ohne Layout liefert die Rohdaten-Mappe, aus der man das Layout baut.

---

## OmniReport

**Technik:** EIN Report fuer beliebige Tabellen: Benutzer waehlt auf der Requestpage die Tabellennummer, filtert per FilterPageBuilder wie im Standard, und das Integer-Dataitem laeuft ueber einen RecordRef — Spalten via Ref.Field(n).Value.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: BC 26 / runtime 15.0; Technik laeuft ab weit aelteren Versionen

```al
report 57100 OmniReport
{
    dataset
    {
        dataitem(Records; Integer)
        {
            column(c1; Format(Ref.Field(1).Value)) { }
            column(c2; Format(Ref.Field(2).Value)) { }
            trigger OnPreDataItem()
            begin
                Records.SetRange(Number, 1, RecCount);
            end;
            trigger OnAfterGetRecord()
            begin
                if Records.Number = 1 then Ref.FindSet() else Ref.Next();
            end;
        }
    }
    requestpage
    {
        layout { area(Content) {
            field(TableNo; TableNo)
            {
                trigger OnValidate()
                begin
                    Ref.Open(TableNo);
                    RecCount := Ref.Count();
                end;
            }
            field(ViewString; ViewString)
            {
                trigger OnAssistEdit()
                var
                    Builder: FilterPageBuilder;
                    v: Variant;
                begin
                    v := Ref;
                    Builder.AddRecord(Ref.Name, v);
                    if ViewString <> '' then Builder.SetView(Ref.Name, ViewString);
                    if Builder.RunModal() then begin
                        ViewString := Builder.GetView(Ref.Name, true)
                            .Replace('VERSION(1) ', '');
                        Ref.SetView(ViewString);
                        RecCount := Ref.Count();
                    end;
                end;
            } } }
    }
    var
        Ref: RecordRef;
        RecCount: Integer;
        TableNo: Integer;
        ViewString: Text;
}
```

**Fallstricke:** Builder.GetView liefert einen 'VERSION(1) '-Praefix, der vor SetView entfernt werden muss (der .Replace im Original). Der RecordRef muss als GLOBALE Variable zwischen Requestpage und Dataset ueberleben. ⚠⚠ **BERICHTIGT 01.09.2026 (B): Hier stand „FilterPageBuilder braucht den Record als Variant“. DAS IST WIDERLEGT.** MS dokumentiert `AddRecord(Name: Text, Record: Record)` **und** `AddRecordRef(Name: Text, RecordRef: RecordRef)` — für einen RecordRef gibt es die eigene Methode, ein Variant ist **nicht nötig**. Der Variant-Umweg der Demo funktioniert, ist aber kein Muss.

---

## QueryInReport

**Technik:** Eine Query (mit Joins/Aggregaten) als Datenquelle eines Reports nutzen: Integer-Dataitem als Pumpe, Q.Open in OnPreDataItem, Q.Read je OnAfterGetRecord, CurrReport.Break am Ende — Spalten referenzieren direkt Query-Felder.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: BC 24 / runtime 13.0; Muster funktioniert seit es Queries gibt

```al
report 50100 "Query Report"
{
    DefaultLayout = Excel;
    ExcelLayout = 'queryreport.xlsx';
    dataset
    {
        dataitem(CLE; Integer) // Integer-Dataitem pumpt die Query
        {
            column(A1; Q.Amount) { }
            column(A2; Q.Customer_Name) { }
            column(A3; Q.Document_Date) { }

            trigger OnPreDataItem()
            begin
                Q.Open();
            end;

            trigger OnAfterGetRecord()
            begin
                if not Q.Read() then
                    CurrReport.Break();
            end;
        }
    }
    var
        Q: Query "Cust. Ledger Entries";
}
```

**Fallstricke:** Das Integer-Dataitem hat hier bewusst KEIN SetRange — CurrReport.Break() beim ersten fehlgeschlagenen Read ist die einzige Bremse; vergisst man es, laeuft der Report 2^31 Zeilen. Query-Filter setzt man vor Q.Open() per Q.SetRange/SetFilter.

---

## PrintPDF

**Technik:** Ein beliebiges, fertiges PDF durch die BC-Druckinfrastruktur schicken (Cloud-Print, Druckerauswahl), ohne dass es je ein Report gerendert hat: Koeder-Report laedt das PDF hoch, ein SingleInstance-Codeunit haelt den Stream, und ReportManagement::OnAfterDocumentReady ersetzt das Rendering durch die eigenen Bytes.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: BC 24 / runtime 13.0; fuer archivierte PDFs (Plaene, Lieferscheine) direkt uebertragbar

```al
codeunit 50100 "Print PDF"
{
    SingleInstance = true;
    var
        _InS: InStream;

    procedure PDFToPrint(var InS: InStream)
    begin
        _InS := InS;
    end;

    [EventSubscriber(ObjectType::Codeunit, Codeunit::ReportManagement,
        'OnAfterDocumentReady', '', true, true)]
    local procedure OnAfterDocumentReady(ObjectId: Integer;
        var TargetStream: OutStream; var Success: Boolean)
    begin
        if ObjectId = Report::"Print PDF" then begin
            CopyStream(TargetStream, _InS); // eigene Bytes statt Rendering
            Success := true; // "ich habe gerendert" an die Plattform
        end;
    end;
}

report 50100 "Print PDF" // Koeder: Layout/Dataset egal
{
    dataset { dataitem(Integer; Integer) {
        DataItemTableView = where(Number = const(17));
        column(Number; Number) { } } }
    trigger OnPreReport()
    var
        PrintPDF: Codeunit "Print PDF";
    begin
        if UploadIntoStream('', InS) then
            PrintPDF.PDFToPrint(InS);
    end;
    var
        InS: InStream;
}
```

**Fallstricke:** Success := true ist der Schalter — ohne ihn rendert die Plattform doch selbst. SingleInstance-Codeunit als Stream-Transport zwischen OnPreReport und dem Event ist Session-gebunden; bei parallelen Laeufen desselben Benutzers kollidiert es. Nur fuer die eigene Report-ID abfangen, sonst kapert man jeden Druck.

---

## CombinePDFs

**Technik:** Der neue OnPreRendering-Trigger (BC 25/26) gibt den Render-Payload als JsonObject frei, BEVOR das Layout rendert — der Einstiegspunkt, um Dokumente zu buendeln/anzureichern (PDF-Kombination) oder das Rendering zu inspizieren.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: BC 26 / runtime 15.0 — OnPreRendering ist ein BC-26-Feature

```al
report 50100 "Test PreRendering"
{
    WordLayout = 'test.docx';
    DefaultLayout = Word;
    dataset
    {
        dataitem(Customer; Customer)
        {
            column(Address_Customer; Address) { }
            column(Balance_Customer; Balance) { }
        }
    }
    trigger OnPreRendering(var RenderingPayload: JsonObject)
    begin
        // Payload ansehen — Struktur ist der Schluessel zum Kombinieren
        Message(Format(RenderingPayload));
    end;
}
```

**Fallstricke:** Das Demo inspiziert nur (Message) — ⚠⚠ **BERICHTIGT 01.09.2026 (B): Hier stand „die Payload-Struktur ist kaum dokumentiert“. DAS GILT NICHT MEHR.** MS *Attach files, append, and protect report PDFs in AL* führt eine **Report rendering payload schema definition** mit `version`, `saveformat`, `primaryDocument`, `attachments` (name/description/relationship/mimetype/filename), `additionalDocuments` und `protection` (user/admin). **Erst die Schema-Tabelle lesen, dann bauen** — Dumpen ist der Notweg, nicht der erste Griff. Trigger existiert erst ab runtime 15; aeltere Zielversionen kompilieren nicht.

---

## OneClickTwoDownloads

**Technik:** Zwei Dateidownloads aus EINER Benutzeraktion: Der Browser erlaubt pro Client-Interaktion nur einen Download — ein Mini-ControlAddIn, dessen JS sofort per InvokeExtensibilityMethod zurueckruft, erzeugt eine zweite Interaktion, in deren Trigger der zweite DownloadFromStream laeuft.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** app.json: BC 23 / runtime 12.0

```al
controladdin downloader
{
    Scripts = 'downloader.js';
    procedure download();
    event downloadtrigger();
}
// downloader.js:
// function download() {
//   Microsoft.Dynamics.NAV.InvokeExtensibilityMethod('downloadtrigger', []);
// }

pageextension 50200 download extends "Customer List"
{
    layout { addlast(content) {
        usercontrol(down; downloader)
        {
            trigger downloadtrigger()
            begin
                TmpBlob.CreateInStream(InS);
                DownloadFromStream(InS, '', '', '', 'data2.dat'); // #2
            end;
        } } }
    actions { addfirst(processing) {
        action(Download)
        {
            trigger OnAction()
            begin
                TmpBlob.CreateOutStream(OutS);
                OutS.WriteText('...');
                TmpBlob.CreateInStream(InS);
                CurrPage.down.download(); // JS-Roundtrip = 2. Interaktion
                Sleep(1000);              // sonst schluckt der Browser einen
                DownloadFromStream(InS, '', '', '', 'data1.dat'); // #1
            end;
        } } }
    var
        TmpBlob: Codeunit "Temp Blob";
        InS: InStream;
        OutS: OutStream;
}
```

**Fallstricke:** Das Sleep(1000) ist kein Schoenheitsfehler, sondern noetig — feuern beide Downloads zu dicht hintereinander, verwirft der Browser einen. Timing bleibt browserabhaengig fragil; fuer mehr als zwei Dateien lieber ein ZIP (Data Compression Codeunit) liefern.

---

## Create your own headlines

**Technik:** Eigene Rollencenter-Headline ohne Headline-Framework-Zeremonie: pageextension auf die Headline-Page, Textfeld vor Control1 einhaengen, Formatierung per <emphasize>-Tag, Klickziel via OnDrillDown+Hyperlink.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)

```al
pageextension 50500 "Our own headline"
    extends "Headline RC Business Manager"
{
    layout { addbefore(Control1) {
        field(HeadlineTxt; HeadlineTxt)
        {
            ApplicationArea = All;
            trigger OnDrillDown()
            begin
                Hyperlink('https://example.com');
            end;
        } } }

    trigger OnOpenPage()
    begin
        HeadlineTxt := 'Hello <emphasize>User!</emphasize>';
    end;

    var
        HeadlineTxt: Text;
}
```

**Fallstricke:** Die Pseudo-Tags (<emphasize>) rendert nur die Headline-Page, nirgends sonst. Position via addbefore(Control1) — die Control-Namen der Standard-Headline-Pages sind stabil, aber je Rollencenter verschieden.

---

## Übersprungen (bewusst)

- RawReportData (Inhalt themenfremd: HttpClient-POST-Demo)
- ReportExtensions (AL-Datei leer)
- ReportExtension (trivialer add-column-Zweizeiler)
- Emails (Duplikat von Obsolete Email)

