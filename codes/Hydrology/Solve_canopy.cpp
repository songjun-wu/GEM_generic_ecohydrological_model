#include "Basin.h"

/*
Canopy intercpetion modules
Interception_1: Maximum canopy stoages are directly specified by LAI * alpha
Interception_2: Maximum canopy stoages are additionally corrected by rE (Landarf et al., 2024)
*/

int Basin::Solve_canopy(Control &ctrl, Param &par, Atmosphere &atm) {
    
    if (ctrl.opt_intecept == 1){
        Interception_1(ctrl, par, atm);
    } else if (ctrl.opt_intecept == 2){
        Interception_2(ctrl, par, atm);
    }

    if (ctrl.opt_canopy_evap == 1){
        Canopy_evaporation_1(ctrl, par, atm);
    }
    
    // Tracking
    if (ctrl.opt_tracking_isotope==1 or ctrl.opt_tracking_age==1){
        Mixing_canopy_tracking(ctrl, atm);  // d18o change due to canopy mixing and evaporation
    }

    if (ctrl.opt_nitrogen_sim==1){
        Solve_canopy_nitrogen(ctrl, atm);  // no3 change due to canopy mixing and evaporation
    }

    return EXIT_SUCCESS;
}








