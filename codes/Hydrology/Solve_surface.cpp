#include "Basin.h"

int Basin::Solve_surface(Control &ctrl, Param &par, Atmosphere &atm){

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        if (ctrl.opt_snow == 1){
            Snow_acc_melt(par, atm, j);
        }
       
    }

    if (ctrl.opt_tracking_isotope==1 or ctrl.opt_tracking_age==1){
        Mixing_surface_tracking(ctrl, atm, par);
    }

    if (ctrl.opt_nitrogen_sim==1){
        Solve_surface_nitrogen(ctrl, atm, par);
    }

    return EXIT_SUCCESS;
}


int Basin::Snow_acc_melt(Param &par, Atmosphere &atm, int j){

    // Parameters
    double _snow_rain_thre = par._snow_rain_thre->val[j];
    double _deg_day_min = par._deg_day_min->val[j];
    double _deg_day_max = par._deg_day_max->val[j];
    double _deg_day_increase = par._deg_day_increase->val[j];
    double degree_day;  // Degree day factor

    // States and flxues
    double Th = _Th->val[j];  // Throughfall
    double pond = _pond->val[j];  // Ponding water
    double Ta = atm._Ta->val[j]; // Mean air temperature
    double snow_pack = _snow->val[j]; // Snow pack
    double snow_melt = 0;
    double snow_acc = 0;

    

    if (Ta < _snow_rain_thre) {  // snow accumulation
        snow_melt = 0;
        snow_acc = Th;
        snow_pack += Th;  // Throughfall becomes snow
        

    } else { 
        pond += Th; // Through fall becomes ponding water

        // snow melt
        degree_day = min<double>(_deg_day_min + _deg_day_increase * Th, _deg_day_max);
        snow_melt = min<double>(degree_day*(Ta - _snow_rain_thre), snow_pack);
        snow_pack -= snow_melt;
        pond += snow_melt;
        
    }
    
    _snowacc->val[j] = snow_acc;
    _snowmelt->val[j] = snow_melt;
    _snow->val[j] = snow_pack;
    _pond->val[j] = pond;

    return EXIT_SUCCESS;

}