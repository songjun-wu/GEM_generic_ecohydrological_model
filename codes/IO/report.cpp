#include "Report.h"

int Report::report(Control &ctrl, Basin &Bsn){

  /* Report */
  // 1: report time series at gauging stations; 2: report maps
  if (ctrl.report__I==1) {reportTS(ctrl, Bsn._I, "canopy_storage", ctrl.path_ResultsFolder);}
  else if (ctrl.report__I==2) {reportMap(ctrl, Bsn._I, ctrl._sortedGrid, "canopy_storage", ctrl.path_ResultsFolder);}

  if (ctrl.report__snow==1) {reportTS(ctrl, Bsn._snow, "snow_depth", ctrl.path_ResultsFolder);}
  else if (ctrl.report__snow==2) {reportMap(ctrl, Bsn._snow, ctrl._sortedGrid, "snow_depth", ctrl.path_ResultsFolder);}

  if (ctrl.report__pond==1) {reportTS(ctrl, Bsn._pond, "pond", ctrl.path_ResultsFolder);}
  else if (ctrl.report__pond==2) {reportMap(ctrl, Bsn._pond, ctrl._sortedGrid, "pond", ctrl.path_ResultsFolder);}

  if (ctrl.report__theta1==1) {reportTS(ctrl, Bsn._theta1, "SMC_layer1", ctrl.path_ResultsFolder);}
  else if (ctrl.report__theta1==2) {reportMap(ctrl, Bsn._theta1, ctrl._sortedGrid, "SMC_layer1", ctrl.path_ResultsFolder);}

  if (ctrl.report__theta2==1) {reportTS(ctrl, Bsn._theta2, "SMC_layer2", ctrl.path_ResultsFolder);}
  else if (ctrl.report__theta2==2) {reportMap(ctrl, Bsn._theta2, ctrl._sortedGrid, "SMC_layer2", ctrl.path_ResultsFolder);}

  if (ctrl.report__theta3==1) {reportTS(ctrl, Bsn._theta3, "SMC_layer3", ctrl.path_ResultsFolder);}
  else if (ctrl.report__theta3==2) {reportMap(ctrl, Bsn._theta3, ctrl._sortedGrid, "SMC_layer3", ctrl.path_ResultsFolder);}

  if (ctrl.report__GW==1) {reportTS(ctrl, Bsn._GW, "groundwater_storage", ctrl.path_ResultsFolder);}
  else if (ctrl.report__GW==2) {reportMap(ctrl, Bsn._GW, ctrl._sortedGrid, "groundwater_storage", ctrl.path_ResultsFolder);}

  if (ctrl.report__D==1) {reportTS(ctrl, Bsn._D, "interception", ctrl.path_ResultsFolder);}
  else if (ctrl.report__D==2) {reportMap(ctrl, Bsn._D, ctrl._sortedGrid, "interception", ctrl.path_ResultsFolder);}

  if (ctrl.report__Th==1) {reportTS(ctrl, Bsn._Th, "throufall", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Th==2) {reportMap(ctrl, Bsn._Th, ctrl._sortedGrid, "throufall", ctrl.path_ResultsFolder);}

  if (ctrl.report__snowmelt==1) {reportTS(ctrl, Bsn._snowmelt, "snowmelt", ctrl.path_ResultsFolder);}
  else if (ctrl.report__snowmelt==2) {reportMap(ctrl, Bsn._snowmelt, ctrl._sortedGrid, "snowmelt", ctrl.path_ResultsFolder);}

  if (ctrl.report__infilt==1) {reportTS(ctrl, Bsn._infilt, "infiltration", ctrl.path_ResultsFolder);}
  else if (ctrl.report__infilt==2) {reportMap(ctrl, Bsn._infilt, ctrl._sortedGrid, "infiltration", ctrl.path_ResultsFolder);}

  if (ctrl.report__Perc1==1) {reportTS(ctrl, Bsn._Perc1, "perc_layer1", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Perc1==2) {reportMap(ctrl, Bsn._Perc1, ctrl._sortedGrid, "perc_layer1", ctrl.path_ResultsFolder);}

  if (ctrl.report__Perc2==1) {reportTS(ctrl, Bsn._Perc2, "perc_layer2", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Perc2==2) {reportMap(ctrl, Bsn._Perc2, ctrl._sortedGrid, "perc_layer2", ctrl.path_ResultsFolder);}

  if (ctrl.report__Perc3==1) {reportTS(ctrl, Bsn._Perc3, "perc_layer3", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Perc3==2) {reportMap(ctrl, Bsn._Perc3, ctrl._sortedGrid, "perc_layer3", ctrl.path_ResultsFolder);}

  if (ctrl.report__Ei==1) {reportTS(ctrl, Bsn._Ei, "canopy_evap", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Ei==2) {reportMap(ctrl, Bsn._Ei, ctrl._sortedGrid, "canopy_evap", ctrl.path_ResultsFolder);}

  if (ctrl.report__Es==1) {reportTS(ctrl, Bsn._Es, "soil_evap", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Es==2) {reportMap(ctrl, Bsn._Es, ctrl._sortedGrid, "soil_evap", ctrl.path_ResultsFolder);}

  if (ctrl.report__Tr==1) {reportTS(ctrl, Bsn._Tr, "transp", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Tr==2) {reportMap(ctrl, Bsn._Tr, ctrl._sortedGrid, "transp", ctrl.path_ResultsFolder);}

  if (ctrl.report__Tr1==1) {reportTS(ctrl, Bsn._Tr1, "transp_layer1", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Tr1==2) {reportMap(ctrl, Bsn._Tr1, ctrl._sortedGrid, "transp_layer1", ctrl.path_ResultsFolder);}

  if (ctrl.report__Tr2==1) {reportTS(ctrl, Bsn._Tr2, "transp_layer2", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Tr2==2) {reportMap(ctrl, Bsn._Tr2, ctrl._sortedGrid, "transp_layer2", ctrl.path_ResultsFolder);}

  if (ctrl.report__Tr3==1) {reportTS(ctrl, Bsn._Tr3, "transp_layer3", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Tr3==2) {reportMap(ctrl, Bsn._Tr3, ctrl._sortedGrid, "transp_layer3", ctrl.path_ResultsFolder);}

  if (ctrl.report__ovf_in==1) {reportTS(ctrl, Bsn._ovf_in, "overland_flow_input", ctrl.path_ResultsFolder);}
  else if (ctrl.report__ovf_in==2) {reportMap(ctrl, Bsn._ovf_in, ctrl._sortedGrid, "overland_flow_input", ctrl.path_ResultsFolder);}

  if (ctrl.report__ovf_out==1) {reportTS(ctrl, Bsn._ovf_out, "overland_flow_output", ctrl.path_ResultsFolder);}
  else if (ctrl.report__ovf_out==2) {reportMap(ctrl, Bsn._ovf_out, ctrl._sortedGrid, "overland_flow_output", ctrl.path_ResultsFolder);}

  if (ctrl.report__ovf_toChn==1) {reportTS(ctrl, Bsn._ovf_toChn, "overland_flow_toChn", ctrl.path_ResultsFolder);}
  else if (ctrl.report__ovf_toChn==2) {reportMap(ctrl, Bsn._ovf_toChn, ctrl._sortedGrid, "overland_flow_toChn", ctrl.path_ResultsFolder);}

  if (ctrl.report__interf_in==1) {reportTS(ctrl, Bsn._interf_in, "interflow_input", ctrl.path_ResultsFolder);}
  else if (ctrl.report__interf_in==2) {reportMap(ctrl, Bsn._interf_in, ctrl._sortedGrid, "interflow_input", ctrl.path_ResultsFolder);}

  if (ctrl.report__interf_out==1) {reportTS(ctrl, Bsn._interf_out, "interflow_output", ctrl.path_ResultsFolder);}
  else if (ctrl.report__interf_out==2) {reportMap(ctrl, Bsn._interf_out, ctrl._sortedGrid, "interflow_output", ctrl.path_ResultsFolder);}

  if (ctrl.report__interf_toChn==1) {reportTS(ctrl, Bsn._interf_toChn, "interflow_toChn", ctrl.path_ResultsFolder);}
  else if (ctrl.report__interf_toChn==2) {reportMap(ctrl, Bsn._interf_toChn, ctrl._sortedGrid, "interflow_toChn", ctrl.path_ResultsFolder);}

  if (ctrl.report__gwf_toChn==1) {reportTS(ctrl, Bsn._gwf_toChn, "groundwater_flow_toChn", ctrl.path_ResultsFolder);}
  else if (ctrl.report__gwf_toChn==2) {reportMap(ctrl, Bsn._gwf_toChn, ctrl._sortedGrid, "groundwater_flow_toChn", ctrl.path_ResultsFolder);}

  if (ctrl.report__Q==1) {reportTS(ctrl, Bsn._Q, "discharge", ctrl.path_ResultsFolder);}
  else if (ctrl.report__Q==2) {reportMap(ctrl, Bsn._Q, ctrl._sortedGrid, "discharge", ctrl.path_ResultsFolder);}

  /* end of Report */

  return 0;
  }


int Report::reportTS(Control &ctrl, const svector *input, string varname, string filepath){
  fstream ofOutput;
  int length = ctrl._Tsmask.cell.size();
  double outdata[length];
  string filename;

  for (int i = 0; i<length; i++){
      outdata[i] = input->val[ctrl._Tsmask.cell[i]];
  }
  
  filename =  filepath + varname.c_str() + "_TS.bin";
  ofOutput.open(filename.c_str(), ios::binary|ios::app);
  ofOutput.write((char*)&outdata, sizeof(double)*length);
  ofOutput.close();
  return 0;
  }


int Report::reportMap(Control &ctrl, const svector *input, sortedGrid _sortedGrid, string varname, string filepath){

  int r, c;

  int _rowNum = ctrl._rowNum;
  int _colNum = ctrl._colNum;


  fstream ofOutput;
  double outdata[_rowNum*_colNum];
  string filename;

  for(int i = 0; i < _rowNum*_colNum; i++){
      outdata[i] = ctrl._nodata;
}


  for(int j = 0; j < _sortedGrid.size; j++){
    r = _sortedGrid.row[j];
    c = _sortedGrid.col[j];
    outdata[r*_colNum + c] = input->val[j];
  }

  
  filename =  filepath + varname.c_str() + "_map.bin";
  ofOutput.open(filename.c_str(), ios::binary|ios::app);
  ofOutput.write((char*)&outdata, sizeof(double)*_rowNum*_colNum);
  ofOutput.close();
  return 0;
  }