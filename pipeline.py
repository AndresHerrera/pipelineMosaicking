import os
import shutil

inputDir = os.path.join(r"raw")
output1Dir = os.path.join(r"output1")
output2Dir = os.path.join(r"output2")
mosaicDir = os.path.join(r"mosaic")

outputVrtFile =  "mosaic_vrt.vrt"
outputMosaicTif = "mosaic.tif"




def prepare():
  makeFolder(output1Dir)
  makeFolder(output2Dir)
  makeFolder(mosaicDir)

def translateUint16toInt16(fileInput, fileOutput):
  try:
    cmd='gdal_translate %s %s -of GTiff -ot Int16 -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" -co "TILED=YES"' % (fileInput,fileOutput)
    print(cmd)
    os.system(cmd)
  except:
    print('Error at translateUint16toInt16 rutine!')

def buildPiramids(fileInput):
  try:
    cmd='gdaladdo --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC_OVERVIEW YCBCR --config JPEG_QUALITY_OVERVIEW 85 %s 2 4 8 16 32 64 128 256"' % (fileInput)
    print(cmd)
    os.system(cmd)
  except:
    print('Error at buildPiramids rutine!')

def buildVrtFile(outputFile, inputFolder):
  try:
    cmd='gdalbuildvrt %s %s/*.tif"' % (outputFile,inputFolder)
    print(cmd)
    os.system(cmd)
    print("done build .vrt file !")
  except:
    print('Error at buildVrtFile rutine!')

def buildMosaicRaster(inputFile, outputFile):
  try:
    cmd='gdal_translate %s %s' % (inputFile,outputFile)
    print(cmd)
    os.system(cmd)
  except:
    print('Error at buildMosaicRaster rutine!')

def copyFileTo(sourcePath, targetPath):
    try:
        shutil.copyfile(sourcePath, targetPath)
        print("copy from %s to %s" % (sourcePath,targetPath))
    except OSError as error: 
        print(error) 

def makeFolder(path):
    try:
        os.mkdir(path)
        print("folder %s created !" % (path))
    except OSError as error: 
        print(error) 

def pipeline():
  prepare()
  contentsInputDir = os.listdir(inputDir)
  for fileInput in contentsInputDir:
    if fileInput.endswith(".tif"):
      print("processing ->  %s file " % (fileInput) )
      translateUint16toInt16(os.path.join(inputDir,fileInput),os.path.join(output1Dir,fileInput) )
  print("done translate Uin16 to Int16")

  contentsOutput1Dir = os.listdir(output1Dir)
  for fileInput in contentsOutput1Dir:
    if fileInput.endswith(".tif"):
      print("processing ->  %s file " % (fileInput) )
      copyFileTo(os.path.join(output1Dir,fileInput),os.path.join(output2Dir,fileInput))
  print("done copy files from output1 to output2")

  contentsOutput2Dir = os.listdir(output2Dir)
  for fileInput in contentsOutput2Dir:
    if fileInput.endswith(".tif"):
      print("processing ->  %s file " % (fileInput) )
      buildPiramids(os.path.join(output2Dir,fileInput))
  print("done build piramids in output2")

  buildVrtFile(outputVrtFile,output2Dir)

  if os.path.exists(outputVrtFile) :
    print('build mosaic')
    buildMosaicRaster(outputVrtFile,os.path.join(mosaicDir,outputMosaicTif))
    print('Mosaic file %s built !' % (outputMosaicTif) )
  else:
    print("Problem building mosaic file check %s file" % (outputVrtFile))


def main():
    pipeline()
    print('pipeline excecuted sucessfully !!')

if __name__ == "__main__":
    main()  