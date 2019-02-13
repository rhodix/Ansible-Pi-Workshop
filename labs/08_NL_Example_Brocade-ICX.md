# Lab 8: Example - Brocade ICX Switch
In dit lab gaan we een Brocade ICX Switch configureren. Helaas zit er een bug in de Ansible module. Deze moet eerst opgelost worden.

**Note:** Dit lab wordt uitgevoerd op echte hardware. Let er op dat je geen wijzigingen uitvoerd op poort 1/1/24, zodat je de verbinding met de switch niet verliest. 

## Task 8.1: Bug in Ansible module oplossen
Voordat we de Brocade ICX switch kunnen configureren moeten we eerst een bug herstellen. Zorg er voor dat je ingelogd bent op de SSH server (en nog niet op je Raspberry Pi).

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
