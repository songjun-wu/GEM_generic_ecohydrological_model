import os
import shutil
import numpy as np
from develop_tools import *




def includes(fname, signs, datas, max_category):
    for j in range(len(signs)):
        sign = signs[j]
        data = datas[j]
        content = []
        if sign == 'Parameters':
            for kk in range(len(data)):
                content.append('  vector<double> ' + data[kk][0][1:] + ';\n')
        if sign == 'Nitrogen addition':
            for kk in range(len(data)):
                content.append('  vector<double> ' + data[kk][0] + ';\n')
        if sign == 'Irrigation':
            for kk in range(len(data)):
                content.append('  vector<double> ' + data[kk][0] + ';\n')
        with open(fname, 'r') as f:
            lines = f.readlines()
            start, end = locate_text(lines, '/* '+sign+' */', '/* end of '+sign+' */')
            
            keys, grouped_data = group_text(data)
            for key in keys:
                for i in range(len(grouped_data[key])):
                    if grouped_data[key][i][3] == 'grid':
                        content.append('  svector *' + grouped_data[key][i][0] + ';  // ' + grouped_data[key][i][2] + '\n')
                    if grouped_data[key][i][4] == 'spatial_TS':
                        content.append('  ifstream if_' + grouped_data[key][i][0] + ';  // ' + grouped_data[key][i][2] + '\n')         
            content = lines[:start] + content + lines[end:]
        
        if(('').join(content) != ('').join(lines)):
            with open(fname, 'w') as f:
                f.writelines(content)
    

def atmos_read_climate_maps(fname, signs, datas):

    for j in range(len(signs)):
        sign = signs[j]
        data = datas[j] 
        with open(fname, 'r') as f:
            lines = f.readlines()
            start, end = locate_text(lines, 'int Atmosphere::open_climate(Control &ctrl)', 'int Atmosphere::read_climate(Control &ctrl)')
            end -= 3
            content = []
            keys, grouped_data = group_text(data)
            for key in keys:
                text = ['  open_climate_maps(ctrl.path_ClimateFolder + ctrl.fn_' + grouped_data[key][i][0] + ', if_' + grouped_data[key][i][0] + ');\n' for i in range(len(grouped_data[key]))]
                content.append(if_condition_build(key, text))               
            content = lines[:start] + content + lines[end:]
        if(('').join(content) != ('').join(lines)):
            with open(fname, 'w') as f:
                f.writelines(content)
    
    for j in range(len(signs)):
        sign = signs[j]
        data = datas[j] 
        with open(fname, 'r') as f:
            lines = f.readlines()
            start, end = locate_text(lines, 'int Atmosphere::read_climate(Control &ctrl)', 'int Atmosphere::open_climate_maps(string fname, ifstream &ifHandle)')
            end -= 3
            content = []
            keys, grouped_data = group_text(data)
            for key in keys:
                text = ['  read_climate_maps(if_' + grouped_data[key][i][0] + ', *' + grouped_data[key][i][0] + ');\n' for i in range(len(grouped_data[key]))]
                content.append(if_condition_build(key, text))               
            content = lines[:start] + content + lines[end:]
        if(('').join(content) != ('').join(lines)):
            with open(fname, 'w') as f:
                f.writelines(content)
    
    for j in range(len(signs)):
        sign = signs[j]
        data = datas[j] 
        with open(fname, 'r') as f:
            lines = f.readlines()
            start, end = locate_text(lines, 'int Atmosphere::init_climate(Control &ctrl)', 'int Atmosphere::update_climate(Control &ctrl)')
            end -= 3
            content = []
            keys, grouped_data = group_text(data)
            for key in keys:
                text = ['  init_climate_maps(ctrl.path_ClimateFolder + ctrl.fn_' + grouped_data[key][i][0] + ', if_' + grouped_data[key][i][0] + ');\n' for i in range(len(grouped_data[key]))]
                content.append(if_condition_build(key, text))               
            content = lines[:start] + content + lines[end:]
        if(('').join(content) != ('').join(lines)):
            with open(fname, 'w') as f:
                f.writelines(content)

    for j in range(len(signs)):
        sign = signs[j]
        data = datas[j] 
        with open(fname, 'r') as f:
            lines = f.readlines()
            start, end = locate_text(lines, 'int Atmosphere::update_climate(Control &ctrl)', 'int Atmosphere::init_climate_maps(string fname, ifstream &ifHandle)')
            end -= 3
            content = []
            keys, grouped_data = group_text(data)
            for key in keys:
                text = ['  update_climate_maps(if_' + grouped_data[key][i][0] + ', *' + grouped_data[key][i][0] + ');\n' for i in range(len(grouped_data[key]))]
                content.append(if_condition_build(key, text))               
            content = lines[:start] + content + lines[end:]
        if(('').join(content) != ('').join(lines)):
            with open(fname, 'w') as f:
                f.writelines(content)

