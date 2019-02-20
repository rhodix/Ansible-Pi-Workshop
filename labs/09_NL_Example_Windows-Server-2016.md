# Lab 9: Example - Windows Server 2016
In dit lab gaan we een Windows Server 2016 VM configureren.

Ansible heeft veel kant-en-klare modules om Windows te configureren en beheren. Denk bijvoorbeeld aan het installeren van extra roles of features, installatie van MSI pakketten of aanpassen van de firewall. Natuurlijk zijn er ook modules voor basis taken, zoals files bewerken / kopieëren. Mocht er toch geen standaard module zijn voor je probleem, dan kun je altijd terugvallen op de modules ``win_command`` of ``win_psexec`` (voor Powershell commando's). Een overzicht van alle modules vind je terug op: https://docs.ansible.com/ansible/latest/modules/list_of_windows_modules.html.

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

* Vul de inventory file met (vervang <ipaddress> door het IP adres van de switch):

  ```
  [windows]
  windows-01 ansible_host=<ipaddress>

  [windows:vars]
  ansible_connection=winrm
  ansible_user=administrator
  ansible_winrm_server_cert_validation=ignore
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

