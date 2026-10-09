# ControlAddIns & JavaScript im Client

_Destilliert aus Erik Hougaards Youtube-Video-Sources (Ordnername = Videothema)._
_Vollquellen: https://github.com/hougaard/Youtube-Video-Sources (lokal klonen; Ordnername = Videothema)_

Der Cluster lehrt die komplette ControlAddIn-Mechanik: den Lebenszyklus (StartupScript laeuft, meldet per InvokeExtensibilityMethod ein ControlReady-Event, erst danach ruft AL Prozeduren im JS), den Datentransport (JsonObject/JsonArray gehen verlustfrei in beide Richtungen) und drei Abkuerzungen, die eigene JS-Dateien oft ueberfluessig machen: die eingebauten Addins BusinessChart, WebPageViewer und BarcodeScannerProviderAddIn. Die zweite grosse Lektion ist das unsichtbare 1x1-Pixel-Addin als Client-Hook — damit fängt Hougaard Keyboard-Wedge-Scanner ab, oeffnet Popups und baut eine JS-REPL in den Client. Drittens: Geraete-APIs (Camera, Geolocation) und Bild-/Media-Handling (Codeunit Image, Media-Referenz-Zuweisung per FieldRef) sind reine AL-Sache ohne JS. Chronischer Schmerzpunkt ist die iframe-Hoehe des Addins, fuer die es nur einen undokumentierten window.parent-Hack gibt. Fuer das Referenzprojekt am direktesten verwertbar: Scanner-Erfassung, POS-artiges Schnellerfassungsmuster auf Standardbelegen, Gantt fuer Bauzeitplaene, Kamera+GPS fuer Rapporte und HTML-Rendering fuer LV-Vorschauen.

**Wertvollste Ordner:** Point of Sale · ScannerApp1 · PoorManControlAddin · URLControl · Gantt

## Themen (nach Praxis-Relevanz)

- ●●●  **PoorManControlAddin** — Das eingebaute "Microsoft.Dynamics.Nav.Client.WebPageViewer" als Instant-ControlAddIn: beliebiges HTML per SetContent rendern und Klicks/Werte ueber WebPageViewerHelper.TriggerCallback nach AL zurueckmelden — ganz ohne eigenes controladdin-Objekt und JS-Dateien.
- ●●●  **Dynamic HTML Render** — Minimales generisches HTML-Render-Addin: eine einzige Prozedur Render(HTML: Text), das HTML wird serverseitig in AL gebaut (TextBuilder/Konkatenation) und per insertAdjacentHTML in den controlAddIn-Div gesetzt. Grundmuster fuer jede eigene HTML-Vorschau (Belege, LV, Tabellen mit Farblogik).
- ●●●  **ScannerApp1** — Keyboard-Wedge-Barcodescanner ohne Fokus-Feld abfangen: ein unsichtbares 1x1-Pixel-Addin registriert einen keydown-Listener auf window.parent (dem ganzen BC-Client!) und unterscheidet Scanner von Mensch per Tipp-Tempo — Zeichen im Abstand <100ms gelten als Scan und werden per preventDefault vor BC-Feldern versteckt.
- ●●●  **Point of Sale** — Komplette Kasse auf Standard-Verkaufsrechnung: unsichtbares Scanner-Addin + Zustandsautomat (Option-Variable) auf der Page — ein Scan legt den Beleg an, weitere Scans erhoehen Mengen oder legen Zeilen an, und Zahlungsarten haben selbst Barcodes, sodass der Zahlungs-Scan direkt bucht. Muster fuer jede Schnellerfassungs-Maske auf Standardbelegen.
- ●●●  **BarcodeAddIn** — Der Standard-Weg fuer Kamera-Scans in der BC-Mobile-App: eingebautes usercontrol BarcodeScannerProviderAddIn (Namespace System.Device) mit Trigger BarcodeReceived — kein eigenes JS, kein Scanner-Timing, funktioniert mit der Geraetekamera.
- ●●●  **camera** — Zwei Wege zum Foto in AL ohne jedes JS: Codeunit Camera (ein Aufruf, Bild als InStream) fuer den Schnellfall, Page Camera fuer Kontrolle ueber Qualitaet, Encoding und Nachbearbeitung durch den Benutzer.
- ●●●  **CameraPart2** — Kamera-Bild ohne Blob-Umweg direkt in ein Media-Feld: Camera.GetPicture liefert den InStream, Media.ImportStream speichert ihn im Tenant-Media-Store — zwei Zeilen statt Stream-Kopiererei.
- ●●●  **location** — GPS-Position des Geraets in AL abfragen: Codeunit Geolocation mit RequestGeolocation (loest die Berechtigungsabfrage aus), HasGeolocation und GetGeolocation — fertig fuer Geo-Stempel auf Rapporten oder Baustellen-Ankunft.
- ●●●  **Gantt** — Gantt-Diagramm aus Projekt (Job) und Projektaufgaben (Job Task) mit der lokal gebundelten dhtmlxGantt-Library: AL baut das data/links-JSON, JS ist nur gantt.init + gantt.parse. Direkt das Muster fuer Bauzeitplaene.
- ●●●  **image** — Bildbearbeitung in purem AL mit Codeunit Image: FromStream laden, Metadaten lesen (Breite/Hoehe/Format), Crop, Resize, RotateFlip und Formatkonvertierung via SetFormat — z.B. Baustellenfotos vor dem Speichern verkleinern, ohne externen Dienst.
- ●●○  **mediaref** — Media-Felder sind Referenzen in den Tenant-Media-Store, keine Kopien — deshalb laesst sich ein Media-Wert per FieldRef von Tabelle zu Tabelle ZUWEISEN: Bild in einen temporaeren Record importieren, dann FR.Value := TempRec.Image auf die Zieltabelle.
- ●●○  **URLControl** — Chrome-loses BC-Popup mit vorgefiltertem Datensatz: GetUrl mit Record-Parameter und true haengt die aktuellen Filter an die URL, URL-Schalter (showribbon=0, shownavigation=0, showuiparts=0, showheader=0) blenden die Client-Huelle aus ⚠⚠ **BERICHTIGT 01.09.2026 (B): Hier stand „undokumentierte URL-Schalter". DAS IST WIDERLEGT** — MS dokumentiert sie regulaer (*Web client URL*, Abschnitt URL parameters, und *Embed Business Central Web Client in Other Websites*): „showribbon — Specifies whether to show the action bar on pages when they open … To hide the action bar, use showribbon=0". Sie sind also **zugesichert**, nicht geduldet, ein unsichtbares Addin oeffnet das Ganze per window.open.
- ●●○  **Wysiwyg - Streams** — Dieselbe CKEditor-Integration, aber Speicherung in einem Blob-Feld statt Text[2048] — unbegrenzte Laenge, dazu Import/Export des HTML per Upload-/DownloadFromStream.
- ●●○  **Wysiwyg** — CKEditor als Rich-Text-Editor im Client mit sauberer Event-Choreografie: ControlReady -> Init() baut den Editor asynchron, ein EIGENES OnAfterInit-Event signalisiert "jetzt darfst du laden", ContentChanged -> RequestSave -> SaveRequested(data) bringt den HTML-Inhalt zurueck ins Feld. Blaupause fuer jedes zustandsbehaftete JS-Widget.
- ●●○  **JavascriptModules** — ES-Module in ControlAddIns schmuggeln: Die Scripts-Property laedt alles als klassisches Script (ES-Module brechen dort) — der Trick ist, die Modul-Datei als Images-Ressource zu deklarieren und im Startup-Script per dynamischem import(Microsoft.Dynamics.NAV.GetImageResource(...)) zu laden. So laufen moderne Web-Components (hier: deep-chat) in BC.
- ●●○  **Charts.css** — Balkendiagramme voellig ohne Chart-JavaScript: das CSS-Framework charts.css macht aus einer nackten HTML-Tabelle ein Chart — die StyleSheets-Property laedt das CSS vom CDN, AL baut nur die Tabelle mit --size-CSS-Variablen per TextBuilder.
- ●●○  **ControlAddInHeightHack** — Der notorische Hoehen-Hack: ein ControlAddIn-iframe bekommt vom BC-Client keine dynamische Hoehe — das Startup-Script greift per window.parent auf das umgebende 'control-addin-form'-Div zu und setzt die eigene iframe-Hoehe darauf, inkl. resize-Listener.
- ●●○  **Mermaid** — Text-zu-Diagramm live im Client: Mermaid vom CDN laden, ein MultiLine-Textfeld mit OnValidate ruft Draw(code), JS rendert per mermaid.mermaidAPI.render den Mermaid-Code zu SVG in den Addin-Container. Dazu das Muster, einem AL-Event ein JsonObject aus JS mitzugeben.
- ●●○  **BusinessCharts** — Charts komplett ohne eigenes JS: eingebautes usercontrol "Microsoft.Dynamics.Nav.Client.BusinessChart" plus temporaerer Record "Business Chart Buffer" — Measures anlegen, X-Achse setzen, Werte per Index fuellen, Update. Sogar gemischte Chart-Typen (Column + Pie) je Measure und Klick-Events inklusive.
- ●●○  **AppIsAlsoAWebPage** — Klickbarer Weblink als Seitenfeld ohne Addin: ein Label-Feld mit ShowCaption=false und OnDrillDown -> Hyperlink() macht aus jedem Card-Bereich einen Link (Hilfe, Doku, Portal).
- ●○○  **InjectHtml** — Negativ-Befund mit Lehrwert: HTML in Message()-Dialogen wird vom Client escaped und als Klartext angezeigt — HTML-Injection in Standard-Dialoge funktioniert nicht. Wer klickbare Inhalte will, braucht ein ControlAddIn, den WebPageViewer oder Hyperlink().
- ●○○  **GoogleCharts** — Die Scripts-Property akzeptiert direkte HTTPS-CDN-URLs neben lokalen Dateien — Google Charts laden ohne die Library zu bundeln. AL uebergibt eine JsonArray-of-Arrays exakt im Format von google.visualization.arrayToDataTable.
- ●○○  **Wav file from BC** — Binaerdateien in purem AL erzeugen: OutStream.Write auf Byte/Integer schreibt ROHE Little-Endian-Bytes (keinen Text!). Das Demo baut einen kompletten RIFF/WAV-Header plus 16-bit-PCM-Sinustoene — und zeigt den Trick, einen Integer per Temp-Blob-Roundtrip in Einzelbytes zu zerlegen, weil AL keinen Short-Typ hat.
- ●○○  **JavaScriptWorkBench** — Eine JS-REPL im laufenden BC-Client: unsichtbares 1x1-Addin mit Execute(Code) das eval() aufruft, Fehler und Ausgaben kommen ueber ein Error-Event zurueck in ein Seitenfeld. Als CardPart in jede Seite einhaengbar — perfekt, um DOM und Client-Verhalten live zu erforschen.

