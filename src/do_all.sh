python3 src/preprocess.py
printf "\n\n\nFINISHED preprocess.py!\n\n\n"
python3 src/train_ols.py
printf "\n\n\nFINISHED train_ols.py!\n\n\n"
python3 src/train_nn.py
printf "\n\n\nFINISHED train_nn.py!\n\n\n"
python3 src/evaluate.py