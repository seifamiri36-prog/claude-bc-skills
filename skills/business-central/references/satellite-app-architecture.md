# Architektur: Ein BC-Hub, viele kleine Satelliten-Apps

Das ist das eigentliche Produktkonzept hinter den kommenden Projekten: statt eines monolithischen Frontends, das versucht, ganz BC nachzubauen, bekommt jede Rolle/jeder Prozess **ihre eigene kleine App** mit modernem UI — angebunden über die APIs aus `bc-api-integration.md`.

## Grundprinzip: eine App = ein Job-to-be-done

Bevor Code entsteht, den Scope einer neuen App scharf schneiden:

- **Wer** nutzt sie? (eine Rolle, nicht "alle")
- **Welcher eine Prozess** wird abgedeckt? (nicht "Verwaltung", sondern z. B. "Tagesrapport erfassen")
- **Welche BC-Daten** braucht diese Rolle wirklich zu sehen? (nicht der ganze Datensatz — siehe `$select` in `bc-api-integration.md`)
- **Welche BC-Aktionen** soll diese Rolle auslösen können? (das bestimmt, ob eine Custom-API-Page mit `BoundAction` nötig ist)

Wenn eine "App-Idee" mehrere Rollen/Prozesse gleichzeitig abdecken will, ist das ein Signal, sie in mehrere kleine Apps aufzuteilen statt eine große zu bauen.

## Warum viele kleine Apps statt einer großen

- **UX**: Eine App mit 5 Buttons für eine Rolle schlägt eine App mit 50 Menüpunkten für alle Rollen — besonders mobil.
- **Deployment/Iteration**: Eine kleine App lässt sich unabhängig von den anderen updaten, testen, sogar für einzelne Kunden anpassen.
- **Rechte/Sicherheit**: Jede App braucht nur die Entra-ID-Scopes/BC-Permissions ihrer eigenen Rolle — kleinere Angriffsfläche als eine App mit Zugriff auf alles.
- **Time-to-Value**: Eine fokussierte App ist in Tagen/Wochen baubar, nicht Monaten — wichtig, wenn mehrere solcher Apps pro Kunde entstehen sollen.

## Gemeinsame Basis, damit das skaliert

Damit nicht jede neue App die BC-Anbindung neu erfindet:

- Eine dünne, gemeinsame API-Client-Schicht (Auth-Handling, Base-URLs, Fehlerbehandlung) — pro Kunde/BC-Umgebung einmal bauen, in jeder App wiederverwenden.
- Ein gemeinsames Design-System/Component-Set für "cooles UI", damit alle Satelliten-Apps eines Kunden wie eine Familie aussehen, auch wenn sie unterschiedliche Prozesse abdecken.
- Konsistente Auth-Strategie über alle Apps (siehe Entra-ID-Abschnitt in `bc-api-integration.md`) — nicht pro App neu entscheiden.

## Mobil vs. Desktop — eine UX-Entscheidung, kein Zwang

Nicht jede App muss auf beiden Plattformen existieren. Die Plattform folgt der Arbeitssituation der Rolle:

| Rollentyp | Typische Plattform | Warum |
|---|---|---|
| Vor Ort/unterwegs (Baustelle, Lager, Außendienst) | Mobil-first, offline-tolerant | Kein Schreibtisch, oft schwache Verbindung |
| Büro/Sachbearbeitung (Einkauf, Buchhaltung) | Desktop/Web | Mehrere Fenster, Tastatur-Workflows, längere Sitzungen |
| Führung/Überblick | Beides, aber leichtgewichtig (Dashboard-artig) | Kurze Check-ins, nicht Dateneingabe |

## Tech-Stack — bewusst offen gehalten

Diese Skill schreibt keinen festen Stack vor, weil das pro Projekt/Kunde variiert. Gängige, sinnvolle Optionen als Ausgangspunkt für die Diskussion mit dem Nutzer:

- **Mobil**: React Native oder Flutter für native Cross-Platform-Apps; eine PWA, wenn App-Store-Deployment vermieden werden soll.
- **Desktop/Web**: eine moderne Web-App (React/Vue/Svelte) reicht meistens — Electron nur, wenn echte Desktop-OS-Integration nötig ist (Dateisystem, Tray, Offline-first mit lokaler DB).
- **API-Schicht**: entweder die App spricht direkt gegen BC-APIs (einfacher, weniger Komponenten), oder es gibt eine dünne eigene Backend-Schicht dazwischen (sinnvoll, wenn mehrere Apps dieselbe aufbereitete Sicht auf BC-Daten brauchen, oder wenn Business-Logik nicht in AL, sondern näher am Frontend leben soll).

Bei jedem neuen Projekt diese Entscheidung explizit mit dem Nutzer treffen, statt eine Standardwahl anzunehmen.

## Ablauf beim Entwurf einer neuen Satelliten-App

1. Rolle + einen Prozess festlegen (siehe oben).
2. BC-Datenbedarf klären: reicht Standard-API v2.0, oder braucht es eine Custom-API-Page? → `bc-api-integration.md`.
3. Plattform (mobil/Desktop/beides) aus der Arbeitssituation der Rolle ableiten, nicht raten.
4. Auth-Scope für genau diese Rolle festlegen (nicht "Admin-Zugriff, weil einfacher").
5. UI so schlank wie möglich halten — die Versuchung, "während wir schon dabei sind" weitere Funktionen reinzupacken, aktiv zurückweisen. Das widerspricht dem ganzen Sinn des Musters.

Ein konkretes durchgespieltes Beispiel (Bau-Branche) steht in `construction-industry-example.md`.