---

## PoorManControlAddin

**Technik:** Das eingebaute "Microsoft.Dynamics.Nav.Client.WebPageViewer" als Instant-ControlAddIn: beliebiges HTML per SetContent rendern und Klicks/Werte ueber WebPageViewerHelper.TriggerCallback nach AL zurueckmelden — ganz ohne eigenes controladdin-Objekt und JS-Dateien.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** Demo auf BC 21 / runtime 10.0

```al
pageextension 50100 CustomerListExt extends "Customer List"
{
    layout
    {
        addfirst(content)
        {
            usercontrol(Html; "Microsoft.Dynamics.Nav.Client.WebPageViewer")
            {
                ApplicationArea = All;
                trigger ControlAddInReady(callbackUrl: Text)
                begin
                    CurrPage.Html.SetContent(
                      '<button onclick="window.parent.WebPageViewerHelper.TriggerCallback(''clicked'');">' +
                      'Click Me!</button>');
                    // oder ein <textarea> mit OnChange-Callback: liefert den Textinhalt an AL
                end;

                trigger Callback(data: Text)
                begin
                    Message(data); // Daten aus dem HTML zurueck in AL
                end;
            }
        }
    }
}
```

**Fallstricke:** Callback transportiert genau ein Text-Argument — komplexe Daten selbst als JSON-Text serialisieren. SetContent ersetzt den kompletten Inhalt. Das Addin ist offiziell fuer Webseiten gedacht; die Helper-API ist undokumentiert, funktioniert aber seit Jahren stabil.

---

## Dynamic HTML Render

**Technik:** Minimales generisches HTML-Render-Addin: eine einzige Prozedur Render(HTML: Text), das HTML wird serverseitig in AL gebaut (TextBuilder/Konkatenation) und per insertAdjacentHTML in den controlAddIn-Div gesetzt. Grundmuster fuer jede eigene HTML-Vorschau (Belege, LV, Tabellen mit Farblogik).

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
controladdin HTML
{
    // startup.js: HTMLContainer = document.getElementById("controlAddIn");
    //             Microsoft.Dynamics.NAV.InvokeExtensibilityMethod("ControlReady",[]);
    // scripts.js: function Render(html){ HTMLContainer.insertAdjacentHTML('beforeend', html); }
    StartupScript = 'startup.js';
    Scripts = 'scripts.js';
    HorizontalStretch = true;
    VerticalStretch = true;
    RequestedHeight = 400;
    event ControlReady();
    procedure Render(HTML: Text);
}

