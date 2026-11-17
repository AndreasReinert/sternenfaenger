import math
import random
from pathlib import Path
import pygame

BREITE, HOEHE = 800, 600
RADIUS = 18
ABSTAND = 220  # Vertikaler Abstand zwischen den Sternen.
SPIELER_TEMPO = 6
BOMBEN_INTERVALL = 5000  # Fünf Sekunden Spielzeit; bei höherem Tempo kürzer.
BOMBEN_RADIUS = 18
BOMBEN_SCHADEN = 2
PUNKTE_PRO_EXTRA_BOMBE = 15


HIGHSCORE_DATEI = Path(__file__).resolve().with_name("highscore.txt")


# Alle Pfade beziehen sich auf main.py, nicht auf das aktuelle Terminal-Verzeichnis.
ASSET_ORDNER = Path(__file__).resolve().parent / "assets"
BILDER = {}
TOENE = {}


def bilder_laden():
    """Eigene transparente PNG-Dateien laden und auf Spielgrösse skalieren."""
    for name, groesse in {"figur": (100, 25), "stern": (40, 40), "bombe": (48, 56)}.items():
        pfad = ASSET_ORDNER / "bilder" / f"{name}.png"
        try:
            bild = pygame.image.load(str(pfad)).convert_alpha()
            BILDER[name] = pygame.transform.smoothscale(bild, groesse)
        except (pygame.error, OSError) as fehler:
            raise RuntimeError(f"Bild fehlt oder ist unlesbar: {pfad}") from fehler


def toene_vorbereiten():
    """WAV-Dateien laden. Audiofehler sichtbar melden, aber weiterspielen."""
    TOENE.clear()
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2)
        print("Audio initialisiert:", pygame.mixer.get_init())
    except pygame.error as fehler:
        print(f"Audio nicht verfügbar; das Spiel läuft ohne Ton: {fehler}")
        return
    for name in ("fangen", "verlust", "sterben", "bombe"):
        pfad = ASSET_ORDNER / "sounds" / f"{name}.wav"
        try:
            TOENE[name] = pygame.mixer.Sound(str(pfad))
            TOENE[name].set_volume(0.7)
        except (pygame.error, OSError) as fehler:
            print(f"Ton konnte nicht geladen werden: {pfad}: {fehler}")


def ton_spielen(name):
    ton = TOENE.get(name)
    if ton is not None:
        ton.play()


def highscore_laden():
    """Fehlende oder ungültige Dateien bedeuten: noch kein Rekord."""
    try:
        return max(0, int(HIGHSCORE_DATEI.read_text(encoding="utf-8").strip()))
    except (OSError, ValueError):
        return 0


def highscore_speichern(punkte):
    """Erst temporär schreiben, dann die alte Datei sicher ersetzen."""
    try:
        temporaer = HIGHSCORE_DATEI.with_suffix(".tmp")
        temporaer.write_text(str(punkte), encoding="utf-8")
        temporaer.replace(HIGHSCORE_DATEI)
        return True
    except OSError as fehler:
        print(f"Highscore konnte nicht gespeichert werden: {fehler}")
        return False


def rekord_pruefen(spiel):
    if spiel["punkte"] > spiel["highscore"]:
        spiel["highscore"] = spiel["punkte"]
        spiel["speicherfehler"] = not highscore_speichern(spiel["highscore"])


def neue_runde(highscore=None):
    """Alle Werte inklusive Geschwindigkeit und Sternpositionen zurücksetzen."""
    sterne = [
        {"x": 400, "y": float(-RADIUS - i * ABSTAND)}
        for i in range(3)
    ]
    # Nahe Startpositionen machen auch die erste Sternfolge erreichbar.
    for i in range(1, 3):
        sterne[i]["x"] = random.randint(150, 650)
    return {
        "figur": pygame.Rect(350, 550, 100, 25),
        "figur_x": 350.0,  # Nachkommastellen für flüssige Bewegung erhalten.
        "gestartet": False,
        "zeitfaktor": 1.0,
        "sterne": sterne,
        "bomben": [],
        "bomben_zeit": 0.0,
        "punkte": 0,
        "highscore": highscore_laden() if highscore is None else highscore,
        "speicherfehler": False,
        "leben": 5,
        "ticks": 0,
        "tempo": 3.0,
    }


