# Lab 7: Example - Cisco IOS Switch
In dit lab gaan we een Cisco IOS Switch configureren.

**Note:** Dit lab wordt uitgevoerd op echte hardware. Let er op dat je geen wijzigingen uitvoerd op de port ``GigabitEthernet0/2``, zodat je de verbinding met de switch niet verliest. 

Voor Cisco IOS zijn diverse modules beschikbaar die het configureren van poorten, routes, vlans etc. erg gemakkelijk maken. Zie https://docs.ansible.com/ansible/latest/modules/list_of_network_modules.html#ios voor het complete overzicht van modules. Tevens zijn de 3 "standaard" modules ``ios_facts``, ``ios_command`` en ``ios_config`` aanwezig, zodat elke uitdaging met Ansible geautomatiseerd kan worden.
