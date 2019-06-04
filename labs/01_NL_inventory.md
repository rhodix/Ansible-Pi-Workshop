# Lab 1: Inventory file aanmaken
Een belangrijk onderdeel voor Ansible is de inventory file. In deze file wordt beschreven hoe de omgeving er uit ziet.

Alle acties worden uitgevoerd in de home directory van de **SSH server** (Bastion).

## Task 1.1: Inventory file aanmaken
In de inventory file wordt beschreven hoe Ansible je Raspberry Pi kan bereiken. Een Ansible inventory werkt altijd met een groep, welke tussen blokhaken wordt gezet: [ en ]. Onder de groep worden alle hosts omschreven. In dit geval gaat het om maar 1 host. Omdat het aanspreken van een host makkelijker gaat met een naam, dan met een IP adres, geven we de Raspberry een naam. Met de variable ansible_host koppelen we deze naam aan het juiste IP adres.

* Edit de file inventory:

  ``$ vi inventory``

* Vul de inventory file met (vervang ``<ipaddress>`` door het IP adres van de Raspberry Pi:

  ```
  [workshop]
  pi ansible_host=<ipaddress>
  ```

## Task 1.2: Ansible vertellen waar de inventory file staat
Ansible zoekt standaard in de volgende paden naar de inventory file:

* /etc/ansible/hosts
  
In het configuratie bestand ansible.cfg kan een alternatief pad geconfigueerd worden naar de inventory file. Ansible zoekt in de volgende paden naar de ansible.cfg:

* ansible.cfg (in de huidige directory)
* .ansible.cfg (in de home directory
* /etc/ansible/ansible.cfg

Door een ansible.cfg in dezelfde directory te zetten als het playbook (welke we in een later lab aanmaken), worden alle default instellingen overruled door de instellingen in deze ansible.cfg. We laten de inventory wijzen naar ~/inventory (de ~ is een alias voor je home directory; de plek waar de inventory file is aangemaakt). Nu we toch bezig zijn, configureren we alvast de user waarmee we straks via Ansible inloggen op de Raspberry. Bij Raspberries is dat standaard de user: pi. Verder schakelen we host_key_checking uit. 

* Maak een ansible.cfg aan:

  ``$ vi ansible.cfg``

* Vul de ansible.cfg met:
  ```
  [defaults]
  inventory = ~/inventory
  remote_user = pi

  host_key_checking = False
  ```

## Task 1.3: Test de werking
Ansible werkt met modules. Voor bijna elke functie is wel een module te vinden. Voor het aanmaken van een gebruiker wordt bijvoorbeeld de module ``user`` gebruikt. In onze eerste stap met Ansible gaan we de module ``ping`` gebruiken. Met de module ``ping`` kun je de verbinding met je clients testen. Anders dan je gewend bent van de ping commando's van je Operating System (bijvoorbeeld Windows of Linux), test de ``ping`` module niet alleen of de client bereikbaar is (icmp reply), maar controleert of Ansible daadwerkelijk in kan loggen op de client (voor Linux clients logt Ansible in met SSH). Zie https://docs.ansible.com/ansible/latest/modules/ping_module.html#ping-module.

**Tip:** Een overzicht van alle modules is terug te vinden in de online documentatie van Ansible op: https://docs.ansible.com/ansible/latest/modules/list_of_all_modules.html.

* Controleer of de inventory file en de ansible.cfg in je home directory staan:

  ``$ ls``

  ```
  ansible.cfg  inventory
  ```
  
* Controleer of de Ansible module ``ping`` antwoord geeft:

  ``$ ansible --ask-pass -m ping workshop``

  ```
  SSH password:
  raspberry | SUCCESS => {
      "changed": false,
      "ping": "pong"
  }
  ```
  
**Tip:** In ons voorbeeld vraagt Ansible om een SSH password. In een geautomatiseerd scenario is het gebruikelijk om met SSH Autorized Keys te werken. In een later lab richten we de Raspberry Pi in met Autorized keys, zodat Ansible direct, zonder wachtwoord, in kan loggen op de Pi. Omdat we nog geen Authorized keys hebben ingericht, geven we met ``--ask-pass`` de instructie om een SSH password te vragen.

In de inventory file hebben we de groep [workshop] gedefineerd. De ``ping`` module zal daarom alle hosts controleren. In ons lab hebben we maar 1 host gedefineerd: ``pi``. Als we meerdere hosts in de groep hadden gezet, zouden alle hosts antwoorden. 

**Tip:** Het is ook mogelijk om een enkele host te testen. Met ``ansible --ask-pass -m ping pi`` wordt de module alleen maar op de host ``pi`` uitgevoerd.

Volgende stap: [Lab 02: Playbook - User aanmaken](/labs/02_NL_playbook_user.md)