page 50100 "Dynamic HTML Rendering"
{
    layout
    {
        area(Content)
        {
            usercontrol(html; HTML)
            {
                trigger ControlReady()
                begin
                    // HTML in AL bauen: '<table>' + ... + '</table>'
                    CurrPage.html.Render(CreateTable(10, 8));
                end;
            }
        }
    }
}
```

**Fallstricke:** insertAdjacentHTML('beforeend', ...) HAENGT AN statt zu ersetzen — wiederholtes Render() stapelt den Inhalt; fuer Updates vorher innerHTML leeren. Erst nach dem ControlReady-Event darf AL Prozeduren rufen, sonst laufen sie ins Leere. Inline-Styles funktionieren, externe Ressourcen nur ueber StyleSheets-Property.

---

## ScannerApp1

**Technik:** Keyboard-Wedge-Barcodescanner ohne Fokus-Feld abfangen: ein unsichtbares 1x1-Pixel-Addin registriert einen keydown-Listener auf window.parent (dem ganzen BC-Client!) und unterscheidet Scanner von Mensch per Tipp-Tempo — Zeichen im Abstand <100ms gelten als Scan und werden per preventDefault vor BC-Feldern versteckt.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** platform 16.0 / runtime 5.0

```al
controladdin ScannerInterface
{
    MaximumHeight = 1; MinimumHeight = 1; MaximumWidth = 1; MinimumWidth = 1;
    HorizontalShrink = true; VerticalShrink = true;
    RequestedHeight = 1; RequestedWidth = 1;
    StartupScript = 'Scanner.js';
    event Scanned(Barcode: Text);
}
// Scanner.js (Kern):
// window.parent.addEventListener('keydown', event => {
//   Ziffern (keyCode>=48) mit <100ms Abstand -> Buffer aufbauen, sonst Buffer neu;
//   schnelles Enter (13) -> preventDefault + auf Terminator warten;
//   Terminator 'J' (74)  -> InvokeExtensibilityMethod('Scanned',[Buffer]); Buffer=''; });

// Auf der Seite:
usercontrol(Scanner; ScannerInterface)
{
    ApplicationArea = All;
    trigger Scanned(Barcode: Text)
    var
        ScanRec: Record "Scanned Data";
    begin
        ScanRec.Init();
        ScanRec.Data := CopyStr(Barcode, 1, MaxStrLen(ScanRec.Data));
        ScanRec.Insert(true); // Entry No. per AutoIncrement
        CurrPage.Update(false);
    end;
}
```

**Fallstricke:** Die Zeitfenster (100/200ms) und der Suffix 'J' (keyCode 74, als Scanner-Terminator konfiguriert) sind auf den konkreten Scanner abgestimmt — ohne konfigurierten Suffix feuert das Scanned-Event nie. String.fromCharCode(keyCode) liefert nur Grossbuchstaben/Ziffern; keyCode ist eine deprecated Browser-API. Der window.parent-Zugriff klappt nur, weil das Addin-iframe same-origin ist.

---

## Point of Sale

**Technik:** Komplette Kasse auf Standard-Verkaufsrechnung: unsichtbares Scanner-Addin + Zustandsautomat (Option-Variable) auf der Page — ein Scan legt den Beleg an, weitere Scans erhoehen Mengen oder legen Zeilen an, und Zahlungsarten haben selbst Barcodes, sodass der Zahlungs-Scan direkt bucht. Muster fuer jede Schnellerfassungs-Maske auf Standardbelegen.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** BC 24 / runtime 13.0, mit Uebersetzungen (de-AT!)

```al
usercontrol(Scanner; ScannerInterface)
{
    trigger Scanned(Barcode: Text)
    begin
        case PosStatus of
            PosStatus::"Awaiting new Receipt":
                begin
                    NewReceipt(); // Sales Header (Invoice) anlegen, Cash-Kunde aus POS Setup validieren
                    if Item.Get(Barcode) then ScanItem(Item);
                end;
            PosStatus::"Receipt Active":
                if Item.Get(Barcode) then
                    ScanItem(Item) // Zeile existiert: Validate(Quantity, Quantity+1); sonst neue Sales Line (+10000)
                else
                    if PM.Get(Barcode) then // Zahlungsart traegt selbst einen Barcode!
                        PayAndPost(PM);
        end;
    end;
}

local procedure PayAndPost(PM: Record "Payment Method")
var
    Post: Codeunit "Sales-Post";
begin
    Rec.Validate("Payment Method Code", PM.Code);
    Rec.Modify(true);
    Post.SetSuppressCommit(true);
    Post.Run(Rec);
    Page.Run(Page::"Point of sale"); // Seite neu starten = sauberer Reset
end;
```

**Fallstricke:** Der auskommentierte Code verraet: In-Place-Reset nach dem Buchen (Filter zuruecksetzen, Status umschalten, SetFocus) hat nicht funktioniert — Hougaard startet stattdessen die ganze Seite neu per Page.Run. Sales-Post mit SetSuppressCommit(true) fuer Kassen-Tempo. Zeilensuche erst auf Item filtern, bei Neuanlage Filter zuruecksetzen (SetRange ohne Argument), sonst zaehlt FindLast die Line No. falsch. AboutTitle/AboutText liefern die eingebaute Teaching-Tour gratis.

---

## BarcodeAddIn

**Technik:** Der Standard-Weg fuer Kamera-Scans in der BC-Mobile-App: eingebautes usercontrol BarcodeScannerProviderAddIn (Namespace System.Device) mit Trigger BarcodeReceived — kein eigenes JS, kein Scanner-Timing, funktioniert mit der Geraetekamera.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** BC 25 / runtime 14.0, Namespace-Syntax

```al
namespace MyPublisher.Scanning;

using Microsoft.Sales.Customer;
using System.Device;

pageextension 50100 CustomerListExt extends "Customer List"
{
    layout
    {
        addfirst(content)
        {
            usercontrol(BarCode; BarcodeScannerProviderAddIn)
            {
                ApplicationArea = All;
                Visible = true;
                trigger BarcodeReceived(Barcode: Text; Format: Text)
                begin
                    Message(Barcode); // Format nennt die Symbologie (EAN, QR, ...)
                end;
            }
        }
    }
}
```

**Fallstricke:** Funktioniert nur in der BC-Mobile-App (Telefon/Tablet), nicht im Desktop-Browser — dort bleibt das Control stumm. Fuer Desktop-Scanner (Keyboard-Wedge) braucht es weiterhin das ScannerApp1-Muster; beide ergaenzen sich.

---

## camera

**Technik:** Zwei Wege zum Foto in AL ohne jedes JS: Codeunit Camera (ein Aufruf, Bild als InStream) fuer den Schnellfall, Page Camera fuer Kontrolle ueber Qualitaet, Encoding und Nachbearbeitung durch den Benutzer.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** BC 20 / runtime 9.0

```al
// Weg 1: Codeunit Camera — minimal
if Camera.IsAvailable() then
    if Camera.GetPicture(InS, FileName) then begin
        Rec.Picture.CreateOutStream(OutS); // Blob-Feld
        CopyStream(OutS, InS);
        Rec.Modify();
    end;

