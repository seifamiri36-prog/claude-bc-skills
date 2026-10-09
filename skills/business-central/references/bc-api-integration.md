# BC-Daten & Prozesse per API ansprechen

Das ist die Brücke zwischen dem BC-Backend und den kleinen Satelliten-Apps: Business Central ist API-first gebaut, jede App (mobil oder Desktop) sollte gegen diese APIs sprechen — nicht gegen die BC-UI oder eine direkte DB-Verbindung.

> ### ⚠ ZUERST LESEN: hier läuft es lokal, nicht in der Cloud
>
> **Alles weiter unten zu Entra ID, OAuth2 und `api.businesscentral.dynamics.com` gilt für
> BC Online.** Für einen lokalen Docker-Container (BcContainerHelper, NavUserPassword-Auth)
> gilt stattdessen:
>
> ```
> Basis (eigene APIs)     http://<container>:7048/BC/api/<publisher>/<gruppe>/v1.0
> Basis (Standard-API)    http://<container>:7048/BC/api/v2.0
> Instanzname             BC          (steht im Pfad, wird gern vergessen)
> Port 7048               API/OData.  Port 80 ist der WEB-CLIENT, nicht die API.
> Mandant                 ?tenant=default   an JEDE URL, auch an jede selbstgebaute
> Auth                    Basic (Benutzer + Passwort), NICHT Entra ID / OAuth2
> ```
>
> ```powershell
> $cred = New-Object System.Management.Automation.PSCredential('<benutzer>', $sicher)
> Invoke-RestMethod -Uri "$basis/companies?tenant=default&`$select=id,name" `
>                   -Credential $cred -AllowUnencryptedAuthentication
> ```
>
> ⚠ `-AllowUnencryptedAuthentication` ist nötig, **weil die Verbindung `http` ist** — Basic
> Auth ohne TLS. Das ist für eine lokale Sandbox vertretbar und **für einen Kunden nicht.**
>
> ⚠ **Den Container-NAMEN als Host benutzen, nicht die Container-IP** — sie wechselt.
> Und `?tenant=default` fehlt in selbstgebauten URLs regelmäßig; die Antwort ist dann ein
> Fehler, der wie ein Rechteproblem aussieht.


## Zwei Wege, Daten/Aktionen zu exponieren

### 1. Standard-API v2.0 (OData v4)

Microsoft liefert für Kernentitäten (Customer, Item, SalesOrder, Vendor, …) fertige API-Endpunkte, ohne dass dafür AL-Code geschrieben werden muss:

```
# Cloud (Kunden-Tenant):
GET https://api.businesscentral.dynamics.com/v2.0/{tenant}/{environment}/api/v2.0/companies({companyId})/customers

