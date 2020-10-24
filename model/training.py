#!/usr/bin/env python
import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import pandas as pd
import os

# Preprocessing
dataset, info = tfds.load('imdb_reviews/subwords32k', with_info = True, as_supervised = True)
train_dataset = dataset['train']
test_dataset = dataset['test']

tokenizer = info.features['text'].encoder
print ('Vocabulary size: {}'.format(tokenizer.vocab_size))


# In[10]:


BUFFER_SIZE = 10000
BATCH_SIZE = 64
train_dataset = train_dataset.shuffle(BUFFER_SIZE)
train_dataset = train_dataset.padded_batch(BATCH_SIZE, train_dataset.output_shapes)
test_dataset = test_dataset.padded_batch(BATCH_SIZE, test_dataset.output_shapes)


# In[12]:


model = tf.keras.Sequential([
    tf.keras.layers.Embedding(tokenizer.vocab_size, 64),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])


# In[13]:


model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])


# In[9]:


history = model.fit(train_dataset, epochs=40, validation_data=test_dataset, steps_per_epoch=9, validation_steps=9)


model.save("trained.h5")


test_loss, test_acc = model.evaluate(test_dataset)
print('Test Loss: {}'.format(test_loss))
print('Test Accuracy: {}'.format(test_acc))

def predictHappiness(sample_pred_text):
    tokenized_sample_pred_text = tokenizer.encode(sample_pred_text)
    predictions = model.predict(tf.expand_dims(tokenized_sample_pred_text, 0))
    return(predictions)

samples = [
    "I hate my life and want to die",
    "Life is a wonderful, beautiful adventure",
    "My day was OK, a lot of stuff to take in but I'm ok",
    "HEy wya"
]
print([predictHappiness(s) for s in samples])

