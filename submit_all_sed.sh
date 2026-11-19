#!/bin/bash

for submit_script in $1/*/anthill/submit_sed.sh
do
  bash $submit_script
done
