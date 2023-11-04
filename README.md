# Cluster.IO

# Frontend Setup Guide

To run the frontend of this project, follow these steps:

## Prerequisites

1. **Download and Install Anaconda:**

   If you haven't already, make sure to download and install Anaconda. You can find installation instructions [here](https://docs.anaconda.com/free/anaconda/install/).

2. **Install Node.js:**

   Use Conda to install Node.js by running the following command:

   ```bash
   conda install -c conda-forge nodejs

3. **Install Yarn:**
      After Node.js is installed, you can install Yarn globally with npm:
   ```bash
   npm install --global yarn
## Running the Frontend

4. **Install Frontend Dependencies:**

   Navigate to the project's frontend directory and run the following command to install the necessary dependencies:

   ```bash
   yarn install

5. **Start the Frontend Server:**

   Once the dependencies are installed, you can start the frontend server by running:
   
   ```bash
   yarn start

# Backend Setup Guide

To set up the backend of this project, follow these steps:

1. **Create a Python 3.9 Environment:**

   Using Conda, create a new Python 3.9 environment for the backend. Replace `your_env_name` with your desired environment name.

   ```bash
   conda create -n your_env_name python=3.9

2. **Activate the Environment:**

   Activate the newly created environment:

   ```bash
   conda activate your_env_name
   
3. **Install Required Backend Packages:**

   Use pip to install the necessary Python packages for the backend. Run the following command to install them:

   ```bash
   pip install uvicorn ariadne pandas boto3 scikit-learn scikit-learn-extra seaborn fuzzy-c-means openpyxl

4. **Install HDBSCAN:**

   Install HDBSCAN using Conda from the conda-forge channel:

   ```bash
   conda install -c conda-forge hdbscan

5. **Run the Backend Server:**

   Navigate to your backend/server_files directory(with your_env_name activated), and then run the following command to start the backend server:

   ```bash
   uvicorn server:app



