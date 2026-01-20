import arcpy
import arcview
import rasterio
import numpy as np
import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

    
def TellTheGeoInfo(InputRaster):
    """
    parameter InputRaster: input image
    return:
      1) dims (rows, cols)
      2) transform (rasterio.Affine)
      3) crs (rasterio CRS object; or None)
    """
    with rasterio.open(InputRaster) as src:
        band1 = src.read(1)
        dims = band1.shape  # (rows, cols)
        print("Dimension of the data is:", dims[0], dims[1])

        transform = src.transform
        crs = src.crs

    return dims, transform, crs
    
def TellExtent(InputFile):
    '''
    parameter InputFile: input could be Shpfile or image file
    return: the coordinates of the extent, 4 values
    '''
    
    Grid_Describe = arcpy.Describe(InputFile)
    Grid_Extent = Grid_Describe.extent
    ExtentShpfile = "{} {} {} {}".format(Grid_Extent.XMin, Grid_Extent.YMin, Grid_Extent.XMax, Grid_Extent.YMax)
    print("The extent is: " + ExtentShpfile)
    return(ExtentShpfile)
    
def TellResolution(Raster_File):
    '''
    To know the resolution of the raster file.
    :param Raster_File: put the raster file inside
    :return: the resolution (x,y) will be shown
    '''

    rastersize_x = arcpy.GetRasterProperties_management(Raster_File, "CELLSIZEX")
    rastersize_y = arcpy.GetRasterProperties_management(Raster_File, "CELLSIZEY")
    rastersize_x = round(float(rastersize_x.getOutput(0)), 3)
    rastersize_y = round(float(rastersize_y.getOutput(0)), 3)
    print("The horizontal resolution is " + str(rastersize_x) + "m and the vertical resolution is " + str(
        rastersize_y) + "m.")
    return (rastersize_x, rastersize_y)


def WriteTiffData(folder_out, name_out_file, ysize, xsize, Array_Content, transform, crs, nodata=None):
    """
    Writing the array with geographic information (GeoTIFF).
    :param floder_out: directory that you wish to save this output
    :param name_out_file: a name for the output, like "Result"
    :param ysize: dimension on y
    :param xsize: dimension on x
    :param Array_Content: the array that you wish to save in the Tiff file
    :param geotransform: geotransform information
    :param projection: projection information
    :return: no return on screen, but an output in the folder
    """
    out_path = os.path.join(folder_out, name_out_file)

    arr = np.asarray(Array_Content)
    if arr.shape != (ysize, xsize):
        raise ValueError(f"Array shape {arr.shape} does not match (ysize,xsize)=({ysize},{xsize}).")

    profile = {
        "driver": "GTiff",
        "height": ysize,
        "width": xsize,
        "count": 1,
        "dtype": "float32",
        "transform": transform,
        "crs": crs,
    }
    if nodata is not None:
        profile["nodata"] = nodata

    with rasterio.open(out_path, "w", **profile) as dst:
        dst.write(arr.astype("float32"), 1)

    print("Done!!! Tiff data has been written:", out_path)

    
def FolderCreater(path):
    '''
    Create a new folder    
    path: for example (path = r'D:\Example\Folder_1')
    '''
    
    if not os.path.exists(path):
        os.makedirs(path)

def Extreme_Value_TIF_Limited_Area(file_input_raster,file_mask,dir_output):
    '''
    Obtaining the maximum and minimum values from the raster data within the research area.
    :param file_input_raster: raster data (.tif)
    :param file_mask: interesting research area (.shp)
    :param dir_output: a folder where to save results
    :return: maximum and minimum values
    '''
    import arcpy
    import os
    import numpy as np
    arcpy.env.overwriteOutput = True

    out_tmp = arcpy.sa.ExtractByMask(file_input_raster,file_mask)
    out_tmp.save(dir_output+"\\tmp_extract.tif")
    raster_tmp = arcpy.RasterToNumPyArray(dir_output+"\\tmp_extract.tif",nodata_to_value=np.nan)
    print("The maximum value is:",round(np.nanmax(raster_tmp),2),"| The minimum value is:",round(np.nanmin(raster_tmp),2))
    
    return(round(np.nanmax(raster_tmp),2),round(np.nanmin(raster_tmp),2))
    
def Raster_Value_To_Points(file_points,file_raster,file_output):
    '''
    Extract raster values to points.
    :param file_points: a shapefile (points)
    :param file_raster: a raster image 
    :param file_output: a shapefile path (including folder path and shapefile name)
    :return: nothing
    '''
    import arcpy
    import os
    import numpy as np
    arcpy.env.overwriteOutput = True
    
    arcpy.sa.ExtractValuesToPoints(file_points, 
                                   file_raster, 
                                   file_output, 
                                   "NONE", "ALL")
    
    return

