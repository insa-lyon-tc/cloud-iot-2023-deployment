#!/usr/bin/env bash

# Deploy 64 bits and 32 bits k3s clusters and applications

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd "$SCRIPT_DIR" && ansible-playbook -i "$SCRIPT_DIR/inventory/hosts_64.ini" "$SCRIPT_DIR/playbooks/64/deploy_all.yml"
cd "$SCRIPT_DIR" && ansible-playbook -i "$SCRIPT_DIR/inventory/hosts_32.ini" "$SCRIPT_DIR/playbooks/32/deploy_all.yml"
