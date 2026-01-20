[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16730652.svg)](https://doi.org/10.5281/zenodo.16730652)
![Visitors Badge](https://visitor-badge.laobi.icu/badge?page_id=RuiGao9.LWP_Vineyard_Features)<br>

# LWP_Vineyard_Features
This repository and another one ([LWP_Mapping_sUAS_California](https://github.com/RuiGao9/LWP_Mapping_sUAS_California)) support a peer-reviewed journal paper (A Machine Learning Framework for California Vineyard Water Status Monitoring Using sUAS Imagery and Meteorological Time Series from the Prior 24 Hours) showing a simplified model for California vineyard leaf water potential mapping. A subtitle or the main title is below.<br>
In this repository, we provided:
- `1_Data`, a folder contains materials that support running the Python program.<br>
  - This folder contains three images: (1) “Demo_DSM.tif” is the digital surface model data with 0.15 m resolution in the unit of meter. (2) “Demo_RGBNIR.tif” is the spectral image with red, green, blue, and near-infrared bands at 0.15 m resolution and a value range between 0 and 10,000; and (3) “Demo_TIR.tif” is the thermal image with 0.60 m resolution in the unit of degrees Celsius (Cº).
  - This folder contains two shapefiles. (1) “Area.shp” is a mask file highlighting the working area. (2) “Points.shp” is a point file, and the distance between each adjacent point is 0.6 m. The coordinates, latitude (Lat) and longitude (Lon), are required to include in this file.
- `2_Scripts`, a folder contains two files.  
  - `Function_Package.py` is a function package containing all functions needed by the main Python program.
  - `main.ipynb` is the primary notebook that specifies where the input data are located and calls the functions defined in `Functions_Package.py` are located. Each parameter is documented within the Python program.

- `3_Results` <br>
Among all the results, the “CSV” file is the final result containing coordinates and the seventeen features. Other images and shapefiles are the intermediate products that can be ignored. “DF20150602_1041.csv” is the final result for this demo project. These variables are:
  - DSM: digitial surface model data (elevation, m);
  - R: reflectance in the red band;
  - G: reflectance in the green band;
  - B: reflectance in the blue band;
  - NIR: reflectance in the near-infrared band;
  - NDVI: normalized difference vegetation index calculated based on the NIR and R bands;
  - CIg: green chlorophyll index calculated based on the NIR and G bands;
  - MSAVI: modified soil adjusted vegetation index calculated based on the NIR and R bands;
  - MTVI2: modified triangular vegetation index calculated based on the NIR, R, and G bands;
  - NDWI: normalized difference water index calculated based on the NIR and G bands;
  - EVI: enhanced vegetation index calculated based on the NIR, R, and B bands;
  - GNDVI: green normalized difference vegetation index calculated based on the NIR and G bands;
  IronOxide: iron oxide ratio calculated based on the R and B bands;
  - SAVI: soil adjusted vegetation index calculated based on the NIR and R bands;
  - SR: simple ratio calculated based on the NIR and R bands;
  - VARI: visible atmospherically resistant index calculated based on the R, G, and B bands;
  - Tr: temperature from the thermal band (Celsius);

## Feature Extraction from the High-resolution AggieAir Images for Leaf Water Potential Estimation in California Vineyards

<p align="center">Rui Gao<sup>1,2,3</sup>, Alfonso Torres-Rua<sup>1</sup></p>
<sup>1</sup>Department of Civil and Environmental Engineering, Utah State University, Logan, UT 84321, USA<br>
<sup>2</sup>Department of Civil and Environmental Engineering, University of California, Merced, CA 95343, USA<br>
<sup>3</sup>Valley Institute for Sustainable Technology & Agriculture, University of California, Merced, CA 95343, USA<br>

## Citation 
If you use this repository in your work, please consider following reference/DOIs:<br>
[![DOI](https://zenodo.org/badge/DOI/10.21203/rs.3.rs-7952103/v1.svg)](https://doi.org/10.21203/rs.3.rs-7952103/v1)<br>
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16730652.svg)](https://doi.org/10.5281/zenodo.16730652)<br>
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15885589.svg)](https://doi.org/10.5281/zenodo.15885589)<br>
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18305013.svg)](https://doi.org/10.5281/zenodo.18305013)

**BibTeX:**
```bibtex
@misc{gao2025lwpis,
  author       = {Rui Gao, Mimar, Alfonso Torres-Rua},
  title        = {Integrating Time-Series Meteorological Data and sUAS Information into a Machine Learning Framework for California Vineyard Water Stress Monitoring},
  year         = {2025},
  publisher    = {Irrigation Science},
  doi          = {10.21203/rs.3.rs-7952103/v1},
  url          = {https://doi.org/10.21203/rs.3.rs-7952103/v1}
  doi          = {10.21203/rs.3.rs-7952103/v1},
  url          = {https://doi.org/10.21203/rs.3.rs-7952103/v1}
}
```
```bibtex
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
  author       = {Rui Gao, Alfonso Torres-Rua, Maria Mar Alsina},
  title        = {A Simplified Model for California Grapevine Leaf Water Potential Mapping at the Field Scale Based on a Machine Learning Approach},
  year         = {2025},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.15885589},
  url          = {https://doi.org/10.5281/zenodo.15885589}
}
```
```bibtex
@misc{gao2026windex,
  author       = {Rui Gao, Alfonso Torres-Rua, Mohammad Safeeq, and Joshua H. Viers},
  title        = {A Python Tool for Winkler Index Calculation based on Hourly Air Temperature Records},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.18305013},
  url          = {https://doi.org/10.5281/zenodo.18305013}
}
```

## Contact info
Rui.Ray.Gao@Gmail.com<br>
RuiGao@USU.edu<br>
RuiGao@UCMerced.edu
