# Lab 8: Example - Brocade ICX Switch
In dit lab gaan we een Brocade ICX Switch configureren.

**Note:** Dit lab wordt uitgevoerd op echte hardware. Let er op dat je geen wijzigingen uitvoerd op de Management port, zodat je de verbinding met de switch niet verliest. 

De modules voor Brocade switches (Ironware) zijn helaas niet zo uitgebreid als modules van andere merken (bijvoorbeeld Cisco IOS). De module ``ironware_command`` is geschikt voor het uitvoeren van adhoc of enkele commando's. In een playbook kun je beter de ``ironware_config`` module gebruiken. Hoewel je met deze module in principe elk onderdeel van je switch configuratie kunt uitvoeren, vereist dit nog wel kennis van de werking van Brocade ICX switches. Bij Cisco IOS of Juniper Junos zijn er biijvoorbeeld modules om VLAN's aan te maken, of poorten te configureren. Daarbij is geen kennis nodig van de daadwerkelijke commando's die uitgevoerd moeten worden op de switch.

Toch kan het nuttig zijn om de configuratie van je switch te automatiseren. Een playbook zou op de switch een vlan aan kunnen maken, vervolgens in de virtualisatie infrastructuur dit vlan aanmaken in de vSwitch en vervolgens een VM in dit netwerk kunnen zetten.

## Task 8.1: Bug in Ansible module oplossen en SSH configureren
Helaas zit er een bug in de Ansible module ``ironware_config``. Voordat we de Brocade ICX switch kunnen configureren moeten we eerst een bug herstellen. Zorg er voor dat je ingelogd bent op de SSH server (en nog niet op je Raspberry Pi).

* Maak de directory ``files`` aan:
  
  ``$ mkdir files``
  
* Download de fix in de ``files`` directory:

  ``$ curl https://raw.githubusercontent.com/rhodix/Ransible-Pi-Workshop/master/downloads/ironware.patch > files/ironware.patch``
  
* Vul je playbook aan met:

  ```
      - name: Ensure the ironware module is patched
        patch:
          src: files/ironware.patch
          dest: /opt/ansible/lib/ansible/plugins/terminal/ironware.py
  ```

Verder ondersteund de switch helaas de laatste encryptie methodes voor SSH nog niet. 

* Vul je playbook aan met:
  
  ```
      - name: Ensure SSH is configured with supported encryption methods
        blockinfile:
          path: ~/.ssh/config
          block: |
            Host 172.17.16.*
              KexAlgorithms +diffie-hellman-group1-sha1
          create: Yes
        become: false
  ```  
  **Tip:** De SSH configuratie moet in het account van de user ``pi`` uitgevoerd worden. Het playbook wordt echter door ``become: true`` als root uitgevoerd. In de task voor SSH zetten we ``become`` tijdelijk op ``false``, zodat de taak voor het account ``pi`` wordt uitgevoerd.
  
* Start je playbook:
  
  ``$ ansible-playbook workshop.yml``

  ```
  TASK [Ensure the ironware module is patched*****************************************************************************
  changed: [pi]

  TASK [Ensure SSH is configured with supported encryption methods] ******************************************************
  changed: [pi]

  PLAY RECAP *************************************************************************************************************
  pi                         : ok=7    changed=2    unreachable=0    failed=0
  ```

## Task 8.2: Inventory aanpassen
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

## Task 8.3: Playbook maken - SNMP configureren
Een simpel voorbeeld om mee te starten is het configureren van SNMP. Daarvoor moeten de volgende 2 regels in de switch worden configureerd:

```
snmp-server contact ansible@demo.local
snmp-server location Demorack
```

* Maak het playbook ``brocade.yml``:

  ```
  ---
  - hosts: switches
    connection: local
    gather_facts: false
    remote_user: workshop

    tasks:

    - name: Configure SNMP
      ironware_config:
        lines:
          - snmp-server contact ansible@demo.local
          - snmp-server location Demorack
  ```