def stern_neu_starten(stern, spiel):
    # Hinter dem obersten anderen Stern einreihen: keine gleichzeitigen Starts.
    andere = [s for s in spiel["sterne"] if s is not stern]
    vorgaenger = min(andere, key=lambda s: s["y"])
    stern["y"] = min(-RADIUS, vorgaenger["y"] - ABSTAND)

    # Bei hohem Tempo kleinere horizontale Sprünge wählen. So bleibt Zeit,
    # zwischen zwei aufeinanderfolgenden Sternen mit dem Korb zu wechseln.
    zeitabstand = (vorgaenger["y"] - stern["y"]) / spiel["tempo"]
    reichweite = int(zeitabstand * SPIELER_TEMPO * 0.65)
    links = max(RADIUS, int(vorgaenger["x"]) - reichweite)
    rechts = min(BREITE - RADIUS, int(vorgaenger["x"]) + reichweite)
    stern["x"] = random.randint(links, rechts)


def aktualisieren(spiel, links=False, rechts=False, delta_ms=1000 / 60):
    if not spiel["gestartet"] or spiel["leben"] <= 0:
        return
    # Derselbe Faktor beschleunigt Spieler, Sterne, Bomben und Spawn-Timer.
    schritt = delta_ms / (1000 / 60) * spiel["zeitfaktor"]
    figur = spiel["figur"]
    spiel["figur_x"] += (int(rechts) - int(links)) * SPIELER_TEMPO * schritt
    spiel["figur_x"] = max(0.0, min(BREITE - figur.width, spiel["figur_x"]))
    figur.x = round(spiel["figur_x"])

    spiel["ticks"] += 1
    if spiel["ticks"] % 60 == 0:
        spiel["tempo"] *= 1.0001  # Weiterhin +0,01 % alle 60 Ticks.

    for stern in spiel["sterne"]:
        vorher_y = stern["y"]
        stern["y"] += spiel["tempo"] * schritt
        # Überstrichener Bereich verhindert Durchrutschen bei hohem Tempo.
        trefferbereich = pygame.Rect(
            stern["x"] - RADIUS, vorher_y - RADIUS,
            2 * RADIUS, math.ceil(stern["y"] - vorher_y + 2 * RADIUS),
        )
        if figur.colliderect(trefferbereich):
            spiel["punkte"] += 1
            ton_spielen("fangen")
            rekord_pruefen(spiel)
            if spiel["punkte"] % 5 == 0:
                spiel["zeitfaktor"] *= 1.025  # +2,5 % auf das gesamte Spiel je 5 Punkte.
            stern_neu_starten(stern, spiel)
        elif stern["y"] - RADIUS >= HOEHE:
            spiel["leben"] -= 1
            ton_spielen("sterben" if spiel["leben"] == 0 else "verlust")
            stern_neu_starten(stern, spiel)
            if spiel["leben"] == 0:
                break


    if spiel["leben"] <= 0:
        return

    # Auch Bomben erscheinen bei höherem Spieltempo häufiger.
    spiel["bomben_zeit"] += schritt * (1000 / 60)
    while spiel["bomben_zeit"] >= BOMBEN_INTERVALL:
        spiel["bomben_zeit"] -= BOMBEN_INTERVALL
        # 0–14 Punkte: 1 Bombe, 15–29: 2 Bomben, ab 30: 3 usw.
        anzahl = 1 + spiel["punkte"] // PUNKTE_PRO_EXTRA_BOMBE
        for _ in range(anzahl):
            spiel["bomben"].append({
                "x": random.randint(BOMBEN_RADIUS, BREITE - BOMBEN_RADIUS),
                "y": float(-BOMBEN_RADIUS),
            })

    for bombe in spiel["bomben"][:]:
        vorher_y = bombe["y"]
        bombe["y"] += spiel["tempo"] * schritt
        # Kreis gegen Rechteck, inklusive des Weges seit dem letzten Bild.
        naechstes_x = max(figur.left, min(bombe["x"], figur.right))
        abstand_x = bombe["x"] - naechstes_x
        abstand_y = max(figur.top - bombe["y"], vorher_y - figur.bottom, 0)
        if abstand_x ** 2 + abstand_y ** 2 <= BOMBEN_RADIUS ** 2:
            spiel["leben"] = max(0, spiel["leben"] - BOMBEN_SCHADEN)
            ton_spielen("bombe")
            if spiel["leben"] == 0:
                ton_spielen("sterben")
            spiel["bomben"].remove(bombe)  # Jede Bombe verursacht einmalig zwei Schaden.
            if spiel["leben"] == 0:
                break
        elif bombe["y"] - BOMBEN_RADIUS >= HOEHE:
            spiel["bomben"].remove(bombe)  # Ausweichen kostet keine Leben.


