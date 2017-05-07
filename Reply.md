1) 일단, 독자/리뷰어에게 강조하고 싶은 contribution이 뭔지 조금 더 명확하면 좋겠습니다.
  - CNN으로 classification을 잘 할 수 있다 인지 (이를 위해 부수적으로 Image Resize와 Color quantization을 이용),
  - CNN을 쓰기 위해서 적절한 Image Resize와 Color Quantization가 중요하다인지,
   즉, 전자가 핵심인지 후자가 핵심인지 아니면 둘 다 인지...본인의 마음이 아직 정해지지 않은것 같아요.

답변 1)
모니터링, 분류하기 위해서 CNN을 사용할 때, Training이나 Prediction과정에서 이미징 센서를 부착한 노드가 굳이 RAW이미지를 보내지 않아도 Classification Accuracy에 크게 문제가 되지 않는다는 것, 적당한 이미지 프로세싱을 통해서 에너지 소비량이 훨씬 적어진다는 것을 보여주고 싶었습니다.
또, 실험결과 Raw Image를 사용하는 것보다 processing 후 결과가 더 좋았습니다.

2) 미안합니다, union distribution이 뭔지 제가 잘 몰라서...

답변 2)
죄송합니다... uniform distribution을 말한 것이었는데 정신이 없어서 Union이라고 한 것 같습니다. 히스트그램이  픽셀별로 눈에 띄는 분포가 있는게 아닌 일정함을 보인다는 것을 말씀드릴려고 했습니다. 

3) class를 4개만 두고 실험을 하는데...
    그 아래, 예외의 경우가 많아서 traditional ML이 잘 안된다라고 말하는데... 
    사실 이 문제는 동일한 상황 아닌가요?

답변 3)
네, 동일한 문제입니다. 하지만 Traditional ML은 이 문제를 해결할 수 없다고 생각합니다. CNN은 Data Driven으로 해결할 수 있다고 생각해서 그렇게 말씀드렸습니다.

4) 위와 관련하여, training set에서 아예 예외상황을 배재한 경우와, 배재하지 않는 경우를 따로 실험해보셨나요?
     즉, 아예 청소년 새 사진들은 모두 제거하고 training과 validation을 한 경우, 그리고
     전체 dataset을 가지고 training과 validation을 한 경우를 비교해 보면
     예외 상황으로 인한 정확도 감소가 어느정도인지 감을 잡을 수 있을 것 같은데....

답변 4) 교수님의 말씀대로 진행해보았는데 큰 차이가 없었습니다.

5) color quantization을 세가지 방식을 사용할 수 있다고 하셨는데, 결국 어떤 한가지로 결정을 하신건가요?
     ("straight-line distance", "nearest color" algorithm, K-means )
     아래 evaluation 부분에 K-means 를 이용한 결과가 있긴 하던데, 이걸로 결정을 한건지,
     아니면 아직도 세가지를 모두 살펴보고 있는 건지 궁금합니다.

답변 5)
고정된 픽셀값을 사용, 매우 단순하게 합니다. 전력측정 결과 상당히 낮게 나왔습니다.
K=8일 때(사용하는 Color가 8개일 때), Pixel 값을 Color_Quantized = {15, 47, 79, 111, 143, 175, 207, 239} 로 설정하고
전체 픽셀을 읽으면서 픽셀을 Color_Quantized 와 가장 가까운 값으로 치환합니다. 아래 C 코드를 참고하시면 될 것 같습니다.

unsigned char get_nearest_centroid(unsigned char pixel)
{

        unsigned char div = 256 >> logK;
        unsigned char sub = 2 << ((8-logK-1)) -1;
        unsigned char ret = (pixel - sub) / div;

        if((pixel-sub)%div > sub+1)
        {
                ret = ret + 1;
        }
        return ret;
}

//header size = 1078
void drop_image_quality(unsigned char image[41078])
{
        int i;
        for(i = 1078; i < WIDTH_SQUARE+1078; i++)
        {
                printf("%d ", get_nearest_centroid(image[i]));
        }

}


