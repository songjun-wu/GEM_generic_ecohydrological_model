


class setting:
    max_category = 10

class Opt:
    cond = {}
    # Options
    cond['none'] = {'key':None, 'value':None,  'description':'General variables'}

    cond['climate_input_format_2'] = {'key':'opt_climate_input_format', 'value':2,
                                      'general_description':'How is climate inputs orgainsed?\n# 1: raster\n# 2: aggregated binary file (climate_zone file should be specified)',
                                      'description':'Binary inputs based on cliamte zones'}
    cond['tracking_isotope_1'] = {'key':'opt_tracking_isotope', 'value':1,
                                  'general_description':'Enable isotopic tracking?\n# 0: disabled\n# 1: enabled',
                                  'description':'Isotopic tracking'}
    
    cond['intecept_1']   = {'key':'opt_intecept', 'value':1, 
                        'general_description':'Canopy interception\n# 1 :maximum canopy storage unmodified\n# 2 :storage corrected (Landarf et al., 2024)',
                        'description':'Maximum canopy storage unmodified'}
    
    cond['intecept_2']   = {'key':'opt_intecept', 'value':2, 
                        'general_description':'Canopy interception\n# 1: maximum canopy storage unmodified\n# 2: maximum canopy storage corrected (Landarf et al., 2024)',
                        'description':'Maximum canopy storage corrected (Landarf et al., 2024)'}

    cond['snow_1']   = {'key':'opt_snow', 'value':1, 
                        'general_description':'Snow accumulation method\n# 1: Degree day factor method',
                        'description':'Degree day factor method for snow melt'}


    
    
    cond['pedotransf_1']   = {'key':'opt_pedotransf', 'value':1, 
                        'general_description':'Pedo-transfer function to estimate Van Genuchten parameters\n# 1: Wosten et al., (1999)\n# 2: Wosten et al., (1997)\n# 3: Zacharias et al., (2007)',
                        'description':'Pedo-transfer function to estimate Van Genuchten parameters based on silt, clay, and OM content, Wosten et al., (1999)'}
    
    cond['pedotransf_2']   = {'key':'opt_pedotransf', 'value':2, 
                        'general_description':'Pedo-transfer function to estimate Van Genuchten parameters\n# 1: Wosten et al., (1999)\n# 2: Wosten et al., (1997)\n# 3: Zacharias et al., (2007)',
                        'description':'Pedo-transfer function to estimate Van Genuchten parameters based on silt, clay, and OM content, Wosten et al., (1997)'}

    cond['pedotransf_3']   = {'key':'opt_pedotransf', 'value':3, 
                        'general_description':'Pedo-transfer function to estimate Van Genuchten parameters\n# 1: Wosten et al., (1999)\n# 2: Wosten et al., (1997)\n# 3: Zacharias et al., (2007)',
                        'description':'Pedo-transfer function to estimate Van Genuchten parameters based on sand and clay, Zacharias et al., (2007)'}
    
    
    cond['fc_2']   = {'key':'opt_fieldcapacity', 'value':2, 
                        'general_description':'Method to estimate field capacity\n# 1: based on Van Genuchten Model\n# 2: Ks considered, Twarakavi et al., (2007)',
                        'description':'Method to estimate field capacity based on Ks and Van Genuchten Model, Twarakavi et al., (2007)'}
    
    cond['fc_1']   = {'key':'opt_fieldcapacity', 'value':1, 
                        'general_description':'Method to estimate field capacity\n# 1: based on Van Genuchten Model\n# 2: Ks considered, Twarakavi et al., (2007)',
                        'description':'Method to estimate field capacity based on Van Genuchten Model'}
    
    cond['depthprofile_3']   = {'key':'opt_depthprofile', 'value':3, 
                        'general_description':'The way to estimate soil characteristics in deeper layer\n# 1: All layers remain the same\n# 2: exponential profile based on depth\n# 3: Pedo-transfer function for each layer',
                        'description':'The way to estimate soil characteristics in deeper layer: Pedo-transfer function for each layer'}
    cond['depthprofile_2']   = {'key':'opt_depthprofile', 'value':2, 
                        'general_description':'The way to estimate soil characteristics in deeper layer\n# 1: All layers remain the same\n# 2: exponential profile based on depth\n# 3: Pedo-transfer function for each layer',
                        'description':'The way to estimate soil characteristics in deeper layer: exponential profile based on depth'}
    cond['depthprofile_1']   = {'key':'opt_depthprofile', 'value':1, 
                        'general_description':'The way to estimate soil characteristics in deeper layer\n# 1: All layers remain the same\n# 2: exponential profile based on depth\n# 3: Pedo-transfer function for each layer',
                        'description':'The way to estimate soil characteristics in deeper layer: all layers remain the same'}
    
    
    
    

    cond['infil_1']   = {'key':'opt_infil', 'value':1, 
                        'general_description':'Iniltration model\n# 1: Green-Ampt model\n# 2: based on soil deficit and a exponential parameter; Feddes et al., (1976)',
                        'description':'Method of iniltration and percolation based on Green-Ampt model'}





    cond['perc_1']   = {'key':'opt_percolation', 'value':1, 
                        'general_description':'Percolation model\n# 1: based on travel time and excess water above FC; SWAT\n# 2: based on soil deficit and a exponential parameter; Feddes et al., (1976)\
                        \n# 3: based on soil deficit',
                        'description':'Percolation based on based on travel time and excess water above FC'}
    
    cond['perc_2']   = {'key':'opt_percolation', 'value':2, 
                       'general_description':'Percolation model\n# 1: based on travel time and excess water above FC; SWAT\n# 2: based on soil deficit and a exponential parameter; Feddes et al., (1976)\
                        \n# 3: based on soil deficit',
                        'description':'Percolation based on soil deficit and a exponential parameter; Feddes et al., (1976)'}

    cond['perc_3']   = {'key':'opt_percolation', 'value':2, 
                       'general_description':'Percolation model\n# 1: based on travel time and excess water above FC; SWAT\n# 2: based on soil deficit and a exponential parameter; Feddes et al., (1976)\
                        \n# 3: based on soil deficit',
                        'description':'Percolation based on soil deficit. Percolation exists after soil saturation'}          
    
    
    cond['evap_1']   = {'key':'opt_evap', 'value':1, 
                        'general_description':'Evapotranspiration function\n# 1: based on PET and a soil water dependent root extraction function (Feddes et al., 1976)',
                        'description':'Evapotranspiration calculation based on Feddes et al., (1976)'}
    
    cond['routOvf_1']   = {'key':'opt_routOvf', 'value':1, 
                        'general_description':'Overland flow routing\n# 1: All ponding water goes to next cell',
                        'description':'Overland flow routing: all ponding water goes to next cell'}
    
    cond['routinterf_1']   = {'key':'opt_routinterf', 'value':1, 
                        'general_description':'Interflow routing\n# 1: linear approximation of Kinematic Wave',
                        'description':'Interflow routing: linear approximation of Kinematic Wave'}
    
    cond['routGWf_1']   = {'key':'opt_routGWf', 'value':1, 
                        'general_description':'GW routing\n# 1: linear approximation of Kinematic Wave',
                        'description':'GW routing: linear approximation of Kinematic Wave'}
    
    cond['routQ_1']   = {'key':'opt_routQ', 'value':1, 
                        'general_description':'Stream routing\n# 1: Kinematic Wave',
                        'description':'Stream routing: Kinematic Wave'}
    
    




    