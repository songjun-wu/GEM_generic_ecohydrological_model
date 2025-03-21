import os
import GEM_tools
from def_GEM import *

""""""
# set the env for model runs


# Model structure update
os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/development')
os.system('python3 develop.py')

# 
#os.chdir('/home/wusongj/GEM/GEM_generic_ecohydrological_model/python/preprocessing')
#os.system('python3 test_run.py')

# Model preprocessing
GEM_tools.set_env(Path)
GEM_tools.set_config(Path)

# Model run
os.chdir(Path.run_path)
os.system('./gEcoHydro')


