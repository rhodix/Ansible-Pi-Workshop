# Lab 6: Ansible Vault

Ansible Vault is een functie van Ansible waarmee je gevoelige gegevens, zoals wachtwoorden of private keys (bijvoorbeeld voor SSL certificaten), kunt versleutelen. Dit maakt het mogelijk om deze gegevens toch in een ``SCM`` te zetten. Het is namelijk niet de bedoeling dat je deze gegevens in plain tekst in een ``SCM`` zet.

Vault variablen worden door Ansible automatisch ontsleutelt, mits het ``vault password`` bekend is. Een vault variable begint altijd met ``$ANSIBLE_VAULT;1.1;AES256``.


## Task 6.1: Bestand encrypten

**Tip:** ansible-vault gebruikt standaard de editor ``vi``. Mocht je liever ``nano`` gebruiken, dan kun je de editor aanpassen door de environment variable ``EDITOR`` te vullen met: ``/bin/nano``. Gebruik hiervoor het commando: ``export EDITOR=/bin/nano``.

* Maak een nieuw bestand:

  ``$ ansible-vault create foo``

* Bedenk zelf een wachtwoord:

  ```
  New Vault password:
  Confirm New Vault password:
  ```

* Zet een geheime boodschap in het bestand en sla deze op (in ``vi`` gaat dat met ``:wq``).
* Bekijk het bestand:

  ``$ cat foo``
  
  ```
  $ANSIBLE_VAULT;1.1;AES256
  36323433633666373164336366383438613964306431646537643863343762663465376265326337
  6335663530313034653733323431376236316637643536610a323537336233373139363538383438
  65633532333866356339333238653964633938363661353331373237343366306239313632623935
  3738363065653864660a326666316531643837366161656531366239376338343534336230613832
  6563
  ```

## Task 6.2: Encrypted bestand bewerken

* Edit het bestand:

  ``$ ansible-vault edit foo``

* Ansible vault vraagt om het wachtwoord. Alleen als het wachtwoord correct wordt ingevoerd zal de editor openen

  ```
  Vault password:
  ```

* Maak een wijziging en sla het bestand weer op.


## Task 6.3: Encrypted bestand inzien

* Bekijk het bestand:

  ``$ ansible-vault view foo``

* Ansible vault vraagt om het wachtwoord. Alleen als het wachtwoord correct wordt ingevoerd zal het bestand weergegeven worden:

  ```
  Vault password:
  <inhoud van het bestand>
  ```

## Task 6.4: Wachtwoord wijzigen van een encrypted bestand

* Pas het wachtwoord aan:

  ``$ ansible-vault rekey foo``
  
   ```
   Vault password:
   New Vault password:
   Confirm New Vault password:
   Rekey successful
   ```

## Task 6.5: Encrypted bestand in je playbook gebruiken

Ansible herkent zelf of een bestand encrypt is en zal deze automatisch decrypten. Dit werkt voor alle modules. Voorwaarde is wel dat het ``vault password`` meegegeven wordt in het ``ansible-playbook`` commando. De parameter daarvoor is ``--ask-vault-pass``.

* Vul je playbook ``workshop.yml`` aan met:

  ```
    - name: "Ensure foo is copied and decrypted"
      template:
        src: foo
        dest: /home/pi/foo 
  ```

* Voer je playbook uit (Let er op dat je de parameter ``--ask-vault-pass`` mee geeft):

  ``$ ansible-playbook workshop.yml --ask-vault-pass``

* Controleer of het bestand decrypted op je Pi staat:

  ``$ cat foo``
  
  ```
  $ cat foo 
  <inhoud van het bestand>
  ```

**Tip:** Een mooie usecase voor Vault is het gebruik van SSL certificaten. Een SSL certificaat bestaat altijd uit een public en een private key, waarbij de private key (de naam zegt het al) beschermd dient te worden. Het is natuurlijk niet de bedoeling dat een private key in plain tekst in een Ansible script gezet wordt. Deze kun je daarom het beste dmv. Ansible Vault encrypten. Uiteindelijk belandt het certificaat natuurlijk wel unencrypted op het systeem.

Terug naar: [Inhoudsopgave](/README.md)
