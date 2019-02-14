# Lab 8: Example - Brocade ICX Switch
In dit lab gaan we een Brocade ICX Switch configureren.

**Note:** Dit lab wordt uitgevoerd op echte hardware. Let er op dat je geen wijzigingen uitvoerd op de Management port, zodat je de verbinding met de switch niet verliest. 

De modules voor Brocade switches (Ironware) zijn helaas niet zo uitgebreid als modules van andere merken (bijvoorbeeld Cisco IOS). De module ``ironware_command`` is geschikt voor het uitvoeren van adhoc of enkele commando's. In een playbook kun je beter de ``ironware_config`` module gebruiken. Hoewel je met deze module in principe elk onderdeel van je switch configuratie kunt uitvoeren, vereist dit nog wel kennis van de werking van Brocade ICX switches. Bij Cisco IOS of Juniper Junos zijn er biijvoorbeeld modules om VLAN's aan te maken, of poorten te configureren. Daarbij is geen kennis nodig van de daadwerkelijke commando's die uitgevoerd moeten worden op de switch.

Toch kan het nuttig zijn om de configuratie van je switch te automatiseren. Een playbook zou op de switch een vlan aan kunnen maken, vervolgens in de virtualisatie infrastructuur dit vlan aanmaken in de vSwitch en vervolgens een VM in dit netwerk kunnen zetten.

## Task 8.1: Bug in Ansible module oplossen
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

* Start je playbook:
  
  ``$ ansible-playbook workshop.yml``

  ```
  TASK [Ensure the ironware module is patched] ***************************************************************************************************************************************************
  changed: [pi]

  PLAY RECAP *************************************************************************************************************************************************************************************
  pi                         : ok=7    changed=1    unreachable=0    failed=0
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

* Vul de inventory file met (vervang <ipaddress> door het IP adres van de switch:

  ```
  [switches]
  switch-01 ansible_host=<ip address>
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

## Task 8.3: Playbook maken


