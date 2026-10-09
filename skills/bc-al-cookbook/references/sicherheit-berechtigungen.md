# Sicherheit, Berechtigungen & Geheimnisse

_Destilliert aus Erik Hougaards Youtube-Video-Sources (Ordnername = Videothema)._
_Vollquellen: https://github.com/hougaard/Youtube-Video-Sources (lokal klonen; Ordnername = Videothema)_

Dieser Cluster zeigt, wie BC-Berechtigungen wirklich funktionieren und wo sie truegen. Kernlehre: das Rechtemodell ist zweistufig — direkte vs. INDIREKTE Rechte (Klein-/Grossbuchstaben in Masken, die Permissions-Eigenschaft an Codeunits), und genau diese Indirektion ist der Hebel fuer kontrollierte Buchungswege auf sonst gesperrte Ledger-Tabellen. Mehrere Ordner sind Lehrvideos ueber Angriffsflaechen: der Change Log ist nicht manipulationssicher (Modify(false) umgeht ihn), "Namen nicht exponiert" schuetzt keine Tabelle (RecordRef.Open per ID), Install-Codeunits laufen erhoeht, und Extension-eigene Tabellen sind ein Geiselnahme-Risiko. Geheimnisse gehoeren in IsolatedStorage (verschluesselt), nicht in Tabellenfelder, und Maskierung ist nur Anzeigeschutz. Dazu praktische Bausteine: Feature-Gating ueber die "Access Control"-Tabelle, ein User-Admin-Cockpit ueber verstreute Setup-Tabellen und Standard-Hashing per "Cryptography Management".

**Wertvollste Ordner:** indirectpermissions · IsolatedStorage · custompermissions · BetterUserManagement · CheatTheChangeLog

## Themen (nach Praxis-Relevanz)

- ●●●  **indirectpermissions** — Die Permissions-Eigenschaft an einer Codeunit erhoeht die Rechte NUR fuer Code, der durch dieses Objekt laeuft (indirekte Rechte). Man braucht das immer, wenn Nutzer eine geschuetzte Tabelle nicht frei aendern duerfen, eine kontrollierte Aktion aber schon.
- ●●●  **custompermissions** — Aktionen/Features an die Mitgliedschaft in einem bestimmten Permission Set binden, indem man die Zuordnungstabelle "Access Control" (User <-> Role ID) abfragt. Nuetzlich fuer Rollen-Gating ohne eigene Rechtefelder.
- ●●●  **IsolatedStorage** — Geheimnisse (Passwoerter, API-Keys) in IsolatedStorage ablegen statt in ein Tabellenfeld, gebunden an eine ungebundene maskierte Page-Variable. Braucht man fuer jede Integration mit Zugangsdaten.
- ●●●  **BetterUserManagement** — Admin-Cockpit: eine Liste ueber Tabelle "User" mit ungebundenen Statusfeldern, die je Nutzer pruefen, welche verstreuten Setup-Saetze existieren (User Setup, Warehouse Employee, Resource, Employee, FA Journal Setup ...), und per OnDrillDown direkt dorthin springen.
- ●●○  **CheatTheChangeLog** — ⚠⚠ **KERNBEHAUPTUNG GEMESSEN WIDERLEGT 01.09.2026 (B)** — siehe Abschnitt unten. Hier stand: „der Change Log protokolliert nur, was durch die Tabellen-Trigger laeuft." Modify(false)/ModifyAll(...,false)/Delete(false) ueberspringen die Trigger und damit den Change Log - Audit ist nicht manipulationssicher.
- ●●○  **Hash Values** — Standard-Codeunit "Cryptography Management" fuer Hashes ohne Eigencode; auch einen ganzen Datensatz via Format(Record) hashen, z.B. zur Aenderungs-/Integritaetserkennung.
- ●●○  **FieldMasking** — Sensible Werte (Kreditkarte, IBAN) nur maskiert anzeigen: ein ungebundenes Control zeigt Sterne+letzte 4 Stellen, der Klartext bleibt im Record; nach jedem GetRecord und nach OnValidate wird neu maskiert.
- ●●○  **InstallPermissions** — Install-/Upgrade-Codeunits (Subtype = Install) laufen in erhoehtem/System-Kontext und duerfen Tabellen vorbelegen, die normaler Code und der Nutzer nicht anfassen duerfen - oft ueber RecordRef, wenn kein Symbol referenzierbar ist.
- ●●○  **RestrictedTable** — Tabellen, die man nicht per Namen referenzieren kann (Access = Internal in fremdem Modul), lassen sich zur Laufzeit ueber RecordRef.Open(<ID>) erreichen - zeigt, dass Compile-Zeit-Abschottung allein kein Schutz ist.
- ●●○  **PermissionAL** — PowerShell-Modul, das alte DB-Rechtetabellen ([Permission]/[Tenant Permission]) in moderne AL permissionset-Objekte konvertiert - lehrreich vor allem fuer die Maskensemantik und die Zielform, die jede Extension mitliefern sollte.
- ●○○  **Ransomware** — Defensive Lehre aus der Ransomware-Reihe: eine Extension besitzt ihre Tabellen und bringt eigene Permission Sets mit. Fremd-Apps bekommen volle Rechte auf ihre eigenen Objekte, und in App-Tabellen liegende Daten haengen am Lebenszyklus der App.
- ●○○  **FNVHash** — FNV-Hash in reinem AL inklusive selbstgebautem BitwiseXor per div/mod-Schleife - Zeitdokument aus einer Zeit ohne AL-Bitoperatoren; heute meist obsolet.

