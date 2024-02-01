# Deploy the CIT project on a HA Load Balanced k3s cluster

Based on: <https://github.com/techno-tim/k3s-ansible>

## Usage

Replace the `ansible_user` field in `inventory/group_vars/all.yml` by your username on the machines you will use.

Change the inventories `inventory/hosts.ini` file to include the machines on which you want to deploy the cluster.

```bash
ansible-playbook -i <inventory/hosts_32.ini | inventory/hosts_64.ini> <playbook-path>
```
