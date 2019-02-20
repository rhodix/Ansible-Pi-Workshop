# Lab 10: Example - Linux Server

In dit lab gaan we een Linux server configureren.

## Task 10.1: Inventory aanpassen

Voer deze task uit op je Raspberry Pi.

* Log in op je Raspberry Pi.

  ``$ ssh -l pi <ipaddress>`` 

* Als het goed is log je direct in (zonder wachtwoord):

  ``` 
  pi@raspberry:~ $ 
  ```

* Maak een inventory file:

  ``$ vi inventory``

* Vul de inventory file met (vervang <ipaddress> door het IP adres van de switch):

  ```
  [linux]
  linux-01 ansible_host=<ipaddress>
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

## Task 9.2: Verbinding testen

* Test de verbinding met de module ``ping``

  ``$ ansible -m ping linux --ask-pass``
  
  ```
  linux-01 | SUCCESS => {
    "changed": false,
    "ping": "pong"
  }
  ```
  
## Task 9.3: Apache installeren

* Maak het playbook ``linux.yml``:

  ```
  ---
  - hosts: linux

    tasks:
      - name: Install apache packages
        yum:
          name: httpd

      - name: ensure httpd is running
        service:
          name: httpd 
          state: started
  ```

* Voer het playbook uit:

  ``$ ansible-playbook linux.yml -k``
  
 ## Task 9.4: Firewall configureren
 
 * Pas het playbook ``linux.yml`` aan:
 
   ```
       - name: Ensure port 80 is open for http access
         firewalld:
           service: http
           permanent: true

       - name: Ensure firewalld service is restarted after the firewall changes
         service: 
           name: firewalld 
           state: restarted
   ```
   
   