---

## indirectpermissions

**Technik:** Die Permissions-Eigenschaft an einer Codeunit erhoeht die Rechte NUR fuer Code, der durch dieses Objekt laeuft (indirekte Rechte). Man braucht das immer, wenn Nutzer eine geschuetzte Tabelle nicht frei aendern duerfen, eine kontrollierte Aktion aber schon.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)

```al
// Der Nutzer hat KEIN Direktrecht auf "G/L Entry".
// Permissions an der Codeunit hebt die Rechte an - aber NUR fuer Code,
// der durch diese Codeunit laeuft (= indirekte Rechte).
codeunit 50100 "Post Controlled"
{
    Permissions = tabledata "G/L Entry" = RM;   // erhoehtes Recht
    procedure Touch()
    var
        GLEntry: Record "G/L Entry";
    begin
        GLEntry.FindFirst();
        GLEntry.Description := 'Geaendert ueber kontrollierten Kanal';
        GLEntry.Modify();
    end;
}
// Im Permission Set des Nutzers reicht dann Execute auf die Codeunit;
// direkte tabledata-Rechte auf "G/L Entry" bleiben weg -> Nutzer kann
// die Tabelle NICHT frei aendern, nur diese eine Aktion ausloesen.
```

**Fallstricke:** Indirekt wirkt ausschliesslich durch das rechtetragende Objekt. Ruft die Codeunit Standard-Code auf, der wiederum modifiziert, muss die Kette luecklos indirekt gedeckt sein, sonst schlaegt die Laufzeitpruefung zu. Gross RIMDX = direkt, klein rimdx = indirekt.

> ⚠ **Ergänzung (B, 31.08.2026, bei Microsoft belegt — fehlt im Hougaard-Fundus):**
> **„Direct permissions override indirect permissions."** Ein großes D (direkt) aus
> EINEM eingebundenen Satz wird durch ein kleines d (indirekt) in einem anderen Satz
> NICHT entschärft — die weiteste direkte Gewährung gewinnt über alle Sätze des
> Benutzers. Wer die Wirkung eines Satzes beurteilt, liest deshalb ALLE Sätze des
> Kontos, nicht den einen. Und: „fremde Verkaufsbelege" sind SECHS Tabellen, deren
> Rechte sich IM SELBEN Satz unterscheiden können (Sales Header RIMD, Sales Invoice
> Line Rimd …) — die Frage je Tabelle aufzählen, nie als eine Größe behandeln.

---

## custompermissions

**Technik:** Aktionen/Features an die Mitgliedschaft in einem bestimmten Permission Set binden, indem man die Zuordnungstabelle "Access Control" (User <-> Role ID) abfragt. Nuetzlich fuer Rollen-Gating ohne eigene Rechtefelder.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** application 21, runtime 10 (NoImplicitWith); Mechanik seit jeher

