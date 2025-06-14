/***************************************************************
* Generic Ecohydrological Model (GEM), a spatial-distributed module-based ecohydrological models
* for multiscale hydrological, isotopic, and water quality simulations

* Copyright (c) 2025   Songjun Wu <songjun.wu@igb-berlin.de / songjun-wu@outlook.com>

  * GEM is a free software under the terms of GNU GEneral Public License version 3,
  * Resitributon and modification are allowed under proper aknowledgement.

* Contributors: Songjun Wu       Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB)

* Basin.h
  * Created  on: 30.02.2025
  * Modified on: 04.06.2025
***************************************************************/


#ifndef BASIN_H_
#define BASIN_H_

#include "Param.h"
#include "Atmosphere.h"
#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

class Basin {
  /* Properties */
  double roundoffERR;
  int _rowNum, _colNum;
  double _dx, _nodata;
  int num_landuse;        // The number of land use types
  vector<int> landuse_idx;  // The location of each land use type in param.ini or N_addition.ini
  sortedGrid _sortedGrid; 
  /* end of Properties */

  public:
  /* GIS */
  svector *_chnwidth;  // Channel width [m]
  svector *_chndepth;  // Channel depth [m]
  svector *_chnlength;  // Channel length [m]
  svector *_slope;  // Slope [m/m]
  svector *_depth1;  // Depth of soil layer 1 [m]
  svector *_depth2;  // Depth of soil layer 2 [m]
  svector *_sand1;  // Sand content of layer 1 [decimal]
  svector *_clay1;  // Clay content of layer 1 [decimal]
  svector *_organic1;  // Organic content of layer 1 [decimal]
  svector *_bulkdensity1;  // Bulk density of layer 1 [g/cm3]
  svector *_sand2;  // Sand content of layer 2 [decimal], only needed when opt_depthprofile = 3
  svector *_sand3;  // Sand content of layer 3 [decimal], only needed when opt_depthprofile = 3
  svector *_clay2;  // Clay content of layer 2 [decimal], only needed when opt_depthprofile = 3
  svector *_clay3;  // Clay content of layer 3 [decimal], only needed when opt_depthprofile = 3
  svector *_silt2;  // Silt content of layer 2 [decimal], only needed when opt_depthprofile = 3
  svector *_silt3;  // Silt content of layer 3 [decimal], only needed when opt_depthprofile = 3
  svector *_organic2;  // Organic content of layer 2 [decimal], only needed when opt_depthprofile = 3
  svector *_organic3;  // Organic content of layer 3 [decimal], only needed when opt_depthprofile = 3
  svector *_bulkdensity2;  // Bulk density of layer 2 [g/cm3], only needed when opt_depthprofile = 3
  svector *_bulkdensity3;  // Bulk density of layer 3 [g/cm3], only needed when opt_depthprofile = 3
  svector *_silt1;  // Silt content of layer 1 [decimal], only needed when opt_pedotransf = 1 or 2
  svector *_no3_rain;  // The nitrate concentration in rain water [mgN/L], only needed when nitrogen_sim_1 = 1
  svector *_N_fertilization;  // The fertilization amount [g/m2], only needed when opt_fert_input = 1
  /* end of GIS */

  /* GroundTs */
  svector *_LAI;  // Leaf area index [decimal]
  ifstream if__LAI;  // Leaf area index [decimal]
  /* end of GroundTs */