* Voer je playbook uit:

  ``$ ansible-playbook brocade.yml --ask-pass``

## Task 8.4: Playbook maken - Switchpoorten en VLANs configureren
In het volgende playbook gaan we switchpoorten en vlans configureren.

**Tip:** Voor het configureren van poorten in VLANs gebruiken we een variable: ``switchport``. Deze variable heeft 2 sub-elements: ``vlan`` en ``port``. In Ansible kun je deze variablen gebruiken door ze tussen een ``{`` en ``}`` te zetten. Als je variablen gebruikt moet de hele waarde genoteerd worden tussen double-quotes: ``"``
  
* Vul het playbook aan met (zet tussen ``remote_user`` en ``tasks``):

  ```
    vars:
      switchport:
        vlan: 350
        port: 1/1/10
  ```

* Maak de tasks aan (in het einde van je playbook):

  ```
    - name: "Create VLAN {{ switchport.vlan }}"
      ironware_config:
        lines:
          - "vlan {{ switchport.vlan }} by port"

    - name: "Add port {{ switchport.port}} to VLAN {{ switchport.vlan }}"
      ironware_config:
        lines:
          - "untagged ethernet {{ switchport.port }}"
        parents: ["vlan {{ switchport.vlan }} by port"]

  ```

* Voer je playbook uit:
  ``$ ansible-playbook brocade.yml --ask-pass``

Het toevoegen van een VLAN, of meerdere poorten aan een VLAN, is nu een kwestie van aanpassen van de variable en het playbook opnieuw starten:

  * Zet switchpoort 1/1/11 in vlan 351, door de variable aan te passen en het playbook opnieuw te starten.
  * Voeg switchpoort 1/1/12 ook toe aan vlan 351.
  
## Task 8.5: Variable list
Wanneer je de hele configuratie vanuit Ansible zou doen, kun je zelfs het playbook gebruiken voor disaster recovery. Bij problemen sluit je gewoon een nieuwe switch aan en draai je het playbook. Het zou daarbij natuurlijk wel handiger zijn om een lijst met poorten en vlans te hebben, in plaats van steeds het playbook met het juiste vlan aan te moeten passen. In de praktijk zul je daarom vaak met variable lijsten werken, om alle poorten in 1 play in het juiste VLAN te zetten. 

```
  vars:
    switchports:
      - { port: 1/1/10, vlan: 350 }
      - { port: 1/1/11, vlan: 351 }
      - { port: 1/1/12, vlan: 351 }
```

De task van je playbook ziet er dan zo uit:

```
  - name: "Add ports to VLAN" 
    ironware_config:
      lines:
        - "untagged ethernet {{ item.port }}"
      parents: ["vlan {{ item.vlan }} by port"]
    with_items: "{{ switchports }}"
```

* Pas je playbook aan met de bovenstaande onderdelen en voer deze uit.

**Tip:** Mocht er onverhoopt wat mis zijn gegaan, download dan het playbook via: https://raw.githubusercontent.com/rhodix/Ransible-Pi-Workshop/master/downloads/brocade.yml.

## Task 8.6: Controleer het resultaat
Is het je opgevallen dat je nog niet bent ingelogd op de switch? Met SSH kun je inloggen op de switch. Via het commando ``show running-config`` kun je het resultaat controleren:

* Log in op de switch (vervang ``<ipaddress>`` door het IP adres van de switch):

  ``$ ssh -l workshop <ipaddress>``
  
  ```
  Password:
  SSH@test-switch-02#
  ```

* Controleer de configuratie:

  ``# show running-config``
  
  ```
  ...
  vlan 350 by port
   untagged ethe 1/1/10
  !
  vlan 351 by port
   untagged ethe 1/1/11 to 1/1/12
  ...
  snmp-server contact ansible@demo.local
  snmp-server location Demorack
  ...
  ```
  