```al
// Aktion nur fuer Mitglieder eines Permission Sets freigeben.
action(OnlyForTheFew)
{
    ApplicationArea = All;
    trigger OnAction()
    var
        AccessControl: Record "Access Control";
    begin
        AccessControl.SetRange("User Security ID", UserSecurityId());
        AccessControl.SetRange("Role ID", 'ABC-BAULEITER');
        if AccessControl.IsEmpty() then
            Error('Du bist nicht berechtigt.');
        // ... berechtigte Logik (z.B. Buchen)
    end;
}
// "Access Control" ist die Zuordnung User <-> zugewiesenes Permission Set.
```

**Fallstricke:** Prueft die ZUWEISUNG einer Rolle, nicht die tatsaechliche effektive Berechtigung (vererbte/zusammengesetzte Rechte werden nicht aufgeloest). SUPER-Nutzer taucht ggf. nicht mit jeder Role ID auf. ⚠ **UNBELEGT (Prüfung 01.09.2026, D+B):** Diese Aussage trägt **weder die Demo noch die MS-Doku** — sie ist nicht widerlegt, sondern **unbelegt**. ⚠ **Ein Arbeitspaket in `PLAN-A-Musterzuordnung` baut darauf: vor dem Bau am Bestand MESSEN, nicht übernehmen.** *(AP-1 Fundament: custompermissions)* Role ID ist der technische Set-Code, nicht der Caption.

---

## IsolatedStorage

**Technik:** Geheimnisse (Passwoerter, API-Keys) in IsolatedStorage ablegen statt in ein Tabellenfeld, gebunden an eine ungebundene maskierte Page-Variable. Braucht man fuer jede Integration mit Zugangsdaten.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** application 16, runtime 5.0 (IsolatedStorage ab BC15/16)

```al
// Kein Klartext-Feld: Secret liegt in IsolatedStorage, nicht in der Tabelle.
table 59300 "ISO Setup"
{
    fields { field(1; PKey; Code[10]) { } field(10; "User Name"; Text[30]) { } }
    procedure SetPassword(pw: Text)
    begin
        // Fuer echte Secrets VERSCHLUESSELT speichern:
        IsolatedStorage.SetEncrypted('password', pw, DataScope::Company);
    end;
    procedure GetPassword() pw: Text
    begin
        if not IsolatedStorage.Get('password', DataScope::Company, pw) then
            pw := '';
    end;
}
// Page: field an globale Text-Var binden, ExtendedDatatype = Masked,
// OnValidate ruft SetPassword, OnAfterGetRecord laedt GetPassword.
```

**Fallstricke:** Das Original-Demo nutzt IsolatedStorage.Set OHNE Verschluesselung - das ist Klartext auf dem Server; fuer Secrets zwingend SetEncrypted. DataScope steuert die Sichtbarkeit (Module/Company/User/CompanyAndUser); Company-Scope ist innerhalb der App lesbar. Das Feld pw ist ungebunden ([InDataSet] in alten Runtimes) - der Wert steht nie in der Tabelle.

---

## BetterUserManagement

**Technik:** Admin-Cockpit: eine Liste ueber Tabelle "User" mit ungebundenen Statusfeldern, die je Nutzer pruefen, welche verstreuten Setup-Saetze existieren (User Setup, Warehouse Employee, Resource, Employee, FA Journal Setup ...), und per OnDrillDown direkt dorthin springen.

**Praxis-Relevanz (Bau-ERP):** ●●● (3/3)  ·  **Version:** application 25, runtime 14

```al
page 50100 "User Management"
{
    PageType = List; SourceTable = User; Editable = false;
    UsageCategory = Administration;
    layout { area(Content) { repeater(g) {
        field("User Name"; Rec."User Name") { }
        field(WhCtl; Warehouse)              // ungebundenes Anzeigefeld
        {
            Editable = false; Caption = 'Warehouse';
            trigger OnDrillDown()
            var U: Record "Warehouse Employee";
            begin
                U.SetRange("User ID", Rec."User Name");
                Page.RunModal(Page::"Warehouse Employees", U);
            end;
        }
    } } }
    trigger OnAfterGetRecord() begin UpdateFlags(); end;
    local procedure UpdateFlags()
    var WhEmp: Record "Warehouse Employee";
    begin
        WhEmp.SetRange("User ID", Rec."User Name");
        if WhEmp.IsEmpty() then Warehouse := '❌' else Warehouse := '✅';
    end;
    var Warehouse: Text;
}
```

