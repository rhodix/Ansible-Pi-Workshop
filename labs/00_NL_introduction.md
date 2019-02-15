# Introductie
Welkom bij de workshop Ransible-Pi. In deze workshop gaan we een Raspberry Pi inrichten met Ansible, zodat je deze kunt gebruiken als jumpstart voor in je eigen omgeving. Na de workshop is je Raspberry Pi gereed om aangesloten te worden in je netwerk, zodat je deze kunt gebruiken voor de ontwikkeling van je eigen Ansible playbooks. Je kunt er natuurlijk ook een demo mee geven aan je collega's. 

De workshop is zo opgezet, dat deze vanuit thuis (of op je werk) verder afgemaakt kan worden. Na **Lab 4** kun je de Raspberry gebruiken als Linux server met SSH toegang en Ansible.

## Benodigdheden
Voor deze workshop heb je nodig:
- Een Linux server met SSH toegang en Ansible
- Een Raspberry Pi
- Sheet met account gegevens

Elke Raspberry heeft een kleur codering rechtsboven. Controleer of de kleur codering overeen komt met de codering op je sheet (anders werken de inlog gegevens niet).

## Eigen Raspbery Pi (of reset uitvoeren)
De Raspberry's in de workshop zijn voorbereid met ``Rasbian``. Deze software is eenvoudig te downloaden via ``https://www.raspberrypi.org/downloads/raspbian/``. De workshop is getest met ``Rasbian Stretch Lite``. De installatie van ``Rasbian`` vind je terug in de installation guide: https://www.raspberrypi.org/documentation/installation/installing-images/README.md.

Om de workshop wat vloeiender te kunnen laten verlopen is het volgende aangepast (maar dat is voor je eigen Raspberry Pi niet nodig):
- Hostname
- Password
- Locale settings (Language, keyboard etc)

Verder is de Raspberry up-to-date gebracht met het commando: ``apt-get dist-upgrade``.
