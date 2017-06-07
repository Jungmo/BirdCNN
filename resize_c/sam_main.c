#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "hex2.h"

// unsigned char image[41078]
#define ORIGINAL_SIZE 100
#define RESIZED_SIZE 70
#define ORIGIN_SQUARE ORIGINAL_SIZE * ORIGINAL_SIZE
#define RESIZE_SQUARE RESIZED_SIZE * RESIZED_SIZE
#define HEADER_LENGTH 1078
int resizeBilinearGray(unsigned char pixels[ORIGIN_SQUARE], unsigned char ret[RESIZED_SIZE * RESIZED_SIZE],  int w, int h, int w2, int h2);
int count = 0;
int main()
{
	int i;
	/*	
	for(i = 0; i < 41078; i++)
	{
		printf("%d", image[i]);
	}
	*/
	//FILE* src;
	//FILE* dst;
	
	//char BMPHEADER[HEADER_LENGTH];
	
	//unsigned char pixels[ORIGIN_SQUARE];
	//unsigned char copy[ORIGIN_SQUARE];
	unsigned char ret[RESIZE_SQUARE];
	//unsigned char retcopy[RESIZE_SQUARE];
	//unsigned char dummy[2] = {0x00, 0x00};
	//unsigned char buf[606];
	//int idx = 0;
	//src = fopen("src.bmp", "rb");
	//dst = fopen("dst.bmp", "wb");

	//fread(BMPHEADER, HEADER_LENGTH, 1, src);
	//fwrite(BMPHEADER, HEADER_LENGTH, 1, dst);
	//fseek(src,1078, SEEK_SET);
	//idx = 1078
	//fread(pixels, ORIGINAL_SIZE * ORIGINAL_SIZE, 1, src);
	
	//for(i = 0; i < ORIGINAL_SIZE * ORIGINAL_SIZE; i++)
	//{
	//	copy[i] = pixels[39999-i];
	//}

	i = resizeBilinearGray(image, ret, ORIGINAL_SIZE, ORIGINAL_SIZE, RESIZED_SIZE, RESIZED_SIZE);
	/*	
	for(i = 0; i < 22500; i++)
	{
		retcopy[i] = ret[22499-i];
	}
	
	printf("%d", i);	
	int count = 0;
	int iter = 0;
	while(count < RESIZED_SIZE * RESIZED_SIZE)
	{		
		for( i  = 0; i < 150; i++)
		{
			buf[i] = retcopy[i+iter*150];
		}
		fwrite(buf, 150, 1, dst);
		fwrite(dummy, 2, 1, dst);
		iter++;
		count = count + 150;
	}
	for(i = 0; i < RESIZED_SIZE*RESIZED_SIZE; i++)
	{
		printf("%d", ret[i]);
	}
	
	*/
	printf("%d", count);
	return 0;	
}

/*
int resizeBilinearGray(unsigned char pixels[ORIGINAL_SIZE * ORIGINAL_SIZE], unsigned char ret[RESIZED_SIZE * RESIZED_SIZE],  int w, int h, int w2, int h2)
{
	int A, B, C, D, x, y, index, gray;
	float x_ratio = ((float)(w - 1)) / w2;
	float y_ratio = ((float)(h - 1)) / h2;
	float x_diff, y_diff, ya, yb;
	int offset = 0;
	int i, j;
	for(i = 0; i < h2; i++)
	{
		for(j = 0; j < w2; j++)
		{
			x = (int)(x_ratio * j);
			y = (int)(y_ratio * i);
			x_diff = (x_ratio * j) - x;
			y_diff = (y_ratio * i) - y;
			index = y * w + x;

			A = pixels[index] & 0xff;
			B = pixels[index+1] & 0xff;
			C = pixels[index+w] & 0xff;
			D = pixels[index+w+1] & 0xff;
			
			gray = (int)(A * (1 - x_diff) * (1 - y_diff) + B * (x_diff) * (1-y_diff) + C * (y_diff) * (1 - x_diff) + D * (x_diff * y_diff));

			ret[offset++] = gray;
		}
	}

	return offset;
}
*/

int resizeBilinearGray(unsigned char image[ORIGIN_SQUARE], unsigned char ret[RESIZED_SIZE * RESIZED_SIZE],  int w, int h, int w2, int h2)
{
	int A, B, C, D, x, y, index, gray;
	float x_ratio = ((float)(w - 1)) / w2;
	float y_ratio = ((float)(h - 1)) / h2;
	float x_diff, y_diff, ya, yb;
	int offset = 0;
	int i, j;
	for(i = 0; i < h2; i++)
	{
		for(j = 0; j < w2; j++)
		{
			x = (int)(x_ratio * j);
			y = (int)(y_ratio * i);
			x_diff = (x_ratio * j) - x;
			y_diff = (y_ratio * i) - y;
			index = y * w + x;// + 1078; //1078 - header

			A = image[index] & 0xff;
			B = image[index+1] & 0xff;
			C = image[index+w] & 0xff;
			D = image[index+w+1] & 0xff;
			
			gray = (int)(A * (1 - x_diff) * (1 - y_diff) + B * (x_diff) * (1-y_diff) + C * (y_diff) * (1 - x_diff) + D * (x_diff * y_diff));

			ret[offset++] = gray;
			count++;
		}
	}

	return offset;
}
