hexadecimal = open("hex3.h", "w");
hexadecimal.write("unsigned char image[100] = {")
#for l in contents:
for l in range(100):
	hexadecimal.write("0x59,")
hexadecimal.write("};");
