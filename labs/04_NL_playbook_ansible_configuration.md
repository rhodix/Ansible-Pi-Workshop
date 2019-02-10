# Lab 4: Playbook - Ansible configureren
In dit lab gaan we Ansible configureren, zodat Ansible vanuit elk path gestart kan worden.

## Task 4.1: Ansible configureren
Om Ansible te kunnen starten uit de git reposistory moet deze geconfigureerd worden. Ansible levert hiervoor een script mee.
  
* Vul je playbook aan met:

  ```
      - name: Ensure ansible is configured
        command: /bin/sh /opt/ansible/hacking/env-setup
        args:
          creates: /opt/ansible/lib/ansible.egg-info/requires.txt
  ```

**Tip:** De Ansible modules ``command`` of ``shell`` zijn een laatste redmiddel. Probeer je probleem altijd op te lossen met Ansible modules. Pas als er nog geen module bestaat voor je probleem, grijp je terug op de ``command`` module. Met deze mpdule kun je in principe elk commando uitvoeren.

## Task 4.2: Environment variablen configureren
De laatste stap is het zetten van de environment variablen. Daarnaast voegen we ``/opt/ansible/bin`` toe aan de path variable, zodat Ansible vanuit elk path te starten is. We voegen daarvoor een block toe aan ``/etc/bash.bashrc``.

* Vul je playbook aan met:

  ```
      - name: Ensure ansible variables are set in bashrc
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

## Task 4.3: Werking testen
