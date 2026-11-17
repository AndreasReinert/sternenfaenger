# Eigene Bilder und Sounds

Dieses Paket enthält main.py und selbst erstellte Beispielgrafiken und Soundeffekte.
Ersetze main.py in deinem Projekt und kopiere den kompletten Ordner assets daneben.
Deine vorhandene highscore.txt bleibt erhalten; sie ist nicht Bestandteil des Pakets.

## Ordnerstruktur

```text
main.py
assets/
  bilder/
    figur.png
    stern.png
    bombe.png
  sounds/
    fangen.wav
    verlust.wav
    sterben.wav
    bombe.wav
```

## Eigene Dateien verwenden

Ersetze die Dateien unter denselben Namen. Der Code lädt sie beim nächsten Spielstart.
PNG mit transparentem Hintergrund verwenden. Die Bilder werden auf folgende Grössen
skaliert: Figur 100 × 25, Stern 40 × 40, Bombe 48 × 56 Pixel.
Bei der Bombe sitzt der Körper mittig bei (24, 36), Radius 18 Pixel; oben ist Platz
für die Zündschnur. Die Zündschnur gehört nicht zum Trefferbereich. Die bestehenden
Kollisionsbereiche bleiben unverändert; stark andere Formen passen eventuell nicht.

Sounds am besten als unkomprimierte 16-Bit-PCM-WAV-Dateien mit 44.100 Hz speichern.
Die Beispiele sind Stereo. Kurze Clips eignen sich am besten:
- fangen.wav: Stern gefangen
- verlust.wav: Stern verpasst, noch Leben übrig
- bombe.wav: Bombentreffer
- sterben.wav: Game Over (bei tödlichem Bombentreffer zusammen mit bombe.wav)

Die Lautstärke steht in main.py bei set_volume(0.7), zwischen 0.0 und 1.0.
Fehlende Sounds werden im Terminal gemeldet; das Spiel läuft dann ohne diesen Ton.
Fehlende Bilder verhindern den Start und werden mit ihrem Dateipfad gemeldet.

## Start und Regeln

In der aktivierten virtuellen Umgebung: python main.py
Benötigt pygame oder pygame-ce. Space startet die Runde bzw. startet nach Game Over neu.
Pfeiltasten bewegen die Figur. Drei Sterne fallen versetzt; jeder Fang gibt einen Punkt.
Fünf Leben, ein Lebensverlust je verpasstem Stern oder Bombentreffer.
Alle fünf Punkte steigt das gesamte Spieltempo um 2,5 Prozent; die zusätzliche
Sternbeschleunigung von 0,01 Prozent alle 60 Ticks bleibt erhalten.
Bomben erscheinen alle fünf Sekunden Spielzeit, mit höherem Tempo entsprechend häufiger.
Der Highscore wird weiterhin neben main.py gespeichert.

## Falls kein Ton hörbar ist

Externe Sounddateien beheben keine falsche Windows-Ausgabezuordnung.
Das gewünschte Ausgabegerät vor dem Spielstart auswählen und im Windows-Lautstärkemixer
Python prüfen. Audiofehler und fehlende WAV-Dateien erscheinen im Terminal.
