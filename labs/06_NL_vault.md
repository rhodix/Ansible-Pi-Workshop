# Lab 6: Ansible Vault


## Task 6.1: Bestand encrypten

**Tip:** ansible-vault gebruikt standaard de editor ``vi``. Mocht je liever ``nano`` gebruiken, dan kun je de editor aanpassen door de environment variable ``EDITOR`` te vullen met: ``/bin/nano`` met het commando: ``export EDITOR=/bin/nano``.

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


Volgende stap: [Lab 7 - Example - Cisco IOS switch](/labs/07_NL_Example_Cisco-IOS.md)