**Fallstricke:** Trotz Editable=false funktionieren die DrillDowns. Die Flags werden je Zeile in OnAfterGetRecord neu berechnet (mehrere IsEmpty-Abfragen pro Nutzer) - bei grossen User-Listen Performance beachten. Einige Setup-Tabellen verknuepfen ueber "User ID"=User Name, andere ueber "No." (Resource/Employee) - Schluesselfeld je Tabelle pruefen.

---

## CheatTheChangeLog

**Technik:** ⚠⚠ **BERICHTIGT 01.09.2026 (B) — MIT LAUFZEIT-BELEG, nicht aus Lektüre.** Hier stand: „der Change Log protokolliert nur, was durch die Tabellen-Trigger läuft; `Modify(false)` überspringt beides". **DAS IST GEMESSEN WIDERLEGT.** Lauf vom 01.09., Tabelle 1003, Setup `Some Fields`, Positivkontrolle bestanden:
> ```
> Modify()        -> Eintrag   (Default ist false!)
> Modify(false)   -> Eintrag
> Modify(true)    -> Eintrag
> Alt->Neu-Ketten lueckenlos: 0->11, 11->22, 22->33 auf Standard- UND Erweiterungsfeld
> ```
> **Der Change Log hängt am PLATTFORM-Trigger, nicht am Tabellen-Trigger:** `GlobalTriggerManagement:88-98` abonniert `Codeunit::"Global Triggers".OnDatabaseModify` und ruft dort `ChangeLogMgt.LogModification`. Der `RunTrigger`-Parameter steuert den *Tabellen*-Trigger und erreicht diese Ebene nicht.
>
> ⚠ **REICHWEITE — was der Lauf NICHT gemessen hat:** `ModifyAll(…, false)`, `Delete(false)`, `Rename` und `RecordRef.Modify` sind **UNGEMESSEN**. Der Mechanismus legt nahe, dass sie ebenso erfasst werden (es gibt `OnDatabaseDelete`/`OnDatabaseRename` parallel zu `OnDatabaseModify`) — **aber das ist eine Lesung, keine Messung, und genau dieser Unterschied hat diese Passage dreimal falsch werden lassen.**
>
> ⚠ **DRITTER FEHLER IN DIESER PASSAGE** — und der schwerste. Die ersten zwei betrafen ein Detail (`Modify(true)` sei der Default: falsch, der Default ist `false`); dieser betrifft die **Behauptung selbst**. Wer sich auf die alte Fassung verließ, hielt eine Compliance-Lücke für belegt, die es nicht gibt.

Hier stand: „Defensive Lehre: der Change Log protokolliert nur, was durch die Tabellen-Trigger laeuft." Modify(false)/ModifyAll(...,false)/Delete(false) ueberspringen die Trigger und damit den Change Log - Audit ist nicht manipulationssicher.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** nutzt namespace/using -> runtime 13+/BC24-Syntax; Verhalten selbst versionsunabhaengig

```al
// ⚠⚠ BERICHTIGT 01.09.2026 (B), MIT LAUFZEIT-BELEG. Hier stand:
//     "LEHRE (defensiv): Change Log haengt an den Triggern.
//      RunTrigger = false umgeht Trigger UND Change Log."
// GEMESSEN WIDERLEGT: Modify(), Modify(false) und Modify(true) erzeugen ALLE DREI
// einen Change-Log-Eintrag (Lauf 01.09., Tabelle 1003, Positivkontrolle bestanden).
// Die Erfassung haengt am PLATTFORM-Trigger OnDatabaseModify
// (GlobalTriggerManagement:88-98), nicht am Tabellen-Trigger. Der RunTrigger-
// Parameter erreicht diese Ebene nicht.
// ⚠ UNGEMESSEN bleiben ModifyAll(...,false), Delete(false), Rename und
//   RecordRef.Modify - dort ist der Mechanismus dieselbe LESUNG, keine Messung.
// Der folgende Code UMGEHT den Change Log also NICHT.
Customer.Get('C00010');
Customer."Credit Limit (LCY)" := 8000;
Customer.Modify(false);        // -> KEIN Change-Log-Eintrag
// ebenso: Customer.ModifyAll("Credit Limit (LCY)", 8000, false);
// und der RecordRef-Weg Ref.Modify() ohne Trigger.
//
// Konsequenz: Change Log ist KEIN revisionssicheres Audit.
// Schutz: Execute-Rechte eng vergeben, kritische Aenderungen ueber
// kontrollierte Codeunits mit Modify(true) leiten, fuer echte
// Revisionssicherheit externes/DB-seitiges Auditing ergaenzen.
```