// Weg 2: Page Camera — mit Optionen
if CameraPage.IsAvailable() then begin
    CameraPage.SetAllowEdit(true); // Benutzer darf zuschneiden
    CameraPage.SetEncodingType("Image Encoding"::PNG);
    CameraPage.SetQuality(10); // 1..100 — klein halten fuer Baustellen-Uploads
    CameraPage.RunModal();
    if CameraPage.HasPicture() then begin
        CameraPage.GetPicture(InS);
        Rec.Picture.CreateOutStream(OutS);
        CopyStream(OutS, InS);
        Rec.Modify();
    end;
end;
```

**Fallstricke:** IsAvailable() immer zuerst pruefen — je nach Client (Browser vs. Mobile-App) ist keine Kamera erreichbar und GetPicture wuerde scheitern. SetQuality wirkt nur auf komprimierende Formate; die Kombination PNG + Quality 10 im Demo ist widerspruechlich (PNG ist verlustfrei).

---

## CameraPart2

**Technik:** Kamera-Bild ohne Blob-Umweg direkt in ein Media-Feld: Camera.GetPicture liefert den InStream, Media.ImportStream speichert ihn im Tenant-Media-Store — zwei Zeilen statt Stream-Kopiererei.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** BC 25 / runtime 14.0, Namespace-Syntax

```al
using System.Device;

trigger OnOpenPage()
var
    Camera: Codeunit Camera;
    InS: InStream;
    PictureName: Text;
begin
    if Camera.IsAvailable() then begin
        if Camera.GetPicture(InS, PictureName) then begin
            Rec.Image.ImportStream(InS, PictureName); // Media-Feld direkt befuellen
            Rec.Modify();
        end;
    end else
        Message('Boo, no camera!');
end;
```

**Fallstricke:** ImportStream verlangt keinen CalcFields-Tanz wie Blob — Media-Felder sind Referenzen, kein Inhalt im Record. Der zweite Parameter ist der Anzeigename des Mediums, nicht der Dateiname auf Platte.

---

## location

**Technik:** GPS-Position des Geraets in AL abfragen: Codeunit Geolocation mit RequestGeolocation (loest die Berechtigungsabfrage aus), HasGeolocation und GetGeolocation — fertig fuer Geo-Stempel auf Rapporten oder Baustellen-Ankunft.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** BC 20 / runtime 9.0

```al
trigger OnOpenPage()
var
    GeoLocation: Codeunit Geolocation;
    Latitude, Longitude : Decimal;
begin
    GeoLocation.SetHighAccuracy(true);
    if GeoLocation.RequestGeolocation() then
        if GeoLocation.HasGeolocation() then begin
            GeoLocation.GetGeolocation(Latitude, Longitude);
            Message('I see you at %1,%2', Latitude, Longitude);
        end;
end;
```

**Fallstricke:** RequestGeolocation ist ein Dialog-Roundtrip — der Browser/die App fragt den Benutzer um Erlaubnis; Ablehnung liefert einfach false, kein Fehler. SetHighAccuracy(true) vor dem Request setzen. Zwei-Schritt-Pruefung (Request erfolgreich UND HasGeolocation) noetig.

---

## Gantt

**Technik:** Gantt-Diagramm aus Projekt (Job) und Projektaufgaben (Job Task) mit der lokal gebundelten dhtmlxGantt-Library: AL baut das data/links-JSON, JS ist nur gantt.init + gantt.parse. Direkt das Muster fuer Bauzeitplaene.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** BC 23 / runtime 12.0; dhtmlxGantt GPL-Edition gebundelt

```al
controladdin gantt
{
    Scripts = 'gantt/dhtmlxgantt.js', 'gantt/gantt.js'; // gantt.js: function Load(d){ gantt.parse(d); }
    StartupScript = 'gantt/startup.js'; // gantt.config.date_format="%Y-%m-%d %H:%i"; gantt.init("controlAddIn");
    StyleSheets = 'gantt/dhtmlxgantt.css';
    VerticalStretch = true; HorizontalStretch = true;
    event ControlReady();
    procedure Load(Data: JsonObject);
}

// AL: Job/Job Task -> dhtmlx-Format { data: [...], links: [...] }
NullValue.SetValueToNull(); // echtes JSON-null fuer Sammelknoten
Project.Add('id', 1); Project.Add('text', JobRec.Description);
Project.Add('start_date', NullValue); Project.Add('duration', NullValue);
Project.Add('parent', 0); Project.Add('open', true);
Tasks.Add(Project);
// je Posting-Task:
Task.Add('start_date', JobTask."Start Date");
Task.Add('duration', JobTask."End Date" - JobTask."Start Date" + 1); // Datumsdifferenz = Tage
Task.Add('parent', ParentId);
Out.Add('data', Tasks); Out.Add('links', Links);
CurrPage.Gantt.Load(Out);
```

**Fallstricke:** Hougaards eigener Kommentar im Code: "This won't work, do better Erik!!!" — die Parent-Zuordnung aus Indentation via 'id - 1' ist falsch, sobald Begin-Total-Gruppen mehr als eine Aufgabe enthalten; wer die Hierarchie will, muss einen Parent-Stack ueber die Indentation-Ebenen fuehren. JsonValue.SetValueToNull() ist der einzige Weg zu echtem JSON-null. Datumssubtraktion zweier Dates liefert Integer-Tage.

---

## image

**Technik:** Bildbearbeitung in purem AL mit Codeunit Image: FromStream laden, Metadaten lesen (Breite/Hoehe/Format), Crop, Resize, RotateFlip und Formatkonvertierung via SetFormat — z.B. Baustellenfotos vor dem Speichern verkleinern, ohne externen Dienst.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
var
    Img: Codeunit Image;
    TempBlob: Codeunit "Temp Blob";
    InS: InStream;
    OutS: OutStream;
    FileName: Text;
begin
    if UploadIntoStream('Upload Image', '', '', FileName, InS) then begin
        Img.FromStream(InS);
        Message('%1 x %2, Format %3', Img.GetWidth(), Img.GetHeight(), Img.GetFormat());

        Img.Crop(100, 100, 100, 100); // x, y, Breite, Hoehe
        Img.Resize(Round(Img.GetWidth() * 0.5, 1), Round(Img.GetHeight() * 0.5, 1));
        Img.RotateFlip("Rotate Flip Type"::Rotate270FlipX);
        Img.SetFormat("Image Format"::Gif); // Konvertierung beim Save

        TempBlob.CreateOutStream(OutS);
        Img.Save(OutS);
        TempBlob.CreateInStream(InS);
        DownloadFromStream(InS, '', '', '', 'out.gif');
    end;
end;
```

