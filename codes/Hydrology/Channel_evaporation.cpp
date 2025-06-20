/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Channel_evaporation.cpp
  * Created  on: 30.02.2025
  * Modified on: 04.06.2025
***************************************************************/


#include "Basin.h"

/*
Canopy evaporation modules
*/


int Basin::Channel_evaporation_1(Control &ctrl, Atmosphere &atm, Param &par) {

    double Ta, Ta_k, airpress, windspeed, Rnet;
    double ea_s, eact, Delta, cp, Lambda, gamma, Ea, Echan;
    double dx_square = ctrl._dx * ctrl._dx;


    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        if (_chnwidth->val[j] > 0){

            Ta = atm._Ta->val[j];   // Air temperature [degree C]
            Ta_k = Ta + 273.3;      // Air temperature [K]
            airpress = atm._airpressure->val[j]; // Air pressure [Pa]
            windspeed = atm._windspeed->val[j]; // Wind speed at 2 m [m s-1]
            Rnet = atm._Rnet->val[j] * ctrl.Simul_tstep; // Net radiation [J m2-1 d-1]

            // Saturated vapour pressures [Pa]
            ea_s = 611 * exp(17.27 * Ta / (Ta + 237.3));  // Saturated pressure [Pa]
            eact = ea_s * atm._RH->val[j]; // Actual pressure [Pa]
            // Slope of saturation vapor pressure curve (Δ) [Pa/K]
            Delta = ea_s * 4098 / (Ta_k * Ta_k);

            // Psychrometric constant (γ) [Pa/K]
            
            cp = 0.24 * 4185.5 * (1 + 0.8 * (0.622 * eact / (airpress - eact))); // Specific heat of air [J kg-1 K-1]
            Lambda = 4185.5 * (751.78 - 0.5655 * (Ta + 273.15)); // Latent heat of vapourisation from air temperature [J kg-1]
            gamma = cp * airpress / (0.622 * Lambda); // Psychrometric constant (γ) [Pa/K]

            Ea = (1 + 0.536 * windspeed) * (ea_s / 1000 - eact / 1000);
            Echan = (Delta / (Delta + gamma) * Rnet / Lambda + gamma / (Delta + gamma) *
            6430000 * Ea / Lambda);  // [mm]
            Echan *= (_chnwidth->val[j] * _chnlength->val[j]) / dx_square / 1000;  // Corrected with actual channel area; [m]
            Echan = max(par._Echan_alpha->val[j]* Echan, 0.0);
            Echan = min(0.5*Echan, _chanS->val[j]);
                        
            _Echan->val[j] = Echan;     // Correct negative evaporation [m]
            _chanS->val[j] -= Echan;    // Update Channel storage [m]
        }

    }

    return EXIT_SUCCESS;
}

int Basin::Channel_evaporation_2(Control &ctrl, Atmosphere &atm, Param &par) {
    // Wind speed is replaced by 3.2 m/s - the average wind speed in Berlin-Brandenburg regions during 1992-2019
    double Ta, Ta_k, airpress, windspeed, Rnet;
    double ea_s, eact, Delta, cp, Lambda, gamma, Ea, Echan;
    double dx_square = ctrl._dx * ctrl._dx;


    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        if (_chnwidth->val[j] > 0){

            Ta = atm._Ta->val[j];   // Air temperature [degree C]
            Ta_k = Ta + 273.3;      // Air temperature [K]
            airpress = atm._airpressure->val[j]; // Air pressure [Pa]
            windspeed = 3.2; // Wind speed at 2 m [m s-1]
            Rnet = atm._Rnet->val[j] * ctrl.Simul_tstep; // Net radiation [J m2-1 d-1]

            // Saturated vapour pressures [Pa]
            ea_s = 611 * exp(17.27 * Ta / (Ta + 237.3));  // Saturated pressure [Pa]
            eact = ea_s * atm._RH->val[j]; // Actual pressure [Pa]
            // Slope of saturation vapor pressure curve (Δ) [Pa/K]
            Delta = ea_s * 4098 / (Ta_k * Ta_k);

            // Psychrometric constant (γ) [Pa/K]
            
            cp = 0.24 * 4185.5 * (1 + 0.8 * (0.622 * eact / (airpress - eact))); // Specific heat of air [J kg-1 K-1]
            Lambda = 4185.5 * (751.78 - 0.5655 * (Ta + 273.15)); // Latent heat of vapourisation from air temperature [J kg-1]
            gamma = cp * airpress / (0.622 * Lambda); // Psychrometric constant (γ) [Pa/K]

            Ea = (1 + 0.536 * windspeed) * (ea_s / 1000 - eact / 1000);
            Echan = (Delta / (Delta + gamma) * Rnet / Lambda + gamma / (Delta + gamma) *
            6430000 * Ea / Lambda);  // [mm]
            Echan *= (_chnwidth->val[j] * _chnlength->val[j]) / dx_square / 1000;  // Corrected with actual channel area; [m]
            Echan = max(par._Echan_alpha->val[j]* Echan, 0.0);
            Echan = min(Echan, _chanS->val[j]);
                        
            _Echan->val[j] = Echan;     // Correct negative evaporation [m]
            _chanS->val[j] -= Echan;    // Update Channel storage [m]
        }

    }

    return EXIT_SUCCESS;
}