**Fallstricke:** ⚠⚠ **BERICHTIGT 01.09.2026 (B): Hier stand „Modify(true) ist der Default“. DAS IST DAS GEGENTEIL DER DOKU.** MS *Record.Modify([Boolean]) Method*: „If this parameter is **false (default)**, then the code in the OnModify trigger is not executed.“ **Der Default ist FALSE.** ⚠ Damit ist die Falle **schlimmer als bisher beschrieben**: nicht erst ein explizit gesetztes `false` umgeht den Change Log, sondern schon das **schlichte `Modify()` ohne Parameter** — der häufigste Aufruf im Code überhaupt. Auch DeleteAll(false) und der RecordRef.Modify()-Weg entkommen. Wer Change Log als Compliance-Nachweis (z.B. bei Rechnungen) verkauft, muss diese Luecke kennen.

---

## Hash Values

**Technik:** Standard-Codeunit "Cryptography Management" fuer Hashes ohne Eigencode; auch einen ganzen Datensatz via Format(Record) hashen, z.B. zur Aenderungs-/Integritaetserkennung.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
var
    Crypt: Codeunit "Cryptography Management";
    Hash: Text;
begin
    // Algorithmus-Nr.: 0=MD5, 1=SHA1, 2=SHA256, 3=SHA384, 4=SHA512
    Hash := Crypt.GenerateHashAsBase64String(InputText, 2);   // SHA256, Base64
    // Ganzen Datensatz als Fingerabdruck:
    Customer.FindFirst();
    Hash := Crypt.GenerateHash(Format(Customer), 2);
end;
```

**Fallstricke:** Format(Record) ist von Feldreihenfolge, Formatierung und Kultur abhaengig - als stabiler Fingerabdruck riskant; besser definierte Felder gezielt konkatenieren. MD5/SHA1 (0/1) nur fuer Pruefsummen, nie fuer Sicherheit. Fuer Passwoerter Hash+Salt statt rohem Hash.

---

## FieldMasking

**Technik:** Sensible Werte (Kreditkarte, IBAN) nur maskiert anzeigen: ein ungebundenes Control zeigt Sterne+letzte 4 Stellen, der Klartext bleibt im Record; nach jedem GetRecord und nach OnValidate wird neu maskiert.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
pageextension 50100 MyCustomer extends "Customer Card"
{
    layout { addafter(Name) {
        field(CreditCardCtl; MaskedCreditCard)   // ungebunden an globale Var
        {
            ApplicationArea = All; Caption = 'Credit Card No.';
            trigger OnValidate()
            begin
                Rec.CreditCardNo := MaskedCreditCard;   // Eingabe -> echtes Feld
                MaskedCreditCard := PerformMasking();    // sofort re-maskieren
            end;
        }
    } }
    trigger OnAfterGetRecord() begin MaskedCreditCard := PerformMasking(); end;
    trigger OnAfterGetCurrRecord() begin MaskedCreditCard := PerformMasking(); end;
    procedure PerformMasking(): Text
    begin
        if StrLen(Rec.CreditCardNo) > 4 then
            exit('*************' + Rec.CreditCardNo.Substring(StrLen(Rec.CreditCardNo) - 3));
        exit('');
    end;
    var MaskedCreditCard: Text[50];
}
```

**Fallstricke:** Reiner ANZEIGE-Schutz. Der Klartext liegt weiter im Tabellenfeld -> in DB, Exporten, RapidStart und Change Log lesbar. Fuer echte Vertraulichkeit IsolatedStorage/Verschluesselung. ExtendedDatatype=Masked allein verdeckt nur die Eingabe, nicht den gespeicherten Wert.

---

## InstallPermissions