**Fallstricke:** Deckt auch den Ordner ImageManipulation ab (Resize/RotateFlip/SetFormat) — dessen Demo enthaelt uebrigens ein verwaistes 'Image.' vor DownloadFromStream, das so nicht kompiliert: die Dateien sind Video-Skizzen, kein Copy-Paste-Material. Crop nimmt (x, y, Breite, Hoehe) ab der linken oberen Ecke. Temp Blob als Zwischenpuffer ist das Standardmuster fuer Save+Download.

---

## mediaref

**Technik:** Media-Felder sind Referenzen in den Tenant-Media-Store, keine Kopien — deshalb laesst sich ein Media-Wert per FieldRef von Tabelle zu Tabelle ZUWEISEN: Bild in einen temporaeren Record importieren, dann FR.Value := TempRec.Image auf die Zieltabelle.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
action(UploadMedia)
{
    trigger OnAction()
    var
        TempVendor: Record Vendor temporary; // beliebige Tabelle mit Media-Feld als Import-Vehikel
        InS: InStream;
        FileName: Text;
        Ref: RecordRef;
        FR: FieldRef;
    begin
        if UploadIntoStream('Get Image', '', '', FileName, InS) then begin
            TempVendor.Init();
            TempVendor.Image.ImportStream(InS, ''); // Inhalt landet trotzdem im Tenant-Media-Store
            TempVendor.Insert();

            Ref.GetTable(Rec); // Ziel: Customer
            FR := Ref.Field(Rec.FieldNo(Image));
            FR.Value := TempVendor.Image; // Media-REFERENZ zuweisen — kein Stream-Kopieren
            Ref.Modify(true);
        end;
    end;
}
```

**Fallstricke:** ImportStream auf einem temporary Record schreibt den Inhalt trotzdem persistent in den Media-Store — nur die Referenz ist fluechtig. Wer solche Vehikel-Records massenhaft nutzt, hinterlaesst verwaiste Tenant-Media-Eintraege. FieldRef macht das Muster tabellen-generisch (z.B. Fotos an beliebige Belege haengen).

---

## URLControl

**Technik:** Chrome-loses BC-Popup mit vorgefiltertem Datensatz: GetUrl mit Record-Parameter und true haengt die aktuellen Filter an die URL, URL-Schalter (showribbon=0, shownavigation=0, showuiparts=0, showheader=0) blenden die Client-Huelle aus ⚠⚠ **BERICHTIGT 01.09.2026 (B): Hier stand „undokumentierte URL-Schalter". DAS IST WIDERLEGT** — MS dokumentiert sie regulaer (*Web client URL*, Abschnitt URL parameters, und *Embed Business Central Web Client in Other Websites*): „showribbon — Specifies whether to show the action bar on pages when they open … To hide the action bar, use showribbon=0". Sie sind also **zugesichert**, nicht geduldet, ein unsichtbares Addin oeffnet das Ganze per window.open.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** BC 22 / runtime 11.0

```al
controladdin popup
{
    MaximumHeight = 1; MinimumHeight = 1; MaximumWidth = 1; MinimumWidth = 1;
    HorizontalShrink = true; VerticalShrink = true;
    RequestedHeight = 1; RequestedWidth = 1;
    Scripts = 'script.js'; // function popup(URL){ window.open(URL,'_blank','toolbar=0,location=0,menubar=0,width=500,height=750'); }
    procedure popup(URL: Text);
}

action(PopupAction)
{
    trigger OnAction()
    var
        URL: Text;
        Rec2: Record Customer;
    begin
        Rec2.SetFilter(Name, 'B*');
        URL := GetUrl(ClientType::Current, CompanyName,
                      ObjectType::Page, Page::"Customer List", Rec2, true); // true = Filter in die URL!
        URL += '&mode=View&captionhelpdisabled=0&showribbon=0' +
               '&shownavigation=0&showuiparts=0&showheader=0&redirect=0';
        CurrPage.popup.popup(URL);
    end;
}
```

**Fallstricke:** Der letzte GetUrl-Parameter (true) ist der wenig bekannte Filter-Mitnehmer. Die show*-Parameter sind undokumentiert/unsupported — Microsoft kann sie jederzeit kippen. window.open aus einem Addin faellt unter Popup-Blocker-Regeln des Browsers; aus einer direkten Benutzeraktion heraus aufrufen.

---

## Wysiwyg - Streams

**Technik:** Dieselbe CKEditor-Integration, aber Speicherung in einem Blob-Feld statt Text[2048] — unbegrenzte Laenge, dazu Import/Export des HTML per Upload-/DownloadFromStream.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** platform 16.0 / runtime 5.0

```al
trigger OnAfterInit()
var
    InS: InStream;
    Txt: Text;
begin
    Rec.CalcFields("Description Blob"); // Blob VOR CreateInStream immer laden
    Rec."Description Blob".CreateInStream(InS);
    InS.ReadText(Txt);
    CurrPage.EditCtl.Load(Txt);
end;

trigger SaveRequested(data: Text)
var
    OutS: OutStream;
begin
    Rec."Description Blob".CreateOutStream(OutS);
    OutS.WriteText(data);
end;

// Export als Datei:
Rec.CalcFields("Description Blob");
Rec."Description Blob".CreateInStream(InS);
DownloadFromStream(InS, '', '', '', Rec.Description + '.html');
```

**Fallstricke:** InStream.ReadText liest nur bis zum ersten Zeilenumbruch — bei mehrzeiligem HTML verschwindet alles ab Zeile 2 (CKEditor liefert meist einzeilig, deshalb faellt es im Demo nicht auf). Nach dem OutStream-Write fehlt im Demo das Rec.Modify — der Blob lebt sonst nur im Seitenpuffer. CalcFields vor jedem Blob-Streamzugriff ist Pflicht.

---

## Wysiwyg

**Technik:** CKEditor als Rich-Text-Editor im Client mit sauberer Event-Choreografie: ControlReady -> Init() baut den Editor asynchron, ein EIGENES OnAfterInit-Event signalisiert "jetzt darfst du laden", ContentChanged -> RequestSave -> SaveRequested(data) bringt den HTML-Inhalt zurueck ins Feld. Blaupause fuer jedes zustandsbehaftete JS-Widget.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** platform 16.0 / runtime 5.0; CKEditor 5 gebundelt

```al
controladdin Wysiwyg
{
    HorizontalStretch = true; MinimumHeight = 300; RequestedHeight = 300;
    Scripts = 'Editor/Scripts/ckeditor.js', 'Editor/Scripts/MainScript.js';
    StartupScript = 'Editor/Scripts/startupScript.js';
    RecreateScript = 'Editor/Scripts/recreateScript.js'; // gibt es auch!
    RefreshScript = 'Editor/Scripts/refreshScript.js';
    event ControlReady();
    event OnAfterInit();
    event ContentChanged();
    event SaveRequested(data: Text);
    procedure Init();
    procedure Load(data: Text);
    procedure RequestSave();
    procedure SetReadOnly(readonly: Boolean);
}

