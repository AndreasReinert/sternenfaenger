import math
import random
import pygame

BREITE, HOEHE = 800, 600
RADIUS = 18
ABSTAND = 220  # Vertikaler Abstand zwischen den Sternen.
SPIELER_TEMPO = 6
BOMBEN_INTERVALL = 5000  # Eine neue Bombe alle fünf Sekunden.
BOMBEN_RADIUS = 18


def neue_runde():
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
        "sterne": sterne,
        "bomben": [],
        "bomben_zeit": 0.0,
        "punkte": 0,
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
    if spiel["leben"] <= 0:
        return
    figur = spiel["figur"]
    figur.x += (int(rechts) - int(links)) * SPIELER_TEMPO
    figur.clamp_ip(pygame.Rect(0, 0, BREITE, HOEHE))

    spiel["ticks"] += 1
    if spiel["ticks"] % 60 == 0:
        spiel["tempo"] *= 1.0001  # Weiterhin +0,01 % alle 60 Ticks.

    for stern in spiel["sterne"]:
        vorher_y = stern["y"]
        stern["y"] += spiel["tempo"]
        # Überstrichener Bereich verhindert Durchrutschen bei hohem Tempo.
        trefferbereich = pygame.Rect(
            stern["x"] - RADIUS, vorher_y - RADIUS,
            2 * RADIUS, math.ceil(stern["y"] - vorher_y + 2 * RADIUS),
        )
        if figur.colliderect(trefferbereich):
            spiel["punkte"] += 1
            if spiel["punkte"] % 5 == 0:
                spiel["tempo"] *= 1.002  # Zusätzlich +0,2 % je 5 Punkte.
            stern_neu_starten(stern, spiel)
        elif stern["y"] - RADIUS >= HOEHE:
            spiel["leben"] -= 1
            stern_neu_starten(stern, spiel)
            if spiel["leben"] == 0:
                break


    if spiel["leben"] <= 0:
        return

    # Echte verstrichene Zeit: fünf Sekunden auch bei niedriger Bildrate.
    spiel["bomben_zeit"] += delta_ms
    while spiel["bomben_zeit"] >= BOMBEN_INTERVALL:
        spiel["bomben_zeit"] -= BOMBEN_INTERVALL
        spiel["bomben"].append({
            "x": random.randint(BOMBEN_RADIUS, BREITE - BOMBEN_RADIUS),
            "y": float(-BOMBEN_RADIUS),
        })

    for bombe in spiel["bomben"][:]:
        vorher_y = bombe["y"]
        bombe["y"] += spiel["tempo"]
        # Kreis gegen Rechteck, inklusive des Weges seit dem letzten Bild.
        naechstes_x = max(figur.left, min(bombe["x"], figur.right))
        abstand_x = bombe["x"] - naechstes_x
        abstand_y = max(figur.top - bombe["y"], vorher_y - figur.bottom, 0)
        if abstand_x ** 2 + abstand_y ** 2 <= BOMBEN_RADIUS ** 2:
            spiel["leben"] -= 1
            spiel["bomben"].remove(bombe)  # Jede Bombe kostet nur ein Leben.
            if spiel["leben"] == 0:
                break
        elif bombe["y"] - BOMBEN_RADIUS >= HOEHE:
            spiel["bomben"].remove(bombe)  # Ausweichen kostet keine Leben.


def zeichnen(fenster, schrift, spiel):
    fenster.fill((10, 20, 50))
    pygame.draw.rect(fenster, (100, 190, 255), spiel["figur"])
    for stern in spiel["sterne"]:
        zacken = []
        for i in range(10):
            winkel = math.radians(-90 + i * 36)
            radius = RADIUS if i % 2 == 0 else RADIUS * 0.45
            zacken.append((stern["x"] + math.cos(winkel) * radius,
                           stern["y"] + math.sin(winkel) * radius))
        pygame.draw.polygon(fenster, (255, 220, 50), zacken)
    for bombe in spiel["bomben"]:
        mitte = (round(bombe["x"]), round(bombe["y"]))
        pygame.draw.circle(fenster, (240, 55, 65), mitte, BOMBEN_RADIUS)
        pygame.draw.line(fenster, (255, 190, 80),
                         (mitte[0], mitte[1] - BOMBEN_RADIUS),
                         (mitte[0] + 6, mitte[1] - BOMBEN_RADIUS - 8), 3)
    for text, y in [(f'Punkte: {spiel["punkte"]}', 20),
                    (f'Leben: {spiel["leben"]}', 60)]:
        fenster.blit(schrift.render(text, True, "white"), (20, y))
    if spiel["leben"] == 0:
        for text, y in [("Game Over", 280),
                        ("Leertaste: neue Runde", 325)]:
            bild = schrift.render(text, True, "white")
            fenster.blit(bild, bild.get_rect(center=(400, y)))


def main():
    pygame.init()
    fenster = pygame.display.set_mode((BREITE, HOEHE))
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
            elif (ereignis.type == pygame.KEYDOWN
                  and ereignis.key == pygame.K_SPACE and spiel["leben"] == 0):
                spiel = neue_runde()
        if not laeuft:
            break
        tasten = pygame.key.get_pressed()
        aktualisieren(spiel, tasten[pygame.K_LEFT], tasten[pygame.K_RIGHT], delta_ms)
        zeichnen(fenster, schrift, spiel)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()