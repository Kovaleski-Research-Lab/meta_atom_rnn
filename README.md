# meta_atom_rnn

Time-series models for learning wavefront propagation with 3x3 metasurface dataset. Supports architecture for RNN and LSTM by setting self.choice in config file. ConvLSTM (LSTM with convolutional layers) is still in development.

# The Dataset

The raw dataset was generated using [general_3x3](https://github.com/Kovaleski-Research-Lab/general_3x3/tree/andy_branch). A dataset with 1500 samples is located in the Nautilus hypercluster under the namespace `gpn-mizzou-muem` in a persistent volume claim (PVC) called `meep-dataset-v2`. A subset of 20 samples is located on Marge at `/home/agkgd4/Documents/data/meep-dataset-v2/00{0..19}`. Each folder contains the following meep outputs: 

  dft fields - `dft_0000{idx}.h5`
  
  epislon data - `epsdata_0000{idx}.pkl`
  
  metadata - `metadata_0000{idx}.pkl`.

The dataset is reduced to smaller volumes for training by means of [insert repo here]. These volumes are located in the Nautilus hypercluster under the namespace `gpn-mizzou-muem` in a persistent volume claim (PVC) called `dft-volumes`. A subset of 100 samples is located at `/home/agkgd4/Documents/data/meep-dataset-v2/volumes`. The naming convention for these reduced volumes is 00{00..99}.pkl.

Before the training step, `meta_atom_rnn/preprocess_data/preprocess.py` takes in the reduced volume .pkl files and preprocesses them for the model. The outputs of preprocess.py are located in the Nautilus hypercluster under the namespace `gpn-mizzou-muem` in a persistent volume claim (PVC) called `preprocessed-data`. A subset of 100 samples is located at `/home/agkgd4/Documents/data/meep-dataset-v2/preprocessed_data` and split into `/train` and `valid`. The naming convention for these reduced volumes is 00{00..99}.pkl.

The PVCs can be found by logging on to any machine with kubernetes installed and configured for our namespace (gpn-mizzou-muem) by running `kubectl get pvc`.

## Folder descriptions

- `k8s` : contains files for data preprocessing, network training, loading results, and evaluation via kubernetes.
  - This folder contains multiple scripts for launching kubernetes jobs.
- `configs` contains the configuration file for the entire pipeline, including a flag `deployment_mode` which gives the user the option to develop locally with a limited dataset, or in the cloud with the full dataset.
- `preprocess_data` contains a script that takes in volumes of DFT electric field data from meep simulations and conditions them for the time series networks here.
- `main.py` is the script we run for all processes if we are developing locally. If we're training locally, `train.sh` automates the experiments.
  - Run `main.py -config configs/params.yaml`. Make sure configs/params.yaml is correct for your preferred deployment_mode and experiment, as well as network training parameters, paths, etc.
- `utils` : contains all our implementations of time series networks using PyTorch lightning, as well as helper functions for data processing, building plots, etc.
