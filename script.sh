#!/bin/bash

python3 prefetch_replace.py --graph --graph-name=gowalla.el --bench-name=bfs --l2_replacement=BRRIPRP
python3 prefetch_replace.py --graph --graph-name=gowalla.el --bench-name=bfs --l2_replacement=LIPRP
python3 prefetch_replace.py --graph --graph-name=gowalla.el --bench-name=bfs --l2_replacement=BIPRP
python3 prefetch_replace.py --graph --graph-name=gowalla.el --bench-name=bfs --l2_replacement=SecondChanceRP

