# ⭐ Sternenfänger

Ein kleines Arcade-Spiel mit Python und Pygame: Fange fallende Sterne, weiche roten Bomben aus und verbessere deinen Highscore! Herzen regenerieren Leben, während ein Magnet dir beim Sammeln hilft.

## Spiel starten

Du benötigst Python 3 und die mitgelieferten Bilder im Ordner `assets`. Entwickelt wurde das Spiel mit Python 3.12 und pygame-ce.

### Installation unter Windows (PowerShell)

Öffne dein Projekt in VS Code und starte ein Terminal im Projektordner:

```powershell
cd C:\Projekte\sternenfaenger
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pygame-ce
python main.py
```

Ist `.venv` bereits vorhanden, überspringe das Erstellen der Umgebung. Obwohl das Paket `pygame-ce` heisst, wird es im Code als `pygame` importiert. Installiere nicht zusätzlich das Paket `pygame` in derselben Umgebung.

Falls PowerShell die Aktivierung blockiert, kannst du die Umgebung auch direkt verwenden:

```powershell
.\.venv\Scripts\python.exe -m pip install pygame-ce
.\.venv\Scripts\python.exe main.py
```

In VS Code lässt sich über **Strg+Umschalt+P → Python: Select Interpreter** der Interpreter aus `.venv` auswählen.

## Steuerung

| Taste | Aktion |
| --- | --- |
| Leertaste | Runde auf dem Titelbildschirm starten |
| A oder Pfeil links | Nach links bewegen |
| D oder Pfeil rechts | Nach rechts bewegen |
| R | Nach Game Over eine neue Runde starten |
| X am Fenster | Spiel beenden |

Die Figur bewegt sich nur horizontal am unteren Rand und bleibt innerhalb des Spielfelds.

## Spielregeln

Du startest jede Runde mit **5 Leben und 0 Punkten**. Bei 0 Leben endet das Spiel.

### Sterne

- Drei Sterne fallen zeitlich versetzt von oben herunter.
- Ein gefangener Stern bringt **1 Punkt** und startet oben neu.
- Ein verpasster Stern kostet **1 Leben** und startet ebenfalls neu.
- Die horizontalen Startpositionen variieren; die Abstände werden abhängig vom Tempo begrenzt.

### Bomben

- Alle **5 Sekunden Spielzeit** wird eine neue Bombenwelle geplant.
- Die Bomben starten an zufälligen horizontalen Positionen, innerhalb einer Welle um jeweils **0,2–0,6 Sekunden Spielzeit** versetzt.
- Ein Bombentreffer verursacht **2 Schaden**. Die Bombe verschwindet danach.
- Verpasste Bomben kosten keine Leben.
- Mit steigender Punktzahl werden die Wellen grösser. Der Punkteabstand zur nächsten zusätzlichen Bombe wächst jeweils um **20 %**, auf ganze Punkte aufgerundet.

| Gesamtpunkte | Bomben pro neuer Welle |
| --- | --- |
| 0–14 | 1 |
| 15–32 | 2 |
| 33–54 | 3 |
| 55–81 | 4 |
| ab 82 | 5; weitere Steigerungen folgen |

Die benötigten zusätzlichen Punkte lauten also **15, 18, 22, 27, …** und nicht jedes Mal 15.

### Magnet

- Bei **50, 100, 150, … Punkten** erscheint ein fallender Magnet an einer zufälligen Position.
- Erst beim Einsammeln wird er aktiv.
- Er zieht Sterne **10 Sekunden lang** sanft horizontal zur Figur. Sterne fallen dabei weiter nach unten.
- Die verbleibende Wirkungsdauer wird angezeigt und ist unabhängig vom Spieltempo.
- Ein weiterer eingesammelter Magnet setzt die Dauer wieder auf 10 Sekunden.
- Ein verpasster Magnet kostet kein Leben.

### Herzen

- Nach jeweils **zufällig 15–25 weiteren Punkten** fällt ein Herz an einer zufälligen Position herunter.
- Der nächste Punkteabstand wird jedes Mal neu ausgelost.
- Einsammeln regeneriert **1 Leben**, maximal bis zu **5 Leben**.
- Verpasste Herzen kosten nichts. Bei vollen Leben wird das Herz ohne zusätzliche Heilung eingesammelt.

## Schwierigkeit und Spieltempo

Alle **5 Punkte** steigt das gesamte Spieltempo um **2,5 %** gegenüber dem vorherigen Tempo. Dadurch bewegen sich die Figur und fallende Objekte schneller; auch die Bombenwellen folgen in Echtzeit schneller aufeinander.

