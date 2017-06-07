#include <stdio.h>
#include "hex3.h"

#define K 16

#define STARTPOINT 0 //1078
#define WIDTH 10
#define WIDTH_SQUARE WIDTH*WIDTH

#define COLOR8 1
#define COLOR16 0
#define COLOR32 0

#if COLOR8
unsigned char centroid[K] = {15, 47, 79, 111, 143, 175, 207, 239}; 
#endif
#if COLOR16
unsigned char centroid[K] = {7, 23, 39, 55, 71, 87, 103, 119, 135, 151, 167, 183, 199, 215, 231, 247};
#endif
#if COLOR32
unsigned char centroid[K] = {3, 11, 19, 27, 35, 43, 51, 59, 67, 75, 83, 91, 99, 107, 115, 123, 131, 139, 147, 155, 163, 171, 179, 187, 195, 203, 211, 219, 227, 235, 243, 251};
#endif

unsigned char logK = 0;
void simple_log_for_K()
{
	int cen_leng = K;
	
	while(1)
	{
		cen_leng = cen_leng >> 1;
		logK ++;
		if(cen_leng == 1)
		{
			break;
		}
	}
}

unsigned char get_nearest_centroid(unsigned char pixel)
{
	
	unsigned char div = 256 >> logK;
	unsigned char sub = 2 << ((8-logK-1)) -1;
	unsigned char ret = (pixel - sub) / div; //always in( 0 ~ K-1 ) 
	
	if((pixel-sub)%div > sub+1)
	{
		ret = ret + 1;
	}
	return ret;
}

void drop_image_quality(unsigned char image[41078])
{
	int i;
	for(i = STARTPOINT; i < WIDTH_SQUARE+STARTPOINT; i++)
	{
		printf("%d ", get_nearest_centroid(image[i]));
	} 
	
}
int main()
{
	simple_log_for_K();
	drop_image_quality(image);	
	return 0;
}
