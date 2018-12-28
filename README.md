### creating the required environment
conda create --name python-asyncio python

### activate the environment
source activate python-asyncio

### add conda-forge channel to list of available channels
conda install -c anaconda setuptools

### then run the setup script from project root
python /path/to/algorithms/root/setup.py install