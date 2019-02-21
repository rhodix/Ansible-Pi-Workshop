# Lab 10: Example - Linux Server

In dit lab gaan we een Linux server configureren.

Linux is het Operating System waarvoor verreweg de meeste Ansible modules te vinden zijn. Voor vrijwel elke uitdaging is wel een Ansible module (of role) te vinden. In dit lap gaan we in 3 stappen een webserver configureren én zelfs de web content installeren. 

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

* Vul de inventory file met (vervang ``<ipaddress>`` door het IP adres van de switch):

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

Om zeker te zijn dat de inventory file ``inventory`` en de config file ``ansible.cfg`` correct zijn, voeren we een test uit met de ``adhoc`` module ``ping``. Ansible vraagt om een wachtwoord. Gebruik hiervoor het wachtwoord van het account ``workshop``.

* Test de verbinding met de module ``ping``

  ``$ ansible -m ping linux --ask-pass``
  
  ```
  linux-01 | SUCCESS => {
    "changed": false,
    "ping": "pong"
  }
  ```
  
## Task 9.3: Apache installeren

De eerste stap is de webserver software installeren. Na installatie moet de webserver natuurlijk gestart worden. Beide acties voeren we uit in het onderstaande playbook.

* Maak het playbook ``linux.yml``:

  ```
  ---
  - hosts: linux
    become: true
    become_method: sudo

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

  ``$ ansible-playbook linux.yml --ask-pass``
  
## Task 9.4: Firewall configureren

Om de webserver goed te laten werken, dient poort 80 (http) open gezet te worden. Hiervoor gebruiken we de Ansible module ``firewalld``. Om er zeker van te zijn dat de nieuwe regel ingelezen wordt, herstarten we ``firewalld`` na de wijziging. 
 
* Pas het playbook ``linux.yml`` aan:
 
  ```
      - name: Ensure port 80 is open for http access
        firewalld:
          service: http
          permanent: true
          state: enabled

      - name: Ensure firewalld service is restarted after the firewall changes
        service: 
          name: firewalld 
          state: restarted
   ```

* Voer het playbook uit:

  ``$ ansible-playbook linux.yml -k``
   
## Task 9.5: Installeer content voor de webserver

Met Ansible kun je eenvoudig content kopieën van je Ansible Engine naar de webserver. In dit voorbeeld installeren we een index.html, welke je daarna via de browser op kunt vragen.

* Maak de directory ``files`` aan:
  
  ``$ mkdir files``
  
* Maak een HTML file aan met content (in de directory files):

  ``$ vi files/index.html``
  
  ```
  <html>
    <body>
      <h1>Hello world</h1>
    </body>
  </html>
  ```
  
* Pas het playbook ``linux.yml`` aan:

  ```
      - name: Ensure content is installed in the webserver
        copy:
          src: files/index.html
          dest: /var/www/html/index.html
          owner: apache
          group: apache
          mode: 0644
  ```
    
* Voer het playbook uit:

  ``$ ansible-playbook linux.yml -k``
  
* Open in je browser de url ``http://<ip address>`` (vervang ``<ipaddress>`` door het IP adres van de Linux server).
