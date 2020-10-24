import tensorflow as tf
import tensorflow_datasets as tfds

dataset, info = tfds.load("imdb_reviews/subwords32k", with_info=True, as_supervised=True)
tokenizer = info.features["text"].encoder

model = tf.keras.models.load_model("trained.h5")

def predict(text):

    tokenized_text = tokenizer.encode(text)
    return model.predict(tf.expand_dims(tokenized_text, 0))

samples = [
    ("I want to commit suicide", 0),
    ("I am deeply depressed", 0),
    ("I had a bad day", 0),
    ("My day was average", 0.5),
    ("I woke up and went to school", 0.5),
    ("Pizza hat has new pizza today", 0.5),
    ("I had a good day", 1),
    ("This was an amazing day", 1),
    ("I'm very excited for the future", 1),
    ("I have the best life in the world", 1),
    ("Hello World", 0.5),
    ("I j went to the store and bought stuff for tn", 0.5),
    ("Check the news, Trump just tweeted something", 0.5),
    ("Framing is everything", 0.5),
    ("I hate my life and want to die", 0.0),
    ("Everything sucks and I just failed an exam", 0.0),
    ("Backend development is too damn hard", 0.0),
    ("That party was weird bro", 0.0),
    ("My life is depressing", 0.0),
    ("He just asked me out!", 1.0),
    ("That meme kills me lmao", 1.0),
    ("Life is a wonderful, beautiful adventure", 1.0),
    ("Hackatons are so much fun", 1.0)
]

for text, score in samples:
    print("[{}/{}] \"{}\"".format(predict(text), score, text))