def zeichnen(fenster, schrift, spiel):
    fenster.fill((10, 20, 50))
    if not spiel["gestartet"]:
        titel_schrift = pygame.font.Font(None, 76)
        titel = titel_schrift.render("Sternenfänger", True, (255, 220, 50))
        fenster.blit(titel, titel.get_rect(center=(BREITE // 2, 205)))
        for text, y, farbe in [
            ("Drücke Leertaste zum starten", 295, (255, 255, 255)),
            ("Pfeiltasten: bewegen | Sterne fangen", 355, (160, 205, 255)),
            ("Roten Bomben ausweichen!", 395, (255, 130, 130)),
            (f'Highscore: {spiel["highscore"]}', 465, (255, 220, 50)),
        ]:
            bild = schrift.render(text, True, farbe)
            fenster.blit(bild, bild.get_rect(center=(BREITE // 2, y)))
        return
    fenster.blit(BILDER["figur"], spiel["figur"])
    for stern in spiel["sterne"]:
        bild = BILDER["stern"]
        fenster.blit(bild, bild.get_rect(center=(round(stern["x"]), round(stern["y"]))))
    for bombe in spiel["bomben"]:
        # Der runde Körper liegt bei (24, 36); die Zündschnur zählt nicht als Treffer.
        fenster.blit(BILDER["bombe"], (round(bombe["x"]) - 24, round(bombe["y"]) - 36))
    for text, y in [(f'Punkte: {spiel["punkte"]}', 20),
                    (f'Leben: {spiel["leben"]}', 60)]:
        fenster.blit(schrift.render(text, True, "white"), (20, y))
    rekord = schrift.render(f'Highscore: {spiel["highscore"]}', True, (255, 220, 50))
    fenster.blit(rekord, rekord.get_rect(topright=(BREITE - 20, 20)))
    if spiel["speicherfehler"]:
        warnung = schrift.render("Highscore nicht gespeichert!", True, (255, 150, 150))
        fenster.blit(warnung, (20, 140))
    if spiel["leben"] == 0:
        for text, y in [("Game Over", 280),
                        ("Leertaste: neue Runde", 325)]:
            bild = schrift.render(text, True, "white")
            fenster.blit(bild, bild.get_rect(center=(400, y)))


def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    toene_vorbereiten()
    fenster = pygame.display.set_mode((BREITE, HOEHE))
    bilder_laden()
    pygame.display.set_caption("Sternenfänger")
    schrift = pygame.font.Font(None, 36)
    uhr = pygame.time.Clock()
    spiel = neue_runde()
    laeuft = True
    while laeuft:
        delta_ms = uhr.tick(60)
        for ereignis in pygame.event.get():
            if ereignis.type == pygame.QUIT:
                laeuft = False
            elif ereignis.type == pygame.KEYDOWN and ereignis.key == pygame.K_SPACE:
                if spiel["leben"] == 0:
                    alter_rekord = spiel["highscore"]
                    speicherfehler = spiel["speicherfehler"]
                    spiel = neue_runde(alter_rekord)
                    spiel["speicherfehler"] = speicherfehler
                    spiel["gestartet"] = True
                elif not spiel["gestartet"]:
                    spiel["gestartet"] = True
        if not laeuft:
            break
        tasten = pygame.key.get_pressed()
        aktualisieren(spiel, tasten[pygame.K_LEFT], tasten[pygame.K_RIGHT], delta_ms)
        zeichnen(fenster, schrift, spiel)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()