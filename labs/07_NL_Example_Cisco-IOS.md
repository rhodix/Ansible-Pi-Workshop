# Lab 7: Example - Cisco IOS Switch
In dit lab gaan we een Cisco IOS Switch configureren.

**Note:** Dit lab wordt uitgevoerd op echte hardware. Let er op dat je geen wijzigingen uitvoerd op de port ``GigabitEthernet0/2``, zodat je de verbinding met de switch niet verliest. 

Voor Cisco IOS zijn diverse modules beschikbaar die het configureren van poorten, routes, vlans etc. erg gemakkelijk maken. Zie https://docs.ansible.com/ansible/latest/modules/list_of_network_modules.html#ios voor het complete overzicht van modules. Tevens zijn de 3 "standaard" modules ``ios_facts``, ``ios_command`` en ``ios_config`` aanwezig, zodat elke uitdaging met Ansible geautomatiseerd kan worden.

## Task 7.1: Inventory aanpassen
Voer deze task uit op je Raspberry Pi.

* Log in op je Raspberry Pi.

  ``$ ssh -l pi <ipaddress>`` 

* Als het goed is log je direct in (zonder wachtwoord):

  ``` 
  pi@raspberry:~ $ 
  ```

* Maak een inventory file:

  ``$ vi inventory``

* Vul de inventory file met (vervang ``<ipaddress>`` door het IP adres van de switch:

  ```
  [switches]
  switch-01 ansible_host=<ipaddress>
  ```

* Maak een ansible.cfg aan:

  ``$ vi ansible.cfg``

* Vul de ansible.cfg met:

  ```
  [defaults]
  inventory = ~/inventory
  remote_user = workshop
  
  host_key_checking = False
  ```

## Task 7.2: Playbook maken
Een simpel voorbeeld om mee te starten is het configureren van de inlog banner.

* Maak het playbook ``cisco.yml``:

  ```
  ---
  - hosts: switches
    connection: local
    gather_facts: false
    remote_user: workshop

    tasks:
    - name: Configure banner
      ios_banner:
        banner: login
        text: |
          Dit is een demo switch
        state: present
  ```
  
* Voer je playbook uit:

  ``$ ansible-playbook cisco.yml --ask-pass``
  
Note: Enkele demo switches werken nog met oude Ciphers. Pas eventueel de file ``~/.ssh/config`` aan:
```
Host <ip address>
   Ciphers aes128-cbc,3des-cbc,aes192-cbc,aes256-cbc
```
  
## Task 7.3: Playbook maken - Switchpoorten en VLANs configureren

In het volgende playbook gaan we switchpoorten en vlans configureren.

**Tip:** Voor het configureren van poorten in VLANs gebruiken we een variable: ``switchport``. Deze variable heeft 2 sub-elements: ``vlan`` en ``port``. In Ansible kun je deze variablen gebruiken door ze tussen een ``{`` en ``}`` te zetten. Als je variablen gebruikt moet de hele waarde genoteerd worden tussen double-quotes: ``"``
  
* Vul het playbook aan met (zet tussen ``remote_user`` en ``tasks``):

  ```
    vars:
      switchport:
        vlan: 350
        port: FastEthernet0/10
  ```

* Maak de tasks aan (in het einde van je playbook):

  ```
    - name: Create vlan
      ios_vlan:
        vlan_id: "{{ switchport.vlan }}"
        name: test-vlan
        state: present

    - name: Add interfaces to VLAN
      ios_vlan:
        vlan_id: "{{ switchport.vlan }}"
        interfaces:
          - "{{ switchport.port }}"
  ```

* Voer je playbook uit:
  ``$ ansible-playbook cisco.yml --ask-pass``

Het toevoegen van een VLAN, of meerdere poorten aan een VLAN, is nu een kwestie van aanpassen van de variable en het playbook opnieuw starten:

* Zet switchpoort 0/11 in vlan 351, door de variable aan te passen en het playbook opnieuw te starten.
* Voeg switchpoort 0/12 ook toe aan vlan 351.
  
## Task 7.4: Variable list
Wanneer je de hele configuratie vanuit Ansible zou doen, kun je zelfs het playbook gebruiken voor disaster recovery. Bij problemen sluit je gewoon een nieuwe switch aan en draai je het playbook. Het zou daarbij natuurlijk wel handiger zijn om een lijst met poorten en vlans te hebben, in plaats van steeds het playbook met het juiste vlan aan te moeten passen. In de praktijk zul je daarom vaak met variable lijsten werken, om alle poorten in 1 play in het juiste VLAN te zetten. 

```
    switchports:
      - vlan: 350
        ports:
          - FastEthernet0/10
      - vlan: 351
        ports:
          - FastEthernet0/11
          - FastEthernet0/12
```

De task van je playbook ziet er dan zo uit:

```
  - name: "Add ports to VLAN"
    ios_vlan:
      vlan_id: "{{ item.vlan }}"
      interfaces: "{{ item.ports }}"
    with_items: "{{ switchports }}"
 ```
 
 
 * Pas je playbook aan met de bovenstaande onderdelen en voer deze uit.

**Tip:** Mocht er onverhoopt wat mis zijn gegaan, download dan het playbook via: https://raw.githubusercontent.com/rhodix/Ransible-Pi-Workshop/master/downloads/cisco.yml.

## Task 7.5: Controleer het resultaat
Is het je opgevallen dat je nog niet bent ingelogd op de switch? Met SSH kun je inloggen op de switch. Via het commando ``show running-config`` kun je het resultaat controleren:

* Log in op de switch (vervang ``<ipaddress>`` door het IP adres van de switch):

  ``$ ssh -l workshop <ipaddress>``
  
  ```
  Dit is een demo switch
  Password:

  test-switch-01#  
  ```

* Controleer de configuratie:

  ``# show running-config``

  ```
  ...
  !
  interface FastEthernet0/10  
   switchport access vlan 350
   switchport mode access
  !
  interface FastEthernet0/11
   switchport access vlan 350
   switchport mode access
  !
  interface FastEthernet0/12
   switchport access vlan 351
   switchport mode access
  !
  ...
  !
  banner login ^C
  Dit is een demo switch
  ^C
  !
  ...
  ```
