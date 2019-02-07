# Lab 1: Inventory file aanmaken
Een belangrijk onderdeel voor Ansible is de inventory file. In deze file wordt beschreven hoe de omgeving er uit ziet.

Alle acties worden uitgevoerd in de home directory van de SSH server.

## Task 1.1: Inventory file aanmaken
In de inventory file wordt beschreven hoe Ansible je Raspberry Pi kan bereiken. Een Ansible inventory werkt altijd met een groep, welke tussen blokhaken wordt gezet: [ en ]. Onder de groep worden alle hosts omschreven. In dit geval gaat het om maar 1 host. Omdat het aanspreken van een host makkelijker gaat met een naam, dan met een IP adres, geven we de Raspberry een naam. Met de variable ansible_host koppelen we deze naam aan het juiste IP adres.

``vi inventory``

Vul de inventory file met (vervang <ipaddress> door het IP adres van de Raspberry Pi:

```
[pi]
raspberry ansible_host=<ipaddress>
```

## Task 1.2: Ansible vertellen waar de inventory file staat
Ansible zoekt standaard in de volgende paden naar de inventory file:

<nog aan te vullen>
  
In het configuratie bestand ansible.cfg kan een alternatief pad geconfigueerd worden naar de inventory file. Ansible zoekt in de volgende paden naar de ansible.cfg:

<nog aan te vullen>

Door een ansible.cfg in dezelfde directory te zetten als het playbook (welke we in een later lab aanmaken), worden alle default instellingen overruled door de instellingen in deze ansible.cfg. We laten de inventory wijzen naar ~/inventory (de ~ is een alias voor je home directory; de plek waar de inventory file is aangemaakt). Nu we toch bezig zijn, configureren we alvast de user waarmee we straks via Ansible inloggen op de Raspberry. Bij Raspberries is dat standaard de user: pi. Verder schakelen we host_key_checking uit. 

Maak een ansible.cfg aan:

``vi ansible.cfg``

Vul de ansible.cfg met:
```
[defaults]
inventory = ~/inventory
remote_user = pi

host_key_checking = False
```


