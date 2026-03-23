[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16730652.svg)](https://doi.org/10.5281/zenodo.16730652)
![Visitors Badge](https://visitor-badge.laobi.icu/badge?page_id=RuiGao9.LWP_Vineyard_Features)<br>

## Feature Extraction from the High-resolution AggieAir Images for Leaf Water Potential Estimation in California Vineyards
This repository and another one ([LWP_Mapping_sUAS_California](https://github.com/RuiGao9/LWP_Mapping_sUAS_California)) support a peer-reviewed journal paper published in *Irrigation Science* (A machine learning framework for California vineyard water status monitoring using sUAS Imagery and short-term meteorological data) showing a simplified model for California vineyard leaf water potential mapping. A subtitle or the main title is below.<br>
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

## Reference
Gao, R., Alsina, M. M., Torres-Rua, A. F., Hipps, L., Kustas, W. P., Anderson, M., ... & Dokoozlian, N. (2026). A machine learning framework for California vineyard water status monitoring using sUAS Imagery and short-term meteorological data. Irrigation Science, 44(3), 60.<br>
Gao, R., Torres-Rua, A., & Alsina, M. M. (2025). A Simplified Model for California Grapevine Leaf Water Potential Mapping at the Field Scale Based on a Machine Learning Approach (v0.0.1). Zenodo. https://doi.org/10.5281/zenodo.15885590
Gao, R., & Torres-Rua, A. (2025). Feature Extraction from the High-resolution AggieAir Images for Leaf Water Potential Estimation in California Vineyards (Initial). Zenodo. https://doi.org/10.5281/zenodo.16730652

## Citation 
If you use this repository in your work, please consider following reference/DOIs:<br>

**BibTeX:**
```bibtex
@misc{gao2025lwpis,
  author       = {Rui Gao, Maria Mar Alsina, Alfonso Torres-Rua, Lawrence Hipps, William P. Kustas, Martha Anderson, Héctor Nieto, Andrew J. McElrone, Kyle Knipper, Nicolas Bambach Ortiz, Sebastian J. Castro, John H. Prueger, Joseph Alfieri, Lynn G McKee, William A. White, Feng Gao, Calvin Coopmans, Ian Gowing, Nurit Agam, Luis Sanchez, Nick Dokoozlian},
  title        = {A machine learning framework for California vineyard water status monitoring using sUAS imagery and short-term meteorological data},
  year         = {2026},
  publisher    = {Irrigation Science},
  doi          = {https://doi.org/10.1007/s00271-026-01102-8},
  url          = {https://link.springer.com/article/10.1007/s00271-026-01102-8}
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

## Contact info
Rui.Ray.Gao@Gmail.com<br>
RuiGao@USU.edu<br>
RuiGao@UCMerced.edu
