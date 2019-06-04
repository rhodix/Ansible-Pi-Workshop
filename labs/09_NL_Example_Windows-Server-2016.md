# Lab 9: Example - Windows Server 2016
In dit lab gaan we een Windows Server 2016 VM configureren.

Ansible heeft veel kant-en-klare modules om Windows te configureren en beheren. Denk bijvoorbeeld aan het installeren van extra roles of features, installatie van MSI pakketten of aanpassen van de firewall. Natuurlijk zijn er ook modules voor basis taken, zoals files bewerken / kopieëren. Mocht er toch geen standaard module zijn voor je probleem, dan kun je altijd terugvallen op de modules ``win_command`` of ``win_psexec`` (voor Powershell commando's). Een overzicht van alle modules vind je terug op: https://docs.ansible.com/ansible/latest/modules/list_of_windows_modules.html.

De Windows VM in deze workshop is al voorbereid op Ansible. De handleiding voor het voorbereiden van Windows op Ansible vind je terug op: https://www.ansible.com/blog/connecting-to-a-windows-host.

## Task 9.1: Inventory aanpassen

Voer deze task uit op je Raspberry Pi.

* Log in op je Raspberry Pi.

  ``$ ssh -l pi <ipaddress>`` 

* Als het goed is log je direct in (zonder wachtwoord):

  ``` 
  pi@raspberry:~ $ 
  ```

* Maak een inventory file:

  ``$ vi inventory``

* Vul de inventory file met (vervang ``<ipaddress>`` door het IP adres van de windows server):

  ```
  [windows]
  windows-01 ansible_host=<ipaddress>

  [windows:vars]
  ansible_connection=winrm
  ansible_winrm_server_cert_validation=ignore
  ansible_user=workshop
  ```

**Tip:** Voor Windows dient de ``ansible_connection`` aangepast te worden naar winrm (Windows Remote Management). De WinRM module gebruikt SSL om de verbinding te beveiligen. Het SSL certificaat dient dan wel vertrouwd te worden. In een enterprise omgeving is meestal een PKI infrastructuur aanwezig, waardoor alleen het root certificaat geïnstalleerd hoeft te worden. Alle certificaten, ondertekend met dit root certificaat, worden daarmee automatisch vertrouwd. In deze workshop hebben we geen PKI. We schakelen daarom de verificatie uit met de variable ``ansible_winrm_server_cert_validation``.

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

Waar je voor Linux de module ``ping`` zou gebruiken, moet je voor Windows de module ``win_ping`` gebruiken. De werking is verder hetzelfde:

* Test de verbinding met ``win_ping``

  ``$ ansible -m win_ping windows --ask-pass``
  
  ```
  windows-01 | SUCCESS => {
    "changed": false,
    "ping": "pong"
  }
  ```

## Task 9.3: IIS Webserver role installeren

* Maak het playbook ``windows.yml``:

  ```
  ---
  - hosts: windows

    tasks:
      - name: Install IIS Web-Server with sub features and management tools
        win_feature:
          name:
          - Web-Server
          include_sub_features: yes
          include_management_tools: yes
  ```
  
  * Voer het playbook uit:
  
    ``$ ansible-playbook windows.yml --ask-pass``
    
    ```
    PLAY [windows] ****************************************************************************

    TASK [Gathering Facts] ********************************************************************
    ok: [windows-01]

    TASK [Install IIS Web-Server with sub features and management tools] **********************
    changed: [windows-01]

    PLAY RECAP ********************************************************************************
    windows-01                 : ok=2    changed=1    unreachable=0    failed=0
    ```
 
## Task 9.4: Packages installeren met Chocolatey
 
Bijna elke Linux distributie heeft wel een package manager. Voor Debian varianten is dat ``apt`` en op Red Hat varianten is dat ``yum``. Voor Windows is er standaard geen package manager. Maar er bestaat wel 3rd party software die deze rol kan vervullen. Een voorbeeld daarvan is ``Chocolatey`` (zie: https://chocolatey.org/). Ansible heeft een module om packages via Chocolatey te installeren. Een overzicht van deze packages is te vinden op: https://chocolatey.org/packages. Ideaal voor installatie van standaard software die op bijna elk Windows systeem is te vinden (bijvoorbeeld Adobe Acrobat Reader: ``adobereader`` of Java: ``jre8``).
 
* Vul je playbook ``windows.yml`` aan met:

  ```
      - name: Install packages with Chocolatey
        win_chocolatey:
          name: '{{ item }}'
        with_items:
        - adobereader
        - putty
        - windirstat
        - googlechrome
  ```
  
  * Voer het playbook uit:
  
    ``$ ansible-playbook windows.yml --ask-pass``
    
    ```
    TASK [Install packages with Chocolatey] **************************************************
    changed: [windows-01] => (item=adobereader)
    changed: [windows-01] => (item=putty)
    changed: [windows-01] => (item=windirstat)
    changed: [windows-01] => (item=googlechrome)
     [WARNING]: Chocolatey was missing from this system, so it was installed during this task run.

    PLAY RECAP *******************************************************************************
    windows-01                 : ok=3    changed=1    unreachable=0    failed=0
    ```
  
**Tip:** Chocolaty is standaard niet geïnstalleerd. De module ``win_chocolatey`` installeerd automatisch Chocolatey. Omdat dit nog niet geïnstalleerd was, krijg je de warning ``Chocolatey was missing from this system, so it was installed during this task run.``

## Task 9.5: Windows update

Met Ansible kun je Windows updates geautomatiseerd uitvoeren. In deze workshop gaat het maar om 1 server, maar dit kan natuurlijk op meerdere servers tegelijk. Zelfs automatisch herstarten is mogelijk.

* Vul je playbook ``windows.yml`` aan met:

  ```
      - name: Install Windows Update
        win_updates:
          category_names:
          - SecurityUpdates
          reboot: yes
  ```

* Voer het playbook uit:
  
    ``$ ansible-playbook windows.yml --ask-pass``
