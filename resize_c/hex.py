image = open("src.bmp", "rb")
hexadecimal = open("hex3.h", "w");
contents = image.read()
hexadecimal.write("unsigned char image[100] = {")
#for l in contents:
for l in range(100):
	hexadecimal.write("0xff,")
hexadecimal.write("};");
