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

- [K8s folder](https://github.com/Kovaleski-Research-Lab/meta_atom_rnn/tree/main/k8s) : contains files for data preprocessing, network training, loading results, and evaluation via kubernetes.
  - This folder contains multiple scripts for launching kubernetes jobs.
- [Configs folder](https://github.com/Kovaleski-Research-Lab/meta_atom_rnn/tree/main/configs) : contains the configuration file for the entire pipeline, including a flag `deployment_mode` which gives the user the option to develop locally (on Marge) with a limited dataset, or in the cloud with the full dataset.
- [Preprocess_data folder](https://github.com/Kovaleski-Research-Lab/meta_atom_rnn/tree/main/preprocess_data) : contains a script that takes in volumes of DFT electric field data from meep simulations and conditions them for the time series networks here.
- [main.py](https://github.com/Kovaleski-Research-Lab/meta_atom_rnn/blob/main/main.py) is the script we run for all processes if we are developing locally. If we're training locally, `train.sh` automates the experiments.
  - Run `main.py -config configs/params.yaml`. Make sure configs/params.yaml is correct for your preferred deployment_mode and experiment, as well as network training parameters, paths, etc.
- [Utils folder](https://github.com/Kovaleski-Research-Lab/meta_atom_rnn/tree/main/utils) : contains all our implementations of time series networks using PyTorch lightning, as well as helper functions for data processing, building plots, etc.

## How to run this code

### Prerequisites:
1. [Kubernetes](https://github.com/Kovaleski-Research-Lab/Global-Lab-Repo/blob/main/sops/software_development/kubernetes.md) must be installed if using Nautilus resources.
2. Must be running the appropriate docker container for [local deployment](https://hub.docker.com/layers/kovaleskilab/meep/v3_lightning/images/sha256-e550d12e2c85e095e8fd734eedba7104e9561e86e73aac545614323fda93efb2?context=repo) or [kubernetes deployment](https://hub.docker.com/layers/kovaleskilab/meep_ml/launcher/images/sha256-464ec5f4310603229e96b5beae9355055e2fb2de2027539c3d6bef94b7b5a4f1?context=repo)
3. Your docker container for local deployment should be mounted as follows (data is mounted to agkgd4 - code and results should be unique to you):
   ```
   -v /home/{your_pawprint}/Documents/code:/develop/code \
   -v /home/agkgd4/Documents/data:/develop/data \
   -v /home/{your_pawprint}/Documents/results:/develop/results \
   ```
4. Your docker container for kubernetes deployment should be mounted as follows:
   ```
   -v /home/{your_pawprint}/Documents/code:/develop/code \
   -v /home/agkgd4/Documents/data:/develop/data \
   -v /home/{your_pawprint}/Documents/results:/develop/results \
   -v ~/.kube:/root/.kube 
   ```
   
  - Note: You may prefer a conda environment instead of a docker container for launching Kubernetes jobs. A barebones environment should have jinja2 installed (not necessary to install kubernetes in the conda environment if you used `snap install` per the Kubernetes link in item 1.
  - Note: The data subset is located on Marge and Kubernetes is already installed.

### Running the code

#### Option 1: Running locally:
- Note: The storage required for the complete dataset is upwards of 10 TB, so it is stored in a PVC on the Nautilus cluster and requires use of Kubernetes. To run locally, we use a subset of 100 samples, as described above in the Dataset section.

**Step 1** Preprocessing the data (This assumes you have generated the raw data via [general_3x3](https://github.com/Kovaleski-Research-Lab/general_3x3/tree/andy_branch), and the raw data has been reduced to volumes via [repo here].)
  
  1. Update the [config file](https://github.com/Kovaleski-Research-Lab/meta_atom_rnn/blob/main/configs/params.yaml):
     
  - deployment_mode : 0
  - experiment : 0
 
  2. From your Docker container, navigate to `/develop/code/meta_atom_rnn` and run
     ```
     python3 main.py -config configs/params.yaml
     ```
**Step 2** Train the network.

  1. Update the [config file](https://github.com/Kovaleski-Research-Lab/meta_atom_rnn/blob/main/configs/params.yaml):
     
  - deployment_mode : 0
  - experiment : 1

  2. Then you can either train a single model by specifying `network.arch` and `dataset.seq_len` to your preference and running
     ```
     python3 main.py -config configs/params.yaml
     ```
     or you can train all models - LSTM and RNN, each with sequence lengths of 5, 10, 15 ... 60 by setting `visualize.sequences` to your preference and running
     ```
     train.sh
     ```
**Step 3** Load model results

  1. Update the [config file](https://github.com/Kovaleski-Research-Lab/meta_atom_rnn/blob/main/configs/params.yaml):
     
  - deployment_mode : 0
  - experiment : 2

  2. Load all the results by running
     ```
     python3 main.py -config configs/params.yaml
     ```

**Step 4** Run evaluation

  1. Update the [config file](https://github.com/Kovaleski-Research-Lab/meta_atom_rnn/blob/main/configs/params.yaml):
     
  - deployment_mode : 0
  - experiment : 3

  2. Run the evaluation by running
     ```
     python3 main.py -config configs/params.yaml
     ```
     This will output loss plots, as well quantitative and qualitative metrics showing model performance. These files will be output into a folder, `/develop/results/meta_atom_rnn/analysis`

#### Option 2: Scale up, launch Kubernetes jobs:

**Step 1** Preprocessing the data (This assumes you have generated the raw data via [general_3x3](https://github.com/Kovaleski-Research-Lab/general_3x3/tree/andy_branch), and the raw data has been reduced to volumes via [repo here].)
  
  1. Update the [config file](https://github.com/Kovaleski-Research-Lab/meta_atom_rnn/blob/main/configs/params.yaml):
     
  - deployment_mode : 1
  - experiment : 0
 
  2. From your (launch kube) Docker container, navigate to `/develop/code/meta_atom_rnn/k8s` and run
     ```
     python3 launch_preprocess.py -config ../configs/params.yaml
     ```
**Step 2** Train the network.

  1. Update the [config file](https://github.com/Kovaleski-Research-Lab/meta_atom_rnn/blob/main/configs/params.yaml):
     
  - deployment_mode : 1
  - experiment : 1

  2. Launch the training jobs using
     ```
     python3 launch_training.py -config ../configs/params.yaml
     ```
**Step 3** Load model results

  1. Update the [config file](https://github.com/Kovaleski-Research-Lab/meta_atom_rnn/blob/main/configs/params.yaml):
     
  - deployment_mode : 1
  - experiment : 2

  2. Load all the results by running
     ```
     python3 load_results.py -config ../configs/params.yaml
     ```

**Step 4** Run evaluation

  1. Update the [config file](https://github.com/Kovaleski-Research-Lab/meta_atom_rnn/blob/main/configs/params.yaml):
     
  - deployment_mode : 1
  - experiment : 3

  2. Run the evaluation by running
     ```
     python3 launch_evaluation.py -config configs/params.yaml
     ```
     This will output loss plots, as well quantitative and qualitative metrics showing model performance. These files will be output into the `training-results` pvc.