  /* Storages */ 
  svector *_I;  // Canopy storage [m]
  svector *_snow;  // Snow depth in [m]
  svector *_pond;  // Ponding water in [m]
  svector *_theta1;  // Soil moisture in layer 1 [decimal]
  svector *_theta2;  // Soil moisture in layer 2 [decimal]
  svector *_theta3;  // Soil moisture in layer 3 [decimal]
  svector *_vadose;  // Vadose storage (unsaturated zone) [m]
  svector *_GW;  // Groundwater storage [m]
  svector *_chanS;  // Channel storage [m3]
  svector *_I_old;  // Canopy storage [m]
  svector *_snow_old;  // Snow depth in [m]
  svector *_pond_old;  // Ponding water in [m]
  svector *_theta1_old;  // Soil moisture in layer 1 [decimal]
  svector *_theta2_old;  // Soil moisture in layer 2 [decimal]
  svector *_theta3_old;  // Soil moisture in layer 3 [decimal]
  svector *_vadose_old;  // Vadose storage [m]
  svector *_GW_old;  // Groundwater storage [m]
  svector *_chanS_old;  // Channel storage [m3]
  /* end of Storages */ 
 

  /* Fluxes */
  svector *_Th;  // Throughfall [m]
  svector *_snowmelt;  // Snow melt [m]
  svector *_infilt;  // Inflitration into soil layer 1 [m]
  svector *_Perc1;  // Percolation into layer 2 [m]
  svector *_Perc2;  // Percolation into layer 3 [m]
  svector *_Perc3;  // Percolation into vadose storage [m]
  svector *_Perc_vadose;  // Percolation from vadose storage into gw reservior [m]
  svector *_rPerc_vadose;  // Repercolation from vadose storage into gw reservior [m]
  svector *_Ei;  // Canopy evaporation [m]
  svector *_Es;  // Soil evaporation [m]
  svector *_Tr;  // Total transpiration in three layers [m]
  svector *_Tr1;  // Transpiration in layer 1 [m]
  svector *_Tr2;  // Transpiration in layer 2 [m]
  svector *_Tr3;  // Transpiration in layer 3 [m]
  svector *_irrigation_from_river;  // Water extraction from river [m]
  svector *_irrigation_from_GW;  // Water extraction from GW [m]
  svector *_Ks1;  // Saturated hydraulic conductivity in layer 1
  svector *_Ks2;  // Saturated hydraulic conductivity in layer 2
  svector *_Ks3;  // Saturated hydraulic conductivity in layer 3
  svector *_thetaS1;  // Saturated soil moisture in layer 1
  svector *_thetaS2;  // Saturated soil moisture in layer 2
  svector *_thetaS3;  // Saturated soil moisture in layer 3
  svector *_thetaFC1;  // Field capacity in layer 1
  svector *_thetaFC2;  // Field capacity in layer 2
  svector *_thetaFC3;  // Field capacity in layer 3
  svector *_thetaWP1;  // Wilting point in layer 1
  svector *_thetaWP2;  // Wilting point in layer 2
  svector *_thetaWP3;  // Wilting point in layer 3
  svector *_ovf_in;  // Overland flow from upstream cell(s) [m]
  svector *_ovf_out;  // Overland flow to downstream cell [m]
  svector *_ovf_toChn;  // Overland flow to Channel [m]
  svector *_interf_in;  // Interflow from upstream cell(s) [m]
  svector *_interf_out;  // Interflow to downstream cell [m]
  svector *_interf_toChn;  // Interflow to Channel [m]
  svector *_GWf_in;  // GW flow from upstream cell(s) [m]
  svector *_GWf_out;  // GW flow to downstream cell [m]
  svector *_GWf_toChn;  // Groundwater flow to Channel [m]
  svector *_Q;  // Discharge [m3/s]
  svector *_Qupstream;  // Upstream inflow [m3/s]
  svector *_Echan;  // Channel evaporation [m]
  svector *_tmp;  // Temporal variable for testing [-]
  svector *_snowacc;  // Snow accumulation for testing [m]
  svector *_TchanS;  // Instream temperature conceptualised as 20-day's average of air temperature [degree C]
  svector *_rinfilt;  // Reinflitration into soil layer 1 [m]
  svector *_rPerc1;  // Repercolation into layer 2 due to overland flow routing [m]
  svector *_rPerc2;  // Repercolation into layer 3 due to overland flow routing [m]
  svector *_rPerc3;  // Repercolation into gw reservior due to overland flow routing [m]
  svector *_froot_layer1;  // froot coefficient for all soil profile
  svector *_froot_layer2;  // froot coefficient for layer 2
  svector *_froot_layer3;  // froot coefficient for layer 3
  svector *_PE;  // Potential evaporation [m]
  svector *_PT;  // Potential transpiration [m]
  svector *_p_perc1;  // Percolation proportion in layer 1
  svector *_p_perc2;  // Percolation proportion in layer 2
  svector *_p_perc3;  // Percolation proportion in layer 3
  svector *_flux_ovf_in_acc;  // Total amount of solutes in overland inflow [original unit * m]
  svector *_flux_interf_in_acc;  // Total amount of solutes in inter-inflow [original unit * m]
  svector *_flux_GWf_in_acc;  // Total amount of solutes in GW inflow [original unit * m]
  svector *_flux_Qupstream_acc;  // Total amount of solutes in upstream inflow to channel storage [original unit * m]
  /* end of Fluxes */


