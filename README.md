# Sternenfänger ⭐

Ein kleines Spiel mit **Python und Pygame**, entstanden im Rahmen der IT-Schnuppertage. Bewege die hellblaue Spielfigur, fange gelbe Sterne und weiche roten Bomben aus!

## Spielregeln

- Du startest mit **5 Leben** und **0 Punkten**.
- Für jeden gefangenen Stern erhältst du **einen Punkt**.
- Jeder Stern, der unten vollständig aus dem Fenster fällt, kostet **ein Leben**.
- Es gibt **drei Sterne**, die mit vertikalem Abstand zeitlich versetzt herunterfallen. Nicht alle müssen gleichzeitig sichtbar sein.
- Alle **5 Sekunden** erscheint eine rote Bombe an einer zufälligen horizontalen Position.
- Berührst du eine Bombe, verlierst du **ein Leben**. Die Bombe verschwindet danach.
- Bomben, denen du ausweichst, kosten keine Leben.
- Bei **0 Leben** endet die Runde. Mit der Leertaste kannst du neu starten.

### Steigende Schwierigkeit

Sterne und Bomben nutzen dieselbe Fallgeschwindigkeit. Diese steigt:

- alle **60 Spielschleifen-Durchläufe (Ticks)** um **0,01 %**;
- zusätzlich bei jedem fünften Punkt um **0,2 %**.

Beide Steigerungen werden auf die jeweils aktuelle Geschwindigkeit angewendet. Bei 60 Bildern pro Sekunde entsprechen 60 Ticks ungefähr einer Sekunde. Der Bomben-Timer verwendet dagegen tatsächlich verstrichene Zeit.

Beim Neustart werden Punkte, Leben, Geschwindigkeit, Sternpositionen und Bomben-Timer zurückgesetzt; vorhandene Bomben werden entfernt.

## Steuerung

| Taste / Aktion | Funktion |
| --- | --- |
| Pfeiltaste links `←` | Spielfigur nach links bewegen |
| Pfeiltaste rechts `→` | Spielfigur nach rechts bewegen |
| Leertaste `Space` | Nach Game Over eine neue Runde starten |
| Fenster-X | Spiel beenden |

Die Spielfigur kann das Fenster nicht verlassen.

## Voraussetzungen

- Python 3 mit `pip`
- Pygame
- Eine grafische Desktop-Umgebung
- Optional: VS Code zum Bearbeiten und Git für die Versionsverwaltung

Zusätzliche Bilder, Schriftdateien oder Sounds werden nicht benötigt: Pygame zeichnet alle Spielfiguren direkt.

## Installation und Start unter Windows

Führe die Befehle in **PowerShell im Projektordner** aus.

### 1. Projekt herunterladen

Wenn du das Projekt noch nicht auf deinem Computer hast:

```powershell
git clone https://github.com/AndreasReinert/sternenfaenger.git
cd sternenfaenger
```

Wenn du bereits mit dem Projekt arbeitest, öffne stattdessen deinen bestehenden Projektordner in VS Code und dort ein Terminal. Du musst das Repository nicht erneut klonen.

### 2. Virtuelle Umgebung erstellen

Nur erforderlich, wenn noch keine `.venv` vorhanden ist:

```powershell
python -m venv .venv
```

### 3. Pygame installieren

```powershell
.\.venv\Scripts\python.exe -m pip install pygame
```

### 4. Spiel starten

```powershell
.\.venv\Scripts\python.exe main.py
```

Diese Befehle nutzen Python direkt aus der virtuellen Umgebung. Eine Aktivierung per PowerShell-Skript ist nicht nötig. Ist deine `.venv` bereits aktiviert, reichen auch `python -m pip install pygame` und `python main.py`.

## So ist der Code aufgebaut

Der Spielcode befindet sich in **`main.py`**.

| Funktion | Aufgabe |
| --- | --- |
| `neue_runde()` | Erstellt den Anfangszustand einer Runde |
| `stern_neu_starten()` | Setzt einen Stern oben hinter die anderen Sterne und wählt seine horizontale Position |
| `aktualisieren()` | Verarbeitet Bewegung, Treffer, Punkte, Leben, Geschwindigkeit und Bomben |
| `zeichnen()` | Zeichnet Hintergrund, Spielfigur, Sterne, Bomben und Texte |
| `main()` | Startet Pygame und führt die Spielschleife aus |

### Die Spielschleife

Die Schleife läuft mit höchstens **60 Bildern pro Sekunde**:

1. Verstrichene Zeit messen und die Bildrate begrenzen.
2. Ereignisse prüfen: Fenster schliessen oder nach Game Over neu starten.
3. Gedrückte Pfeiltasten abfragen.
4. Den Spielzustand aktualisieren.
5. Das neue Bild zeichnen und anzeigen.

Nach Game Over wird der Spielzustand nicht weiter aktualisiert. Die Ereignisverarbeitung läuft weiter, damit Neustart und Schliessen funktionieren.

## Eigene Anpassungen

Einige Einstellungen stehen oben in `main.py`:

| Einstellung | Aktueller Wert | Bedeutung |
| --- | --- | --- |
| `BREITE, HOEHE` | `800, 600` | Fenstergrösse in Pixeln |
| `SPIELER_TEMPO` | `6` | Bewegung der Spielfigur in Pixeln pro Tick |
| `ABSTAND` | `220` | Vertikaler Abstand beim Einreihen der Sterne |
| `RADIUS` | `18` | Äusserer Sternradius in Pixeln |
| `BOMBEN_INTERVALL` | `5000` | Zeit zwischen neuen Bomben in Millisekunden |
| `BOMBEN_RADIUS` | `18` | Bombenradius in Pixeln |

Startleben (`5`) und anfängliches Falltempo (`3.0` Pixel pro Tick) findest du in `neue_runde()`.

**Hinweis:** Die Sternpositionen werden so gewählt, dass horizontale Wechsel bei höherem Tempo kleiner werden. Das garantiert jedoch nicht, dass jede Kombination aus Sternen und zufälligen Bomben gefahrlos erreichbar ist.

## Häufige Probleme

**`ModuleNotFoundError: No module named 'pygame'`**  
Installiere Pygame mit dem Python-Interpreter, mit dem du das Spiel startest. Die obigen `.venv`-Befehle stellen das sicher.

**Die Spielfigur reagiert nicht auf die Pfeiltasten.**  
Klicke zuerst ins Spielfenster, damit es den Tastaturfokus erhält.

**Git kann keine Verbindung zu GitHub herstellen.**  
Das Spiel funktioniert auch ohne GitHub-Verbindung. Für einen Upload müssen Netzwerkzugriff und gegebenenfalls Firmenproxy-Einstellungen funktionieren.
