@echo off
@echo Translate raw images from Uint16 to Int16
call translate_to_int16.bat
@echo Copy from output 1 to output2
xcopy output1 output2
@echo Build piramids
call build_piramids.bat
@echo Build .vrt file
call build_vrt.bat
@echo Build Mosaic file
call build_mosaic.bat
@echo Done
pause