  /* Tracking */
  svector *_d18o_I;  // d18o in Canopy storage [‰]
  svector *_d18o_snow;  // d18o in Snow depth in [‰]
  svector *_d18o_pond;  // d18o in Ponding water in [‰]
  svector *_d18o_layer1;  // d18o in Soil moisture in layer 1 [‰]
  svector *_d18o_layer2;  // d18o in Soil moisture in layer 2 [‰]
  svector *_d18o_layer3;  // d18o in Soil moisture in layer 3 [‰]
  svector *_d18o_vadose;  // d18o in vadose storage [‰]
  svector *_d18o_GW;  // d18o in Groundwater storage [‰]
  svector *_d18o_chanS;  // d18o in Channel storage [‰]
  svector *_age_vadose;  // Age in vadose storage [‰]
  svector *_age_I;  // Age in Canopy storage [days]
  svector *_age_snow;  // Age in Snow depth in [days]
  svector *_age_pond;  // Age in Ponding water in [days]
  svector *_age_layer1;  // Age in Soil moisture in layer 1 [days]
  svector *_age_layer2;  // Age in Soil moisture in layer 2 [days]
  svector *_age_layer3;  // Age in Soil moisture in layer 3 [days]
  svector *_age_GW;  // Age in Groundwater storage [days]
  svector *_age_chanS;  // Age in Channel storage [days]
  /* end of Tracking */

  // Nitrogen addition and plant uptakes are identical for each year, so they only need to be sorted once (or once after change in parameterisation)
  // 2d vector [num_landuse][366 days]
  vector<vector <double>> _fertN_add_layer1_IN;
  vector<vector <double>> _fertN_add_layer2_IN;
  vector<vector <double>> _fertN_add_layer1_fastN;
  vector<vector <double>> _fertN_add_layer2_fastN;
  vector<vector <double>> _resN_add_layer1_fastN;
  vector<vector <double>> _resN_add_layer2_fastN;
  vector<vector <double>> _resN_add_layer1_humusN;
  vector<vector <double>> _resN_add_layer2_humusN;

  vector<vector <double>> _potential_uptake_layer1;
  vector<vector <double>> _potential_uptake_layer2;
  vector<vector <double>> _potential_uptake_layer3;
  /* Nitrogen addition */
  vector<double> is_crop;
  vector<double> fert_add;
  vector<double> fert_day;
  vector<double> fert_down;
  vector<double> fert_period;
  vector<double> fert_IN;
  vector<double> manure_add;
  vector<double> manure_day;
  vector<double> manure_down;
  vector<double> manure_period;
  vector<double> manure_IN;
  vector<double> residue_add;
  vector<double> residue_day;
  vector<double> residue_down;
  vector<double> residue_period;
  vector<double> residue_fastN;
  vector<double> up1;
  vector<double> up2;
  vector<double> up3;
  vector<double> upper_uptake;
  vector<double> plant_day;
  vector<double> emerge_day;
  vector<double> harvest_day;
  /* end of Nitrogen addition */

