/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Routing_Q.cpp
  * Created  on: 30.02.2025
  * Modified on: 27.05.2025
***************************************************************/


#include "Basin.h"

int Basin::Routing_Q_1(Control &ctrl, Param &par){

    int from_j, count;
    double chnwidth, chnlength, Qall, Qupstream;
    double sqrtS, Manningn, a;
    double avQ, abQ, Qk, Qk1, fQj1i1, dfQj1i1, C;  // Variables used in Kinematic water solver
    

    double dx = ctrl._dx;
    double dt = ctrl.Simul_tstep;
    // double dtdx = dt / dx;
    double dx_square = dx * dx;
    double dtdx;

    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {

        chnwidth = _chnwidth->val[j];  // [m]
        
        if (chnwidth>0){
            Qall = (_chanS->val[j] + _ovf_toChn->val[j] + _interf_toChn->val[j] + _GWf_toChn->val[j]) * dx / dt; // Channel storage and all inflow from terrestrial grid [m] to [m2/s]
            Qupstream = _Qupstream->val[j];  // Upstream discharge [m3/s]

            
            chnlength = _chnlength->val[j];  // [m]

            dtdx = dt / chnlength;  // todo

            from_j = _sortedGrid.to_cell[j];

            if (Qall + Qupstream > 0){

                sqrtS = pow(_slope->val[j], 0.5);

                //Manningn = par._Manningn->val[j] * chnlength;  // Manning's N scaled with channel length
                Manningn = par._Manningn->val[j];
                a = pow(pow(chnwidth,0.67)*Manningn/sqrtS, 0.6); // Wetted perimeter approximated with channel width

                //initial guess
                avQ = 0.5*(Qupstream);
                if (avQ==0) abQ=0;
                else abQ = a*0.6*pow(avQ, 0.6-1);

                Qk1 = ((dtdx*Qupstream) + dt*Qall)/(dtdx+abQ);

                C =  dtdx * Qupstream + dt*Qall;
                
                count = 0;
                do{
                    Qk=Qk1;
                    fQj1i1 = dtdx*Qk+a*powl(Qk, 0.6)-C;
                    dfQj1i1 = dtdx+a*0.6*powl(Qk, 0.6-1);
                    Qk1 = Qk - (fQj1i1/dfQj1i1);
                    if (Qk1 <=0){// if NR cannot converge then get some of the available water out and exit the loop
                        Qk1 = 0.61803*((dtdx*Qupstream) + dt*Qall)/(dtdx+abQ);
                        break;
                    }
                    count++;
                }while(fabs(fQj1i1)>0.00001 && count < 50);
                
                _chanS->val[j] = std::max(0.0,(Qupstream+Qall*_dx  - Qk1)*dt) / dx_square;  // Channel storage [m]
                _Q->val[j] = Qk1; // Discharge [m3/s]
                
                if (_sortedGrid.lat_ok[j] == 1){
                    _Qupstream->val[from_j] += Qk1;  // Discharge inflow [m3/s]
                }

                // cout << _chanS->val[j] * dx_square / (_chnlength->val[j] * _chnwidth->val[j]) << "    "<< _chnlength->val[j] << "     " << _chnwidth->val[j] << "     " << _Q->val[j] << endl;
            }
        }    
    }

    return EXIT_SUCCESS;
}