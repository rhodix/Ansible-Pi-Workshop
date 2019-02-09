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
      - python-yaml
      - python-cryptography
      - python-setuptools
      - sshpass
  ```

* Test je playbook:

  ``$ ansible-playbook workshop.yml``

