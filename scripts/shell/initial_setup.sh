# Environment Setup
cd ../../
conda init
conda env create -f environment.yaml
conda activate rldiff

# Satori
conda config --prepend channels https://public.dhe.ibm.com/ibmdl/export/pub/software/server/ibm-ai/conda/
conda config --prepend channels https://opence.mit.edu
