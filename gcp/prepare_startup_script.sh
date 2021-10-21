#!/bin/bash

TRITONS="dm1 dm2 dtau ak4 ak8 ak8md ak8mr"

export FOLDER=/home/lincy
for mo in ${TRITONS}; do
  export mo
  envsubst <  startup.sh.tpl >  startup-${mo}.sh
done
