# HTTP, APIs & Cloud-Integration

_Destilliert aus Erik Hougaards Youtube-Video-Sources (Ordnername = Videothema)._
_Vollquellen: https://github.com/hougaard/Youtube-Video-Sources (lokal klonen; Ordnername = Videothema)_

Der Cluster lehrt die komplette Außenwelt-Anbindung von BC in beide Richtungen: ausgehend HttpClient mit sauberem Fehler-Layering (Verbindung / Statuscode / Parsen getrennt behandeln), JSON- und XML-Verarbeitung ohne Dateisystem (alles über Streams und Temp Blob, bis hin zu ZIP-Downloads), und eingehend API-Pages mit ihren Eigenheiten (DelayedInsert, Blob-Felder nur über Text-Variablen, Enums als Namen). Die stärksten Aha-Momente: die Report-Pipeline lässt sich per ReportManagement.OnAfterDocumentReady kapern, um beliebige PDFs durch BC zu drucken; Content-Length ist Byte-Länge (UTF-8), nicht strlen; und für Azure (Blob Storage, Functions) wie S2S-OAuth bringt der Standard fertige Module bzw. wohldefinierte Token-Endpunkte mit, die niemand von Hand nachbauen sollte. Für ein Bau-ERP-Projekt sind API-Pages (Bauleiter-App), Azure-Module (Sync-Gateway, Foto-Ablage), Geolocation (Rapporte) und die XML/XPath-Handgriffe (ÖNORM A2063) direkt verwertbar.

**Wertvollste Ordner:** S2S · APIsInBC24 · BlobAsTextInAPI · ExchangeRatesFromECB · UploadToSharePoint

## Themen (nach Praxis-Relevanz)

- ●●●  **GeoLocation** — GPS-Position des Clients mit der System-Codeunit Geolocation abfragen — drei Zeilen: SetHighAccuracy, RequestGeolocation (loest die Berechtigungsabfrage aus), GetGeolocation.
- ●●●  **S2S** — Service-to-Service-Auth gegen BC (client_credentials): Token von login.microsoftonline.com holen mit scope api.businesscentral.dynamics.com/.default, dann Bearer-Header auf die BC-API. Quelle ist eine C#-Konsole, das Token-Muster funktioniert 1:1 auch aus AL heraus.
- ●●●  **AzureFunctions** — Azure Functions aus AL mit dem Standard-Modul aufrufen: CreateCodeAuth (Function-Key) liefert das Auth-Interface, SendGetRequest nimmt Query-Parameter als Dictionary, die Response kapselt Erfolg/Fehler/Body.
- ●●●  **AzureBlobStorage** — Azure Blob Storage mit den fertigen System-App-Modulen (ABS Container Client / ABS Blob Client / Storage Service Authorization) — Container anlegen, Blob schreiben/lesen/listen, ohne eine Zeile eigenes HTTP.
- ●●●  **APIsInBC24** — Skelett einer Custom-API-Page (APIPublisher/APIGroup/APIVersion + EntityName/EntitySetName + DelayedInsert) — das Demo legt gezielt lauter Enum-/Option-Felder hinein, um deren Serialisierung im JSON zu zeigen.
- ●●●  **BlobAsTextInAPI** — Blob-Felder koennen nicht direkt auf eine API-Page — der Trick: eine globale Text-Variable als Feldquelle und in OnAfterGetRecord den Blob per CalcFields + InStream in die Variable lesen.
- ●●●  **QRCodesFromWebService** — Binaere HTTP-Antwort (Bild) direkt in ein Blob-Feld mit Subtype=Bitmap streamen — ReadAs(InStream) + CopyStream in den Blob-OutStream; dazu der UI-Kniff, ein Label-Feld mit OnDrillDown als Klick-'Button' im Layout zu nutzen.
- ●●○  **HttpClient** — Minimales GET-Muster und die Kernfrage der Instanz-Wiederverwendung: EIN HttpClient als globale Variable statt je Aufruf ein neuer — das Demo misst 100 Aufrufe in Serie mit Time().
- ●●○  **Blob Storage** — Persistent Blob: BLOBs ohne eigene Tabelle speichern — die System-Codeunit verwaltet Inhalte unter einem BigInteger-Schluessel; dazu das Zusammenspiel UploadIntoStream → Temp Blob → Blob-Feld.
- ●●○  **UploadToSharePoint** — Drei produktreife Muster aus einer SharePoint-Integration: (1) der Kern-Trick — ein Platzhalter-Report, dessen Ausgabe per ReportManagement.OnAfterDocumentReady durch ein beliebiges PDF ersetzt wird, damit BC fremde PDFs drucken/vorschauen kann; (2) Folder-Lesen in zwei Schritten, wobei Schritt 1 rein HTTP/read-only ist und damit in Page Background Tasks (DB read-only!) laeuft; (3) Dateinamen-Sanitizing fuer SharePoint via Handled-Event.
- ●●○  **ODataFromCSharp** — BC-OData typisiert aus C# konsumieren: 'OData Connected Service' generiert Klassen aus $metadata, das BuildingRequest-Event injiziert den Auth-Header je Request, AddQueryOption haengt $filter an. (C#-Demo, kein AL.)
- ●●○  **ExchangeRatesFromECB** — Die komplette Kette HTTP→ZIP→CSV→Records ohne eine einzige Datei auf Platte: HttpResponse als InStream lesen, mit 'Data Compression' das ZIP oeffnen und einen Eintrag in einen Temp Blob extrahieren, dann per 'CSV Buffer' als Matrix (Zeile, Spalte) auslesen.
- ●●○  **CountryAPI** — REST-GET + JsonArray-Iteration mit den direkten JsonObject-Gettern (GetText/GetObject) statt des alten JsonToken-Tanzes — plus Upsert-Muster gegen eine Stammtabelle (Get→Init/Insert, dann Validate/Modify).
- ●●○  **OAuth from AL Code** — Kompletter OAuth2-Authorization-Code-Flow rein in AL, ohne Standard-Modul: ControlAddin öffnet die Auth-URL im Popup, die redirect_uri ist eine BC-SEITE, deren startup.js code+state aus der URL fischt, und IsolatedStorage dient als Briefkasten zwischen Login-Fenster und Redirect-Fenster.
- ●●○  **HttpClientProblem** — Byte-Länge vs. Zeichen-Länge: strlen() zählt Zeichen, HTTP (Content-Length, byte-limitierte APIs) zählt UTF-8-Bytes. Die UTF-8-Byte-Länge eines Text misst man über einen Temp-Blob-OutStream mit TextEncoding::UTF8.
- ●●○  **USPS App** — XML-basierte Legacy-API komplett in AL: Request-XML mit XmlElement komponieren (AddField-Helper), XML URL-encodiert im Query-String verschicken, Antwort per XPath (SelectSingleNode) in Felder lesen — verpackt als Mini-Produkt mit Setup-Tabelle, Vergleichs-UI und Integration Events an jeder Naht.
- ●○○  **webscraping** — Regex in AL: Codeunit Regex fuellt temporaere Records (Matches/Groups) statt Strings zu liefern — den Treffertext schneidet man selbst per copystr aus dem Original, mit Index-Korrektur.
- ●○○  **Exchange from Openrates** — Wechselkurs-Import in 'Currency Exchange Rate' mit dem Upsert-Idiom `if Insert(true) then Validate+Modify` und der BC-Semantik: bei LCY-Basis ist 'Exchange Rate Amount' = 1 und 'Relational Exch. Rate Amount' = 1/API-Rate.
- ●○○  **Hacking Teams** — Die Brick-Fieldgroup bestimmt, welche Felder Karten-Renderer (Teams-Karten, Kachel-Ansichten) fuer einen Datensatz zeigen — per tableextension erweiterbar. Der zweite Teil des Demos injiziert per ControlAddin einen Teams-Share-Button ins Client-DOM.

