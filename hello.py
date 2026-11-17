from datetime import date

name = input("Wie heisst du? ")
alter = int(input("Wie alt bist du? "))

aktuelles_jahr = date.today().year
jahr_mit_18 = aktuelles_jahr + (18 - alter)

print(f"Hallo {name}, willkommen in der IT!")

if alter < 18:
    print(f"Du wirst ungefähr im Jahr {jahr_mit_18} 18 Jahre alt.")
elif alter == 18:
    print("Du bist bereits 18 Jahre alt!")
else:
    print(f"Du bist ungefähr im Jahr {jahr_mit_18} 18 Jahre alt geworden.")