Zusätzlich steigt das Basistempo der fallenden Objekte alle **60 aktiven Spielschleifen-Durchläufe um 0,01 %**. Bei 60 Bildern pro Sekunde entspricht das ungefähr einer Sekunde.

Beim Neustart werden Punkte, Leben, Tempo, fallende Objekte und Bonus-Timer zurückgesetzt. Der Highscore bleibt erhalten.

## Highscore

Neue Rekorde werden automatisch in `highscore.txt` neben `main.py` gespeichert und beim nächsten Start geladen. Eine fehlende oder ungültige Datei wird als Highscore 0 behandelt.

Der Projektordner muss zum Speichern beschreibbar sein. Um den Rekord zurückzusetzen, beende das Spiel und lösche `highscore.txt`. Der Rekord ist lokal, nicht mit einem Online-Konto verknüpft.

## Projektstruktur

```text
sternenfaenger/
├── main.py
├── README.md
├── .gitignore
├── assets/
│   ├── bilder/
│   │   ├── figur.png
│   │   ├── stern.png
│   │   └── bombe.png
│   └── sounds/
│       ├── fangen.wav
│       ├── verlust.wav
│       ├── sterben.wav
│       └── bombe.wav
├── highscore.txt       # Wird beim ersten neuen Rekord erzeugt
└── .venv/             # Lokale Python-Umgebung, nicht hochladen
```

Die README und `.gitignore` dienen der Dokumentation beziehungsweise Versionsverwaltung; zum Spielen benötigt werden `main.py` und die Assets.

## Eigene Grafiken und Sounds

Ersetze die Dateien im Ordner `assets` durch eigene Dateien mit **denselben Namen und Formaten**. Transparente PNG-Dateien eignen sich besonders gut.

Die Bilder werden automatisch auf die folgenden Grössen im logischen Spielfeld skaliert:

| Bild | Grösse |
| --- | --- |
| `figur.png` | 100 × 25 Pixel |
| `stern.png` | 40 × 40 Pixel |
| `bombe.png` | 48 × 56 Pixel |

Herzen und Magnete werden direkt im Code gezeichnet und benötigen keine eigenen Bilddateien. Die Treffererkennung erfolgt geometrisch, nicht pixelgenau anhand der Bildtransparenz.

| Sound | Ereignis |
| --- | --- |
| `fangen.wav` | Stern, Herz oder Magnet eingesammelt |
| `verlust.wav` | Stern verpasst, solange noch Leben bleiben |
| `bombe.wav` | Bombentreffer |
| `sterben.wav` | Game Over |

Nutze für veröffentlichte Bilder und Sounds nur eigene oder entsprechend lizenzierte Dateien.

## Fenster und Darstellung

Das Spiel verwendet intern ein **800 × 600 Pixel** grosses Spielfeld. Das Fenster passt sich beim Start an die Bildschirmgrösse an und lässt sich vergrössern oder verkleinern. Die Darstellung wird proportional skaliert; je nach Seitenverhältnis können Ränder entstehen. Die Spielregeln und Treffererkennung bleiben unabhängig von der Fenstergrösse.

## Häufige Probleme

**`No module named pygame`**  
Installiere `pygame-ce` mit dem Python-Interpreter deiner Projektumgebung. Prüfe auch die Interpreter-Auswahl in VS Code.

**Bild fehlt oder ist unlesbar**  
Prüfe die Ordnerstruktur und Dateinamen unter `assets/bilder`. Fehlende oder beschädigte Pflichtbilder verhindern den Spielstart. Die Pfade beziehen sich auf den Speicherort von `main.py`.

**Kein Ton**  
Prüfe das Windows-Ausgabegerät, den Lautstärkemixer und die WAV-Dateien unter `assets/sounds`. Schliesse dein Audiogerät vor dem Start an. Audio- und Ladefehler werden im Terminal gemeldet; das Spiel kann auch ohne Ton weiterlaufen.

**Highscore wird nicht gespeichert**  
Prüfe die Schreibrechte im Projektordner und die Fehlermeldung im Terminal.

## Git-Hinweis

Die virtuelle Umgebung und lokale Python-Cache-Dateien gehören nicht ins Repository. Wenn der persönliche Highscore nicht veröffentlicht werden soll, ergänze diese Einträge in deiner `.gitignore`:

```gitignore
.venv/
__pycache__/
*.pyc
highscore.txt
highscore.tmp
```

Bereits von Git erfasste Dateien werden durch neue `.gitignore`-Einträge nicht automatisch aus der Versionsverwaltung entfernt.
