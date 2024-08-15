# Code Environment
cd ../../
conda env export > environment.yaml
pip list --format=freeze > requirements.txt
