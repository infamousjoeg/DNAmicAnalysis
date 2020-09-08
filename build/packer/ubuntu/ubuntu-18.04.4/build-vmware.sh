#!/bin/bash
set -eo pipefail

summon -f ../../secrets.yml packer build -only=vmware-iso ubuntu-18.04.4-minimal.json