**Technik:** Install-/Upgrade-Codeunits (Subtype = Install) laufen in erhoehtem/System-Kontext und duerfen Tabellen vorbelegen, die normaler Code und der Nutzer nicht anfassen duerfen - oft ueber RecordRef, wenn kein Symbol referenzierbar ist.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)

```al
codeunit 50100 "Seed Setup"
{
    Subtype = Install;
    trigger OnInstallAppPerCompany()
    var
        Ref: RecordRef;
    begin
        Ref.Open(8912);              // z.B. "Email Rate Limit"
        if Ref.FindFirst() then begin
            Ref.Field(5).Value := 10;
            Ref.Modify();
        end;
    end;
}
// Nutzen: geschuetzte Setup-Tabellen bei Installation initialisieren.
```

**Fallstricke:** Dieselbe Erhoehung, die das Seeding ermoeglicht, macht Install-Code zum Angriffsvektor - Install-/Upgrade-Logik minimal und pruefbar halten. OnInstallAppPerCompany laeuft je Mandant, OnInstallAppPerDatabase einmal; bei RecordRef.Modify laufen Trigger nur mit Ref.Modify(true).

---

## RestrictedTable

**Technik:** Tabellen, die man nicht per Namen referenzieren kann (Access = Internal in fremdem Modul), lassen sich zur Laufzeit ueber RecordRef.Open(<ID>) erreichen - zeigt, dass Compile-Zeit-Abschottung allein kein Schutz ist.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** application 25, runtime 14; Demo liest Shopify-Connector-Tabelle 30114

```al
var
    Ref: RecordRef;
    FR: FieldRef;
begin
    Ref.Open(30114);            // interne Tabelle nur ueber ihre ID
    Ref.FindFirst();
    FR := Ref.Field(2);
    Message('%1', FR.Value);
end;
// LEHRE: "Name nicht exponiert" ist KEIN Schutz. Wirklich abschotten
// nur durch LAUFZEIT-Rechte: Access = Internal PLUS restriktive
// Permission Sets / InherentPermissions - sonst bleibt der
// RecordRef-per-ID-Weg offen.
```

**Fallstricke:** RecordRef.Open umgeht nur die Compile-Zeit-Namenssperre, nicht die Laufzeit-Rechtepruefung: ob der Zugriff gelingt, entscheidet das effektive Permission Set. Fazit fuer eigene sensible Tabellen: nie auf Access-Modifier allein verlassen, immer mit engen Rechten kombinieren.

---

## PermissionAL

**Technik:** PowerShell-Modul, das alte DB-Rechtetabellen ([Permission]/[Tenant Permission]) in moderne AL permissionset-Objekte konvertiert - lehrreich vor allem fuer die Maskensemantik und die Zielform, die jede Extension mitliefern sollte.

**Praxis-Relevanz (Bau-ERP):** ●●○ (2/3)  ·  **Version:** PowerShell-Migrationswerkzeug (sqlps), nicht AL - fuer Alt-DB-Rechte vor AL-Permissionsets

```al
// Zielform: ein AL permissionset-Objekt. Maskenbuchstaben:
//   Gross R I M D X = DIREKTE Rechte, klein r i m d x = INDIREKTE Rechte.
permissionset 50100 "ABC Bauleiter"
{
    Access = Public;
    Assignable = true;
    Caption = 'ABC Bauleiter';
    Permissions =
        tabledata "Sales Header" = RIMD,        // volle Direktrechte
        tabledata "G/L Entry"    = Rm,          // lesen direkt, aendern indirekt
        page   "Customer List"   = X,
        codeunit "Post Controlled" = X;
}
// Das Skript liest die DB-Spalten (Wert 1 = direkt -> Grossbuchstabe,
// 2 = indirekt -> Kleinbuchstabe) und schreibt genau diese Objekte.
```

**Fallstricke:** Der Spaltenwert 2 in der Permission-Tabelle bedeutet INDIREKT (Kleinbuchstabe), nicht 'mehr' als 1 - eine haeufige Fehldeutung. MenuSuite-Rechte lassen sich nicht in permissionset uebersetzen (werden uebersprungen). System-Objektrechte (Object Type 10) haben eigene, benannte IDs (z.B. 6110 Export-to-Excel).

---

