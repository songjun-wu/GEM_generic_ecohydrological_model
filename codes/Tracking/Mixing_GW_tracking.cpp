#include "Basin.h"

int Basin::Mixing_GW_tracking(Control &ctrl, Atmosphere &atm){

    if (ctrl.opt_tracking_isotope==1) {

        // Mixing GW storage with percolation from layer 3
        for (unsigned int j = 0; j < _sortedGrid.row.size(); j++) {
            Mixing_full(_GW_old->val[j], _d18o_GW->val[j], _Perc3->val[j], _d18o_layer3->val[j]);
        }

    }

    return EXIT_SUCCESS;
}
