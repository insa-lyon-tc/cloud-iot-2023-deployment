# Deploy the CIT project on two kubernetes clusters (64 and 32 bits)

Based on: <https://github.com/k3s-io/k3s-ansible>

## Usage

Replace the `ansible_user` field in `inventory/group_vars/all.yml` by your username on the machines you will use.

Change the inventories `inventory/hosts_64.ini` and `inventory/hosts_32.ini` to include the machines on which you want to deploy the cluster.

Use the scripts `deploy_32.sh` `deploy_64.sh` `deploy_all.sh` to conveniently deploy respectively the 32 bits cluster, the 64 bits cluster or both (with their apps).

You can also use the playbooks located in `playbooks` to deploy individually the k3s clusters and the applications, or to reset the clusters. To do so, use the following command, setting the inventory and playbook to your needs:

```bash
ansible-playbook -i <inventory/hosts_32.ini | inventory/hosts_64.ini> <playbook-path>
```