  /* Irrigation */
  vector<double> irrigation_thres;
  /* end of Irrigation */

  /* Nitrogen */
  svector *_no3_I;  // no3 in Canopy storage [mgN/L]
  svector *_no3_snow;  // no3 in Snow depth in [mgN/L]
  svector *_no3_pond;  // no3 in Ponding water in [mgN/L]
  svector *_no3_layer1;  // no3 in Soil moisture in layer 1 [mgN/L]
  svector *_no3_layer2;  // no3 in Soil moisture in layer 2 [mgN/L]
  svector *_no3_layer3;  // no3 in Soil moisture in layer 3 [mgN/L]
  svector *_no3_vadose;  // no3 in vadose storage [mgN/L]
  svector *_no3_GW;  // no3 in Groundwater storage [mgN/L]
  svector *_no3_chanS;  // no3 in Channel storage [mgN/L]
  svector *_nitrogen_add;  // Nitrogen addition of fertilizer, manure, and plant residues [mgN/L*m = gN/m2]
  svector *_plant_uptake;  // Plant uptake [mgN/L*m = gN/m2]
  svector *_deni_soil;  // Soil denitrification [mgN/L*m = gN/m2]
  svector *_minerl_soil;  // Soil mineralisation [mgN/L*m = gN/m2]
  svector *_degrad_soil;  // Soil degradation [mgN/L*m = gN/m2]
  svector *_deni_river;  // Aquatic denitrification [mgN/L*m = gN/m2]
  svector *_humusN1;  // Humus nitrogen storage in layer 1 [mgN/L*m = gN/m2]
  svector *_humusN2;  // Humus nitrogen storage in layer 2 [mgN/L*m = gN/m2]
  svector *_humusN3;  // Humus nitrogen storage in layer 3 [mgN/L*m = gN/m2]
  svector *_fastN1;  // Fast nitrogen storage in layer 1 [mgN/L*m = gN/m2]
  svector *_fastN2;  // Fast nitrogen storage in layer 2 [mgN/L*m = gN/m2]
  svector *_fastN3;  // Fast nitrogen storage in layer 3 [mgN/L*m = gN/m2]
  /* end of Nitrogen */

  /* Save TS output to speed up calibration; Temporary implementation */
  vector<double> vector_Q;
  vector<double> vector_d18o_chanS;
  vector<double> vector_no3_chanS;
  
 
  
  Basin(Control &ctrl, Param &par);  // constrcuctor of Basin
  //dtor
  ~Basin();  // destrcuctor of Basin
  int dtor(Control &ctrl);


  int Solve_timesteps(Control &ctrl, Param &par, Atmosphere &atm);

  // Model test
  int Check_mass_balance(Control &ctrl, Param &par, Atmosphere &atm);

  // Init
  int Initialisation(Control &ctrl, Param &par, Atmosphere &atm);
  int Store_states();  // Store all water storages for mixing

  // Open and read ground inputs such as LAI
  int open_groundTs(Control &ctrl);
  int read_groundTs(Control &ctrl);
  int open_groundTs_maps(string fname, ifstream &ifHandle);
  int read_groundTs_maps(ifstream &ifHandle, svector &GroundTsMap);
  int init_groundTs(Control &ctrl);
  int update_groundTs(Control &ctrl, Param &par);
  int init_groundTs_maps(string fname, ifstream &ifHandle);
  int update_groundTs_maps(ifstream &ifHandle, Param &par, svector &GroundTsMap);

  /* Canopy interception */
  int Solve_canopy(Control &ctrl, Param &par, Atmosphere &atm);
  int Interception_1(Control &ctrl, Param &par, Atmosphere &atm);
  int Interception_2(Control &ctrl, Param &par, Atmosphere &atm);

  /* Snow accumulation and melt */
  int Solve_surface(Control &ctrl, Param &par, Atmosphere &atm);
  int Snow_acc_melt(Param &par, Atmosphere &atm, int j);

