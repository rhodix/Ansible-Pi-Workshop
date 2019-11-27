# Lab 4: Playbook - Workshop voorzetten vanaf de Raspberry Pi
In dit lab gaan we de workshop files overzetten naar de Raspberry Pi, zodat de rest van de workshop vanaf de Raspberry Pi uitgevoerd kan worden.

## Task 4.1: Workshop files overzetten
Om de workshop files over te zetten, maken we gebruik van de copy module om de files naar de Pi te kopieëren.
  
* Vul je playbook aan met:

  ```
    - name: "Ensure Ansible workshop files are copied to the pi"
      copy:
        src: "{{ item }}"
        dest: "/home/pi/{{ item }}"
        owner: "pi"
        group: "pi"
      with_items:
      - ansible.cfg
      - inventory
      - workshop.yml
  ```

**Tip:** Met ``with_items`` kun je een lijst genereren. Ansible vult dan steeds de variable ``item`` met de onderdelen uit de lijst.

## Task 4.2: SSH key overzetten
De laatste stap is het overzetten van de SSH key. 

* Vul je playbook aan met:

  ```
    - name: "Ensure SSH key is installed on the pi"
      copy:
        src: "~/.ssh/{{ item }}"
        dest: "/home/pi/.ssh/{{ item }}"
        owner: "pi"
        group: "pi"
        mode: "0600"
      with_items:
      - id_rsa
      - id_rsa.pub
  ```

* Start het playbook. Als alles goed is gegaan, is nu Ansible start-klaar op je Raspberry!

  ``$ ansible-playbook workshop.yml``

**Tip:** Mocht er onverhoopt wat mis zijn gegaan, download dan het playbook via: https://raw.githubusercontent.com/rhodix/Ransible-Pi-Workshop/master/downloads/workshop.yml.

## Task 4.3: Werking testen
Als het playbook alleen nog maar "ok" meldingen geeft, is het tijd om in te loggen op de Raspberry Pi, om te controleren of Ansible werkt.

```
PLAY RECAP ****************************************************************************************************************************
pi                         : ok=6    changed=0    unreachable=0    failed=0
```

* Log in op je Raspberry (vervang ``<ipaddress>`` met het IP adres van je Raspberry Pi):

  ``$ ssh -l pi <ipaddress>``
  
* Controleer de versie van Ansible (2.9.0):

  ``$ ansible --version``
  
  ```
  ansible 2.9.0
    config file = /home/pi/ansible.cfg
    configured module search path = [u'/home/pi/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
    ansible python module location = /usr/local/lib/python2.7/dist-packages/ansible
    executable location = /usr/local/bin/ansible
    python version = 2.7.16 (default, Oct 10 2019, 22:02:15) [GCC 8.3.0]
  ```

* Test of het ``adhoc`` commando ``ping`` werkt:

  ``$ ansible -m ping workshop``
  
  ```
  pi | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
  }
  ```

* Voer het playbook uit:

  ``$ ansible-playbook workshop.yml``
   
Volgende stap: [Lab 5 - Role - User aanmaken](/labs/05_NL_role_user.md)
