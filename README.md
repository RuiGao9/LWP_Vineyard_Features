[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16730652.svg)](https://doi.org/10.5281/zenodo.16730652)
![Visitors Badge](https://visitor-badge.laobi.icu/badge?page_id=RuiGao9.LWP_Vineyard_Features)<br>
# LWP_Vineyard_Features
This repository and another one ([LWP_Mapping_sUAS_California](https://github.com/RuiGao9/LWP_Mapping_sUAS_California)) support a peer-reviewed journal paper (Integrating Time-Series Meteorological Data and sUAS Information into a Machine Learning Framework for California Vineyard Water Stress Monitoring) showing a simplified model for California vineyard leaf water potential mapping. A subtitle or the main title is below.<br>
In this repository, we provided:
1. `INput_data`, a folder contains demo data. `Demo_INput_TIR.tif` is the temperature image (in Celsius) obtained from the AggieAir sUAS. `Demo_Input_VNIR.tif` is the multi-spectral image (red, green, blue, and near-infrared).
2. `main_program.ipynb` is the main program, which is a simplifed model from the research **Integrating Time-Series Meteorological Data and sUAS Information into a Machine Learning Framework for California Vineyard Water Stress Monitoring**.
3. `xgb_tt.pkl` is the trained machine learning model (using the XGBoost approach). The required inputs are listed in the research paper, and we also list them below.
   - , air temperature in Celsius at 2 m above ground level.
   - , canopy temperature in Celsius.

## Feature Extraction from the High-resolution AggieAir Images for Leaf Water Potential Estimation in California Vineyards

<p align="center">Rui Gao<sup>1,2,3</sup>, Alfonso Torres-Rua<sup>1</sup></p>
<sup>1</sup>Department of Civil and Environmental Engineering, Utah State University, Logan, UT 84321, USA<br>
<sup>2</sup>Department of Civil and Environmental Engineering, University of California, Merced, CA 95343, USA<br>
<sup>3</sup>Valley Institute for Sustainable Technology & Agriculture, University of California, Merced, CA 95343, USA<br>

## Citation 
If you use this repository in your work, please cite following DOIs:<br>
[![DOI](https://zenodo.org/badge/DOI/10.1007/s00271-022-00776-0.svg)](https://doi.org/10.1007/s00271-022-00776-0)<br>
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16730652.svg)](https://doi.org/10.5281/zenodo.16730652)<br>
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15885589.svg)](https://doi.org/10.5281/zenodo.15885589)

**BibTeX:**
```bibtex
@misc{gao2025lwpis,
  author       = {Rui Gao, Mimar, Alfonso Torres-Rua},
  title        = {Integrating Time-Series Meteorological Data and sUAS Information into a Machine Learning Framework for California Vineyard Water Stress Monitoring},
  year         = {2025},
  publisher    = {Irrigation Science},
  doi          = {10.XXXXXXX},
  url          = {https://doi.org/10.XXXXXXX}
}
```
```
@misc{gao2025lwpfeature,
  author       = {Rui Gao, Alfonso Torres-Rua},
  title        = {Feature Extraction From the High-resolution AggieAir Images for Leaf Water Potential Estimation in California Vineyards},
  year         = {2025},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.16730652},
  url          = {https://doi.org/10.5281/zenodo.16730652}
}
```
```bibtex
@misc{gao2025lwpmap,
  author       = {Rui Gao, Alfonso Torres-Rua},
  title        = {A Simplified Model for California Grapevine Leaf Water Potential Mapping at the Field Scale Based on a Machine Learning Approach},
  year         = {2025},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.15885589},
  url          = {https://doi.org/10.5281/zenodo.15885589}
}
```

## Contact info
Rui.Ray.Gao@Gmail.com<br>
RuiGao@USU.edu<br>
RuiGao@UCMerced.edu