  /* Soil profiles */
  int Solve_soil_profile(Control &ctrl, Param &par, Atmosphere &atm);
  // Calculate soil proporties
  int Soil_proporty(Control &ctrl, Param &par);
  int Pedo_transfer_1(Control &ctrl, Param &par, svector &sv_sand,  svector &sv_clay,  svector &sv_silt,  svector &sv_organic_content, \
                      svector &sv_bulk_density, svector &sv_Ks, svector &sv_thetaS, svector &sv_thetaFC, svector &sv_thetaWP);
  int Pedo_transfer_2(Control &ctrl, Param &par, svector &sv_sand,  svector &sv_clay,  svector &sv_silt,  svector &sv_organic_content, \
                        svector &sv_bulk_density, svector &sv_Ks, svector &sv_thetaS, svector &sv_thetaFC, svector &sv_thetaWP);
  int Pedo_transfer_3(Control &ctrl, Param &par, svector &sv_sand,  svector &sv_clay,  \
                          svector &sv_bulk_density, svector &sv_Ks, svector &sv_thetaS, svector &sv_thetaFC, svector &sv_thetaWP);
  
  // Infiltration
  int Infiltration_1(Control &ctrl, Param &par);
  int Reinfiltration_1(Control &ctrl, Param &par, int j, double &db_rinfilt, double &db_theta1, double &db_pond);

  // Evapotranspiration
  int Canopy_evaporation_1(Control &ctrl, Param &par, Atmosphere &atm);
  int Seperate_PET(Param &par, Atmosphere &atm);  // Seperate PET to PE and PT based on LAI and a rExtinct parameter; Rutter (1972)
  int Evapotranspiration_1(Control &ctrl, Param &par, Atmosphere &atm);

  int Percolation_1(Control &ctrl, Param &par);
  int Percolation_2(Control &ctrl, Param &par);
  int Percolation_3(Control &ctrl, Param &par);
  int Repercolation_1(Control &ctrl, Param &par, int j, double &db_theta1, double &db_theta2, double &db_theta3, double &db_vadose, double &db_rPerc1, double &db_rPerc2, double &db_rPerc3);
  int Repercolation_2(Control &ctrl, Param &par, int j, double &db_theta1, double &db_theta2, double &db_theta3, double &db_vadose, double &db_rPerc1, double &db_rPerc2, double &db_rPerc3);
  int Repercolation_3(Control &ctrl, Param &par, int j, double &db_theta1, double &db_theta2, double &db_theta3, double &db_vadose, double &db_rPerc1, double &db_rPerc2, double &db_rPerc3);

  int GWrecharge_1(Control &ctrl, Param &par);
  int GWrecharge_2(Control &ctrl, Param &par);
  int ReGWrecharge_1(Control &ctrl, Param &par, int j, double &db_vadose, double &db_GW, double &db_rPerc_vadose);
  int ReGWrecharge_2(Control &ctrl, Param &par, int j, double &db_vadose, double &db_GW, double &db_rPerc_vadose);


  /* Soil profiles */
  int Routing(Control &ctrl, Param &par);
  int Routing_ovf_1(Control &ctrl, Param &par); // overland flow routing; All ponding water goes to next cell
  int Routing_interflow_1(Control &ctrl, Param &par); // Interflow routing based on linear approximation of Kinematic Wave
  int Routing_Q_1(Control &ctrl, Param &par); // Stream routing based on Kinematic Wave
  int Routing_GWflow_1(Control &ctrl, Param &par); // GW flow routing based on linear approximation of Kinematic Wave

  /* Energy balance */
  double Get_soil_temperature(const double Ta, const double LAI);

