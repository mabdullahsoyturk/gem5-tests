#!/bin/bash

python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=bfs --l2_replacement=BRRIPRP
python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=bfs --l2_replacement=LIPRP
python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=bfs --l2_replacement=BIPRP
python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=bfs --l2_replacement=SecondChanceRP

python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=cc --l2_replacement=BRRIPRP
python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=cc --l2_replacement=LIPRP
python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=cc --l2_replacement=BIPRP
python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=cc --l2_replacement=SecondChanceRP

python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=pr --l2_replacement=BRRIPRP
python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=pr --l2_replacement=LIPRP
python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=pr --l2_replacement=BIPRP
python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=pr --l2_replacement=SecondChanceRP

python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=sssp --l2_replacement=BRRIPRP
python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=sssp --l2_replacement=LIPRP
python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=sssp --l2_replacement=BIPRP
python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=sssp --l2_replacement=SecondChanceRP

python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=tc --l2_replacement=BRRIPRP
python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=tc --l2_replacement=LIPRP
python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=tc --l2_replacement=BIPRP
python3 prefetch_replace.py --graph --graph-name=dblp.el --bench-name=tc --l2_replacement=SecondChanceRP


