# python3 eog.py --config ../configs/parameters_cdr.yaml --train --gpu 0 --epoch 130   #   MS 
# python3 eog.py --config ../configs/parameters_cdr.yaml --train --gpu 1 --epoc 100   #   ES
# python3 eog.py --config ../configs/parameters_cdr.yaml --train --gpu 2 --epoch 80 # MM, MS
# python3 eog.py --config ../configs/parameters_cdr.yaml --train --gpu 3 --epoch 80 # MM, MS, SS

python3 eog.py --config ../configs/parameters_cdr.yaml --test --gpu -1 --epoch 3