def basin_read_groundTs_maps(fname, signs, datas):

    for j in range(len(signs)):
        sign = signs[j]
        data = datas[j] 
        with open(fname, 'r') as f:
            lines = f.readlines()
            start, end = locate_text(lines, 'int Basin::open_groundTs(Control &ctrl)', 'int Basin::read_groundTs(Control &ctrl)')
            end -= 3
            content = []
            keys, grouped_data = group_text(data)
            for key in keys:
                text = ['  open_groundTs_maps(ctrl.path_ClimateFolder + ctrl.fn_' + grouped_data[key][i][0] + ', if_' + grouped_data[key][i][0] + ');\n' for i in range(len(grouped_data[key]))]
                content.append(if_condition_build(key, text))               
            content = lines[:start] + content + lines[end:]
        if(('').join(content) != ('').join(lines)):
            with open(fname, 'w') as f:
                f.writelines(content)
    
    for j in range(len(signs)):
        sign = signs[j]
        data = datas[j] 
        with open(fname, 'r') as f:
            lines = f.readlines()
            start, end = locate_text(lines, 'int Basin::read_groundTs(Control &ctrl)', 'int Basin::open_groundTs_maps(string fname, ifstream &ifHandle)')
            end -= 3
            content = []
            keys, grouped_data = group_text(data)
            for key in keys:
                text = ['  read_groundTs_maps(if_' + grouped_data[key][i][0] + ', *' + grouped_data[key][i][0] + ');\n' for i in range(len(grouped_data[key]))]
                content.append(if_condition_build(key, text))               
            content = lines[:start] + content + lines[end:]
        if(('').join(content) != ('').join(lines)):
            with open(fname, 'w') as f:
                f.writelines(content)
    
    for j in range(len(signs)):
        sign = signs[j]
        data = datas[j] 
        with open(fname, 'r') as f:
            lines = f.readlines()
            start, end = locate_text(lines, 'int Basin::init_groundTs(Control &ctrl)', 'int Basin::update_groundTs(Control &ctrl, Param &par)')
            end -= 3
            content = []
            keys, grouped_data = group_text(data)
            for key in keys:
                text = ['  init_groundTs_maps(ctrl.path_ClimateFolder + ctrl.fn_' + grouped_data[key][i][0] + ', if_' + grouped_data[key][i][0] + ');\n' for i in range(len(grouped_data[key]))]
                content.append(if_condition_build(key, text))               
            content = lines[:start] + content + lines[end:]
        if(('').join(content) != ('').join(lines)):
            with open(fname, 'w') as f:
                f.writelines(content)

    for j in range(len(signs)):
        sign = signs[j]
        data = datas[j] 
        with open(fname, 'r') as f:
            lines = f.readlines()
            start, end = locate_text(lines, 'int Basin::update_groundTs(Control &ctrl, Param &par)', 'int Basin::init_groundTs_maps(string fname, ifstream &ifHandle)')
            end -= 3
            content = []
            keys, grouped_data = group_text(data)
            for key in keys:
                text = ['  update_groundTs_maps(if_' + grouped_data[key][i][0] + ', par, *' + grouped_data[key][i][0] + ');\n' for i in range(len(grouped_data[key]))]
                content.append(if_condition_build(key, text))               
            content = lines[:start] + content + lines[end:]
        if(('').join(content) != ('').join(lines)):
            with open(fname, 'w') as f:
                f.writelines(content)

def basin_includes(fname, signs, datas):
    for j in range(len(signs)):
        sign = signs[j]
        Contents = datas[j] 
        with open(fname, 'r') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                if '/* '+sign+' */' in lines[i]:
                    start = i + 1
                if '/* end of '+sign+' */' in lines[i]:
                    end = i
            content = []
               
            for i in range(len(Contents)):
                if Contents[i][1] == 0:
                    if Contents[i][3] == 'grid':
                        content.append('  '+Contents[i][3]+' *' + Contents[i][0] + ';  // ' + Contents[i][2] + '\n')
                    else:
                        content.append('  '+Contents[i][3]+' ' + Contents[i][0] + ';  // ' + Contents[i][2] + '\n')
            content = lines[:start] + content + lines[end:]

        if(('').join(content) != ('').join(lines)):  
            with open(fname, 'w') as f:
                f.writelines(content)

def destructor(fname, signs, datas):
    for j in range(len(signs)):
        sign = signs[j]
        data = datas[j] 
        with open(fname, 'r') as f:
            lines = f.readlines()
            start, end = locate_text(lines, '/* '+sign+' */', '/* end of '+sign+' */')
            content = []
            keys, grouped_data = group_text(data)
            for key in keys:
                text = []
                for i in range(len(grouped_data[key])):                  
                    if grouped_data[key][i][4] == 'spatial_TS':
                        text.append('  if (if_'+grouped_data[key][i][0]+'.is_open())  if_'+grouped_data[key][i][0]+'.close();\n')  
                    if grouped_data[key][i][3] == 'grid' or grouped_data[key][i][3] == 'grid_param':
                        text.append('  if('+grouped_data[key][i][0]+') delete '+grouped_data[key][i][0]+';\n')

                content.append(if_condition_build(key, text))              
            content = lines[:start] + content + lines[end:]
        if(('').join(content) != ('').join(lines)):
            with open(fname, 'w') as f:
                f.writelines(content)


