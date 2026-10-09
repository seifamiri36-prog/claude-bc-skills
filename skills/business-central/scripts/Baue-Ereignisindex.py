# Baue-Ereignisindex.py - erzeugt bc28-ereignisse.txt aus dem entpackten BC-Standard
#
# WOZU:
#   Die beiden SQL-Extrakte (Felder, Objekt-IDs) kennen keine EREIGNISSE - die sind
#   Code, keine Daten. Fuer "welche Felder hat X" ist Nachschlagen eine Sekunde;
#   fuer "woran kann ich mich haengen" braucht es diesen Index aus dem AL-Quelltext.
#
# AUFRUF:
#   python Baue-Ereignisindex.py [QUELLE] [ZIEL]
#     QUELLE  Ordner mit dem entpackten Standard-Quelltext (Vorgabe: C:\bcsrcfull)
#             - z. B. die mit BcContainerHelper / dem Symbol-Download ausgepackten
#               .app-Quellen der Base Application und System Application
#     ZIEL    Ausgabedatei (Vorgabe: ../references/bc28-ereignisse.txt neben diesem Skript)
#
# AUSGABEFORMAT:  Objekttyp ID "Name"|Ereignis|Art|Datei|Zeile|Signatur
#   Der Objektname traegt seine ANFUEHRUNGSZEICHEN, damit die Zeile ins Abo
#   kopierbar ist:  Codeunit::"Purch.-Post"
#
# ⚠ Liefert die Quelle 0 Dateien, bleibt der alte Index stehen - die Ausgabe nennt
#   die Dateizahl. Die Selbstpruefung am Ende meldet Indexzeilen OHNE Objektnamen;
#   steht dort nicht 0, ist der Index unbrauchbar und die Ursache gehoert geprueft.

import io, os, re, sys, time

sys.stdout.reconfigure(encoding="utf-8")

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = sys.argv[1] if len(sys.argv) > 1 else "C:\\bcsrcfull"
ZIEL = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HIER, "..", "references", "bc28-ereignisse.txt")

RE_OBJ = re.compile(
    r'^\s*(codeunit|table|page|report|xmlport|query|enum|interface|'
    r'tableextension|pageextension|reportextension|enumextension)\s+(\d+)\s+("([^"]+)"|[\w.]+)',
    re.I,
)
RE_ATTR = re.compile(r'^\s*\[(IntegrationEvent|InternalEvent|BusinessEvent)\s*\(', re.I)
RE_PROC = re.compile(
    r'^\s*(?:local\s+|internal\s+|protected\s+)?procedure\s+(\w+)\s*\((.*)$', re.I
)

if not os.path.isdir(WURZEL):
    sys.exit("Quelle nicht gefunden: %s" % WURZEL)

zeilen = []
dateien = gefunden = ohne_proc = ohne_objektkopf = 0
t0 = time.time()

