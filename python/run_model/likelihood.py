import os
import GEM_tools
import shutil
import subprocess
import numpy as np
from def_GEM_cali import *


def likelihood(param, chainID):

    local_path = os.getcwd()
    runpath = Path.work_path + '/chain_' +str(chainID)  + '/run/'
    GEM_tools.gen_param(runpath, Info, Param, param)
    GEM_tools.gen_no3_addtion(runpath, Info)

    os.chdir(runpath)

    if os.path.exists('outputs'):
        shutil.rmtree('outputs')
    os.mkdir('outputs')
    #os.system('./gEcoHydro')
    subprocess.run('./gEcoHydro', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    err = 0
    for key in Output.sim.keys():
        dict = Output.sim.get(key)
        _sim = np.fromfile(runpath + 'outputs/' + dict['sim_file']).reshape(-1, Output.N_sites).T[:, Info.spin_up:]
        _obs = np.fromfile(Path.data_path + dict['obs_file']).reshape(len(dict['sim_idx']), -1)
        if key == 'q':
            _sim += 1e-3
            _obs += 1e-3
        if key == 'iso_stream':
            obs_min = np.nanmin(_obs)
            _sim -= obs_min
            _obs -= obs_min
        for i in range(_obs.shape[0]):
            sim = _sim[dict['sim_idx'][i], :]
            obs = _obs[i,:]
            err += (1 - GEM_tools.kge_modified(sim, obs)) * dict['weights'][i]
            #err += GEM_tools.nselnnse(sim, obs, 0.9, 0.1) * dict['weights'][i]

    
    loglikeli = np.log(err) * (-1*100)


    if np.isnan(loglikeli):
        loglikeli = -np.inf
    
    os.chdir(local_path)
    return loglikeli

#likelihood(np.full(200, 0.5), 0)