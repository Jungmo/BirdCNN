import math
import argparse

'''
parser = argparse.ArgumentParser()
parser.add_argument('--K', type = int)
parser.add_argument('--WIDTH', type = int)

args = parser.parse_args()

WIDTH = args.WIDTH
K = args.K
'''

w = [200, 150, 140, 130, 120, 110, 100]
k = [256, 32, 16, 8]

for WIDTH in w:
	for K in k:
		logK = math.log(K, 2)
		logK = int(logK)
		WIDTH_SQUARE = WIDTH**2

		numofbits = WIDTH_SQUARE * logK

		print numofbits
		numofbytes = numofbits/8

		print WIDTH, K, numofbytes

		hexadecimal = open("hex"+str(WIDTH)+"_"+str(K)+".h", "w");
		hexadecimal.write("unsigned char image["+str(numofbytes)+"] = {")
		for l in range(numofbytes):
			hexadecimal.write("0xff,")
		hexadecimal.write("};");
