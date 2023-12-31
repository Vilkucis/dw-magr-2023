# Testy

Przed rozpoczęciem testów należy zainstalować wszystkie wymagane paczki:

`pip install -r requirements.txt`

Trzyargumentowe opcje mają taką samą składnię jak funkcja `range`: https://python-reference.readthedocs.io/en/latest/docs/functions/range.html

Przykładowo, podając argument `--number-of-edges 2 4 1`, będą przeprowadzone testy dla grafów z 2 i 3 krawędźmi, ponieważ 
`range(2, 4, 1) == [2,3]`

### BF vs WMGC

Przykładowe przeprowadzenie testów porównujących BF i WMGC

`python src/bf_vs_wmgc.py --iterations 10 --vertex-count 20 --number-of-edges 2 4 1 --number-of-arcs 100 200 30`

### WMGC vs GC

Przykładowe przeprowadzenie testów porównujących WMGC i GC dla 3 zadań:

`python src/wmgc_vs_gc.py --number-of-machines 1 5 1 --iterations 100`

### GJS vs GC

Przykładowe przeprowadzenie testów porównujących WMGC i GC dla 3 zadań:

`python src/gjs_vs_gc.py --iterations 20 --number-of-machines 2 10 2 --number-of-jobs 2 5 1`

## Interpretacja wyników
Wszystkie programy podają na końcu tabele z pomiarami, których interpretację można znaleźć w pracy