# Lokale Sandbox (das hier ist der Alltag):
GET http://<container>:7048/BC/api/v2.0/companies?tenant=default
```

Gut für: Standardentitäten, schneller Einstieg, wenn die Satelliten-App nur Standarddaten braucht.

### 2. Custom API-Pages (AL)

Wenn eine App eigene Felder, eigene Entitäten oder eigene **Aktionen** (nicht nur CRUD) braucht, wird eine eigene API-Page definiert:

```al
// Gekürztes Beispiel aus einem realen Bau-ERP-Projekt (Tagesrapport-API)
page 50028 "Site Report API"
{
    PageType = API;
    Caption = 'Site Reports';
    APIPublisher = 'meinefirma';
    APIGroup = 'report';
    APIVersion = 'v1.0';
    EntityName = 'siteReport';
    EntitySetName = 'siteReports';
    SourceTable = "Site Report Header";
    ODataKeyFields = SystemId;
    DelayedInsert = true;

    // Lesend offen, schreibend ausschliesslich ueber die Bound Action submitReport.
    // Ohne diese Sperre liesse sich der Status eines abgeschlossenen Rapports per PATCH
    // direkt zurueck auf Entwurf setzen - oder ohne SubmitReport auf Abgeschlossen,
    // wodurch "Submitted DateTime" leer bliebe und OnAfterSubmitReport nie feuert.
    Editable = false;
    InsertAllowed = false;
    ModifyAllowed = false;

    layout { area(content) { repeater(General) {
        field(id; Rec.SystemId) { }
        field(status; Rec.Status) { }
        // ...
    } } }
}
```

⚠ **Zwei Dinge an diesem Beispiel sind kein Zufall:**

1. **Die Objekt-ID stammt aus dem eigenen Range** (hier 50000–50999). **Eine freie ID wird
   geprüft, nicht erinnert** — gegen den **Quelltext** *und* gegen den **Container**; der
   Schnappschuss in `bc28-objektinventar.txt` taugt dafür **nicht** (siehe dessen Warnkopf).
2. **Schreibend zu ist der Normalfall, nicht die Ausnahme.** Eine offene API-Page hat hier
   schon einmal eine Statussperre umgangen: Was die UI verbietet, erlaubt die API, solange
   niemand sie zusperrt. Schreibzugriff läuft über eine **Bound Action**, die die Regel
   mitbringt — nicht über freies `PATCH`.


Aktionen (Prozesse anstoßen, nicht nur Daten lesen/schreiben) werden als `BoundAction`/`UnboundAction` auf einer API-Page oder einem API-Query definiert — das ist der Mechanismus, mit dem eine App z. B. "Rapport abschließen" oder "Bestellung freigeben" direkt in BC auslösen kann.

Gut für: alles, was über Standard-CRUD hinausgeht — eigene Branchenlogik (z. B. Bau-Rapporte), eigene Prozess-Trigger.

## Authentifizierung — **Cloud-Teil, für einen späteren Kunden-Tenant**

⚠ **Gilt NICHT für die lokale Sandbox** (dort Basic Auth, siehe Kasten oben).
In BC Online laufen die APIs über **Microsoft Entra ID** (früher Azure AD), nicht über eigene BC-Logins:

1. App-Registrierung in Entra ID anlegen (Client-ID, Client-Secret oder Zertifikat).
2. API-Berechtigungen für Dynamics 365 Business Central hinzufügen.
3. Je nach App-Typ:
   - **Client Credentials Flow** (App-zu-App, kein Nutzerkontext) — passend für Server-Jobs, Integrationen, Hintergrundprozesse.
   - **Delegated/Auth-Code Flow** (Nutzer meldet sich an) — passend für die Satelliten-Apps selbst, wenn Aktionen einem konkreten BC-Benutzer zugeordnet werden sollen (z. B. "wer hat den Rapport abgeschlossen").
4. Access Token im `Authorization: Bearer <token>`-Header an die API-Requests hängen.

Bei mehreren kleinen Apps: überlegen, ob eine gemeinsame App-Registrierung mit rollenbasierten Scopes sinnvoller ist als eine Registrierung pro App — hält die Entra-ID-Verwaltung überschaubar.

## Die Automation-API — der dritte Weg, und er kann Dinge, die Cmdlets nicht können

Neben Standard-API und eigenen API-Pages gibt es die **Automation-API**: Verwaltungsobjekte
(Benutzer, Berechtigungssätze, Firmen, Extensions) statt Geschäftsdaten.

```
http://<container>:7048/BC/api/microsoft/automation/v2.0/companies({cid})/users({uid})/userPermissions({id})
```

**Gemessener Fall — einen Berechtigungssatz entziehen, als alles andere scheiterte:**

```
Lage      Der Benutzer war nach dem ersten Login UNLOESCHBAR
          („cannot be deleted because the user has been logged on" - BC-Regel).
          Remove-NAVServerUserPermissionSet scheiterte auf VIER Wegen.

Weg       DELETE  .../users({uid})/userPermissions({id})
          Header  If-Match: *
          Auth    admin, Basic  ->  „DELETE OK"

Belegt    25.08.2026 am lokalen BC-28-Container, mit unabhaengiger
          SQL-Gegenmessung (Satzliste, kein SUPER, Positivkontrolle).
```

⚠ **Zwei Nebenbefunde, die im Betrieb mehr wiegen als der Haupttreffer:**

1. **`admin` + Basic Auth kommt an der Automation-API durch.** Ein API-401 bei einem
   *anderen* Konto ist damit **konto- oder endpunktspezifisch, nicht global** — aus einem
   401 an einer Stelle darf man nicht auf gesperrte APIs schließen.
2. ⚠ **Eine Rechteänderung über diese API wirft die laufende Web-Session.** Gemessen: die
   offene Sitzung lief auf eine Fehlerseite und dann auf SignIn. **Betriebsregel:
   „Access-Control-Änderung wirft die Session"** — wer Rechte per API dreht, plant den
   Neu-Login ein, statt ihn als Störung zu erleben.

> ### ⚠ Warum du diese API im BC-Quelltext nicht findest
>
> Ein `grep` durch die **BaseApp**-Quelle (entpackter Standard-Quelltext) nach einer API-Page mit
> `Permission` im `EntitySetName` liefert **null Treffer** — und das ist **kein Beleg gegen
> die Existenz.** Die Automation-API liegt in der **Plattform / System Application**, nicht
> in der BaseApp. **Sie ist dort weder positiv noch negativ messbar.**
>
> Wer sie sucht, sucht am Endpunkt oder in Microsoft Learn, nicht im BaseApp-Quelltext.

**Weitere Automation-Entitäten** (gleicher Pfad): `companies`, `users`, `userGroups`,
`permissionSets`, `extensions`, `automationCompanies`. Vor Gebrauch am Endpunkt prüfen —
der Satz oben gilt: der Quelltext beantwortet die Frage nicht.

## Query-Optionen (klein & mobil-tauglich halten)

OData-Query-Parameter helfen, Antworten für schwache mobile Verbindungen schlank zu halten:

- `$select=id,siteCode,status` — nur benötigte Felder
- `$filter=status eq 'open'` — nur relevante Datensätze
- `$expand=lines` — verknüpfte Daten in einem Request statt mehrerer Roundtrips
- `$top=50` / `$skiptoken` — Paging für lange Listen

## Push statt Poll: Webhooks & Power Automate

Wenn eine App auf BC-Änderungen reagieren soll (z. B. Benachrichtigung, wenn ein Einkauf freigegeben wurde), sind Webhooks der bessere Weg als ständiges Pollen:
- BC unterstützt Standard-Webhooks (Subscription auf eine Entität, Callback-URL erhält Change-Notifications).
- Alternativ: Power Automate als No-Code-Bindeglied, wenn kein eigener Webhook-Endpunkt gebaut werden soll (z. B. direkt eine Push-Notification oder Teams-Nachricht auslösen).

## Praktischer Ablauf für eine neue Satelliten-App

1. Klären: reicht Standard-API v2.0, oder braucht es eine Custom-API-Page mit eigenen Aktionen? (→ ggf. zurück zu `al-extension-development.md`, denn Custom-API-Pages sind AL-Code, der in BC deployed werden muss.)
2. Auth festlegen — **lokal Basic Auth gegen den Container (Kasten oben), in BC Online Entra-ID-App-Registrierung + Auth-Flow.**
3. Response-Felder auf das Nötigste zuschneiden (`$select`), damit die App schlank bleibt.
4. Wenn die App reaktiv sein soll: Webhook/Power-Automate statt Polling einplanen.
5. Für BC-Prozess-Trigger (nicht nur Datenanzeige): passende `BoundAction` in der Custom-API-Page vorsehen.
