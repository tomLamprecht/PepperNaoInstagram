from imageai.Classification import ImageClassification
import os
import json
import PictureDownloader
import jsonManager
from deep_translator import GoogleTranslator


def main(shortcode):

    path = '#Pictures'
    PictureDownloader.downloadPicture(shortcode , path)

    execution_path = os.getcwd()

    prediction = ImageClassification()
    prediction.setModelTypeAsResNet50()
    prediction.setModelPath(os.path.join(execution_path, "data/resnet50_imagenet_tf.2.0.h5"))
    prediction.loadModel()

    predictions, probabilities = prediction.classifyImage(os.path.join(execution_path, os.path.join(path,'0.jpg')), result_count=5 )


    translated_predictions = []
    results = []
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        result = {'prediction' : eachPrediction, 'probability' : eachProbability , 'prediction_translated' : GoogleTranslator(source='en', target='de').translate(eachPrediction)}
        results.append(result)
    
    jsonManager.dumpImageRecoginitionResults(results)

    result = predictions[0]

    
  #  print("BEEP BOOP: ICH GLAUBE AUF DEM BILD BEFINDET SICH: " + translator.translate(str(result).replace('_', ' ')))
  #  print("ich bin mir zu " + str(probabilities[0]) +'%' +" sicher")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--shortcode", type=str, required=True, help = "Shortcode of the Instagram Picture. E.g. https://www.instagram.com/p/CDQvCMAJNZk/ CDQvCMAJNZk is the Shortcode")
    args = parser.parse_args()
    print(args.shortcode)
    main(args.shortcode)
