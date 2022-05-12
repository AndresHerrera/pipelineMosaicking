@echo off
color 20
for %%x in (raw/*.tif) do gdal_translate raw/%%~nx.tif output1/%%~nx.tif -of GTiff -ot Int16 -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "TILED=YES"