6) Image augmentation에서 "X배" 했다는 건, 해당 이미지들의 갯수를 X배로 늘렸다는 말이죠?
     - 특정 배수 X를 정한 기준은 무엇인가요? 해당 class의 이미지 갯수를 동일하게 맞춘건가요?
     - blur는 어느정도 한건가요?
     - filp는... flip을 말하는 거죠?

답변 6) 모두 맞습니다. blur는 7x7 Gaussian Blur를 한번 사용했습니다. **Update된 결과에서는 Blur를 사용하지 않았습니다.**

7) "전송량 대비 정확도"라는 표현을 했는데, 계산을 어떻게 한거죠? 정확도% 나누기 전송량%?
      하나의 새로운 metric 형태로 만들어도 나쁘지 않겠네요.

답변 7)
계산을 해서 말씀드린건 아니고 제가 적당히 수치보고 작성했습니다. 교수님께서 말씀해주신 방법이 가장 일반적으로 알 수 있는 방법인 것 같습니다. 관련해서 그래프 첨부하겠습니다.

8) 결과의 표현을 3차원 곡면 그래프로 하면 좋을 듯. 
     뭔가 3차원 곡면 그래프가 들어가면 논문이 폼나 보임. 또한 연속되는 막대그래프의 향연을 줄일 수 있음.
     예1) x축은 이미지 크기 %, y축은 색상 갯수 %, z 축은 정확도
     예2) x축은 이미지 크기 %, y축은 색상 갯수 %, z 축은 압축률

답변 8) 만들어서 추가 및 업데이트 하겠습니다.

9) "Image Augmentation을 많이 한 경우에 8, 16 Color의 경우 Accuracy가 상승했지만 256, 32의 경우에는 Accuracy가 크게 떨어졌습니다."
      ...라고 말씀 하셨는데, 이 문장은 좀 명확한 해석이 필요할 것 같습니다.
      색상이 더 정확한데 정확도가 떨어졌다고 하면 믿기가 힘들기 때문에, 왜 그런지 어떤 조건인지 명확해야 하겠습니다.

답변 9)
32 Color 150 Resolution 의 경우 Confusion Matrix입니다.
Accuracy: 85.27 
Confusion Matrix:
     새       알   빈둥지  새끼새
   새[10908    21    17    62]
   알[   64  1296    71    17]
빈둥지[ 1113     1  6547  1461]
새끼새[  646     7    79  1853]]

16 Color 150 Resolution 의 경우 Confusion Matrix입니다.
Accuracy: 90.07 
Confusion Matrix:
[[10849    24    34   101]
 [   43  1308    89     8]
 [  205    23  7570  1324]
 [  442    13    94  2036]]
 
 위에서 말씀하신 것과 같이 새끼새의 경우에는 청소년 새 때문인지 '새'로 Classification된 경우가 많습니다. 

 32Color와 16Color의 가장 큰 차이점은 '빈둥지'를 '새'라고 판단하는 경우가 많아졌다는 것인데 제 생각에는 Data Augmentation과정에서 Bluebird에 blur를 한 것이 하나의 문제가 될 수 있을 것 같고 또 Data Augmentation을 적게 했을 경우에 16color 8 color에서는 빈둥지로 분류하는 경우가 높게 나오는 경향이 있습니다. 이것이 하나의 답이 될 수 있지 않을까 싶습니다.
 즉 '원래 8과 16 Color의 경우 빈둥지 검출 능력은 좋은데 다른 것들 검출 능력이 좋지 않았다. 하지만 Data Augmentation을 통해서 다른 것들을 검출하는 능력을 높혔다.' 이라고 생각합니다.

10) 참고 논문
      - http://www.cs.cornell.edu/~destrin/resources/journals/2010-aug-Ko.pdf
         -- (TR 버젼) http://vision.ucla.edu/~tko/pubs/tech1_07.pdf

고맙습니다.