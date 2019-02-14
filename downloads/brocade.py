---
- hosts: switches
  connection: local
  gather_facts: false
  remote_user: workshop

  vars:
    switchport:
      vlan: 350
      port: 1/1/10
    switchports:
      - { port: 1/1/10, vlan: 350 }
      - { port: 1/1/11, vlan: 351 }
      - { port: 1/1/12, vlan: 351 }

  tasks:

  - name: Configure SNMP
    ironware_config:
      lines:
        - snmp-server contact ansible@demo.local
        - snmp-server location Demorack

  - name: "Create VLAN {{ switchport.vlan }}"
    ironware_config:
      lines:
        - "vlan {{ switchport.vlan }} by port"

  - name: "Add port {{ switchport.port}} to VLAN {{ switchport.vlan }}"
    ironware_config:
      lines:
        - "untagged ethernet {{ switchport.port }}"
      parents: ["vlan {{ switchport.vlan }} by port"]

        
  - name: "Add ports to VLAN"
    ironware_config:
      lines:
        - "untagged ethernet {{ item.port }}"
      parents: ["vlan {{ item.vlan }} by port"]
    with_items: "{{ switchports }}"

