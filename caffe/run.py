import numpy as np
import os
import sys
import argparse
import glob
import time

import caffe


BIRD_ROOT = os.getcwd()+"/"
BINARYPROTO_PATH = os.path.join(BIRD_ROOT, "db/mean.binaryproto")
NPY_PATH = os.path.join(BIRD_ROOT, "db/mean.npy")
CAFFE_BIN = "/home/jungmo/apps/caffe/build/tools/"
network = 'MobileNets'
#network = 'googLeNet'
IMG_SIZE = 224
TRAIN_LIST = os.path.join(BIRD_ROOT, "bird_no_adole","train", "train.txt")
VALID_SET = "test_256_200"
VALID_LIST = os.path.join(BIRD_ROOT, "bird_no_adole", "test","test.txt")# VALID_SET + ".txt")

def binaryproto_to_npy():
    blob = caffe.proto.caffe_pb2.BlobProto()
    data = open( BINARYPROTO_PATH , 'rb' ).read()
    blob.ParseFromString(data)
    arr = np.array( caffe.io.blobproto_to_array(blob) )
    out = arr[0]
    np.save( NPY_PATH, out )

def evaluate_model():
        input_file = VALID_LIST
        output_file = os.path.join(BIRD_ROOT, "db/output.npy")
        model_def = os.path.join(BIRD_ROOT, "model_prototxt/"+network+"/deploy.prototxt")
        pretrained_model = os.path.join(BIRD_ROOT, "googlenet_iter_60000.caffemodel")
        gpu = True
        images_dim='224,224'
        mean_file = NPY_PATH
        ext='jpg'
        channel_swap='2,1,0'
        raw_scale = 255.0
        center_only=True
	input_scale = None
        image_dims = [int(s) for s in images_dim.split(',')]

        mean, channel_swap = None, None
        if mean_file:
            mean = np.load(mean_file)
	if channel_swap:
	    channel_swap=[int(s) for s in args.channel_swap.split(',')]
        caffe.set_mode_gpu()

        # Make classifier.
        classifier = caffe.Classifier(model_def, pretrained_model,
                image_dims=image_dims, mean=mean,
                input_scale=input_scale, raw_scale=raw_scale,
                channel_swap=channel_swap)

        # Load numpy array (.npy), directory glob (*.jpg), or image file.
        imgs_list = tuple(open(input_file,'r'))
        print("Loading file: %s" % input_file)
        inputs =[caffe.io.load_image(im_f)
                     for im_f in glob.glob(input_file + '/*.' + ext)]

        print("Classifying %d inputs." % len(imgs_list))

        BATCH_SIZE = 100

        # Classify.
        confusion_matrix = np.zeros((4,4),dtype=np.int32)
        accuracy = 0.0
        start = time.time()
        for i in range(0, len(imgs_list), BATCH_SIZE):
            if i > 0 and i % (BATCH_SIZE * 25) == 0:
                print("Finished %d imgs." % (i))
                cur_accuracy = accuracy / i * 100
                print("Accuracy: %.2f " % cur_accuracy)
                print("Confusion Matrix:")
                print confusion_matrix
            imgs = [imgs_list[i + j].split(' ')[0] for j in range(min(BATCH_SIZE,len(imgs_list)-i))]
            gts = [int(imgs_list[i + j].split(' ')[1]) for j in range(min(BATCH_SIZE,len(imgs_list)-i))]
            inputs = [caffe.io.load_image(path) for path in imgs]
            predictions = classifier.predict(inputs, not center_only)
            for j in range(len(imgs)):
                probs = predictions[j]
                pred = np.argmax(probs)
                confusion_matrix[gts[j]][pred] += 1
                if pred == gts[j]:
                    accuracy += 1.0
        accuracy = accuracy / len(imgs_list) * 100

        print("Done in %.2f s." % (time.time() - start))
        # Save
        print("Accuracy: %.2f " % accuracy)
        print("Confusion Matrix:")
        print confusion_matrix
	np.save(VALID_SET+".npy", confusion_matrix)

def main():
    '''
    print "Make DB : Training set"
    os.system(os.path.join(CAFFE_BIN,"convert_imageset.bin")+" -backend=\"lmdb\" -shuffle=true -resize_height "+str(IMG_SIZE)+" -resize_width "+str(IMG_SIZE)+ " / " + TRAIN_LIST + " " + BIRD_ROOT + "db/train_imageData_lmDB")
    print "Make DB : Test set"
    os.system(os.path.join(CAFFE_BIN,"convert_imageset.bin")+" -backend=\"lmdb\" -shuffle=true -resize_height "+str(IMG_SIZE)+" -resize_width "+str(IMG_SIZE) + " / " + VALID_LIST +" "+ BIRD_ROOT + "db/val_imageData_lmDB")

    print "Make image mean file"
    os.system(os.path.join(CAFFE_BIN,"compute_image_mean.bin")+
                   " -backend=lmdb "+ BIRD_ROOT + "db/train_imageData_lmDB " + BIRD_ROOT+ "db/mean.binaryproto")
    print "Image mean file .binaryproto to .npy"
    binaryproto_to_npy()
    
    print "Training model"
    os.system(os.path.join(CAFFE_BIN,"caffe.bin")+" train "
                   "-solver="+BIRD_ROOT+"model_prototxt/"+network+"/solver.prototxt "
                   "-weights="+BIRD_ROOT+"model_prototxt/"+network+"/bvlc_googlenet.caffemodel"+" -gpu all")
    '''
    os.system(os.path.join(CAFFE_BIN,"caffe.bin")+" train "
                   "-solver="+BIRD_ROOT+"model_prototxt/"+network+"/solver.prototxt "+"-gpu all"
                   )#"-weights="+BIRD_ROOT+"model_prototxt/"+network+"/bvlc_googlenet.caffemodel"+" -gpu all")

    print "Evaluate model"
    evaluate_model()

if __name__ == '__main__':
    main()
