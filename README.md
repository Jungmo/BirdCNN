# BirdCNN

* 딥러닝의 발전함에 따라 이미지 분류 도메인의 주도권은 고전적 머신 러닝 알고리즘 (SVM, Linear Classifier)에서 ConvNN으로 주도권이 넘어감.
* ConvNN을 실생활에 적용하기 위해서 의미있고 실용적인 이미지를 수집하는 것이 필요함
* 이미지를 수집하는 것에는 Wireless Image Sensor Networks (WISN)가 하나의 해결책이 될 수 있음
* 하지만 WISN 상에서 멀티미디어 데이터를 전송하는 것은 데이터소모가 크기 때문에 원본 이미지를 전송하는 것은 에너지 비효율적임
* 이 문제를 해결하기위해 Image resize와 Color Quantization을 사용하려고 함.
* 중요한 Contribution은 WISN 상의 노드가 원본 이미지를 전송하지 않고 Quality를 감소시켜도 ConvNN 결과에 크게 영향을 미치지 않는 것을 보여주는 것
* 전송량 측면에서 50% 이하로의 전송량 감소, 85% 이상 의 분류 정확도, ~%의 에너지 감소를 보임을 알아냄.

# Motivation 

# Image Preprocessing for reducing transmission amount
임베디드 디바이스에서 쉽게 구현 및 적은 계산량, 적은 에너지 소모가 필수적이다.
preprocessing 된 이미지 몇개 예시(SSIM, PSNR, MSE 등의 Image distortion metric과 같이)

* Previous Approach
    * Find ROI and Crop
        * 임베디드 디바이스가 ROI를 잘 찾아서 ROI만 전송할 수 있다면 Traditional Image classifier에서는 잘 동작할 수 있다. 하지만 ROI 검출은 SIFT, SURF 등의 복잡한 알고리즘이 필요하다. 또는 시계열 이미지에서 이전 이미지와 현재 이미지간의 차이를 통해 변화한 부분을 ROI로 사용하는 방법도 있다. 그러나 원본 이미지가 grayscale 단채널이어서 색상정보가 부족하다는 점, 그에 따른 Pixel histogram이 각 Class마다 차이가 많이 나지않아 classification accuracy가 상당히 낮게 나온다.
        * ConvNN의 경우 학습된 데이터에 따라서 Validation이 진행되는데 학습시키는 과정에서 ROI를 추출해서 학습시키기가 어려운 점, ConvNN의 경우 완벽하게 잘리지 않은 이미지에 대해서 검출이 어려운 점 때문에 ROI Crop 방법은 적절하지 않다. 그래서 이미지의 전체 크기를 줄이기로 함.
* Image Scaling
    * Bilinear Image Scaling(이선형 보간법)
        * Interpolation(인터폴레이션, 보간)이란 알려진 지점의 값 사이(중간)에 위치한 값을 알려진 값으로부터 추정하는 것을 말한다.
            * 출처 : http://darkpgmr.tistory.com/117 [다크 프로그래머]
            * 출처 : http://tech-algorithm.com/articles/bilinear-image-scaling/
        * 간단한 Psuedo code box
* Image Color Quantization
    * Color Quantization은 원본 이미지의 256색을 모두 사용하는 것이 아닌 일정 수의 표현 가능한 픽셀 수로 줄여서 사용하는 것이다.
    * Color Quantization의 방법에는 "straight-line distance", "nearest color" algorithm,[위키피디아] K-means[교수님 논문, Celebi, M. E. (2011). "Improving the performance of k-means for color quantization". Image and Vision Computing. 29 (4): 260–271. doi:10.1016/j.imavis.2010.10.002.] 방식 등이 있다.
    * 원본 이미지로 Training한  Conv 모델을 사용할 경우에는 낮은 Distortion(SSIM, PSNR Metric 상)을 유발하는 Algorithm이 좋은 Accuracy result를 줄 수 있겠지만, Training도 Color Quantization한 이미지를 사용할 경우 낮은 Distortion이 크게 문제가 되지 않을 것이다. 그래서 여러번의 iteration을 거치는 것 또는 Pixel간의 euclidean distance 등을 계산하는 것이 아닌 정해진 Color pixel을 고정해서 Quantization을 수행한다. 이로인해 더 적은 연산을 통해 Color Quantization을 할 수 있다.
    * 정해진 Color Pixel 구하는 psuedo code box
    * Color Quantization 후 이미지의 사이즈(bytes) 계산 식 (log(2)(# of Colors) * # of pixel)
[표] Compression ratio

|너비|높이|8|16|32|256|
|---|---|---|---|---|---|
|100|100|9%|13%|16%|25%|
|110|110|11%|15%|19%|30%|
|120|120|14%|18%|23%|36%|
|130|130|16%|21%|26%|42%|
|140|140|18%|25%|31%|49%|
|150|150|21%|28%|35%|56%|
|160|160|24%|32%|40%|64%|
|170|170|27%|36%|45%|72%|
|180|180|30%|41%|51%|81%|
|190|190|34%|45%|56%|90%|
|200|200|38%|50%|63%|100%|

# Image Classification

이미지를 새, 새끼새, 알, 빈둥지로 클래스를 나눈다. 새의 종류 2개, 새끼새, 알, 빈둥지의 여려가지 이미지 첨부

이 때 새의 종류가 2개 인 점, 새끼새의 경우 청소년새가 포함되어 있는 점, 알이 둥지 밑에 숨어있는 점 등을 제시한다.