---

## GeoLocation

**Technik:** GPS-Position des Clients mit der System-Codeunit Geolocation abfragen — drei Zeilen: SetHighAccuracy, RequestGeolocation (loest die Berechtigungsabfrage aus), GetGeolocation.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** app.json: BC22 / runtime 11.0

```al
var
    GeoLocation: Codeunit Geolocation;
    Lat: Decimal;
    Long: Decimal;
begin
    GeoLocation.SetHighAccuracy(true);
    if GeoLocation.RequestGeolocation() then begin
        GeoLocation.GetGeolocation(Lat, Long);
        // z. B. an Rapport-/Aufmass-Zeile oder Baustellen-Check-in haengen
    end;
end;
```

**Fallstricke:** RequestGeolocation braucht einen interaktiven Client (Browser/App fragt den Nutzer) — in Job Queue/Background-Sessions immer false. Liefert false auch bei verweigerter Freigabe: den Fall im UI behandeln, nicht als Fehler. Genauigkeit auf Desktops (IP-basiert) ist grob — fuer Baustellen-Verortung auf dem Handy brauchbar, am Buero-PC nicht.

---

## S2S

**Technik:** Service-to-Service-Auth gegen BC (client_credentials): Token von login.microsoftonline.com holen mit scope api.businesscentral.dynamics.com/.default, dann Bearer-Header auf die BC-API. Quelle ist eine C#-Konsole, das Token-Muster funktioniert 1:1 auch aus AL heraus.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** C#/.NET 6-Konsole, kein AL im Ordner; Endpunkte gelten fuer BC-Cloud v2.0 unveraendert — direkt relevant fuer das geplante Sync-Gateway

```al
procedure GetS2SToken(TenantId: Text; ClientId: Text; ClientSecret: Text): Text
var
    Client: HttpClient;
    Content: HttpContent;
    Headers: HttpHeaders;
    Resp: HttpResponseMessage;
    J: JsonObject;
    T: JsonToken;
    Body: Text;
begin
    Content.WriteFrom('grant_type=client_credentials' +
        '&scope=https://api.businesscentral.dynamics.com/.default' +
        '&client_id=' + ClientId + '&client_secret=' + ClientSecret);
    Content.GetHeaders(Headers);
    Headers.Remove('Content-Type');
    Headers.Add('Content-Type', 'application/x-www-form-urlencoded');
    Client.Post('https://login.microsoftonline.com/' + TenantId +
        '/oauth2/v2.0/token', Content, Resp);
    Resp.Content().ReadAs(Body);
    J.ReadFrom(Body);
    J.Get('access_token', T);
    exit(T.AsValue().AsText());
end;
// danach: Headers.Add('Authorization', 'Bearer ' + Token) auf jeden API-Call
```