usercontrol(EditCtl; Wysiwyg)
{
    trigger ControlReady()   begin CurrPage.EditCtl.Init(); end;
    trigger OnAfterInit()
    begin
        EditorReady := true;
        CurrPage.EditCtl.Load(Rec."Item Description");
        CurrPage.EditCtl.SetReadOnly(not CurrPage.Editable); // Seitenmodus spiegeln!
    end;
    trigger ContentChanged() begin CurrPage.EditCtl.RequestSave(); end;
    trigger SaveRequested(data: Text)
    begin
        Rec."Item Description" := CopyStr(data, 1, MaxStrLen(Rec."Item Description"));
    end;
}
// + trigger OnAfterGetRecord(): if EditorReady then begin EditorReady := false; CurrPage.EditCtl.Init(); end;
```

**Fallstricke:** Load() direkt nach ControlReady schlaegt fehl — CKEditor baut asynchron, daher das selbstgebaute OnAfterInit. Beim Datensatzwechsel (OnAfterGetRecord) muss der Editor komplett neu initialisiert werden, sonst zeigt er den alten Inhalt. ContentChanged feuert bei JEDEM Tastendruck einen Server-Roundtrip — fuer Produktion drosseln. SetReadOnly(not CurrPage.Editable) ist der einzige Weg, den View-Modus der Seite ins Addin zu tragen.

---

## JavascriptModules

**Technik:** ES-Module in ControlAddIns schmuggeln: Die Scripts-Property laedt alles als klassisches Script (ES-Module brechen dort) — der Trick ist, die Modul-Datei als Images-Ressource zu deklarieren und im Startup-Script per dynamischem import(Microsoft.Dynamics.NAV.GetImageResource(...)) zu laden. So laufen moderne Web-Components (hier: deep-chat) in BC.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** BC 27 / runtime 16.0

```al
controladdin DeepChat
{
    Scripts = 'deepchat/script.js';
    StartupScript = 'deepchat/startup.js';
    Images = 'deepchat/deepchat.js'; // ES-Modul als "Image"-Ressource!
    VerticalStretch = true; HorizontalStretch = true;
    event ControlReady();
    procedure Init();
}
// startup.js:
// import(Microsoft.Dynamics.NAV.GetImageResource('deepchat/deepchat.js'));
// Microsoft.Dynamics.NAV.InvokeExtensibilityMethod("ControlReady",[]);
// script.js:
// function Init() {
//   document.getElementById("controlAddIn").innerHTML =
//     `<deep-chat demo="true" ...></deep-chat>`; // Web-Component nutzbar
// }

page 50100 "Deep Chat Test"
{
    PageType = UserControlHost; // Addin bekommt die ganze Seite
    layout { area(Content) {
        usercontrol(deepchat; DeepChat)
        {
            trigger ControlReady()
            begin
                CurrPage.deepchat.Init();
            end;
        }
    } }
}
```

**Fallstricke:** GetImageResource liefert eine URL auf jede als Images deklarierte Datei — die Property prueft den Dateityp nicht, sie ist ein generischer Ressourcen-Kanal. Dynamisches import() umgeht die fehlende type=module-Option der Scripts-Property. Achtung Timing: das import ist asynchron, ControlReady feuert hier VOR Modul-Fertigstellung — wer sofort auf die Component zugreift, braucht ein await/then.

---

## Charts.css

**Technik:** Balkendiagramme voellig ohne Chart-JavaScript: das CSS-Framework charts.css macht aus einer nackten HTML-Tabelle ein Chart — die StyleSheets-Property laedt das CSS vom CDN, AL baut nur die Tabelle mit --size-CSS-Variablen per TextBuilder.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** BC 26 / runtime 15.0, PageType UserControlHost

```al
controladdin chartcss
{
    MinimumHeight = 200; MinimumWidth = 200;
    VerticalStretch = true; HorizontalStretch = true;
    StyleSheets = 'https://cdn.jsdelivr.net/npm/charts.css/dist/charts.min.css', // CDN auch fuer CSS!
                  'chartscss.css';
    StartupScript = 'chartscss-startup.js';
    Scripts = 'chartscss-functions.js'; // function Render(html){ HTMLContainer.insertAdjacentHTML('beforeend',html); }
    procedure Render(html: Text);
    event ControlReady();
}

trigger ControlReady()
var
    HtmlBuilder: TextBuilder;
begin
    HtmlBuilder.AppendLine('<table class="charts-css column">');
    HtmlBuilder.AppendLine('<tbody>');
    // je Datenpunkt: --size erwartet einen Anteil 0..1!
    HtmlBuilder.AppendLine('<tr><td style="--size: 0.46">46</td></tr>');
    HtmlBuilder.AppendLine('</tbody></table>');
    CurrPage.chart.Render(HtmlBuilder.ToText());
end;
```

**Fallstricke:** --size erwartet normierte Werte 0..1 — das Demo schiebt rohe Sales-Betraege hinein, was nur zufaellig aussieht wie ein Chart; vorher durch das Maximum teilen. PageType = UserControlHost gibt dem Addin die ganze Seite. Decimal.ToText() liefert kulturabhaengige Formate — fuer CSS immer Punkt-Dezimal erzwingen (Format(x,0,9)).

---

## ControlAddInHeightHack

**Technik:** Der notorische Hoehen-Hack: ein ControlAddIn-iframe bekommt vom BC-Client keine dynamische Hoehe — das Startup-Script greift per window.parent auf das umgebende 'control-addin-form'-Div zu und setzt die eigene iframe-Hoehe darauf, inkl. resize-Listener.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
controladdin testaddin
{
    StartupScript = 'startup.js';
    Scripts = 'script.js', 'raphael.js', 'flowchart-latest.js';
    HorizontalStretch = true;
    VerticalStretch = true; // reicht allein NICHT — daher der Hack:
    event ImAmReady(Parameters: JsonObject);
    procedure Draw(code: Text);
}
// startup.js — der eigentliche Hack (same-origin macht's moeglich):
// var h = window.parent.document.querySelector('div[class~="control-addin-form"]');
// if (h != null) {
//     window.frameElement.style.height = h.offsetHeight + "px";
//     window.addEventListener('resize', ev => {
//         window.frameElement.style.height = h.offsetHeight + "px";
//     }, true);
// }
```

