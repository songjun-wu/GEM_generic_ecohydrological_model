#include "Basin.h"

int Basin::Solve_GW_nitrogen(Control &ctrl, Atmosphere &atm){
    /*
    ### GW:
        (_GW_old)
        + percolation3      (need to mix)
        (_GW)
        + repercolation3    
        + GWf_in
        - GWf_out
        - GWf_toChn         
                            
    */

    
    // Mixing GW storage with percolation from layer 3
    for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
        Mixing_full(_GW_old->val[j], _no3_GW->val[j], _Perc3->val[j], _no3_layer3->val[j]);
    }



    return EXIT_SUCCESS;
}
