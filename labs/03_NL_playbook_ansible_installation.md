# Lab 3: Playbook - Ansible installeren
In dit lab gaan we Ansible installeren. We gebruiken de git versie, omdat de versie die je met apt-get kunt installeren inmiddels al erg verouderd is. Uit git kunnen we de meest versie installeren, of zelfs een specifieke versie kiezen.

## Task 3.1: Dependancies installeren
Om Ansible goed te kunnen laten werken is het nodig om dependancies te installeren. In Ansible is het mogelijk om een lijst te makem met deze dependancies, om deze daarna te installeren.

* Bewerk je playbook:

  ``$ vi workshop.yml``
  
* Vul deze aan met:

  ```
     - name: Install a list of packages
       apt:
         name: "{{ packages }}"
       vars:
         packages:
         - ieee-data
         - python-netaddr
         - python-kerberos
         - python-selinux
         - python-xmltodict
         - python-httplib2
         - python-jinja2
         - python-yaml
         - python-paramiko
         - python-cryptography
         - python-setuptools
         - sshpass
         - git
  ```
  
**Tip:** In Ansible kun je werken met variablen. Variablen worden altijd genoteerd tussen {{ en }}. Als je variablen gebruikt moet de hele waarde genoteerd worden tussen double-quotes: ". In de variable ``packages`` in het bovenstaande playbook is een lijst gemaakt. De onderdelen van deze lijst start je in Ansible gewoon met een -. Zo ontstaat een leesbare lijst.

* Test je playbook:

  ``$ ansible-playbook workshop.yml``

**Het playbook faalt:**

```
TASK [Install a list of packages] **********************************************************************************************
fatal: [pi]: FAILED! => {"cache_update_time": 1549370348, "cache_updated": false, "changed": false, "msg": "'/usr/bin/apt-get
-y -o \"Dpkg::Options::=--force-confdef\" -o \"Dpkg::Options::=--force-confold\"     install 'ieee-data' 'python-netaddr' 
'python-kerberos' 'python-selinux' 'python-xmltodict' 'python-httplib2' 'python-jinja2' 'python-yaml' 'python-paramiko' 
'python-cryptography' 'python-setuptools' 'sshpass'' failed: E: Could not open lock file /var/lib/dpkg/lock - open (13: 
Permission denied)\nE: Unable to lock the administration directory (/var/lib/dpkg/), are you root?\n", "rc": 100, "stderr":
"E: Could not open lock file /var/lib/dpkg/lock - open (13: Permission denied)\nE: Unable to lock the administration directory 
(/var/lib/dpkg/), are you root?\n", "stderr_lines": ["E: Could not open lock file /var/lib/dpkg/lock - open (13: Permission 
denied)", "E: Unable to lock the administration directory (/var/lib/dpkg/), are you root?"], "stdout": "", "stdout_lines": []}
```

Als je goed kijkt naar de foutmeldingen, dan lijkt het er op dat er een rechten probleem is. Wanneer je de packages met ``apt-get`` zou installeren, zou je daar ``sudo`` voor gebruiken. Met Ansible is dat eigenlijk niet anders. Om de packages te installeren, zullen we Ansible moeten instrueren om ``sudo`` te gebruiken

**Tip:** Naast ``sudo`` ondersteund Ansible ook andere methoden om meer rechten te verkrijgen. Zie https://docs.ansible.com/ansible/latest/user_guide/become.html.

## Task 3.2: Task met sudo rechten starten
In Ansible is de variable ``become`` verantwoordelijk voor het starten van een playbook met meer rechten. De methode daarvoor stel je in met ``become_method``.

* Bewerk je playbook:

  ``$ vi workshop.yml``
  
* Zet onder ``hosts``:

  ```
    become: true
    become_method: sudo
  ```
  
* Start het playbook opnieuw en controleer of er nu wel voldoende rechten zijn om packages te installeren.

  ``$ ansible-playbook workshop.yml``

**Tip:** De Raspberry is standaard geconfigueerd dat sudo niet om een wachtwoord vraagt (``NOPASSWD: ALL``). Daarom kunnen we het playbook starten zonder ``-K``. In productie omgevingen is het echter gebruikelijk om sudo met een wachtwoord te starten. Met ``-K`` kun je dit wachtwoord aan Ansible doorgeven.

## Task 3.3: Ansible via Git installeren.
Ansible heeft een ``git`` module. Deze module kan een repository downloaden naar een specifieke directory.

* Bewerk je playbook:

  `` $ vi workshop.yml``
  
* Vul je playbook aan met:

  ```
      - name: "Ensure ansible is installed"
        git:
          repo: "git://github.com/ansible/ansible.git"
          version: v2.7.6
          dest: /opt/ansible
  ```

**Tip:** Controleer altijd de handleiding van Ansible om je playbook nog slimmer te maken. In deze stap gebruiken we de parameter ``version`` om een specifieke versie te selecteren om via git te downloaden.

* Start het playbook.

  ``$ ansible-playbook workshop.yml``
