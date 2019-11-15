# Lab 5: Role - User aanmaken
Voor bijna elke uitdaging is wel een kant-en-klare rol te vinden op Ansible Galaxy (https://galaxy.ansible.com/). Het nadeel is echter dat er te veel roles te vinden zijn, waardoor het lastig is om de parels te vinden. Let bijvoorbeeld op het aantal downloads en het aantal sterren. Bekijk altijd de broncode van de role die je op Ansible Galaxy hebt gevonden en controleer of deze precies doet wat je zoekt. Indien nodig kun je de role altijd aanpassen.

Bijna alle rollen zijn te sturen met variablen. Deze zijn vaak beschreven in de documentatie van de role. Als de beschrijving ontbreekt kun je in de directory ``defaults`` en in de directory ``vars`` de definitie van de variablen terug vinden.

Voor het aanmaken van een user kun je bijvoorbeeld zoeken op ``accounts``. De role ``ontic.account`` (https://galaxy.ansible.com/ontic/account)  lijkt precies te doen wat we willen. Deze gaan we installeren via Ansible Galaxy. 

**Tip** Naast het kijken naar het aantal stars of downloads kun je ook kijken of een ontwikkelaar meerdere roles heeft gebouwd. De ontic roles hebben misschien nog niet zoveel stars, maar de ontwikkelaar heeft wel tientallen roles gebouwd. Enkele bekende ontwikkelaars zijn:
* https://galaxy.ansible.com/debops
* https://galaxy.ansible.com/geerlingguy
* https://galaxy.ansible.com/Oefenweb

## Task 5.1: Role installeren

We gaan een Ansible Role gebruiken om een user account aan te maken. Doordat de tasks in de role al zijn geschreven hoef je alleen maar de role te installeren en met parameters de role aan te sturen.

**Tip** De onderstaande acties worden weer uitgevoerd op de Bastion server (log dus uit je Raspberry).

* Installeer de role via Ansible Galaxy:

  ``$ ansible-galaxy install ontic.account``

De role wordt geïnstalleerd naar de ``.ansible/roles`` directory in je home directory. 

* Controleer of de role is geinstalleerd in ``.ansible/roles``:

  ``$ ls ~/.ansible/roles``
  
  ```
  ontic.account
  ```  

* Bekijk de role:

  ``$ cd ~/.ansible/roles/ontic.account``
  
  ``$ ls``
  
  ```
  defaults  docs  meta  tasks  tests
  ```
  
Een beschrijving van de onderdelen van een role vind je terug in de documentatie van Ansible op: https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html.

**Tip:** Het vervolg van de workshop wordt vanuit je home directory uitgevoerd. Ga terug naar je home directory met het commando: ``$ cd``

## Task 5.2: Password hash genereren
De ``user`` module verwacht het wachtwoord in SHA512 formaat. 

* Je kunt Ansible gebruiken om een SHA512 hash te genereren (vervang ``<WorkshopPassword>`` door een eigen wachtwoord):

  ``$ ansible all -i localhost, -m debug -a "msg={{ '<WorkshopPassword>' | password_hash('sha512') }}"``

  ```
  localhost | SUCCESS => {
    "msg": "$6$uj/GXuBze4eetOeT$ksVseNMTnsRdkVFqUyTICzxri9TeRnsqJyUZVRiiy6ChlDurXWsTkAOdPuSNOPJtPNnzkmrXzfx753hglmH5M/"
  }
  ```

## Task 5.3: Playbook maken met role

* Maak een nieuw playbook ``workshop-role.yml`` (vervang de hash met de hash uit task 5.2):

  ```
  ---
  - hosts: workshop
    become: true
    become_method: sudo

    vars:
      account_groups:
        - name: "workshop"
      account_users:
        - name: "workshop"
          password: "$6$uj/GXuBze4eetOeT$ksVseNMTnsRdkVFqUyTICzxri9TeRnsqJyUZVRiiy6ChlDurXWsTkAOdPuSNOPJtPNnzkmrXzfx753hglmH5M/"

    roles:
      - role: ontic.account
  ```

* Voer het playbook uit:

  ``$ ansible-playbook workshop-role.yml``
  
* Controleer of de user is aangemaakt (vervang ``<ip address>`` door het IP adres van je Raspberry Pi):

  ``$ ssh -l workshop <ip address>``
  
  ```
  workshop@raspberry's password: 
  Linux raspberry 4.9.0-8-amd64 #1 SMP Debian 4.9.130-2 (2018-10-27) x86_64
  $
  ```

# Praktijk voorbeeld
In de praktijk plaats je de variablen in files die je defineerd in je playbook (zie: https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html). Voor webservers zou je een file ``webserver_vars.yml`` kunnen maken, met daarin een beschrijving van de ``accounts``, ``databases`` en ``virtual_hosts``. Het playbook zou dan (fictief) bestaan uit 3 roles: ``accounts``,``mysql`` en ``apache``.

Onderstaand is slechts een voorbeeld (en hoeft dus niet uitgevoerd te worden):

**webserver_vars.yml**:

```
---
account_groups:
  - name: "workshop"
account_users:
  - name: "workshop"
    password: "$6$uj/GXuBze4eetOeT$ksVseNMTnsRdkVFqUyTICzxri9TeRnsqJyUZVRiiy6ChlDurXWsTkAOdPuSNOPJtPNnzkmrXzfx753hglmH5M/"

mysql_root_password: root-password"
mysql_users:
  - name: 'deployer'
    host: '%'
    password: 'strong-password'
    priv: 'my-database.*:ALL'
  - name: 'oldclient'
    state: 'absent'
mysql_databases:
  - name: 'application_database'
    encoding: 'utf8'
    collation: 'utf8_general_ci'
  - name: 'old_database'
    state: 'absent'

apache_vhosts:
  - servername: "local.dev"
    documentroot: "/var/www/html"
```

**playbook.yml**:

```
- hosts: webservers
  vars_files:
    - webserver_vars.yml
  roles:
    - role: accounts
    - role: mysql
    - role: apache
```

Het variable bestand beschrijft precies hoe de webservers er uit moeten zien en het playbook wordt ineens een stuk overzichtelijker.
  
Volgende stap: [Lab 6 - Vault - Encryptie gebruiken](/labs/06_NL_vault.md)
