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
  