for root, _, fs in os.walk(WURZEL):
    for fn in fs:
        if not fn.lower().endswith(".al"):
            continue
        p = os.path.join(root, fn)
        dateien += 1
        try:
            txt = io.open(p, encoding="utf-8-sig", errors="replace").read()
        except Exception:
            continue
        L = txt.split("\n")

        # ⚠ NICHT nur die ersten Zeilen: BC 28 stellt jeder Datei eine namespace-Zeile
        #   und beliebig viele using-Zeilen voran. Bei codeunit 90 "Purch.-Post" steht
        #   der Kopf weit dahinter - ein 60-Zeilen-Fenster liess 512 Dateien und 3.614
        #   Ereigniszeilen ohne Objektnamen, darunter die groessten Buchungscodeunits.
        typ = objid = name = ""
        for z in L:
            m = RE_OBJ.match(z)
            if m:
                typ = m.group(1).lower()
                objid = m.group(2)
                name = m.group(3)  # Rohtext INKLUSIVE Anfuehrungszeichen - kopierbar
                break
        if not typ:
            ohne_objektkopf += 1

        rel = os.path.relpath(p, WURZEL).replace(os.sep, "/")

        i = 0
        while i < len(L):
            ma = RE_ATTR.match(L[i])
            if not ma:
                i += 1
                continue
            art = ma.group(1)
            gefunden += 1
            j = i + 1
            proc = None
            while j < min(i + 8, len(L)):  # Attribute koennen stapeln
                mp = RE_PROC.match(L[j])
                if mp:
                    proc = mp
                    break
                j += 1
            if not proc:
                ohne_proc += 1
                i += 1
                continue
            pname = proc.group(1)
            sig = proc.group(2)
            k = j
            while sig.count("(") + 1 > sig.count(")") and k + 1 < len(L) and k < j + 25:
                k += 1
                sig += " " + L[k].strip()
            if ")" in sig:
                sig = sig[: sig.rfind(")")]
            sig = re.sub(r"\s+", " ", sig).strip()
            zeilen.append("%s %s %s|%s|%s|%s|%d|%s" % (typ, objid, name, pname, art, rel, j + 1, sig))
            i = j + 1

print("  Dateien durchsucht         : %d" % dateien)
print("  Attribute gefunden         : %d" % gefunden)
print("  Zeilen im Index            : %d" % len(zeilen))
print("  ohne zugehoerige procedure : %d" % ohne_proc)
print("  Dateien ohne Objektkopf    : %d" % ohne_objektkopf)

kopflos = [z for z in zeilen if not z.split("|")[0].strip()]
print("  ⚠ Indexzeilen OHNE Objektnamen: %d von %d (%.1f%%)"
      % (len(kopflos), len(zeilen), 100.0 * len(kopflos) / max(1, len(zeilen))))
if kopflos:
    for z in sorted(set(x.split("|")[3] for x in kopflos))[:5]:
        print("       %s" % z)
    print("     ⚠ Diese Zeilen sind nicht nachschlagbar. Ursache pruefen, nicht ignorieren.")

kopf = [
    "# =====================================================================",
    "# bc28-ereignisse.txt - Ereignis-Andockstellen eines BC-Standards",
    "# Format: Objekttyp ID Name|Ereignisname|Art|Datei|Zeile|Signatur",
    "# Erzeugt am %s aus %s (%d AL-Dateien)." % (time.strftime("%d.%m.%Y"), WURZEL, dateien),
    "# Schwester von bc28-standard-datenmodell.txt (Felder) und",
    "# bc28-objektinventar.txt (Objekte). Bedienung: standard-nachschlagen.md",
    "#",
    "# ⚠ GRENZE 1: Das ist eine QUELLTEXT-Messung. Sie sagt, welche Ereignisse",
    "#   DEKLARIERT sind - nicht, ob eines im konkreten Ablauf auch FEUERT.",
    "#   Ein Abo auf ein existierendes Ereignis, das nie ausgeloest wird,",
    "#   kompiliert sauber und tut nichts. Das ist die teurere Fehlerklasse.",
    "# ⚠ GRENZE 2: Gemessen an EINEM entpackten Stand. Ereignisse kommen und",
    "#   gehen zwischen Versionen; vor dem Bau gegen den INSTALLIERTEN Stand",
    "#   gegenpruefen.",
    "# ⚠ GRENZE 3: Der Standard traegt auch Ereignisse in Apps, die NICHT",
    "#   entpackt vorliegen (_Exclude_-Apps ohne Quelltext). Was hier fehlt,",
    "#   ist nicht bewiesen abwesend.",
    "# =====================================================================",
]
os.makedirs(os.path.dirname(os.path.abspath(ZIEL)), exist_ok=True)
io.open(ZIEL, "w", encoding="utf-8", newline="\n").write("\n".join(kopf + sorted(zeilen)) + "\n")
print("  geschrieben: %s" % os.path.abspath(ZIEL))
print("  Sekunden: %.1f" % (time.time() - t0))