def report_destructor(fname, reports):
        sign = 'Report'
        data = reports 
        with open(fname, 'r') as f:
            lines = f.readlines()
            start, end = locate_text(lines, '/* '+sign+' */', '/* end of '+sign+' */')
            content = []
            for i in range(len(data)):
                if data[i][5]!=None and data[i][6]==1:
                    content.append('  if (of_'+data[i][0]+'.is_open())  of_'+data[i][0]+'.close();\n')
            for i in range(len(data)):
                if data[i][5]!=None and data[i][6]==1:
                    content.append('  if (ctrl.report_'+data[i][0]+'==2) delete '+data[i][0]+'_acc;\n')
                    
          
            content = lines[:start] + content + lines[end:]
        if(('').join(content) != ('').join(lines)):
            with open(fname, 'w') as f:
                f.writelines(content)


def constructor(fname, signs, datas):
    for j in range(len(signs)):
        sign = signs[j]
        data = datas[j]
        
        content = []
        

        with open(fname, 'r') as f:
            lines = f.readlines()
            start, end = locate_text(lines, '/* '+sign+' */', '/* end of '+sign+' */')
            
            keys, grouped_data = group_text(data)
            for key in keys:
                text = []
                for i in range(len(grouped_data[key])):                  
                    if grouped_data[key][i][4] == 'new' or grouped_data[key][i][4] == 'spatial_TS' or grouped_data[key][i][4] == 'spatial_param':
                        text.append('  '+grouped_data[key][i][0]+' = new svector(_sortedGrid.size);\n')  
                    if grouped_data[key][i][4] == 'spatial':
                        text.append('  '+grouped_data[key][i][0]+' = new svector(ctrl.path_BasinFolder + ctrl.fn_'+grouped_data[key][i][0]+', _rowNum, _colNum, _sortedGrid);\n')  
                content.append(if_condition_build(key, text))
            content = lines[:start] + content + lines[end:]
        if(('').join(content) != ('').join(lines)):
            with open(fname, 'w') as f:
                f.writelines(content)  

def report_includes(fname, reports):
    with open(fname, 'r') as f:
    
        lines = f.readlines()
        start, end = locate_text(lines, '/* Report */', '/* end of Report */')
        content = []
        for i in range(len(reports)):
            if reports[i][5]!=None:
                content.append('    ofstream of_' + reports[i][0] + ';  // ' + reports[i][2] + '\n')
        content.append('\n')
        for i in range(len(reports)):
            if reports[i][5]!=None:
                content.append('    svector *' + reports[i][0] + '_acc;  // ' + reports[i][2] + '\n')
        content = lines[:start] + content + lines[end:]

    if(('').join(content) != ('').join(lines)):
        with open(fname, 'w') as f:
                f.writelines(content)

def control_includes(fname, options, signs, datas, reports, static_config=False):
    with open(fname, 'r') as f:
        lines = f.readlines()
        start, end = locate_text(lines, '/* Options */', '/* end of Options */')

        content = []

        opt_list = []
        for key in options.keys():
            item = options.get(key)
            if item['key'] is None:
                continue
            if not item['key'] in opt_list:
                opt_list.append(item['key'])
                content.append('  // ' + item['general_description'].replace('#', '  //') + '\n')
                if static_config:
                    content.append('  static constexpr int ' + item['key'] + ' = ' + str(item['value']) +';\n')
                else:
                    content.append('  int ' + item['key'] + ';\n')

        content = lines[:start] + content + lines[end:]
    if(('').join(content) != ('').join(lines)):
        with open(fname, 'w') as f:
                f.writelines(content)


    for j in range(len(signs)):
        sign = signs[j]
        Contents = []
        for data in (datas[j]):

            if 'spatial' in data[4]:
                Contents.append(data)
        with open(fname, 'r') as f:
            lines = f.readlines()
            start, end = locate_text(lines, '/* '+sign+' */', '/* end of '+sign+' */')            
            content = []          
            for i in range(len(Contents)):
                content.append('  string fn_'+Contents[i][0]+';  // '+Contents[i][2] +'\n')
            content = lines[:start] + content + lines[end:]
        if(('').join(content) != ('').join(lines)):
            with open(fname, 'w') as f:
                f.writelines(content)
        
    with open(fname, 'r') as f:
        lines = f.readlines()
        start, end = locate_text(lines, '/* Report */', '/* end of Report */')
        content = []
        content.append('  // 1: report time series at gauging stations; 2: report maps\n')        
        for i in range(len(reports)):
            if reports[i][5] is not None and reports[i][6] == 1:
                content.append('  int report_'+reports[i][0]+';  // report '+reports[i][2]+'\n')
        
        content = lines[:start] + content + lines[end:]
    if(('').join(content) != ('').join(lines)):
        with open(fname, 'w') as f:
            f.writelines(content)
