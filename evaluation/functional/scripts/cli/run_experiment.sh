#!/bin/bash

pid=$(head -n 1 pid)
ckanfetch -h http://localhost:8000 -f csv --csv-delimiter , --include-header "$pid"
Rscript ./RR.R