## Ransomware

**Technik:** Defensive Lehre aus der Ransomware-Reihe: eine Extension besitzt ihre Tabellen und bringt eigene Permission Sets mit. Fremd-Apps bekommen volle Rechte auf ihre eigenen Objekte, und in App-Tabellen liegende Daten haengen am Lebenszyklus der App.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)  ·  **Version:** application 19, runtime 8; altes XML-Permissionset-Format (extensionsPermissionSet.xml)

```al
// LEHRE (defensiv, kein Angriffscode): App-eigene Tabelle + App-eigenes
// Permission Set = App kontrolliert die Daten vollstaendig.
permissionset 50148 "Ransomware"
{
    Assignable = true;
    Permissions = tabledata ImportantTable = RIMD,   // App darf alles
                  table ImportantTable = X,
                  page "Important Data" = X;
}
// Risiken: (1) BERICHTIGT 01.09.2026 (B): Hier stand "Deinstallation der App loescht ihre
//     Tabellendaten mit." DAS IST DAS GEGENTEIL DER DOKU. MS "Install and uninstall
//     extensions (apps) in Business Central": "By default, when you uninstall an app that
//     you've been using your data isn't deleted." Und: "When an extension is
//     uninstalled, its data remains in your database by design."
//     Geloescht wird erst mit "Delete Extension Data" bzw. -ClearSchema / Sync -Mode Clean.
//     Das echte Risiko ist die UMGEKEHRTE Richtung: die Daten BLEIBEN als verwaiste
//     Erweiterungsdaten liegen (Seite "Delete Orphaned Extension Data").
// (2) Eine kostenpflichtige App kann Daten 'verschluesselt' als Geisel
//     halten. Schutz: fremde Apps + ihre Permission Sets vor Install
//     pruefen, geschaeftskritische Daten in EIGENEN Tabellen halten,
//     Exporte/Backups ausserhalb der App fahren.
```

**Fallstricke:** Daten in Tabellen einer Extension werden bei ForceSync/Uninstall mit dem Datenmodell entfernt - Kundendaten nie ausschliesslich in einer fremden App-Tabelle. Das mitgelieferte Permission Set einer App zeigt, wie weit ihre Rechte reichen; vor Zustimmung lesen. ransomware2/ransomware3 sind die zugehoerigen Folge-Demos (abhaengige App bzw. Neuauflage).

---

## FNVHash

**Technik:** FNV-Hash in reinem AL inklusive selbstgebautem BitwiseXor per div/mod-Schleife - Zeitdokument aus einer Zeit ohne AL-Bitoperatoren; heute meist obsolet.

**Praxis-Relevanz (Bau-ERP):** ●○○ (1/3)

```al
// Selbstgebautes XOR, weil aeltere AL-Runtimes keine Bitoperatoren hatten:
local procedure BitwiseXor(A: BigInteger; B: BigInteger): BigInteger
var Result: BigInteger; Bit: BigInteger; i: Integer;
begin
    Bit := 1;
    for i := 1 to 32 do begin
        if (A mod 2) <> (B mod 2) then Result += Bit;
        A := A div 2; B := B div 2;
        if i < 32 then Bit += Bit;
    end;
    exit(Result);
end;
// Kern der Schleife: hash := hash * konstante; hash := BitwiseXor(hash, Byte);
// mod 2^32 als Ueberlauf-Klammer.
```

**Fallstricke:** Neuere BC-Runtimes koennen XOR/AND/OR direkt - der ganze Workaround entfaellt. Definitionsfalle im Demo: die Konstante 2166136261 wird 'fnv_prime' genannt, ist aber der FNV-OFFSET-BASIS (die Prime ist 16777619); es 'stimmt' nur, weil der hartkodierte Erwartungswert darauf getrimmt wurde. Fuer Sicherheit ungeeignet (FNV ist ein Nicht-Krypto-Hash).

---

## Übersprungen (bewusst)

- Password — nur Message-Stub
- StealTheSecret — leere Codeunit
- BadActor — trivialer Message-Stub, Lehre nur im Video
- ransomware2 — kein AL-Code (nur app.json)
- ransomware3 — Duplikat von Ransomware
- TrustedApps — Recommended-Apps-Feature, Sicherheits-Randthema

