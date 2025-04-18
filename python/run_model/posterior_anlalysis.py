import os
import numpy as np
import matplotlib.pyplot as plt
from def_GEM import Path, Info, Cali, Param, Output
import GEM_tools

output_path = Path.output_path
nodata = -9999



def plot_hydrology():
    Vars = ['canopy_storage', 'snow_depth','pond', None, None, None]
    Vars.extend(['SMC_layer1', 'SMC_layer2', 'SMC_layer3', 'groundwater_storage', None, None])
    Vars.extend(['snowmelt', 'throufall', None, None, None, None])
    Vars.extend(['infiltration', 'perc_layer1', 'perc_layer2', 'perc_layer3', None, None])
    Vars.extend(['rinfiltration', 'rperc_layer1', 'rperc_layer2', 'rperc_layer3', None, None])
    Vars.extend(['canopy_evap', 'soil_evap', 'transp_layer1', 'transp_layer2', 'transp_layer3', None])
    Vars.extend(['overland_flow_input','overland_flow_output','interflow_input', 'interflow_output','GWflow_input', 'GWflow_output'])
    Vars.extend(['overland_flow_toChn', None, 'interflow_toChn', None, 'GWflow_toChn', 'discharge'])
    Vars.extend([])

    ylims = [[0, 5e-3],[2.5e-3, 2.7e-3],[0, 5e-3], None, None, None]
    ylims.extend([[0, 0.5],[0, 0.5],[0, 0.5],[19, 21], None, None])
    ylims.extend([[1.1e-4, 1.2e-4], [1.5e-3, 1.55e-3], None, None, None, None])
    ylims.extend([[0, 3e-3],[0, 3e-3],[0, 3e-3],[0, 3e-3], None, None])
    ylims.extend([[0, 3e-3],[0, 3e-3],[0, 3e-3],[0, 3e-3], None, None])
    ylims.extend([[0, 3e-5],[0, 1e-3],[0, 3e-3],[0, 1e-3],[0, 1e-3], None])
    ylims.extend([[0, 8e-3],[0, 8e-3],[0, 8e-3],[0, 8e-3],[0, 8e-4],[0, 8e-4]])
    ylims.extend([[0, 1e-3],None,[0, 1e-3],None,[0, 1e-3], [0,3e-2]])

    #ylims = np.full(len(ylims), None)

    nrow = 8
    ncol = 6


    fig, ax = plt.subplots(nrow, ncol, figsize=(30,18), dpi=300)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.2, hspace=0.2)

    site_idx = 3  # Demnitz Millcreek 26

    for i in range(len(Vars)):
        if Vars[i] == None:
            ax[i//ncol, i%ncol].axis('off')
        else:
            try:
                data = (np.fromfile(output_path + Vars[i] + '_TS.bin').reshape(-1, Output.N_sites).T)[:, Info.spin_up:]
                data = data[site_idx,:]
                
                data[data==nodata] = np.nan
                ax[i//ncol, i%ncol].plot(data, linewidth=0.3, c='skyblue', zorder=1)
                    
                title_hgt = 0.9
                hgt_gradient = 0.11
                if "discharge" in Vars[i]:
                    obs = np.fromfile(Path.data_path + 'discharge_obs.bin').reshape(len(Output.sim['q']['sim_idx']), -1)[site_idx, :]
                    X = np.arange(len(obs))
                    ax[i//ncol, i%ncol].scatter(X, obs, c='salmon', s=0.3, alpha=0.3, zorder=2)
                    ax[i//ncol, i%ncol].text(0.95, title_hgt - hgt_gradient * 1, 'KGE:'+str(np.round(GEM_tools.kge(data+1e-3, obs+1e-3), 2)), fontsize=12, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                    ax[i//ncol, i%ncol].text(0.95, title_hgt - hgt_gradient * 2, 'NSE:'+str(np.round(GEM_tools.nse(data+1e-3, obs+1e-3), 2)), fontsize=12, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 0, Vars[i], fontsize=12, weight='bold', horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 1,'Mean:' + f"{np.mean(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 2,'Max :' + f"{np.max(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
            except Exception as e:
                ax[i//ncol, i%ncol].axis('off')

    fig.savefig(output_path + '999_All_in_Ts.png')
    print('Plot saved at :  ', output_path + '999_All_in_Ts.png')


    fig, ax = plt.subplots(nrow, ncol, figsize=(16,25), dpi=300)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.01, hspace=0.08)
    for i in range(len(Vars)):
        if Vars[i] == None:
            pass
            ax[i//ncol, i%ncol].axis('off')
        else:
            try:
                chanmask = np.loadtxt(Path.data_path + 'spatial/chnwidth.asc', skiprows=6)
                chanmask = chanmask>0

                data = (np.fromfile(output_path + Vars[i] + '_map.bin').reshape(-1, 30, 22))[Info.spin_up:, :, :]
                data[data==nodata] = np.nan

                if ('discharge' in Vars[i]) or ('_toChn' in Vars[i]) or ('chanS' in Vars[i]):
                    for kk in range(data.shape[0]):
                        data[kk,:,:][ ~chanmask] = np.nan

                #print(Vars[i], np.nanmin(np.mean(data, axis=0)), np.nanmax(np.mean(data, axis=0)))  # todo

                if ylims[i] is None:
                    im = ax[i//ncol, i%ncol].imshow(np.mean(data, axis=0), cmap='viridis', zorder=1, label='1')
                else:
                    im = ax[i//ncol, i%ncol].imshow(np.mean(data, axis=0), cmap='viridis', vmin=ylims[i][0], vmax=ylims[i][1], zorder=1, label='1')
                ax[i//ncol, i%ncol].set_frame_on(False)
                ax[i//ncol, i%ncol].set_xticks([])
                ax[i//ncol, i%ncol].set_yticks([])

                tmp = ax[i//ncol, i%ncol].get_position()

                fig.colorbar(im, ax=ax[i//ncol, i%ncol], cax=fig.add_axes([tmp.x1-0.02, tmp.y0+0.005, 0.01, 0.03]), format='%.0e')

                title_hgt = 1.02
                hgt_gradient = 0.11
                
                ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 0, Vars[i], fontsize=15, weight='bold', horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                #ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 1,'Mean:' + f"{np.mean(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                #ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 2,'Max :' + f"{np.max(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
            except Exception as e:
                pass
                #ax[i//ncol, i%ncol].axis('off')
    fig.savefig(output_path + '999_All_in_map.png')
    print('Plot saved at :  ', output_path + '999_All_in_map.png')

def plot_tracking():
    Vars = ['d18o_canopy_storage', 'd18o_snow_depth','d18o_pond', None, None, None]
    Vars.extend(['d18o_SMC_layer1', 'd18o_SMC_layer2', 'd18o_SMC_layer3', 'd18o_groundwater_storage', None, 'd18o_chanS'])
    Vars.extend(['age_canopy_storage', 'age_snow_depth','age_pond', None, None, None])
    Vars.extend(['age_SMC_layer1', 'age_SMC_layer2', 'age_SMC_layer3', 'age_groundwater_storage', None, 'age_chanS'])

    Vars.extend([])

    nrow = 8
    ncol = 6


    fig, ax = plt.subplots(nrow, ncol, figsize=(30,18), dpi=300)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.2, hspace=0.2)

    site_idx = 3  # Demnitz Millcreek 26

    for i in range(len(Vars)):
        if Vars[i] == None:
            ax[i//ncol, i%ncol].axis('off')
        else:
            try:
                data = (np.fromfile(output_path + Vars[i] + '_TS.bin').reshape(-1, Output.N_sites).T)[:, Info.spin_up:]
                data = data[site_idx,:]

                data[data==nodata] = np.nan
                ax[i//ncol, i%ncol].plot(data, linewidth=0.3, c='skyblue', zorder=1)
                    
                title_hgt = 0.9
                hgt_gradient = 0.11
                if "discharge" in Vars[i]:
                    obs = np.fromfile(Path.data_path + 'discharge_obs.bin').reshape(len(Output.sim['q']['sim_idx']), -1)[site_idx, :]
                    X = np.arange(len(obs))
                    ax[i//ncol, i%ncol].scatter(X, obs, c='salmon', s=0.3, alpha=0.3, zorder=2)
                    ax[i//ncol, i%ncol].text(0.95, title_hgt - hgt_gradient * 1, 'KGE:'+str(np.round(GEM_tools.kge(data+1e-3, obs+1e-3), 2)), fontsize=12, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                    ax[i//ncol, i%ncol].text(0.95, title_hgt - hgt_gradient * 2, 'NSE:'+str(np.round(GEM_tools.nse(data+1e-3, obs+1e-3), 2)), fontsize=12, weight='bold', horizontalalignment='right', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 0, Vars[i], fontsize=12, weight='bold', horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 1,'Mean:' + f"{np.mean(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 2,'Max :' + f"{np.max(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
            except Exception as e:
                ax[i//ncol, i%ncol].axis('off')

    fig.savefig(output_path + '999_All_in_Ts_tracking.png')
    print('Plot saved at :  ', output_path + '999_All_in_Ts_tracking.png')


    fig, ax = plt.subplots(nrow, ncol, figsize=(16,25), dpi=300)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.01, hspace=0.08)
    for i in range(len(Vars)):
        if Vars[i] == None:
            ax[i//ncol, i%ncol].axis('off')
            pass
        else:
            try:
                chanmask = np.loadtxt(Path.data_path + 'spatial/chnwidth.asc', skiprows=6)
                chanmask = chanmask>0

                data = (np.fromfile(output_path + Vars[i] + '_map.bin').reshape(-1, 30, 22))[Info.spin_up:, :, :]
                data[data==nodata] = np.nan
                
                if ('discharge' in Vars[i]) or ('_toChn' in Vars[i]) or ('_chanS' in Vars[i]):
                    for kk in range(data.shape[0]):
                        data[kk,:,:][ ~chanmask] = np.nan

                print(Vars[i], np.nanmin(np.mean(data, axis=0)), np.nanmax(np.mean(data, axis=0)))  # todo

                im = ax[i//ncol, i%ncol].imshow(np.mean(data, axis=0), cmap='viridis', zorder=1, label='1')
                ax[i//ncol, i%ncol].set_frame_on(False)
                ax[i//ncol, i%ncol].set_xticks([])
                ax[i//ncol, i%ncol].set_yticks([])

                tmp = ax[i//ncol, i%ncol].get_position()

                fig.colorbar(im, ax=ax[i//ncol, i%ncol], cax=fig.add_axes([tmp.x1-0.02, tmp.y0+0.005, 0.01, 0.03]), format='%.0e')

                title_hgt = 1.02
                hgt_gradient = 0.11
                
                ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 0, Vars[i], fontsize=15, weight='bold', horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                #ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 1,'Mean:' + f"{np.mean(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
                #ax[i//ncol, i%ncol].text(0.05, title_hgt - hgt_gradient * 2,'Max :' + f"{np.max(data):.1e}", fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax[i//ncol, i%ncol].transAxes)
            except Exception as e:
                ax[i//ncol, i%ncol].axis('off')
            
                
    fig.savefig(output_path + '999_All_in_map_tracking.png')
    print('Plot saved at :  ', output_path + '999_All_in_map_tracking.png')

def plot_param():
    param = np.fromfile('/data/scratch/wusongj/paper4/param.bin').reshape(Cali.nchains, -1).T
    keys = Param.ref.keys()
    param_names = []
    for key in keys:
        dict = Param.ref[key]
        if dict['type'] == 'global':
            param_names.append(key)
        elif dict['type'] == 'soil':
            for i in range(Info.N_soil):
                param_names.append(key + '_s' + str(i))
        elif dict['type'] == 'landuse':
            for i in range(Info.N_landuse):
                param_names.append(key + '_v' + str(i))

    fig, ax = plt.subplots(1, 1, figsize=(10,20), dpi=300)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
    ax.imshow(param, cmap='viridis')
    ax.set_yticks(np.arange(param.shape[0]))
    ax.set_yticklabels(param_names, weight='bold')
    fig.savefig('999_param.png')

    fig, ax = plt.subplots(1, 1, figsize=(10,20), dpi=300)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
    for i in range(param.shape[0]):
        param[i] = np.sort(param[i])
    ax.imshow(param, cmap='viridis')
    ax.set_yticks(np.arange(param.shape[0]))
    ax.set_yticklabels(param_names, weight='bold')
    fig.savefig('999_param_sorted.png')




plot_hydrology()
plot_tracking()