def Features_To_Points(file_dsm,file_rgb,file_tr,file_mask,file_points,
                       dir_output,
                       dir_table_output,
                       file_number,resolution_high,resolution_low,
                       threshold_ndvi,
                       l_SAVI,
                       NoDataValue):
    import arcpy
    arcpy.CheckOutExtension("Spatial")
    arcpy.CheckOutExtension("3D")
    import os
    import numpy as np
    import geopandas as gpd
    import pandas as pd
    from matplotlib import pyplot as plt
    import Functions_Package as fp
    import datetime
    import time
    import rasterio

    arcpy.env.overwriteOutput = True
    
    ## Align images
    ### 1. Resample images
    #(1) The resolution of optical and DSM images is 0.15 m;<br>
    #(2) The resolution of thermal images is 0.6 m.
    ### 2. Align images
    #Thermal images are the target.

    # 1. Resample images
    # DSM to 0.15 m
    # Optical to 0.15 m
    # Thermal to 0.6 m

    # DSM
    [res_x,res_y] = TellResolution(file_dsm)
    resample_dsm = "res_dsm_"+file_number+".tif"
    res_resample_high = str(resolution_high)+" "+str(resolution_high)
    arcpy.management.Resample(file_dsm, 
                              dir_output+"\\"+resample_dsm, 
                              res_resample_high, 
                              "CUBIC")

    # RGBNIR
    [res_x,res_y] = TellResolution(file_rgb)
    resample_rgb = "res_rgb_"+file_number+".tif"
    arcpy.management.Resample(file_rgb, 
                              dir_output+"\\"+resample_rgb, 
                              res_resample_high, 
                              "CUBIC")

    # Thermal
    [res_x,res_y] = TellResolution(file_tr)
    resample_tr = "res_tr_"+file_number+".tif"
    res_resample_low = str(resolution_low)+" "+str(resolution_low)
    arcpy.management.Resample(file_tr, 
                              dir_output+"\\"+resample_tr, 
                              res_resample_low, 
                              "CUBIC")

    # Thermal image is the target
    # Gain the coordinates of the shapefile
    Grid_Describe = arcpy.Describe(dir_output+"\\"+resample_tr)
    Grid_Extent = Grid_Describe.extent
    ExtentShpfile = "{} {} {} {}".format(Grid_Extent.XMin, Grid_Extent.YMin, Grid_Extent.XMax, Grid_Extent.YMax)

    # DSM
    clip_dsm = "clip_dsm_"+file_number+".tif"
    arcpy.management.Clip(dir_output+"\\"+resample_dsm, 
                          ExtentShpfile, 
                          dir_output+'\\'+clip_dsm, 
                          dir_output+'\\'+resample_tr, 
                          NoDataValue, "NONE", "MAINTAIN_EXTENT")
    # RGB
    clip_rgb = "clip_rgb_"+file_number+".tif"
    arcpy.management.Clip(dir_output+"\\"+resample_rgb, 
                          ExtentShpfile, 
                          dir_output+'\\'+clip_rgb, 
                          dir_output+'\\'+resample_tr, 
                          NoDataValue, "NONE", "MAINTAIN_EXTENT")

    # Delete middle products
    os.remove(dir_output+"\\"+resample_dsm)
    os.remove(dir_output+"\\"+resample_rgb)


    ## Obtain VIs
    #(1) Only focus on the vegetation pixel;<br>
    #(2) Based on the NDVI value (e.g., NDVI>0.75)
    # Obtain the geology info. from the spectral data: RGBNIR.tif
    [rgb_dims,rgb_img_geo,rgb_img_prj] = fp.TellTheGeoInfo(dir_output+'\\'+clip_rgb)
    extent_rgb = fp.TellExtent(dir_output+'\\'+clip_rgb)

    raster_rgb = arcpy.RasterToNumPyArray(dir_output+'\\'+clip_rgb,nodata_to_value=NoDataValue)
    [raster_r,raster_g,raster_b,raster_nir] = [raster_rgb[0,:,:],raster_rgb[1,:,:],
                                               raster_rgb[2,:,:],raster_rgb[3,:,:]]
    [tmp_r,tmp_g,tmp_b,tmp_nir] = [raster_r/10000,raster_g/10000,
                                   raster_b/10000,raster_nir/10000]

    stack = np.stack([tmp_r, tmp_g, tmp_b, tmp_nir], axis=0).astype("float32")  # (4, rows, cols)

    out_path = os.path.join(dir_output, f"RGBNs_{file_number}.tif")
    with rasterio.open(
        out_path,
        "w",
        driver="GTiff",
        height=rgb_dims[0],
        width=rgb_dims[1],
        count=4,
        dtype="float32",
        transform=rgb_img_geo,   # now rasterio transform
        crs=rgb_img_prj          # now rasterio CRS
    ) as dst:
        dst.write(stack)

    # 1. Obtaining NDVI at 0.15 m scale
    NDVI_raster = arcpy.ia.NDVI(dir_output+"\\RGBNs_"+file_number+".tif", 4, 1)
    NDVI_raster.save(dir_output+"\\vi_"+file_number+"_NDVI.tif")
    # 2. Eliminating NDVI pixels who are smaller than a threshold
    raster_ndvi = arcpy.RasterToNumPyArray(dir_output+"\\vi_"+file_number+"_NDVI.tif", nodata_to_value=NoDataValue)
    raster_ndvi[raster_ndvi<threshold_ndvi] = np.nan
    # 3. Classify the NDVI image into two groups, vegetation and non-vegetation
    cl_ndvi = raster_ndvi.copy()
    cl_ndvi[cl_ndvi>0] = 1
    cl_ndvi[cl_ndvi<1] = 0
    # 4. Export the classification map
    fp.WriteTiffData(dir_output, "cls_"+file_number+"_NDVI.tif", rgb_dims[0], rgb_dims[1], cl_ndvi, rgb_img_geo, rgb_img_prj)
    # 5. Only focus on the VI within the valid pixels
    final_vi_ndvi = raster_ndvi*cl_ndvi
    final_vi_ndvi[final_vi_ndvi<0] = np.nan
    fp.WriteTiffData(dir_output, "tmp_vi_"+file_number+"_NDVI.tif", rgb_dims[0], rgb_dims[1], final_vi_ndvi, rgb_img_geo, rgb_img_prj)
    # 6. Resample to 0.6 m scale
    tmp_ndvi = arcpy.ia.Resample(dir_output+"\\"+"tmp_vi_"+file_number+"_NDVI.tif", "Average", resolution_high, resolution_low)
    tmp_ndvi.save(dir_output+"\\"+"vis_"+file_number+"_NDVI.tif")

    # 2. CIg
    # Calculate VI
    cig_raster = arcpy.ia.CIg(dir_output+"\\RGBNs_"+file_number+".tif", 4, 2)
    cig_raster.save(dir_output+"\\vi_"+file_number+"_CIg.tif")
    raster_cig = arcpy.RasterToNumPyArray(dir_output+"\\vi_"+file_number+"_CIg.tif", nodata_to_value=NoDataValue)
    # VI only for valid pixels
    final_vi_cig = raster_cig*cl_ndvi
    final_vi_cig[final_vi_cig<0] = np.nan
    # Export VI image at 0.15 m scale
    fp.WriteTiffData(dir_output, "tmp_vi_"+file_number+"_cig.tif", rgb_dims[0], rgb_dims[1], final_vi_ndvi, rgb_img_geo, rgb_img_prj)
    # Upscale to 0.6 m scale
    tmp_cig = arcpy.ia.Resample(dir_output+"\\"+"tmp_vi_"+file_number+"_CIg.tif", "Average", resolution_high, resolution_low)
    tmp_cig.save(dir_output+"\\"+"vis_"+file_number+"_CIg.tif")

    # 3. MSAVI
    # Calculate VI
    msavi_raster = arcpy.ia.MSAVI(dir_output+"\\RGBNs_"+file_number+".tif", 4, 1)
    msavi_raster.save(dir_output+"\\vi_"+file_number+"_MSAVI.tif")
    raster_msavi = arcpy.RasterToNumPyArray(dir_output+"\\vi_"+file_number+"_MSAVI.tif", nodata_to_value=NoDataValue)
    # VI only for valid pixels
    final_vi_msavi = raster_msavi*cl_ndvi
    final_vi_msavi[final_vi_msavi<0] = np.nan
    # Export VI image at 0.15 m scale
    fp.WriteTiffData(dir_output, "tmp_vi_"+file_number+"_MSAVI.tif", rgb_dims[0], rgb_dims[1], final_vi_msavi, rgb_img_geo, rgb_img_prj)
    # Upscale to 0.6 m scale
    tmp_msavi = arcpy.ia.Resample(dir_output+"\\"+"tmp_vi_"+file_number+"_MSAVI.tif", "Average", resolution_high, resolution_low)
    tmp_msavi.save(dir_output+"\\"+"vis_"+file_number+"_MSAVI.tif")

    # 4. MTVI2
    # Calculate VI
    mtvi2_raster = arcpy.ia.MTVI2(dir_output+"\\RGBNs_"+file_number+".tif", 4, 1, 2)
    mtvi2_raster.save(dir_output+"\\vi_"+file_number+"_MTVI2.tif")
    raster_mtvi2 = arcpy.RasterToNumPyArray(dir_output+"\\vi_"+file_number+"_MTVI2.tif", nodata_to_value=NoDataValue)
    # VI only for valid pixels
    final_vi_mtvi2 = raster_mtvi2*cl_ndvi
    final_vi_mtvi2[final_vi_mtvi2<0] = np.nan
    # Export VI image at 0.15 m scale
    fp.WriteTiffData(dir_output, "tmp_vi_"+file_number+"_MTVI2.tif", rgb_dims[0], rgb_dims[1], final_vi_mtvi2, rgb_img_geo, rgb_img_prj)
    # Upscale to 0.6 m scale
    tmp_mtvi2 = arcpy.ia.Resample(dir_output+"\\"+"tmp_vi_"+file_number+"_MTVI2.tif", "Average", resolution_high, resolution_low)
    tmp_mtvi2.save(dir_output+"\\"+"vis_"+file_number+"_MTVI2.tif")

    # 5. NDWI
    # Calculate VI
    ndwi_raster = arcpy.ia.NDWI(dir_output+"\\RGBNs_"+file_number+".tif", 4, 2)
    ndwi_raster.save(dir_output+"\\vi_"+file_number+"_NDWI.tif")
    raster_ndwi = arcpy.RasterToNumPyArray(dir_output+"\\vi_"+file_number+"_NDWI.tif", nodata_to_value=NoDataValue)
    # VI only for valid pixels
    final_vi_ndwi = raster_ndwi*cl_ndvi
    final_vi_ndwi[final_vi_ndwi<-100] = np.nan
    # Export VI image at 0.15 m scale
    fp.WriteTiffData(dir_output, "tmp_vi_"+file_number+"_NDWI.tif", rgb_dims[0], rgb_dims[1], final_vi_ndwi, rgb_img_geo, rgb_img_prj)
    # Upscale to 0.6 m scale
    tmp_ndwi = arcpy.ia.Resample(dir_output+"\\"+"tmp_vi_"+file_number+"_NDWI.tif", "Average", resolution_high, resolution_low)
    tmp_ndwi.save(dir_output+"\\"+"vis_"+file_number+"_NDWI.tif")

    # 6. EVI
    # Calculate VI
    evi_raster = arcpy.ia.EVI(dir_output+"\\RGBNs_"+file_number+".tif", 4, 1, 3)
    evi_raster.save(dir_output+"\\vi_"+file_number+"_EVI.tif")
    raster_evi = arcpy.RasterToNumPyArray(dir_output+"\\vi_"+file_number+"_EVI.tif", nodata_to_value=NoDataValue)
    # VI only for valid pixels
    final_vi_evi = raster_evi*cl_ndvi
    final_vi_evi[final_vi_evi<0] = np.nan
    # Export VI image at 0.15 m scale
    fp.WriteTiffData(dir_output, "tmp_vi_"+file_number+"_EVI.tif", rgb_dims[0], rgb_dims[1], final_vi_evi, rgb_img_geo, rgb_img_prj)
    # Upscale to 0.6 m scale
    tmp_evi = arcpy.ia.Resample(dir_output+"\\"+"tmp_vi_"+file_number+"_EVI.tif", "Average", resolution_high, resolution_low)
    tmp_evi.save(dir_output+"\\"+"vis_"+file_number+"_EVI.tif")

    # 7. GNDVI
    # Calculate VI
    gndvi_raster = arcpy.ia.GNDVI(dir_output+"\\RGBNs_"+file_number+".tif", 4, 2)
    gndvi_raster.save(dir_output+"\\vi_"+file_number+"_GNDVI.tif")
    raster_gndvi = arcpy.RasterToNumPyArray(dir_output+"\\vi_"+file_number+"_GNDVI.tif", nodata_to_value=NoDataValue)
    # VI only for valid pixels
    final_vi_gndvi = raster_gndvi*cl_ndvi
    final_vi_gndvi[final_vi_gndvi<0] = np.nan
    # Export VI image at 0.15 m scale
    fp.WriteTiffData(dir_output, "tmp_vi_"+file_number+"_GNDVI.tif", rgb_dims[0], rgb_dims[1], final_vi_gndvi, rgb_img_geo, rgb_img_prj)
    # Upscale to 0.6 m scale
    tmp_gndvi = arcpy.ia.Resample(dir_output+"\\"+"tmp_vi_"+file_number+"_GNDVI.tif", "Average", resolution_high, resolution_low)
    tmp_gndvi.save(dir_output+"\\"+"vis_"+file_number+"_GNDVI.tif")

    # 8. IronOxide
    # Calculate VI
    io_raster = arcpy.ia.IronOxide(dir_output+"\\RGBNs_"+file_number+".tif", 1, 3)
    io_raster.save(dir_output+"\\vi_"+file_number+"_IronOxide.tif")
    raster_io = arcpy.RasterToNumPyArray(dir_output+"\\vi_"+file_number+"_IronOxide.tif", nodata_to_value=NoDataValue)
    # VI only for valid pixels
    final_vi_io = raster_io*cl_ndvi
    final_vi_io[final_vi_io<0] = np.nan
    # Export VI image at 0.15 m scale
    fp.WriteTiffData(dir_output, "tmp_vi_"+file_number+"_IronOxide.tif", rgb_dims[0], rgb_dims[1], final_vi_io, rgb_img_geo, rgb_img_prj)
    # Upscale to 0.6 m scale
    tmp_io = arcpy.ia.Resample(dir_output+"\\"+"tmp_vi_"+file_number+"_IronOxide.tif", "Average", resolution_high, resolution_low)
    tmp_io.save(dir_output+"\\"+"vis_"+file_number+"_IronOxide.tif")

    # 9. SAVI
    # Calculate VI
    savi_raster = arcpy.ia.SAVI(dir_output+"\\RGBNs_"+file_number+".tif", 4, 1, l_SAVI)
    savi_raster.save(dir_output+"\\vi_"+file_number+"_SAVI.tif")
    raster_savi = arcpy.RasterToNumPyArray(dir_output+"\\vi_"+file_number+"_SAVI.tif", nodata_to_value=NoDataValue)
    # VI only for valid pixels
    final_vi_savi = raster_savi*cl_ndvi
    final_vi_savi[final_vi_savi<0] = np.nan
    # Export VI image at 0.15 m scale
    fp.WriteTiffData(dir_output, "tmp_vi_"+file_number+"_SAVI.tif", rgb_dims[0], rgb_dims[1], final_vi_savi, rgb_img_geo, rgb_img_prj)
    # Upscale to 0.6 m scale
    tmp_savi = arcpy.ia.Resample(dir_output+"\\"+"tmp_vi_"+file_number+"_SAVI.tif", "Average", resolution_high, resolution_low)
    tmp_savi.save(dir_output+"\\"+"vis_"+file_number+"_SAVI.tif")

    # 10. SR
    # Calculate VI
    sr_raster = arcpy.ia.SR(dir_output+"\\RGBNs_"+file_number+".tif", 4, 1)
    sr_raster.save(dir_output+"\\vi_"+file_number+"_SR.tif")
    raster_sr = arcpy.RasterToNumPyArray(dir_output+"\\vi_"+file_number+"_SR.tif", nodata_to_value=NoDataValue)
    # VI only for valid pixels
    final_vi_sr = raster_sr*cl_ndvi
    final_vi_sr[final_vi_sr<0] = np.nan
    # Export VI image at 0.15 m scale
    fp.WriteTiffData(dir_output, "tmp_vi_"+file_number+"_SR.tif", rgb_dims[0], rgb_dims[1], final_vi_sr, rgb_img_geo, rgb_img_prj)
    # Upscale to 0.6 m scale
    tmp_sr = arcpy.ia.Resample(dir_output+"\\"+"tmp_vi_"+file_number+"_SR.tif", "Average", resolution_high, resolution_low)
    tmp_sr.save(dir_output+"\\"+"vis_"+file_number+"_SR.tif")

    # 11. VARI
    # Calculate VI
    vari_raster = arcpy.ia.VARI(dir_output+"\\RGBNs_"+file_number+".tif", 1, 2, 3)
    vari_raster.save(dir_output+"\\vi_"+file_number+"_VARI.tif")
    raster_vari = arcpy.RasterToNumPyArray(dir_output+"\\vi_"+file_number+"_VARI.tif", nodata_to_value=NoDataValue)
    # VI only for valid pixels
    final_vi_vari = raster_vari*cl_ndvi
    final_vi_vari[final_vi_vari<-100] = np.nan
    # Export VI image at 0.15 m scale
    fp.WriteTiffData(dir_output, "tmp_vi_"+file_number+"_VARI.tif", rgb_dims[0], rgb_dims[1], final_vi_vari, rgb_img_geo, rgb_img_prj)
    # Upscale to 0.6 m scale
    tmp_vari = arcpy.ia.Resample(dir_output+"\\"+"tmp_vi_"+file_number+"_VARI.tif", "Average", resolution_high, resolution_low)
    tmp_vari.save(dir_output+"\\"+"vis_"+file_number+"_VARI.tif")


    ## DSM only for valid pixels
    # Obtain DSM only for valid pixels at 0.15 m
    raster_dsm = arcpy.RasterToNumPyArray(dir_output+"\\clip_dsm_"+file_number+".tif",nodata_to_value=NoDataValue)
    raster_dsm_tmp = raster_dsm*cl_ndvi
    raster_dsm_tmp[raster_dsm_tmp<=0] = np.nan
    # Export the DSM image at 0.15 m
    fp.WriteTiffData(dir_output, "tmp_"+file_number+"_DSM.tif", rgb_dims[0], rgb_dims[1], raster_dsm_tmp, rgb_img_geo, rgb_img_prj)
    # Resample to 0.6 m scale
    final_dsm = arcpy.ia.Resample(dir_output+"\\"+"tmp_"+file_number+"_DSM.tif", "Average", resolution_high, resolution_low)
    final_dsm.save(dir_output+"\\"+"DSM_"+file_number+".tif")


    ## RGBNIR only for valid pixels
    [tmp_r,tmp_g,tmp_b,tmp_nir] = [raster_r*cl_ndvi/10000,raster_g*cl_ndvi/10000,
                                   raster_b*cl_ndvi/10000,raster_nir*cl_ndvi/10000]
    # Write spectral images at 0.15 m
    fp.WriteTiffData(dir_output,"tmp_"+file_number+"_R.tif",rgb_dims[0],rgb_dims[1],tmp_r,rgb_img_geo,rgb_img_prj)
    fp.WriteTiffData(dir_output,"tmp_"+file_number+"_G.tif",rgb_dims[0],rgb_dims[1],tmp_g,rgb_img_geo,rgb_img_prj)
    fp.WriteTiffData(dir_output,"tmp_"+file_number+"_B.tif",rgb_dims[0],rgb_dims[1],tmp_b,rgb_img_geo,rgb_img_prj)
    fp.WriteTiffData(dir_output,"tmp_"+file_number+"_NIR.tif",rgb_dims[0],rgb_dims[1],tmp_nir,rgb_img_geo,rgb_img_prj)
    # Resample images at 0.6 m
    final_r = arcpy.ia.Resample(dir_output+"\\"+"tmp_"+file_number+"_R.tif", "Average", resolution_high, resolution_low)
    final_r.save(dir_output+"\\"+"R_"+file_number+".tif")
    final_g = arcpy.ia.Resample(dir_output+"\\"+"tmp_"+file_number+"_G.tif", "Average", resolution_high, resolution_low)
    final_g.save(dir_output+"\\"+"G_"+file_number+".tif")
    final_b = arcpy.ia.Resample(dir_output+"\\"+"tmp_"+file_number+"_B.tif", "Average", resolution_high, resolution_low)
    final_b.save(dir_output+"\\"+"B_"+file_number+".tif")
    final_nir = arcpy.ia.Resample(dir_output+"\\"+"tmp_"+file_number+"_NIR.tif", "Average", resolution_high, resolution_low)
    final_nir.save(dir_output+"\\"+"NIR_"+file_number+".tif")
    
    ## Temperature only for valid pixels
    # Geology info. for temperature image (0.6 m scale)
    [tr_dims,tr_img_geo,tr_img_prj] = fp.TellTheGeoInfo(dir_output+'\\'+resample_tr)
    extent_tr = fp.TellExtent(dir_output+'\\'+resample_tr)
    # Only valid pixels
    cl_raster = arcpy.RasterToNumPyArray(dir_output+"\\"+"vis_"+file_number+"_NDVI.tif",nodata_to_value=NoDataValue)
    cl_raster[cl_raster<=0] = 0
    cl_raster[cl_raster>0] = 1
    
    raster_tr = arcpy.RasterToNumPyArray(dir_output+"\\"+resample_tr,nodata_to_value=NoDataValue)
    raster_tr = raster_tr*cl_raster
    raster_tr[raster_tr<=0] = np.nan
    # Export the Tr image at 0.6 m
    fp.WriteTiffData(dir_output, "Tr_"+file_number+".tif", tr_dims[0], tr_dims[1], raster_tr, tr_img_geo, tr_img_prj)
    

    print("NDVI:")
    [tmp_max_ndvi,tmp_min_ndvi] = fp.Extreme_Value_TIF_Limited_Area(dir_output+"\\"+"vis_"+file_number+"_NDVI.tif",file_mask,dir_output)
    print("CIg:")
    [tmp_max_cig,tmp_min_cig] = fp.Extreme_Value_TIF_Limited_Area(dir_output+"\\"+"vis_"+file_number+"_CIg.tif",file_mask,dir_output)
    print("MSAVI:")
    [tmp_max_msavi,tmp_min_msavi] = fp.Extreme_Value_TIF_Limited_Area(dir_output+"\\"+"vis_"+file_number+"_MSAVI.tif",file_mask,dir_output)
    print("MTVI2:")
    [tmp_max_mtvi2,tmp_min_mtvi2] = fp.Extreme_Value_TIF_Limited_Area(dir_output+"\\"+"vis_"+file_number+"_MTVI2.tif",file_mask,dir_output)
    print("NDWI:")
    [tmp_max_ndwi,tmp_min_ndwi] = fp.Extreme_Value_TIF_Limited_Area(dir_output+"\\"+"vis_"+file_number+"_NDWI.tif",file_mask,dir_output)
    print("EVI:")
    [tmp_max_evi,tmp_min_evi] = fp.Extreme_Value_TIF_Limited_Area(dir_output+"\\"+"vis_"+file_number+"_EVI.tif",file_mask,dir_output)
    print("GNDVI:")
    [tmp_max_gndvi,tmp_min_gndvi] = fp.Extreme_Value_TIF_Limited_Area(dir_output+"\\"+"vis_"+file_number+"_GNDVI.tif",file_mask,dir_output)
    print("IronOxide:")
    [tmp_max_io,tmp_min_io] = fp.Extreme_Value_TIF_Limited_Area(dir_output+"\\"+"vis_"+file_number+"_IronOxide.tif",file_mask,dir_output)
    print("SAVI:")
    [tmp_max_savi,tmp_min_savi] = fp.Extreme_Value_TIF_Limited_Area(dir_output+"\\"+"vis_"+file_number+"_SAVI.tif",file_mask,dir_output)
    print("SR:")
    [tmp_max_sr,tmp_min_sr] = fp.Extreme_Value_TIF_Limited_Area(dir_output+"\\"+"vis_"+file_number+"_SR.tif",file_mask,dir_output)
    print("VARI:")
    [tmp_max_vari,tmp_min_vari] = fp.Extreme_Value_TIF_Limited_Area(dir_output+"\\"+"vis_"+file_number+"_VARI.tif",file_mask,dir_output)

    print("\nDSM:")
    [tmp_max_dsm,tmp_min_dsm] = fp.Extreme_Value_TIF_Limited_Area(dir_output+"\\"+"DSM_"+file_number+".tif",file_mask,dir_output)
    print("R:")
    [tmp_max_r,tmp_min_r] = fp.Extreme_Value_TIF_Limited_Area(dir_output+"\\"+"R_"+file_number+".tif",file_mask,dir_output)
    print("G:")
    [tmp_max_g,tmp_min_g] = fp.Extreme_Value_TIF_Limited_Area(dir_output+"\\"+"G_"+file_number+".tif",file_mask,dir_output)
    print("B:")
    [tmp_max_b,tmp_min_b] = fp.Extreme_Value_TIF_Limited_Area(dir_output+"\\"+"B_"+file_number+".tif",file_mask,dir_output)
    print("NIR:")
    [tmp_max_nir,tmp_min_nir] = fp.Extreme_Value_TIF_Limited_Area(dir_output+"\\"+"NIR_"+file_number+".tif",file_mask,dir_output)
    
    print("\nTr:")
    [tmp_max_tr,tmp_min_tr] = fp.Extreme_Value_TIF_Limited_Area(dir_output+"\\"+"Tr_"+file_number+".tif",file_mask,dir_output)


    # 2ND STAGE, ATTACH VALUES ON POINTS
    fp.Raster_Value_To_Points(file_points,dir_output+"\\"+"DSM_"+file_number+".tif",dir_output+"\\"+"SHP_"+file_number+"_1.shp")
    fp.Raster_Value_To_Points(file_points,dir_output+"\\"+"R_"+file_number+".tif",dir_output+"\\"+"SHP_"+file_number+"_2.shp")
    fp.Raster_Value_To_Points(file_points,dir_output+"\\"+"G_"+file_number+".tif",dir_output+"\\"+"SHP_"+file_number+"_3.shp")
    fp.Raster_Value_To_Points(file_points,dir_output+"\\"+"B_"+file_number+".tif",dir_output+"\\"+"SHP_"+file_number+"_4.shp")
    fp.Raster_Value_To_Points(file_points,dir_output+"\\"+"NIR_"+file_number+".tif",dir_output+"\\"+"SHP_"+file_number+"_5.shp")

    fp.Raster_Value_To_Points(file_points,dir_output+"\\"+"vis_"+file_number+"_NDVI.tif",dir_output+"\\"+"SHP_"+file_number+"_6.shp")
    fp.Raster_Value_To_Points(file_points,dir_output+"\\"+"vis_"+file_number+"_CIg.tif",dir_output+"\\"+"SHP_"+file_number+"_7.shp")
    fp.Raster_Value_To_Points(file_points,dir_output+"\\"+"vis_"+file_number+"_MSAVI.tif",dir_output+"\\"+"SHP_"+file_number+"_8.shp")
    fp.Raster_Value_To_Points(file_points,dir_output+"\\"+"vis_"+file_number+"_MTVI2.tif",dir_output+"\\"+"SHP_"+file_number+"_9.shp")
    fp.Raster_Value_To_Points(file_points,dir_output+"\\"+"vis_"+file_number+"_NDWI.tif",dir_output+"\\"+"SHP_"+file_number+"_10.shp")
    fp.Raster_Value_To_Points(file_points,dir_output+"\\"+"vis_"+file_number+"_EVI.tif",dir_output+"\\"+"SHP_"+file_number+"_11.shp")
    fp.Raster_Value_To_Points(file_points,dir_output+"\\"+"vis_"+file_number+"_GNDVI.tif",dir_output+"\\"+"SHP_"+file_number+"_12.shp")
    fp.Raster_Value_To_Points(file_points,dir_output+"\\"+"vis_"+file_number+"_IronOxide.tif",dir_output+"\\"+"SHP_"+file_number+"_13.shp")
    fp.Raster_Value_To_Points(file_points,dir_output+"\\"+"vis_"+file_number+"_SAVI.tif",dir_output+"\\"+"SHP_"+file_number+"_14.shp")
    fp.Raster_Value_To_Points(file_points,dir_output+"\\"+"vis_"+file_number+"_SR.tif",dir_output+"\\"+"SHP_"+file_number+"_15.shp")
    fp.Raster_Value_To_Points(file_points,dir_output+"\\"+"vis_"+file_number+"_VARI.tif",dir_output+"\\"+"SHP_"+file_number+"_16.shp")
    
    fp.Raster_Value_To_Points(file_points,dir_output+"\\"+"Tr_"+file_number+".tif",dir_output+"\\"+"SHP_"+file_number+"_17.shp")
    
    
    df_1 = gpd.read_file(dir_output+"\\"+"SHP_"+file_number+"_1.shp")
    df_2 = gpd.read_file(dir_output+"\\"+"SHP_"+file_number+"_2.shp")
    df_3 = gpd.read_file(dir_output+"\\"+"SHP_"+file_number+"_3.shp")
    df_4 = gpd.read_file(dir_output+"\\"+"SHP_"+file_number+"_4.shp")
    df_5 = gpd.read_file(dir_output+"\\"+"SHP_"+file_number+"_5.shp")
    df_6 = gpd.read_file(dir_output+"\\"+"SHP_"+file_number+"_6.shp")
    df_7 = gpd.read_file(dir_output+"\\"+"SHP_"+file_number+"_7.shp")
    df_8 = gpd.read_file(dir_output+"\\"+"SHP_"+file_number+"_8.shp")
    df_9 = gpd.read_file(dir_output+"\\"+"SHP_"+file_number+"_9.shp")
    df_10 = gpd.read_file(dir_output+"\\"+"SHP_"+file_number+"_10.shp")
    df_11 = gpd.read_file(dir_output+"\\"+"SHP_"+file_number+"_11.shp")
    df_12 = gpd.read_file(dir_output+"\\"+"SHP_"+file_number+"_12.shp")
    df_13 = gpd.read_file(dir_output+"\\"+"SHP_"+file_number+"_13.shp")
    df_14 = gpd.read_file(dir_output+"\\"+"SHP_"+file_number+"_14.shp")
    df_15 = gpd.read_file(dir_output+"\\"+"SHP_"+file_number+"_15.shp")
    df_16 = gpd.read_file(dir_output+"\\"+"SHP_"+file_number+"_16.shp")
    df_17 = gpd.read_file(dir_output+"\\"+"SHP_"+file_number+"_17.shp")

    [lat,lon,
     dsm,r,g,b,nir,
     ndvi,cig,msavi,mtvi2,ndwi,evi,gndvi,ironoxide,savi,sr,vari,
     tr] = [[],[],
            [],[],[],[],[],
            [],[],[],[],[],[],[],[],[],[],[],
            []]
      
    for itable in range(0,len(df_1)):

        lat.append(df_1.Lat[itable])
        lon.append(df_1.Lon[itable])

        dsm.append(df_1.RASTERVALU[itable])
        r.append(df_2.RASTERVALU[itable])
        g.append(df_3.RASTERVALU[itable])
        b.append(df_4.RASTERVALU[itable])
        nir.append(df_5.RASTERVALU[itable])

        ndvi.append(df_6.RASTERVALU[itable])
        cig.append(df_7.RASTERVALU[itable])
        msavi.append(df_8.RASTERVALU[itable])
        mtvi2.append(df_9.RASTERVALU[itable])
        ndwi.append(df_10.RASTERVALU[itable])
        evi.append(df_11.RASTERVALU[itable])
        gndvi.append(df_12.RASTERVALU[itable])
        ironoxide.append(df_13.RASTERVALU[itable])
        savi.append(df_14.RASTERVALU[itable])
        sr.append(df_15.RASTERVALU[itable])
        vari.append(df_16.RASTERVALU[itable])
        
        tr.append(df_17.RASTERVALU[itable])

    df = pd.DataFrame()
    [df['Lat'],df['Lon'],
     df['DSM'],df['R'],df['G'],df['B'],df['NIR'],
     df['NDVI'],df['CIg'],df['MSAVI'],df['MTVI2'],df['NDWI'],
     df['EVI'],df['GNDVI'],df['IronOxide'],df['SAVI'],df['SR'],df['VARI'],
     df['Tr']] = [lat,lon,
                  dsm,r,g,b,nir,
                  ndvi,cig,msavi,mtvi2,ndwi,
                  evi,gndvi,ironoxide,savi,sr,vari,
                  tr]
    df.to_csv(dir_table_output+'\\DF'+file_number+'.csv')

    os.remove(dir_output+"\\"+"SHP_"+file_number+"_1.shp")
    os.remove(dir_output+"\\"+"SHP_"+file_number+"_2.shp")
    os.remove(dir_output+"\\"+"SHP_"+file_number+"_3.shp")
    os.remove(dir_output+"\\"+"SHP_"+file_number+"_4.shp")
    os.remove(dir_output+"\\"+"SHP_"+file_number+"_5.shp")
    os.remove(dir_output+"\\"+"SHP_"+file_number+"_6.shp")
    os.remove(dir_output+"\\"+"SHP_"+file_number+"_7.shp")
    os.remove(dir_output+"\\"+"SHP_"+file_number+"_8.shp")
    os.remove(dir_output+"\\"+"SHP_"+file_number+"_9.shp")
    os.remove(dir_output+"\\"+"SHP_"+file_number+"_10.shp")
    os.remove(dir_output+"\\"+"SHP_"+file_number+"_11.shp")
    os.remove(dir_output+"\\"+"SHP_"+file_number+"_12.shp")
    os.remove(dir_output+"\\"+"SHP_"+file_number+"_13.shp")
    os.remove(dir_output+"\\"+"SHP_"+file_number+"_14.shp")
    os.remove(dir_output+"\\"+"SHP_"+file_number+"_15.shp")
    os.remove(dir_output+"\\"+"SHP_"+file_number+"_16.shp")
    
    return