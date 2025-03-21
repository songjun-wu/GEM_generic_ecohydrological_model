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
  readIntoParam(snow_rain_thre, "snow_rain_thre", lines);
  readIntoParam(deg_day_min, "deg_day_min", lines);
  readIntoParam(deg_day_max, "deg_day_max", lines);
  readIntoParam(deg_day_increase, "deg_day_increase", lines);
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