  /* Isotopic and Age tracking */
  int Mixing_full(double storage, double &cstorage, double input, double cinput);  // Full mixing within the timestep
  int Mixing_baseflow(double storage, double &coutput, double input, double cinput, double output);   // Baseflow mixing for GW storage
  int Mixing_canopy_tracking(Control &ctrl, Atmosphere &atm);  // Canopy storage mixing and fractionaton
  int Mixing_surface_tracking(Control &ctrl, Atmosphere &atm, Param &par);  // Canopy snowpack and throughfall
  int Mixing_soil_profile_tracking(Control &ctrl, Atmosphere &atm, Param &par);  // Soil storage mixing and fractionaton
  int Mixing_vadose_tracking(Control &ctrl, Atmosphere &atm);  // Vadose storage mixing
  int Mixing_GW_tracking(Control &ctrl, Atmosphere &atm);  // GW storage mixing
  int Mixing_routing_tracking(Control &ctrl, Param &par);  // Mixing of overland flow, interflow, and GW flow
  int Mixing_channel_tracking(Control &ctrl, Atmosphere &atm, Param &par);  // Fractionation due to channel evaporation
  int Fractionation(Atmosphere &atm, Param &par, svector &sv_evap, svector &sv_V_new, svector &sv_di_old, svector &sv_di_new, svector &sv_di_evap, int issoil);  // Fractionation due to canopy or soil evaporation
  int Advance_age(); // Advance water ages by 1


  /* Channel */
  int Solve_channel(Control &ctrl, Param &par, Atmosphere &atm);
  int Channel_evaporation_1(Control &ctrl, Atmosphere &atm, Param &par);  // Penman equation
  int Channel_evaporation_2(Control &ctrl, Atmosphere &atm, Param &par);  // Priestley-Taylor equation

  /* Irrigation module */
  int Irrigation(Control &ctrl, Param &par);

  /* Nitrogen module */
  int Solve_canopy_nitrogen(Control &ctrl, Atmosphere &atm);  // Canopy storage mixing with precipitation and erichment due to evaporation
  int Solve_surface_nitrogen(Control &ctrl, Atmosphere &atm, Param &par);  // Ponding water mixing with snow melt
  int Solve_soil_profile_nitrogen(Control &ctrl, Atmosphere &atm, Param &par);  // Soil storage mixing and transformation
  int Solve_vadose_nitrogen(Control &ctrl, Atmosphere &atm);  // vadose storage mixing
  int Solve_GW_nitrogen(Control &ctrl, Atmosphere &atm);  // GW storage mixing
  int Solve_routing_nitrogen(Control &ctrl, Param &par);  // Mixing of overland flow, interflow, and GW flow
  int Solve_channel_nitrogen(Control &ctrl, Atmosphere &atm, Param &par);  // Enrichment due to channel evaporation, and instream nutrient transformation
  
  int Sort_nitrogen_addition(Control &ctrl, Param &par);  // Sort 366 days at first iteration
  int Nitrogen_addition(Control &ctrl, Param &par);
  int Sort_plant_uptake(Control &ctrl, Param &par);
  int Plant_uptake(Control &ctrl, Param &par, Atmosphere &atm);
  int Soil_denitrification(Control &ctrl, Atmosphere &atm, Param &par);
  int Soil_transformation(Control &ctrl, Atmosphere &atm, Param &par);
  int Instream_transformation(Control &ctrl, Atmosphere &atm, Param &par);

  /* Functions */
  int Sort_percolation_travel_time(Control &ctrl, Param &par);
  int Sort_root_fraction(Control &ctrl,Param &par);  // Estimate root fraction
  double Temp_factor(const double T);  // Temperature factor of nitrogen transformation
  double Moist_factor(const double db_theta, const double db_thetaWP, const double db_thetaS, const double db_depth); // Moisture factor of nitrogen transformation

  /* IO functions */
  int ReadCropFile(Control &ctrl, Param &par, string fname);

  /* Save TS output to speed up calibration; Temporary implementation */
  int Report_for_cali(Control &ctrl);
  int Save_for_cali(Control &ctrl);
  bool save_vector_to_binary(const std::vector<double>& vec, const std::string& filename);

};

#endif /* BASIN_H_ */
