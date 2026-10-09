# Referenzbeispiel: BC-Anpassung für die Bau-Branche

> ℹ **Begriffshinweis:** „Baustelle“ wird unten umgangssprachlich benutzt (Ort der Arbeit,
> im Gegensatz zum Büro). In einem realen Datenmodell ist das meist ein definierter Begriff —
> ein *Bauprojekt* kann mehrere Baustellen haben. Wer aus diesem Beispiel ein Modell
> ableitet, definiert den Begriff zuerst.

Dieses Beispiel stammt aus einem Gespräch mit dem Nutzer, der eine BC-Anpassung für die Bau-Branche als Illustration genannt hat — **als Muster zu verstehen, nicht als fertige Spezifikation**. Wenn ein reales Bau-Projekt ansteht, dieses Schema mit dem tatsächlichen Kunden abgleichen statt blind zu übernehmen. Dasselbe Rolle → App → BC-Daten/Aktionen-Schema lässt sich auf andere Branchen übertragen (siehe `satellite-app-architecture.md`).

## Warum Bau-Branche ein gutes Beispiel für das Muster ist

Bauunternehmen haben klar getrennte Rollen mit sehr unterschiedlichen Arbeitssituationen (Baustelle vs. Büro) und viele Prozesse, die heute oft noch auf Papier/Excel laufen, aber eigentlich direkt in ein ERP durchschlagen sollten — ideal für kleine, fokussierte Apps statt einer großen Software, die niemand auf der Baustelle benutzen will.

## Mögliche Rollen und ihre Apps

| Rolle | Arbeitssituation | Mögliche App | BC-Daten (lesen) | BC-Aktionen (auslösen) |
|---|---|---|---|---|
| Bauleiter / Poliere | Vor Ort, mobil, oft schlechte Verbindung | Baustellen-App | Projektstatus, Material-Sollbestand, offene Aufgaben | Tagesrapport erfassen, Materialbedarf melden, Foto/Mängel dokumentieren |
| Lager/Materialdisposition | Lagerhalle, teils mobil (Scanner) | Lager-App | Bestände, offene Materialanforderungen | Wareneingang buchen, Kommissionierung bestätigen |
| Einkauf | Büro | Einkaufs-App/-Dashboard | Lieferantenpreise, offene Bestellungen, Materialbedarfe aus dem Feld | Bestellung auslösen/freigeben |
| Bauleitung/Projektleitung (Führung) | Büro + unterwegs | Projekt-Cockpit | Projektfortschritt, Budget vs. Ist, offene Mängel | Freigaben erteilen (z. B. Nachtragsangebote) |
| Personal/Zeiterfassung | Baustelle, mobil | Zeiterfassungs-App | Zugewiesene Mitarbeiter je Projekt | Arbeitszeiten/Kommen-Gehen buchen |

Das ist eine Ausgangsliste, keine vollständige Aufzählung — reale Projekte bringen oft branchentypische Zusatzprozesse mit (z. B. Aufmaß, Nachträge, Gerätedisposition), die erst im Gespräch mit dem Kunden auftauchen.

## Wie sich das auf BC-Seite abbildet

- **Standarddaten** (Projekte/Jobs, Lieferanten, Bestellungen) laufen meist über BCs **Jobs/Projects**-Modul und die **Standard-API v2.0** — hier reicht oft die Standard-API ohne eigenen AL-Code.
- **Branchenspezifische Daten** (Tagesrapport, Mängelmeldung, Aufmaß) existieren in Standard-BC meist nicht 1:1 — dafür braucht es eigene Tables + Custom-API-Pages (siehe `al-extension-development.md` und `bc-api-integration.md`), z. B. ein Table "Baustellen Rapport" mit Feldern wie Baustellen-Code, Datum, Wetter, geleistete Stunden, Materialverbrauch.
- **Prozess-Trigger** (Freigaben, Statuswechsel) werden als `BoundAction` auf der jeweiligen Custom-API-Page modelliert, damit die App nicht nur Daten anzeigt, sondern echte BC-Workflows anstößt.

## Typischer Gesprächsleitfaden mit einem Bau-Kunden

Bei einem echten Projekt diese Fragen früh klären, statt das Rollenraster oben ungeprüft zu übernehmen:

1. Welche Prozesse laufen heute noch auf Papier/Excel/WhatsApp, die eigentlich BC-Daten erzeugen sollten?
2. Welche Rolle hätte den größten Hebel von einer eigenen App (oft: die, die am weitesten von einem Bürorechner entfernt arbeitet)?
3. Läuft BC bereits mit einem Projekt-/Jobs-Modul, oder muss das erst mit aufgebaut werden?
4. Gibt es bereits andere Extensions/Ranges in der BC-Umgebung, die bei der Objekt-ID-Vergabe zu berücksichtigen sind?

Mit den Antworten daraus eine priorisierte Liste "eine Rolle, eine App" ableiten, statt gleich alle Apps parallel zu planen.
