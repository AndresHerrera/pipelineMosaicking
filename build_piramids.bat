@echo off
color 20
for %%x in (output2/*.tif) do gdaladdo --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC_OVERVIEW YCBCR --config JPEG_QUALITY_OVERVIEW 85 output2/%%~nx.tif 2 4 8 16 32 64 128 256
