/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Solve_soil_profile_nitrogen.cpp
  * Created  on: 30.02.2025
  * Modified on: 04.06.2025
***************************************************************/


#include "Basin.h"

int Basin::Solve_soil_profile_nitrogen(Control &ctrl, Atmosphere &atm, Param &par){

    /* 
    ### Soil layer 1:
    (_thate1_old)
    + infiltration          (need to mix)
    - percolation1
    - Esoil
    - Transp1           
    (_thate1)
    + reinfiltration
    - repercolation1    


    ### Soil layer 2:
    (_thata2_old)
    + percolation1          (need to mix)
    - percolation2
    - Transp2           
    (_theta2)
    + repercolation1
    - repercolation2    

    ### Soil layer 3:
    (_theta3_old)           
    + percolation2          (need to mix)
    - percolation3
    - Transp3
    (_theta3)          
    + repercolation2
    - repercolation3
    + interflow_in      
    - interflow_out
    - interflow_toChn   
    */
    
    double depth1, depth2, depth3;
    double no3_pond, no3_layer1, no3_layer2, no3_layer3;
    double ST1, ST2, ST3;
    double pond_old, no3_pond_old, no3_layer1_old, pond_to_mix;
  
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        depth1 = _depth1->val[j];
        depth2 = _depth2->val[j];
        depth3 = par._depth3->val[j];
        no3_pond = _no3_pond->val[j];
        no3_layer1 = _no3_layer1->val[j];
        no3_layer2 = _no3_layer2->val[j];
        no3_layer3 = _no3_layer3->val[j];
        ST1 = _theta1_old->val[j] * depth1;
        ST2 = _theta2_old->val[j] * depth2;
        ST3 = _theta3_old->val[j] * depth3;

        /* Mixing */
        // Mix ponding water with top layer storage
        pond_old = _pond->val[j] + _infilt->val[j];
        if (pond_old > roundoffERR and ST1 > roundoffERR){
            no3_pond_old = no3_pond;
            no3_layer1_old = _no3_layer1->val[j];
            pond_to_mix = min(pond_old * par._nearsurface_mixing->val[j], ST1);
            no3_pond = (no3_pond_old * (pond_old - pond_to_mix) + no3_layer1_old * pond_to_mix) / pond_old;
            no3_layer1 = (no3_pond_old * pond_to_mix + no3_layer1_old * (ST1 - pond_to_mix)) / ST1;
        }
        
        // Mixing layer 1
        Mixing_full(ST1, no3_layer1, _infilt->val[j], no3_pond);
        ST1 += (_infilt->val[j] - _Perc1->val[j]);
        
        // Mixing layer 2
        Mixing_full(ST2, no3_layer2, _Perc1->val[j], no3_layer1);
        ST2 += (_Perc1->val[j] - _Perc2->val[j]);

        // Mixing layer 3
        Mixing_full(ST3, no3_layer3, _Perc2->val[j], no3_layer2);
        ST3 += (_Perc2->val[j] - _Perc3->val[j]);
 

        // Evapotranspiration happens after percolation
        // Layer 1: erichment due to evaporation and transpiration
        no3_layer1 = (ST1 - _Es->val[j] - _Tr1->val[j])>roundoffERR ? ST1 * no3_layer1 / (ST1 - _Es->val[j] - _Tr1->val[j]) : 0;
        //ST1 -= (_Es->val[j] + _Tr1->val[j]);

        // Layer 2: erichment due to transpiration
        no3_layer2 = (ST2 - _Tr2->val[j])>roundoffERR ? ST2 * no3_layer2 / (ST2 - _Tr2->val[j]) : 0;
        //ST2 -= (_Tr2->val[j]);

        // Layer 3: erichment due to transpiration
        no3_layer3 = (ST3 - _Tr3->val[j])>roundoffERR ? ST3 * no3_layer3 / (ST3 - _Tr3->val[j]) : 0;
        //ST3 -= (_Tr3->val[j]);

        // Save outputs
        _no3_pond->val[j] = no3_pond;
        _no3_layer1->val[j] = no3_layer1;
        _no3_layer2->val[j] = no3_layer2;
        _no3_layer3->val[j] = no3_layer3;
    }

    /* Nitrogen addtion */
    Sort_nitrogen_addition(ctrl, par);
    Nitrogen_addition(ctrl, par);
    /* Plant uptake */
    Sort_plant_uptake(ctrl, par);
    Plant_uptake(ctrl, par, atm);
    /* Nitrogen Transformation */
    Soil_transformation(ctrl, atm, par);  // Degradation and mineralisation
    Soil_denitrification(ctrl, atm, par);  // Denitrification

    return EXIT_SUCCESS;
}
