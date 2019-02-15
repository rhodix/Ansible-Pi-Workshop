# Lab 5: Role - User aanmaken
Voor bijna elke uitdaging is wel een kant-en-klare rol te vinden op Ansible Galaxy. Het nadeel is echter dat er te veel roles te vinden zijn, waardoor het lastig is om de parels te vinden. Let bijvoorbeeld op het aantal downloads en het aantal sterren. Bekijk altijd de broncode van de role die je op Ansible Galaxy hebt gevonden en controleer of deze precies doet wat je zoekt. Indien nodig kun je de role altijd aanpassen.

Bijna alle rollen zijn te sturen met variablen. Deze zijn vaak beschreven in de documentatie van de role. Als de beschrijving ontbreekt kun je in de directory ``defaults`` en in de directory ``vars`` de definitie van de variablen terug vinden.

We gaan de role ``ontic.account`` installeren via Ansible Galaxy. 

## Task 5.1: Role installeren

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
  
Een beschrijving van de onderdelen van een role vind je terug in de documentatie van Ansible op: https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html.

**Tip:** Het vervolg van de workshop wordt vanuit je home directory uitgevoerd. Ga terug naar je home directory met het commando: ``$ cd``.

## Task 5.2: Password hash genereren
De ``user`` module verwacht het wachtwoord in SHA512 formaat. 

* Je kunt Ansible gebruiken om een SHA512 hash te genereren (vervang <WorkshopPassword> door een eigen wachtwoord):

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

# Praktijk voorbeeld.
In de praktijk plaats je de variablen in files die je defineerd in je playbook (zie: https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html). Voor webservers zou je een file ``webserver_vars.yml`` kunnen maken, met daarin een beschrijving van de ``accounts``, ``databases`` en ``virtual_hosts``. Het playbook zou dan (fictief) bestaan uit 3 roles: ``accounts``,``mysql`` en ``apache``.

webserver_vars.yml:

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

playbook.yml:

```
- hosts: webservers
  vars_files:
    - webserver_vars.yml
  roles:
    - role: accounts
    - role: mysql
    - role: apache
```



  
