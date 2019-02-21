# Lab 4: Playbook - Ansible configureren
In dit lab gaan we Ansible configureren, zodat Ansible vanuit elk path gestart kan worden.

## Task 4.1: Ansible configureren
Om Ansible te kunnen starten uit de git reposistory moet deze geconfigureerd worden. Ansible levert hiervoor een script mee.
  
* Vul je playbook aan met:

  ```
     - name: "Ensure ansible is configured"
       command: /bin/sh /opt/ansible/hacking/env-setup
       args:
         creates: /opt/ansible/lib/ansible.egg-info/requires.txt
  ```

**Tip:** De Ansible modules ``command`` of ``shell`` zijn een laatste redmiddel. Probeer je probleem altijd op te lossen met Ansible modules. Pas als er nog geen module bestaat voor je probleem, grijp je terug op de ``command`` module. Met deze mpdule kun je in principe elk commando uitvoeren.

## Task 4.2: Environment variablen configureren
De laatste stap is het zetten van de environment variablen. Daarnaast voegen we ``/opt/ansible/bin`` toe aan de path variable, zodat Ansible vanuit elk path te starten is. We voegen daarvoor een block toe aan ``/etc/bash.bashrc``.

* Vul je playbook aan met:

  ```
     - name: "Ensure ansible variables are set in bashrc"
       blockinfile:
         path: /etc/bash.bashrc
         block: |
           export PATH=/opt/ansible/bin:$PATH
           export PYTHONPATH=/opt/ansible/lib
           export MANPATH=/opt/ansible/docs/man:$MANPATH
           export ANSIBLE_HOME=~/ansible
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

* Log in op je Raspberry (vervang met het IP adres van je Raspberry Pi):

  ``$ ssh -l pi <ipaddress>``
  
* Controleer de versie van Ansible (2.7.6):

  ``$ ansible --version``
  
  ```
  ansible 2.7.6 (detached HEAD 1594ccf533) last updated 2019/02/09 21:47:22 (GMT +200)
    config file = None
    configured module search path = [u'/home/pi/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
    ansible python module location = /opt/ansible/lib/ansible
    executable location = /opt/ansible/bin/ansible
    python version = 2.7.13 (default, Sep 26 2018, 18:42:22) [GCC 6.3.0 20170516]
  ```

* Test of het ``adhoc`` commando ``ping`` werkt. Je kunt dit zonder inventory testen met ``localhost``:

  ``$ ansible -m ping localhost``
  
  ```
  localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
  }
  ```
  
   
Volgende stap: [Lab 5 - Role - User aanmaken](/labs/05_NL_role_user.md)
