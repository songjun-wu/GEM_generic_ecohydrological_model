#include "Report.h"

Report::Report(Control &ctrl){
    
    _rowNum = ctrl._rowNum;
    _colNum = ctrl._colNum;
    _dx = ctrl._dx;
    _nodata = ctrl._nodata;

    advance_report = 0;

    Report_create_maps(ctrl);
    
}