**Fallstricke:** ClientSecret muss URL-encodiert werden (das C#-Original nutzt HttpUtility.UrlEncode — Sonderzeichen wie ~ und _ kommen in Secrets vor). Die Entra-App braucht die Application-Permission fuer BC UND muss in BC unter 'Microsoft Entra Applications' angelegt/aktiviert sein, sonst 401 trotz gueltigem Token. Bonus im Code: der Device-Code-Flow mit Microsofts wohlbekannter First-Party-Client-ID 38ff8e09-04a5-4af9-8153-793418879bde (BC-Client, kein eigenes App-Registrement noetig) — praktisch fuer CLI-Tools. Die Secrets im Repo sind echte (abgelaufene) Werte — nie so einchecken.

---

## AzureFunctions

**Technik:** Azure Functions aus AL mit dem Standard-Modul aufrufen: CreateCodeAuth (Function-Key) liefert das Auth-Interface, SendGetRequest nimmt Query-Parameter als Dictionary, die Response kapselt Erfolg/Fehler/Body.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** app.json: BC21 / runtime 10.0 — 'Azure Functions'-Modul ist seit BC21 in der System App

```al
var
    AzureAuth: Codeunit "Azure Functions Authentication";
    AzureFunc: Codeunit "Azure Functions";
    Auth: Interface "Azure Functions Authentication";
    Response: Codeunit "Azure Functions Response";
    Query: Dictionary of [Text, Text];
    Result: Text;
begin
    Auth := AzureAuth.CreateCodeAuth(
        'https://<app>.azurewebsites.net/api/Function1', '<function key>');
    Query.Add('name', 'Erik');
    Response := AzureFunc.SendGetRequest(Auth, Query);
    if Response.IsSuccessful() then
        Response.GetResultAsText(Result)
    else
        error(Response.GetError());
end;
// POST-Variante: AzureFunc.SendPostRequest(Auth, Body, ContentTypeHeader)
```

**Fallstricke:** Der Function-Key gehoert nicht hart in den Code (Demo!) — IsolatedStorage/Setup. CreateCodeAuth = Key-basiert; fuer Entra-geschuetzte Functions gibt es CreateOAuth2. Das Modul loggt Aufrufe in die Telemetrie mit. Direkter Treffer fuer das geplante Sync-Gateway auf Azure-Functions-Basis: BC-Seite so, nicht handgestrickt.

---

## AzureBlobStorage

**Technik:** Azure Blob Storage mit den fertigen System-App-Modulen (ABS Container Client / ABS Blob Client / Storage Service Authorization) — Container anlegen, Blob schreiben/lesen/listen, ohne eine Zeile eigenes HTTP.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** app.json: BC19 / runtime 8.0 — ABS-Module sind seit BC19 in der System App

```al
var
    ContainerClient: Codeunit "ABS Container Client";
    BlobClient: Codeunit "ABS Blob Client";
    StorageAuth: Codeunit "Storage Service Authorization";
    Authorization: Interface "Storage Service Authorization";
    Response: Codeunit "ABS Operation Response";
    Content: Record "ABS Container Content";
    Txt: Text;
begin
    Authorization := StorageAuth.CreateSharedKey('<storage account key>');
    ContainerClient.Initialize('<accountname>', Authorization);
    ContainerClient.CreateContainer('<container>');

    BlobClient.Initialize('<accountname>', '<container>', Authorization);
    Response := BlobClient.PutBlobBlockBlobText('MyBlob', 'content');
    if not Response.IsSuccessful() then
        error('ABS Error: %1', Response.GetError());

    BlobClient.ListBlobs(Content);
    if Content.FindSet() then
        repeat
            BlobClient.GetBlobAsText(Content.Name, Txt);
        until Content.Next() = 0;
end;
```

**Fallstricke:** Jede Operation liefert eine 'ABS Operation Response' — IsSuccessful() pruefen statt blind weiterzumachen. CreateSharedKey nimmt den Storage-Account-Key (Vollzugriff!) — fuer Produktion SAS-Token (StorageAuth.CreateSAS...) mit engem Scope vorziehen. Fuer Streams gibt es PutBlobBlockBlobStream/GetBlobAsStream — Fotos von der Baustelle gehoeren so in den Blob-Storage statt als DB-Blobs in die BC-Datenbank.

---

## APIsInBC24

**Technik:** Skelett einer Custom-API-Page (APIPublisher/APIGroup/APIVersion + EntityName/EntitySetName + DelayedInsert) — das Demo legt gezielt lauter Enum-/Option-Felder hinein, um deren Serialisierung im JSON zu zeigen.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** app.json: application 23.0 / runtime 12.0 (BC23/24-Aera); Muster gilt unveraendert auf BC28 — Grundlage fuer jede Bauleiter-App-API

```al
page 50140 APITest
{
    PageType = API;
    APIPublisher = 'hougaard';
    APIGroup = 'group';
    APIVersion = 'v2.0';
    EntityName = 'salesheader';
    EntitySetName = 'salesheaders';
    SourceTable = "Sales Line";
    DelayedInsert = true;          // Pflicht bei zusammengesetztem PK
    layout
    {
        area(content)
        {
            repeater(General)
            {
                field(documentNo; Rec."Document No.") { }
                field(documentType; Rec."Document Type") { } // Enum -> Member-NAME im JSON
                field(vatCalculationType; Rec."VAT Calculation Type") { }
            }
        }
    }
}
// URL: .../api/hougaard/group/v2.0/companies(<guid>)/salesheaders
```

**Fallstricke:** Enums kommen als Member-Name (Text) im JSON, nicht als Zahl — wer schreibt (POST/PATCH), muss den Namen schicken; genau die Falle, die in der Praxis als 'Enum-als-Text'-Falle bekannt ist. Feldnamen muessen camelCase ohne Leerzeichen sein. Und ein Warnschild aus dem Demo selbst: EntityName 'salesheader' ueber SourceTable 'Sales Line' — Entity-Namen sind frei waehlbar und koennen luegen; sauber benennen.

---

## BlobAsTextInAPI

**Technik:** Blob-Felder koennen nicht direkt auf eine API-Page — der Trick: eine globale Text-Variable als Feldquelle und in OnAfterGetRecord den Blob per CalcFields + InStream in die Variable lesen.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** app.json: BC26 / runtime 15.0

```al
page 50105 salesorderapi
{
    PageType = API;
    APIPublisher = 'hougaard'; APIGroup = 'group'; APIVersion = 'v2.0';
    EntityName = 'salesorder'; EntitySetName = 'salesorders';
    SourceTable = "Sales Header";
    DelayedInsert = true;
    layout { area(Content) { repeater(General) {
        field(no; Rec."No.") { }
        field(workDescription; WorkDescription_BlobAsTxt) { } // Var statt Feld!
    } } }

    trigger OnAfterGetRecord()
    var
        InS: InStream;
    begin
        Rec.CalcFields("Work Description");        // Blob erst laden!
        Rec."Work Description".CreateInStream(InS);
        InS.Read(WorkDescription_BlobAsTxt);       // liest den ganzen Stream
    end;

    var
        WorkDescription_BlobAsTxt: Text;
}
```

**Fallstricke:** Ohne CalcFields ist der Blob leer — die klassische Falle. InS.Read(Text) liest **bis zur angegebenen Länge ODER bis zum ersten NULL-BYTE** — ohne Längenangabe wird die Größe der Variablen benutzt (MS *InStream.Read(var Text [, Integer]) Method*: „Read reads until the specified length or a zero byte“). ⚠⚠ **BERICHTIGT 01.09.2026 (B): Hier stand „liest bis Stream-Ende“. DAS IST WIDERLEGT** — ein NULL-Byte beendet das Lesen vorher, was bei Binärdaten in einem Blob still abschneidet; bei Sonderzeichen CreateInStream(TextEncoding::UTF8) verwenden. Der Weg ist so nur LESEND — eingehende Werte (POST/PATCH) landen in der Variable und muessten per OnValidate/OnModifyRecord selbst in den Blob geschrieben werden. Direkt relevant fuer LV-Langtexte und Rapport-Beschreibungen, die in einem Bau-ERP oft als Blob liegen und in Apps sichtbar sein sollen.

---

## QRCodesFromWebService

**Technik:** Binaere HTTP-Antwort (Bild) direkt in ein Blob-Feld mit Subtype=Bitmap streamen — ReadAs(InStream) + CopyStream in den Blob-OutStream; dazu der UI-Kniff, ein Label-Feld mit OnDrillDown als Klick-'Button' im Layout zu nutzen.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
// tableextension: field(50100; QRCode; Blob) { Subtype = Bitmap; }
field(GenerateQR; GenerateQRLbl)
{
    ShowCaption = false;   // Label-Feld wirkt als klickbarer Link im Layout
    trigger OnDrillDown()
    var
        Client: HttpClient;
        Response: HttpResponseMessage;
        InS: InStream;
        OutS: OutStream;
    begin
        if Client.Get('https://api.qrserver.com/v1/create-qr-code/?data=' +
                      Rec."No." + '&size=200x200', Response) then
            if Response.IsSuccessStatusCode() then begin
                Response.Content().ReadAs(InS);     // Binaerantwort als Stream
                Rec.QRCode.CreateOutStream(OutS);   // Blob, Subtype = Bitmap
                CopyStream(OutS, InS);
                Rec.Modify();                       // ohne Modify kein Persist!
            end;
    end;
}
var
    GenerateQRLbl: Label 'Generate QR Code';
```

**Fallstricke:** Das Original nutzt http:// — im SaaS-Client scheitert das (Mixed Content/ausgehende Regeln), https verwenden. Subtype=Bitmap laesst den Blob auf Karten als Bild rendern. Fuer QR auf REPORTS ist seit BC18 die eingebaute Barcode-/QR-Schriftart der einfachere Weg — der Webservice lohnt nur, wenn das Bild als Datensatz-Anhang gebraucht wird (Geraete-Etiketten, Lieferscheine).

---

## HttpClient

**Technik:** Minimales GET-Muster und die Kernfrage der Instanz-Wiederverwendung: EIN HttpClient als globale Variable statt je Aufruf ein neuer — das Demo misst 100 Aufrufe in Serie mit Time().

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: BC18 / runtime 7.0

```al
pageextension 50123 CustomerListExt extends "Customer List"
{
    var
        Client: HttpClient; // global — NICHT je Aufruf lokal neu anlegen

    procedure HttpGetText(Url: Text; var Body: Text): Boolean
    var
        Resp: HttpResponseMessage;
    begin
        if not Client.Get(Url, Resp) then
            exit(false);                    // Ebene 1: Verbindungsfehler
        if not Resp.IsSuccessStatusCode() then
            exit(false);                    // Ebene 2: HTTP-Fehlerstatus
        Resp.Content().ReadAs(Body);        // Ebene 3: Inhalt lesen
        exit(true);
    end;
}
```

**Fallstricke:** Im Code ist die lokale Deklaration `//Client: HttpClient;` absichtlich auskommentiert — die Pointe des Videos: der Client gehört als globale Variable wiederverwendet (Connection-Reuse), sonst zahlt man pro Aufruf Aufbau-Kosten. Client.Get liefert false nur bei Verbindungsfehlern; ein 404 ist ein erfolgreicher Send mit schlechtem Statuscode — beide Ebenen getrennt prüfen.

---

## Blob Storage

**Technik:** Persistent Blob: BLOBs ohne eigene Tabelle speichern — die System-Codeunit verwaltet Inhalte unter einem BigInteger-Schluessel; dazu das Zusammenspiel UploadIntoStream → Temp Blob → Blob-Feld.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: BC16 / runtime 5.0

```al
var
    Persistent: Codeunit "Persistent Blob";
    PNo: BigInteger;
    InS: InStream;
    OutS: OutStream;
    FileName: Text;
begin
    // Speichern ohne eigene Tabelle:
    if UploadIntoStream('Select file', '', '', FileName, InS) then begin
        PNo := Persistent.Create();          // Schluessel selbst verwahren!
        Persistent.CopyFromInStream(PNo, InS);
    end;

    // Spaeter in ein Blob-Feld zurueckholen:
    Rec.BLOB.CreateOutStream(OutS);
    Persistent.CopyToOutStream(PNo, OutS);
    Rec.Modify();                            // ohne Modify bleibt der Blob nur im Puffer
end;
```

**Fallstricke:** Die Demo laesst Rec.Modify() nach dem Schreiben in den Blob-OutStream weg (Kommentar: 'The universe does something different!') — Schreiben ueber CreateOutStream aendert nur den Record-Puffer, erst Modify persistiert. Persistent Blob gibt einem NUR die Nummer zurueck: wer sie verliert, verliert den Inhalt — Nummer in einem eigenen Feld ablegen. Daneben existieren 'Temp Blob' (eine Instanz) und 'Temp Blob List' (Sammlung) fuer fluechtige Zwischenspeicher.

---

## UploadToSharePoint

**Technik:** Drei produktreife Muster aus einer SharePoint-Integration: (1) der Kern-Trick — ein Platzhalter-Report, dessen Ausgabe per ReportManagement.OnAfterDocumentReady durch ein beliebiges PDF ersetzt wird, damit BC fremde PDFs drucken/vorschauen kann; (2) Folder-Lesen in zwei Schritten, wobei Schritt 1 rein HTTP/read-only ist und damit in Page Background Tasks (DB read-only!) laeuft; (3) Dateinamen-Sanitizing fuer SharePoint via Handled-Event.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: BC22 / runtime 11.0

```al
report 50101 "Print PDF from SharePoint"
{
    DefaultLayout = Word;
    WordLayout = 'PrintPDF-Placeholder.docx';   // Dummy — wird nie gerendert
    dataset { dataitem(SPFile; "SharePoint File EFQ") { /* PDF als InStream holen */ } }
}

codeunit 50102 "Print PDF Support"
{
    SingleInstance = true;   // InStream zwischen Aufrufer und Event transportieren
    var
        _InS: InStream;

    internal procedure PDFToPrint(var InS: InStream)
    begin
        _InS := InS;
    end;

    [EventSubscriber(ObjectType::Codeunit, Codeunit::ReportManagement,
        'OnAfterDocumentReady', '', true, true)]
    local procedure OnAfterDocumentReady(ObjectId: Integer;
        var TargetStream: OutStream; var Success: Boolean)
    begin
        if ObjectId = Report::"Print PDF from SharePoint" then begin
            CopyStream(TargetStream, _InS);   // beliebiges PDF als "Report-Ausgabe"
            Success := true;
        end;
    end;
}
```

**Fallstricke:** Der Code haengt an der Dritt-App 'SharePoint EFQ' (eFoqus), NICHT am Standard-Modul 'SharePoint Client' (System App seit ~BC20) — die Muster uebertragen sich, die Codeunits nicht. Merksaetze aus den Kommentaren: Auth EINMAL vor der Schleife holen ('too slow' je Record); GetFolderContent ist bewusst zweigeteilt, weil Page Background Tasks die DB nur lesend sehen; SharePoint verweigert bestimmte Zeichen in Dateinamen (zwei Zeichensaetze strict/relaxed im Code). Der OnAfterDocumentReady-Trick ist die eigentliche Perle — z. B. um Baustellen-PDFs (Plaene, Lieferscheine) durch BCs Druckpipeline zu schicken.

---

## ODataFromCSharp

**Technik:** BC-OData typisiert aus C# konsumieren: 'OData Connected Service' generiert Klassen aus $metadata, das BuildingRequest-Event injiziert den Auth-Header je Request, AddQueryOption haengt $filter an. (C#-Demo, kein AL.)

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** .NET-5-Konsole gegen BC18 on-prem; URL-Schemata gelten unveraendert — Referenz fuer Companion-Apps

```al
// C# — OData Connected Service generiert BCAPI.NAV aus $metadata
var ctx = new BCAPI.NAV(new Uri(
    "http://bc:7048/BC/api/v2.0/companies(<company-systemId>)/"));
ctx.BuildingRequest += (s, e) =>
    e.Headers.Add("Authorization", "Basic " + Convert.ToBase64String(
        Encoding.UTF8.GetBytes("user:password")));
foreach (var v in ctx.Vendors.Execute())
    Console.WriteLine($"{v.Number} {v.DisplayName}");

// Klassisches ODataV4 braucht die Company im PFAD, nicht als GUID:
var ctx2 = new BC18.NAV(new Uri("http://bc:7048/BC/ODataV4/Company('Hougaard')/"));
var q = ctx2.Chart_of_Accounts.AddQueryOption("$filter", "Net_Change gt 0");
```

**Fallstricke:** Zwei URL-Welten, die staendig verwechselt werden: api/v2.0 adressiert die Company als companies(guid) (GUID = $systemId der Company), ODataV4 als Company('Name') im Pfad. Der Auth-Header muss im BuildingRequest-Event je Request gesetzt werden — DefaultRequestHeaders greifen beim OData-Client nicht. Feldnamen im generierten Client sind die OData-Namen (Net_Change), nicht die AL-Captions.

---

## ExchangeRatesFromECB

**Technik:** Die komplette Kette HTTP→ZIP→CSV→Records ohne eine einzige Datei auf Platte: HttpResponse als InStream lesen, mit 'Data Compression' das ZIP oeffnen und einen Eintrag in einen Temp Blob extrahieren, dann per 'CSV Buffer' als Matrix (Zeile, Spalte) auslesen.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: BC22 / runtime 11.0

```al
HttpClient.Get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip', Response);
if Response.IsSuccessStatusCode() then begin
    Response.Content.ReadAs(InS);                 // Antwort direkt als Stream
    Zip.OpenZipArchive(InS, false);               // Codeunit "Data Compression"
    Zip.GetEntryList(FileList);
    TmpBlob.CreateOutStream(OutS);
    Zip.ExtractEntry(FileList.Get(1), OutS, LengthOfCsv);
    TmpBlob.CreateInStream(CSVStream);
    CSV.LoadDataFromStream(CSVStream, ',');       // Record "CSV Buffer" temporary
    for Col := 2 to CSV.GetNumberOfColumns() do begin
        CSV.Get(1, Col);                          // Kopfzeile = Waehrungscode
        CurCode := CSV.Value;
        for Line := 2 to CSV.GetNumberOfLines() do begin
            CSV.Get(Line, 1);
            evaluate(StartDate, CSV.Value, 9);    // Format 9 = XML/ISO-Datum
            CSV.Get(Line, Col);                   // Kurswert der Zelle
        end;
    end;
end;
```

**Fallstricke:** CSV Buffer ist eine Matrix mit Get(Line, Col) — Kopfzeile ist Zeile 1, Datenspalten ab 2. evaluate(..., 9) fuer ISO-Daten aus Fremdquellen (kein Locale-Raten). Leere Zellen: das if-evaluate um den Kurswert schluckt sie still. Fuer ein Bau-ERP relevant, weil OeNORM-A2063-Datentraeger ebenfalls als ZIP/Container kommen — dieselbe Stream-Kette traegt.

---

## CountryAPI

**Technik:** REST-GET + JsonArray-Iteration mit den direkten JsonObject-Gettern (GetText/GetObject) statt des alten JsonToken-Tanzes — plus Upsert-Muster gegen eine Stammtabelle (Get→Init/Insert, dann Validate/Modify).

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: BC26 / runtime 15.0 — die direkten Getter (GetText/GetObject/GetInteger) gibt es ab **Runtime 15.0 = BC 2025 Wave 1 (v26)**; auf BC28 vorhanden. ⚠⚠ **BERICHTIGT 01.09.2026 (B): Hier stand „(BC24+)“. DAS IST FALSCH** — MS führt bei allen dreien „Available or changed with runtime version 15.0“, und Runtime 13.0 ist BC 2024 Wave 1 (*JSON files — app.json*). **In BC24 und BC25 gibt es die Getter NICHT** — wer nach der alten Notiz baut, kompiliert dort nicht

```al
Client.Get('https://restcountries.com/v3.1/all?fields=name,cca2,ccn3', Response);
if not Response.IsSuccessStatusCode() then
    error('API returned %1', Response.HttpStatusCode);
Response.Content.ReadAs(ResponseTxt);
CountryArray.ReadFrom(ResponseTxt);
foreach T in CountryArray do begin
    CountryJson := T.AsObject();
    if not CountryRec.Get(CountryJson.GetText('cca2')) then begin
        CountryRec.Init();
        CountryRec.Code := CountryJson.GetText('cca2');
        CountryRec.Insert(true);
    end;
    NameJson := CountryJson.GetObject('name');       // verschachteltes Objekt
    CountryRec.Validate(Name, NameJson.GetText('common'));
    CountryRec.Validate("ISO Numeric Code", CountryJson.GetText('ccn3'));
    CountryRec.Modify(true);
end;
```

**Fallstricke:** GetText/GetObject werfen einen Laufzeitfehler, wenn der Member fehlt — bei APIs mit optionalen Feldern vorher Contains() pruefen oder das alte Get(Member, Token)-Muster nehmen. Country-Code landet ungekuerzt in Code[10] — bei fremden APIs immer gegen maxstrlen sichern.

---

## OAuth from AL Code

**Technik:** Kompletter OAuth2-Authorization-Code-Flow rein in AL, ohne Standard-Modul: ControlAddin öffnet die Auth-URL im Popup, die redirect_uri ist eine BC-SEITE, deren startup.js code+state aus der URL fischt, und IsolatedStorage dient als Briefkasten zwischen Login-Fenster und Redirect-Fenster.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: BC13 / runtime 2.0 — historisch; ab BC17+ nimmt man das System-App-Modul 'OAuth2', der Fenster-/Redirect-Mechanismus bleibt aber lehrreich für Provider ohne Entra

```al
// Login-Seite (ControlAddin 1x1 Pixel):
URL := AuthEndpoint + '?response_type=code&client_id=' + ClientID +
  '&redirect_uri=' + TypeHelper.UrlEncode(CallbackUrl) + // BC-Seite: ...?page=50101
  '&state=' + StateValue + '&scope=...';
CurrPage.oa.LaunchURLinNewWindow(URL);
IsolatedStorage.Set('OAUTH-STATE', StateValue);
CurrPage.oa.StartTimer(); // pollt: sobald OAUTH-TOKEN existiert -> weiter

// startup.js der Redirect-Seite:
// var p = new URLSearchParams(window.location.search);
// if (p.has('code')) InvokeExtensibilityMethod('RedirectReceived',[p.get('code'),p.get('state')]);

// Redirect-Seite, trigger RedirectReceived(Code, State):
IsolatedStorage.Get('OAUTH-STATE', StateValue);
if StateValue <> State then
    Error('OAuth2 State mismatch, aborting!');   // CSRF-Schutz
WebClient.Get(TokenUrl.Replace('AUTH_CODE_HERE', Code), Response);
Response.Content().ReadAs(TokenJson);
JO.ReadFrom(TokenJson);
JO.Get('access_token', JT);
IsolatedStorage.Set('OAUTH-TOKEN', JT.AsValue().AsText());
```

**Fallstricke:** Drei Kniffe: (1) redirect_uri zeigt auf eine BC-Page — der Auth-Server leitet zurück in den Web-Client, das JS der Seite liest die Query-Parameter; (2) Fenster können sich nicht direkt Werte zurufen — IsolatedStorage + Timer-Polling ist der Kanal; (3) im Original steht copystr(Token,2,strlen-2), weil JT.WriteTo() die JSON-Anführungszeichen mitschreibt — JT.AsValue().AsText() ist der saubere Weg. State-Prüfung nicht weglassen. Secrets liegen im Demo als Klartext-Codeunit — heute IsolatedStorage/Setup.

---

## HttpClientProblem

**Technik:** Byte-Länge vs. Zeichen-Länge: strlen() zählt Zeichen, HTTP (Content-Length, byte-limitierte APIs) zählt UTF-8-Bytes. Die UTF-8-Byte-Länge eines Text misst man über einen Temp-Blob-OutStream mit TextEncoding::UTF8.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: BC25 / runtime 14.0 (mit namespace/using-Syntax)

```al
procedure StrlenUTF8(S: Text): Integer
var
    TmpBlob: Codeunit "Temp Blob";
    OutS: OutStream;
begin
    TmpBlob.CreateOutStream(OutS, TextEncoding::UTF8);
    OutS.WriteText(S);
    exit(TmpBlob.Length());   // Bytes, nicht Zeichen
end;
// strlen('❤️') = 2 (Zeichen)  vs.  StrlenUTF8('❤️') = 6 (Bytes)

// Content-Header gehören auf den CONTENT, nicht auf den Request:
// Content.WriteFrom(Data);
// Content.GetHeaders(Headers);
// Headers.Add('Content-Length', format(StrlenUTF8(Data)));
```

**Fallstricke:** Das Demo ist als Negativ-Beweis gebaut: Client.Send soll fehlschlagen ('You should not see the message, then Erik messed up!?') — manuelles Setzen von Content-Length kollidiert mit der .NET-Validierung, der Fehler landet in GetLastErrorText(). Die eigentliche Lehre: bei Umlauten/Emoji weichen strlen und Byte-Länge auseinander; wer Längen an APIs meldet oder Byte-Limits prüft, braucht die Blob-Messung. Wichtig für ÖNORM-Exporte mit Umlauten.

---

## USPS App

**Technik:** XML-basierte Legacy-API komplett in AL: Request-XML mit XmlElement komponieren (AddField-Helper), XML URL-encodiert im Query-String verschicken, Antwort per XPath (SelectSingleNode) in Felder lesen — verpackt als Mini-Produkt mit Setup-Tabelle, Vergleichs-UI und Integration Events an jeder Naht.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** app.json: runtime 5.0 (BC16-Aera); XML-API-Stil historisch, die Xml-/XPath-Muster unveraendert gueltig

```al
local procedure AddField(Name: Text; Value: Text): XmlElement
var
    e: XmlElement;
begin
    e := XmlElement.Create(Name);
    e.Add(Value);
    exit(e);
end;

// Request bauen:
Address := XmlElement.Create('Address');
Address.Attributes().Set('ID', '0');
Address.Add(AddField('City', CompareRec.City));
AVR := XmlElement.Create('AddressValidateRequest');
AVR.Attributes().Set('USERID', Setup.UserID);
AVR.Add(Address);
Parameters := XmlDocument.Create();
Parameters.Add(AVR);

// Versand: XML im Query-String
Parameters.WriteTo(XMLtxt);
TypeHelper.UrlEncode(XMLtxt);              // var-Parameter, veraendert XMLtxt
Request.SetRequestUri(Setup.URL + '?API=Verify&XML=' + XMLtxt);
Request.GetHeaders(Headers);
Headers.Add('User-Agent', 'Dynamics 365 Business Central'); // sonst blockt USPS

// Antwort per XPath:
if Xml.SelectSingleNode('AddressValidateResponse/Address[1]/Error/Description', N) then
    error('%1', N.AsXmlElement().InnerText);
```

**Fallstricke:** Drei Handgriffe mit Wiederverwendungswert: TypeHelper.UrlEncode arbeitet auf dem var-Parameter (kein Rueckgabewert); manche APIs verlangen einen User-Agent-Header und antworten sonst mit Fehlern; XPath-Fehlerpfad ZUERST pruefen (Error/Description), dann erst Nutzdaten. Jede Uebernahme in Customer/Vendor laeuft ueber Validate + copystr(..., maxstrlen(...)) gegen Feldueberlaeufe. Die XmlElement/XPath-Helfer sind 1:1 die Werkzeuge fuer OeNORM-A2063-XML.

---

## webscraping

**Technik:** Regex in AL: Codeunit Regex fuellt temporaere Records (Matches/Groups) statt Strings zu liefern — den Treffertext schneidet man selbst per copystr aus dem Original, mit Index-Korrektur.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** app.json: BC20 / runtime 9.0; Regex-Modul ist System App

```al
var
    Regex: Codeunit Regex;
    Matches: Record Matches temporary;
    Groups: Record Groups temporary;
    RawHtml: Text;
    Version: Text;
begin
    Response.Content.ReadAs(RawHtml);
    Regex.Match(RawHtml, '"AppVersion":"(\d{1,5}\.\d{1,5}\.\d{1,5}\.\d{1,5})"', Matches);
    if Matches.FindSet() then
        repeat
            Regex.Groups(Matches, Groups);
            Groups.Get(1);                       // Gruppe 1 = erste Klammer
            Version := copystr(RawHtml, Groups.Index + 1, Groups.Length);
        until Matches.Next() = 0;
end;
```

**Fallstricke:** Groups.Index ist 0-basiert (aus .NET), AL-Strings sind 1-basiert — das `+ 1` ist der Fallstrick, ueber den jeder stolpert. Scraping von HTML ist naturgemaess fragil (Seitenlayout-Aenderung = kaputt) — das Muster taugt eher fuer Versions-/Statusabfragen als fuer Produktivdaten.

---

## Exchange from Openrates

**Technik:** Wechselkurs-Import in 'Currency Exchange Rate' mit dem Upsert-Idiom `if Insert(true) then Validate+Modify` und der BC-Semantik: bei LCY-Basis ist 'Exchange Rate Amount' = 1 und 'Relational Exch. Rate Amount' = 1/API-Rate.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** app.json: BC17 / runtime 6.0

```al
ExchangeRate.Init();
ExchangeRate."Currency Code" := CurRec.Code;
ExchangeRate."Starting Date" := CurDate;
if ExchangeRate.Insert(true) then begin   // Duplikat (gleicher Tag) -> still ueberspringen
    ExchangeRate.Validate("Exchange Rate Amount", 1);
    ExchangeRate.Validate("Relational Exch. Rate Amount", 1 / CurRate);
    ExchangeRate.Modify(true);
end;
```

**Fallstricke:** api.openrates.io existiert nicht mehr — nur das Record-Muster ist noch verwertbar. Sehenswert ist das Fehler-Layering des Originals: jede Stufe (Connect, Statuscode, ReadAs, JSON-Parse, 'rates'-Member) hat ihre eigene sprechende error()-Meldung mit dem Server-Inhalt als Kontext.

---

## Hacking Teams

**Technik:** Die Brick-Fieldgroup bestimmt, welche Felder Karten-Renderer (Teams-Karten, Kachel-Ansichten) fuer einen Datensatz zeigen — per tableextension erweiterbar. Der zweite Teil des Demos injiziert per ControlAddin einen Teams-Share-Button ins Client-DOM.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** app.json: runtime 5.0 (BC16-Aera)

```al
tableextension 50127 Teams extends Customer
{
    fieldgroups
    {
        addlast(Brick; Address, "Address 2", "Phone No.", "E-Mail") { }
    }
}
// Brick steuert die Karten-/Kachel-Darstellung des Records
// (u. a. die BC-Karten in Microsoft Teams und Listen im Brick-Layout)
```

**Fallstricke:** Nur der Brick-Teil ist tragfaehig. Der DOM-Hack (scripts.js greift via window.top.document.getElementById('centerRegion') in den Web-Client und fuegt HTML ein) ist unsupported, bricht mit jedem Client-Update und funktioniert in aktuellen Versionen wegen Iframe-Sandboxing nicht mehr — als Warnbeispiel lesen, nicht nachbauen.

---

## Übersprungen (bewusst)

- WCFandOAuth (nur 7-Zeilen-SOAP-Echo, Client-Seite fehlt)
- findAPIs (nur HelloWorld-Geruest)
- SendEmailFromAPI (nur HelloWorld-Geruest)
- appws1 (Workshop-Grundgeruest, api.al leer)
- powerautomate (nur Dummy-Testseite)
- woocommerce (Query-Param-Auth, sonst durch CountryAPI abgedeckt)
- Simple Webservice with Json Response (Minimal-GET, durch CountryAPI abgedeckt)

