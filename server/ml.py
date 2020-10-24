import tensorflow as tf
import tensorflow_datasets as tfds
import threading
import json

dataset, info = tfds.load("imdb_reviews/subwords32k", with_info=True, as_supervised=True)
tokenizer = info.features["text"].encoder


with open("adj.json") as rf:
    adj = json.loads(rf.read())


class Predictor:

    def __init__(self):

        self.model = tf.keras.models.load_model("trained.h5")
        self.mutex = threading.Lock()


    def predict(self, text):

        tokenized_text = tokenizer.encode(text)
        self.mutex.acquire()
        output = self.model.predict(tf.expand_dims(tokenized_text, 0))
        self.mutex.release()
        output = output[0][0]

        for word in text.split(" "):
            if word in adj["pos"].keys():
                output += adj["pos"][word]
                break
            elif word in adj["neg"].keys():
                output -= adj["neg"][word]
                break
            elif word in adj["ignore"]:
                return float(output)

        return float(max(output, 0))