**Fallstricke:** Undokumentiert und an einen internen CSS-Klassennamen ('control-addin-form') gekettet — jedes Client-Update kann ihn umbenennen, dann faellt das Addin auf Minihoehe zurueck; deshalb der null-Check. Offizielle Alternative bleibt RequestedHeight (statisch). Gleicher Hack steckt im Mermaid-Ordner — Hougaard brauchte ihn offenbar staendig.

---

## Mermaid

**Technik:** Text-zu-Diagramm live im Client: Mermaid vom CDN laden, ein MultiLine-Textfeld mit OnValidate ruft Draw(code), JS rendert per mermaid.mermaidAPI.render den Mermaid-Code zu SVG in den Addin-Container. Dazu das Muster, einem AL-Event ein JsonObject aus JS mitzugeben.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** BC 21 / runtime 10.0; Mermaid 9.3 vom CDN

```al
controladdin testaddin
{
    StartupScript = 'startup.js'; // mermaid.initialize({ startOnLoad: false });
    Scripts = 'script.js', 'https://cdnjs.cloudflare.com/ajax/libs/mermaid/9.3.0/mermaid.min.js';
    HorizontalStretch = true; VerticalStretch = true;
    event ImAmReady(Parameters: JsonObject); // JS kann Events MIT Payload feuern
    procedure Draw(code: Text);
}
// script.js:
// function Draw(code) {
//   mermaid.mermaidAPI.render('chart', code, svg =>
//     document.getElementById('controlAddIn').innerHTML = svg);
// }

// Seite: Editor-Feld + Live-Vorschau
field(TheCode; TheCode)
{
    MultiLine = true;
    trigger OnValidate()
    begin
        CurrPage.x.Draw(TheCode);
    end;
}
```

**Fallstricke:** startOnLoad:false ist Pflicht, sonst rendert Mermaid beim Laden ins Leere. Das Event ImAmReady zeigt: InvokeExtensibilityMethod('Event',[jsObjekt]) kommt in AL als echtes JsonObject an — Objekte, verschachtelt, alles dabei. Der Ordner enthaelt auch eine generische Rec2Json/Json2Rec-Codeunit via RecordRef (FlowFields werden mit CalcField mitgenommen) — nuetzlich, um jeden Record ans JS zu geben.

---

## BusinessCharts

**Technik:** Charts komplett ohne eigenes JS: eingebautes usercontrol "Microsoft.Dynamics.Nav.Client.BusinessChart" plus temporaerer Record "Business Chart Buffer" — Measures anlegen, X-Achse setzen, Werte per Index fuellen, Update. Sogar gemischte Chart-Typen (Column + Pie) je Measure und Klick-Events inklusive.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** platform 16.0 / runtime 5.0; Addin existiert bis heute

```al
usercontrol(Chart; "Microsoft.Dynamics.Nav.Client.BusinessChart")
{
    ApplicationArea = All;
    trigger AddInReady()
    var
        Buffer: Record "Business Chart Buffer" temporary;
        Customer: Record Customer;
        i: Integer;
    begin
        Buffer.Initialize();
        Buffer.AddMeasure('Sales', 1, Buffer."Data Type"::Decimal, Buffer."Chart Type"::Column);  // Index 0
        Buffer.AddMeasure('Profit', 1, Buffer."Data Type"::Decimal, Buffer."Chart Type"::Pie);    // Index 1
        Buffer.SetXAxis('Customer', Buffer."Data Type"::String);
        if Customer.FindSet() then
            repeat
                Customer.CalcFields("Sales (LCY)", "Profit (LCY)");
                if Customer."Sales (LCY)" <> 0 then begin
                    Buffer.AddColumn(Customer.Name);
                    Buffer.SetValueByIndex(0, i, Customer."Sales (LCY)");
                    Buffer.SetValueByIndex(1, i, Customer."Profit (LCY)");
                    i += 1;
                end;
            until Customer.Next() = 0;
        Buffer.Update(CurrPage.Chart);
    end;

    trigger DataPointClicked(point: JsonObject)
    begin
        // point liefert Measure + X-Wert -> eigenen Drilldown bauen
    end;
}
```

**Fallstricke:** Das Event heisst hier AddInReady (nicht ControlReady). SetValueByIndex adressiert (MeasureIndex, ZeilenIndex) — der Zeilenindex muss selbst mitgezaehlt werden und startet bei 0. Der Buffer MUSS temporary sein. DataPointClicked liefert ein JsonObject, kein Record — Drilldown ist Handarbeit.

---

## AppIsAlsoAWebPage

**Technik:** Klickbarer Weblink als Seitenfeld ohne Addin: ein Label-Feld mit ShowCaption=false und OnDrillDown -> Hyperlink() macht aus jedem Card-Bereich einen Link (Hilfe, Doku, Portal).

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
pageextension 50123 CustomerCardExt extends "Customer Card"
{
    layout
    {
        addlast(General)
        {
            field(HelpLinkCtl; HelpLink)
            {
                ApplicationArea = All;
                ShowCaption = false;
                Editable = false;
                trigger OnDrillDown()
                begin
                    Hyperlink('https://example.com/help');
                end;
            }
        }
    }
    var
        HelpLink: Label 'Get more help, we really need help!';
}
```

**Fallstricke:** Der Ordner enthaelt zusaetzlich eine komplette Kopie von Microsofts Azure-OpenAI-/EntityText-Implementierung (IsolatedStorage mit DataScope::Module, Privacy-Notice-Subscriber, Retry-Schleife mit Backoff) — als Lesestoff wertvoll, gehoert aber thematisch nicht zu diesem Video.

---

## InjectHtml

**Technik:** Negativ-Befund mit Lehrwert: HTML in Message()-Dialogen wird vom Client escaped und als Klartext angezeigt — HTML-Injection in Standard-Dialoge funktioniert nicht. Wer klickbare Inhalte will, braucht ein ControlAddIn, den WebPageViewer oder Hyperlink().

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** BC 25 / runtime 14.0

```al
trigger OnOpenPage()
begin
    Message('App published: <a href="#">Hello</a> world');
    // Ausgabe: der Tag erscheint woertlich als Text —
    // der Web-Client escaped HTML in Message/Confirm/Error konsequent.
