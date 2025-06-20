/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* readParamFile.cpp
  * Created  on: 30.02.2025
  * Modified on: 02.06.2025
***************************************************************/


#include "Param.h"

int Param::ReadParamFile(Control &ctrl, string fname){
    ifstream input;
    vector<string> lines;
    string s;
    
    // read all text in config file into string-based vector
    input.open(fname.c_str());
    if (!input.good()){
      throw runtime_error(string("file not found: ") + fname.c_str());
    }
  
    while (!input.eof()){
      input >> s;
      lines.push_back(s);
    }

  /* Parameters */
  readIntoParam(depth3, "depth3", lines);
  readIntoParam(alpha, "alpha", lines);
  readIntoParam(rE, "rE", lines);
  readIntoParam(snow_rain_thre, "snow_rain_thre", lines);
  readIntoParam(deg_day_min, "deg_day_min", lines);
  readIntoParam(deg_day_max, "deg_day_max", lines);
  readIntoParam(deg_day_increase, "deg_day_increase", lines);
  readIntoParam(irrigation_FC_thres, "irrigation_FC_thres", lines);
  readIntoParam(ref_thetaS, "ref_thetaS", lines);
  readIntoParam(PTF_VG_clay, "PTF_VG_clay", lines);
  readIntoParam(PTF_VG_Db, "PTF_VG_Db", lines);
  readIntoParam(PTF_Ks_const, "PTF_Ks_const", lines);
  readIntoParam(PTF_Ks_sand, "PTF_Ks_sand", lines);
  readIntoParam(PTF_Ks_clay, "PTF_Ks_clay", lines);
  readIntoParam(SWP, "SWP", lines);
  readIntoParam(KvKh, "KvKh", lines);
  readIntoParam(psiAE, "psiAE", lines);
  readIntoParam(KKs, "KKs", lines);
  readIntoParam(Ksat, "Ksat", lines);
  readIntoParam(BClambda, "BClambda", lines);
  readIntoParam(percExp, "percExp", lines);
  readIntoParam(froot_coeff, "froot_coeff", lines);
  readIntoParam(ET_reduction, "ET_reduction", lines);
  readIntoParam(init_GW, "init_GW", lines);
  readIntoParam(perc_vadose_coeff, "perc_vadose_coeff", lines);
  readIntoParam(pOvf_toChn, "pOvf_toChn", lines);
  readIntoParam(Ks_vadose, "Ks_vadose", lines);
  readIntoParam(Ks_GW, "Ks_GW", lines);
  readIntoParam(lat_to_Chn_vadose, "lat_to_Chn_vadose", lines);
  readIntoParam(lat_to_Chn_GW, "lat_to_Chn_GW", lines);
  readIntoParam(interfExp, "interfExp", lines);
  readIntoParam(GWfExp, "GWfExp", lines);
  readIntoParam(Manningn, "Manningn", lines);
  readIntoParam(Echan_alpha, "Echan_alpha", lines);
  readIntoParam(irrigation_coeff, "irrigation_coeff", lines);
  readIntoParam(nearsurface_mixing, "nearsurface_mixing", lines);
  readIntoParam(ratio_to_interf, "ratio_to_interf", lines);
  readIntoParam(CG_n_soil, "CG_n_soil", lines);
  readIntoParam(delta_d18o_init_GW, "delta_d18o_init_GW", lines);
  readIntoParam(delta_no3_init_GW, "delta_no3_init_GW", lines);
  readIntoParam(denitrification_river, "denitrification_river", lines);
  readIntoParam(denitrification_soil, "denitrification_soil", lines);
  readIntoParam(degradation_soil, "degradation_soil", lines);
  readIntoParam(mineralisation_soil, "mineralisation_soil", lines);
  readIntoParam(deni_soil_moisture_thres, "deni_soil_moisture_thres", lines);
  /* end of Parameters */

  input.close();

  return EXIT_SUCCESS;
}


void Param::readIntoParam(vector<double>& param_arr, string key, vector<string> lines){
    for (const auto& row : lines) {
        stringstream ss(row);
        string value;
        if (getline(ss, value, ',')) { // Read the first column as key
            if (value == key) { // Check if it matches the given key
                while (getline(ss, value, ',')) { // Read remaining values
                    try {
                        param_arr.push_back(stod(value)); // Convert string to double
                    } catch (const exception& e) {
                        cerr << "Error: Invalid number format in row." << endl;
                        return;
                    }
                }
                break; // Stop after finding the matching row
            }
         }
    }
}

