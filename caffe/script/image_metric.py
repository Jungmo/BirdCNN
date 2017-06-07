import os
import cv2
from skimage.measure import compare_ssim as ssim
import math
import numpy as np
import statistics as stat
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--color', type=str, default='', help="Color Quantization k")
parser.add_argument('--size', type=str, default='', help = "image WIDTH size") 
args = parser.parse_args()

ROOT = os.getcwd()
IMAGE_ROOT = os.path.join(ROOT, "bird_image", "test")
COLOR = args.color
SIZE = args.size
ORIGIN_PATH = os.path.join(IMAGE_ROOT, "256")
TARGET_PATH = os.path.join(IMAGE_ROOT, COLOR+"_"+SIZE)
KIND = ["swallow", "bluebird", "egg", "empty", "child"]

SSIM = []
MSE = []
PSNR = []

def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    
    return err

def psnr(imageA, imageB):
    MAX = 255
    msee = mse(imageA, imageB)
    ret = 10*math.log10(MAX**2/msee)
    return ret

for kind in KIND:
	origin_target_dir = os.path.join(ORIGIN_PATH, kind)
	modify_target_dir = os.path.join(TARGET_PATH, kind)
	origin_image_list = os.listdir(origin_target_dir)
	for origin_image in origin_image_list:
		if not '.bmp' in origin_image:
			continue
		imageA_path = os.path.join(origin_target_dir, origin_image)
#		imageB_path = os.path.join(modify_target_dir, origin_image[:-4]+"_"+COLOR+"_"+COLOR+"_"+SIZE+".bmp")
		#imageB_path = os.path.join(modify_target_dir, origin_image[:-4]+"_"+COLOR+".bmp")
		print imageA_path
		imageA = cv2.imread(imageA_path, 0)
		#imageB = cv2.imread(imageB_path, 0)
		#imageB = cv2.resize(imageB, (len(imageA), len(imageA)))
		SSIM.append(ssim(imageA, imageA))
		MSE.append(mse(imageA, imageA))
		PSNR.append(psnr(imageA, imageA))

file_mse = open(ROOT+"/image_compare/"+COLOR+"_"+SIZE+"_"+"MSE"+".txt","w")
file_psnr = open(ROOT+"/image_compare/"+COLOR+"_"+SIZE+"_"+"PSNR"+".txt","w")
file_ssim = open(ROOT+"/image_compare/"+COLOR+"_"+SIZE+"_"+"SSIM"+".txt","w")
file_result = open(ROOT+"/image_compare/"+COLOR+"_"+SIZE+"_"+"RESULT"+".txt","w")

for i in range(len(SSIM)):
	file_mse.write(str(MSE[i]))
	file_mse.write("\n")
	file_psnr.write(str(PSNR[i]))
	file_psnr.write("\n")
	file_ssim.write(str(SSIM[i]))
	file_ssim.write("\n")

mse_ave = stat.mean(MSE)
psnr_ave = stat.mean(PSNR)
ssim_ave = stat.mean(SSIM)
mse_std = stat.stdev(MSE)
psnr_std = stat.stdev(PSNR)
ssim_std = stat.stdev(SSIM)

file_result.write("MSE PSNR SSIM AVE : \n")
file_result.write(str(mse_ave) + " " + str(psnr_ave) +" "+ str(ssim_ave)+"\n")
file_result.write("MSE PSNR SSIM STD : \n")
file_result.write(str(mse_std) + " " + str(psnr_std) +" "+ str(ssim_std)+"\n")