end;
```

**Fallstricke:** Gilt fuer Message, Confirm und Error gleichermassen. Einzige Formatierung in Dialogen: \ als Zeilenumbruch. Das ist zugleich die Sicherheitszusage des Clients — Benutzereingaben in Fehlermeldungen koennen kein Markup einschleusen.

---

## GoogleCharts

**Technik:** Die Scripts-Property akzeptiert direkte HTTPS-CDN-URLs neben lokalen Dateien — Google Charts laden ohne die Library zu bundeln. AL uebergibt eine JsonArray-of-Arrays exakt im Format von google.visualization.arrayToDataTable.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** platform 16.0 / runtime 5.0

```al
controladdin GoogleCharts
{
    StartupScript = 'charts/startup.js';
    Scripts = 'charts/script.js', 'https://www.gstatic.com/charts/loader.js'; // CDN-URL direkt!
    HorizontalStretch = true; VerticalStretch = true;
    event ControlReady();
    procedure RunSomeCode(Data: JsonArray);
}
// script.js: google.charts.load('current',{packages:['corechart']});
//            drawChart: new google.visualization.PieChart(document.getElementById('controlAddIn'))
//                       .draw(google.visualization.arrayToDataTable(json), options);

trigger ControlReady()
var
    Customer: Record Customer;
    Data, Row : JsonArray;
begin
    Customer.SetAutoCalcFields("Sales (LCY)");
    Row.Add('Customer'); Row.Add('Sales'); // Kopfzeile zuerst
    Data.Add(Row);
    if Customer.FindSet() then
        repeat
            Clear(Row);
            Row.Add(Customer.Name);
            Row.Add(Customer."Sales (LCY)");
            Data.Add(Row);
        until Customer.Next() = 0;
    CurrPage.Chart.RunSomeCode(Data);
end;
```

**Fallstricke:** CDN-Script heisst: Der Client-Browser braucht Internet und Google-Erreichbarkeit — in abgeschotteten Umgebungen bricht das Addin still. JsonArray in JsonArray kommt drueben als echtes verschachteltes Array an. SetAutoCalcFields spart das CalcFields in der Schleife.

---

## Wav file from BC

**Technik:** Binaerdateien in purem AL erzeugen: OutStream.Write auf Byte/Integer schreibt ROHE Little-Endian-Bytes (keinen Text!). Das Demo baut einen kompletten RIFF/WAV-Header plus 16-bit-PCM-Sinustoene — und zeigt den Trick, einen Integer per Temp-Blob-Roundtrip in Einzelbytes zu zerlegen, weil AL keinen Short-Typ hat.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)

```al
// Integer -> 2 Bytes (AL hat kein 16-bit-Write):
procedure IntegerToShort(Value: Integer; var b1: Byte; var b2: Byte)
var
    Mem: Codeunit "Temp Blob";
    InS: InStream;
    OutS: OutStream;
begin
    Mem.CreateOutStream(OutS);
    OutS.Write(Value);        // schreibt 4 Bytes little-endian
    Mem.CreateInStream(InS);
    InS.Read(b1);             // die 2 niederwertigen Bytes
    InS.Read(b2);             // wieder herauslesen
end;

// Sample-Erzeugung (16-bit PCM):
// s := Round(Ampl * Math.Sin(t * Freq * 2.0 * Math.PI), 1);
// IntegerToShort(s, s1, s2); Writer.Write(s1); Writer.Write(s2);

// Header: Magic-Numbers als Integer schreiben ('RIFF' = 1179011410 usw.),
// Short-Felder als Byte + Null-Byte:
// Writer.Write(RIFF); Writer.Write(fileSize); Writer.Write(WAVE); ...
// am Ende Header-Blob + Daten-Blob per CopyStream hintereinanderhaengen,
// DownloadFromStream(InS, '', '', '', 'sound.wav');
```

**Fallstricke:** Die Kern-Erkenntnis: OutStream.Write ist TYPISIERT — Integer wird als 4-Byte-Binaerwert geschrieben, nicht als Ziffernfolge; wer Text will, braucht WriteText. Da Header-Laenge von der Datenlaenge abhaengt, werden Daten erst in einen eigenen Temp Blob geschrieben und der Header danach davor gesetzt. Uebertragbar auf jedes Binaerformat.

---

## JavaScriptWorkBench

**Technik:** Eine JS-REPL im laufenden BC-Client: unsichtbares 1x1-Addin mit Execute(Code) das eval() aufruft, Fehler und Ausgaben kommen ueber ein Error-Event zurueck in ein Seitenfeld. Als CardPart in jede Seite einhaengbar — perfekt, um DOM und Client-Verhalten live zu erforschen.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** platform 16.0 / runtime 5.0

```al
controladdin Workbench
{
    MaximumHeight = 1; MaximumWidth = 1; MinimumHeight = 1; MinimumWidth = 1;
    HorizontalShrink = true; VerticalShrink = true;
    RequestedHeight = 1; RequestedWidth = 1;
    Scripts = 'Workbench/workbench.js';
    StartupScript = 'Workbench/startup.js';
    event ControlReady();
    procedure Execute(Code: Text);
    event Error(ErrorTxt: Text);
}
// workbench.js: function Execute(code){ try { eval(code); }
//   catch(e){ Microsoft.Dynamics.NAV.InvokeExtensibilityMethod('Error',[e.toString()]); } }
// Helfer: show(x) / showall(x) melden Werte ueber denselben Error-Kanal,
// showall nutzt JSON.stringify mit WeakSet-Replacer gegen zirkulaere Referenzen.

page 56122 Workbench // CardPart
{
    // field(Code): MultiLine, OnValidate -> CurrPage.JS.Execute(CodeTxt);
    // field(Error): Editable=false zeigt GlobalErrorTxt;
    // usercontrol(JS; Workbench): trigger Error(ErrorTxt) -> GlobalErrorTxt := ErrorTxt;
}
```

**Fallstricke:** Ein MultiLine-Textfeld feuert OnValidate erst beim Verlassen des Felds — das ist hier der "Run"-Knopf. eval() im Addin-iframe sieht window.parent (den ganzen Client) — maechtig fuers Debugging, ein Sicherheits-Albtraum in Produktion. Der WeakSet-Circular-Replacer ist das wiederverwendbare Snippet fuer JSON.stringify beliebiger DOM-Objekte.

---

## Übersprungen (bewusst)

- 3D graphics in javascript — WebGL-Spielerei ohne ERP-Lehrwert (belegt nur: 15 lokale JS-Libs + Fullscreen-Canvas laufen im Addin)
- Calendar — unfertige Skizze (kompiliert nicht, kein JS-Kalender)
- Media Test — trivialer Feld-Stub
- mediaset — unfertige Skizze (abgebrochene Codezeile)
- ImageManipulation — im image-Topic mitbehandelt
- workflowchart — nur app.json, kein Code
- GenericChart — Aufruf-Stub ohne Kern (referenzierte Page fehlt im Ordner)
- Color Picker — redundantes Addin-Muster (jscolor-Input, nichts Neues gegenueber anderen Topics)
- Wysiwyg - Streams-Ordner doppelt NICHT geskippt (eigenes Topic)
- BorderShine — fragiler DOM/CSS-Hack (Klassensuche in window.parent-Stylesheets, bricht bei jedem Client-Update)

