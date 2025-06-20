/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* ParamConstruct.cpp
  * Created  on: 30.02.2025
  * Modified on: 02.06.2025
***************************************************************/


#include "Param.h"

Param::Param(Control &ctrl){
  _rowNum = ctrl._rowNum;
  _colNum = ctrl._colNum;
  _dx = ctrl._dx;
  _nodata = ctrl._nodata;
  _sortedGrid = ctrl._sortedGrid;

  // Init flags
  sort_perc_travel_time_OK = 0;  
  sort_root_fraction_OK = 0;  
  sort_plant_uptake_OK = 0;  // The plant uptake only needs to be calculated once (or once within each change)
  sort_nitrogen_addition_OK = 0;  // The nitrogen addtion only needs to be calculated once (or once within each change)

  string fname = "param.ini";
  /* Parameters */
  _depth3 = new svector(_sortedGrid.size);
  _alpha = new svector(_sortedGrid.size);
  _irrigation_FC_thres = new svector(_sortedGrid.size);
  _perc_vadose_coeff = new svector(_sortedGrid.size);
  _nearsurface_mixing = new svector(_sortedGrid.size);
  _ratio_to_interf = new svector(_sortedGrid.size);
  if (ctrl.opt_intecept == 2 or ctrl.opt_evap == 1){
    _rE = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_snow == 1){
    _snow_rain_thre = new svector(_sortedGrid.size);
    _deg_day_min = new svector(_sortedGrid.size);
    _deg_day_max = new svector(_sortedGrid.size);
    _deg_day_increase = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_pedotransf == 1 or ctrl.opt_pedotransf == 2 or ctrl.opt_pedotransf == 3){
    _ref_thetaS = new svector(_sortedGrid.size);
    _PTF_VG_clay = new svector(_sortedGrid.size);
    _PTF_VG_Db = new svector(_sortedGrid.size);
    _PTF_Ks_const = new svector(_sortedGrid.size);
    _PTF_Ks_sand = new svector(_sortedGrid.size);
    _PTF_Ks_clay = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_fieldcapacity == 1){
    _SWP = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_infil == 1 or ctrl.opt_depthprofile == 2){
    _KvKh = new svector(_sortedGrid.size);
    _psiAE = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_depthprofile == 2){
    _KKs = new svector(_sortedGrid.size);
    _Ksat = new svector(_sortedGrid.size);
    _BClambda = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_percolation == 2){
    _percExp = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_evap == 1){
    _froot_coeff = new svector(_sortedGrid.size);
    _ET_reduction = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_init_GW == 1){
    _init_GW = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_routinterf == 1){
    _pOvf_toChn = new svector(_sortedGrid.size);
    _Ks_vadose = new svector(_sortedGrid.size);
    _lat_to_Chn_vadose = new svector(_sortedGrid.size);
    _interfExp = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_routGWf == 1){
    _Ks_GW = new svector(_sortedGrid.size);
    _lat_to_Chn_GW = new svector(_sortedGrid.size);
    _GWfExp = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_routQ == 1){
    _Manningn = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_chanE == 1 or ctrl.opt_chanE == 2){
    _Echan_alpha = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_irrigation == 1){
    _irrigation_coeff = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_tracking_isotope == 1){
    _CG_n_soil = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_init_d18o == 1){
    _delta_d18o_init_GW = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_init_no3 == 1){
    _delta_no3_init_GW = new svector(_sortedGrid.size);
  }
  if (ctrl.opt_nitrogen_sim == 1){
    _denitrification_river = new svector(_sortedGrid.size);
    _denitrification_soil = new svector(_sortedGrid.size);
    _degradation_soil = new svector(_sortedGrid.size);
    _mineralisation_soil = new svector(_sortedGrid.size);
    _deni_soil_moisture_thres = new svector(_sortedGrid.size);
  }
  /* end of Parameters */

  // Read parameter values from param.ini
  ReadParamFile(ctrl, fname);

  param_category = new svector_2d(ctrl.num_category , _sortedGrid);

  // Assign parameter spatially
  Parameterisation(ctrl);

}