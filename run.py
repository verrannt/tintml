# Import before TF to disable TF outputs
from tintml import Tint

import os

# Import TF related stuff
import tensorflow as tf
#tf.get_logger().setLevel('ERROR')
# Can also be set using the AUTOGRAPH_VERBOSITY environment variable
#tf.autograph.set_verbosity(3)

from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model

tint = Tint()

tint.scope('Preparing Data')

with tint.status('Processing'):
    mnist = tf.keras.datasets.mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    # Add a channels dimension
    x_train = x_train[..., tf.newaxis].astype("float32")
    x_test = x_test[..., tf.newaxis].astype("float32")

    train_ds = tf.data.Dataset.from_tensor_slices(
        (x_train, y_train)).shuffle(10000).batch(32)

    test_ds = tf.data.Dataset.from_tensor_slices(
        (x_test, y_test)).batch(32)

    tint.log('Successfully loaded data')

tint.scope('Model Setup')

class MyModel(Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.conv1 = Conv2D(12, 3, activation='relu')
        self.flatten = Flatten()
        self.d1 = Dense(40, activation='relu')
        self.d2 = Dense(10)

    def call(self, x):
        x = self.conv1(x)
        x = self.flatten(x)
        x = self.d1(x)
        return self.d2(x)

with tint.status('Initialization'):
    # Create an instance of the model
    model = MyModel()
    tint.log('Model initialized')

    loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    tint.log('Log function initialized')

    optimizer = tf.keras.optimizers.Adam()
    tint.log('Optimizer initialized')

    train_loss = tf.keras.metrics.Mean(name='train_loss')
    train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')

    test_loss = tf.keras.metrics.Mean(name='test_loss')
    test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='test_accuracy')
    tint.log('Metrics initialized')

@tf.function
def train_step(images, labels):
    with tf.GradientTape() as tape:
        # training=True is only needed if there are layers with different
        # behavior during training versus inference (e.g. Dropout).
        predictions = model(images, training=True)
        loss = loss_object(labels, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    train_loss(loss)
    train_accuracy(labels, predictions)

@tf.function
def test_step(images, labels):
    # training=False is only needed if there are layers with different
    # behavior during training versus inference (e.g. Dropout).
    predictions = model(images, training=False)
    t_loss = loss_object(labels, predictions)

    test_loss(t_loss)
    test_accuracy(labels, predictions)

tint.scope('Training')

EPOCHS = 5

for epoch in range(EPOCHS):

    tint.print("Epoch {}/{}".format(epoch+1, EPOCHS))

    # Reset the metrics at the start of the next epoch
    train_loss.reset_states()
    train_accuracy.reset_states()
    test_loss.reset_states()
    test_accuracy.reset_states()

    for images, labels in tint.iter(train_ds, "Training"):
        train_step(images, labels)

    for test_images, test_labels in tint.iter(test_ds, "Testing"):
        test_step(test_images, test_labels)

    tint.print_metrics({
            'Train Loss': train_loss.result(),
            'Train Accuracy': train_accuracy.result(),
            'Test Loss': test_loss.result(),
            'Test Accuracy': test_accuracy.result()},
        down_is_better=[True, False, True, False],
    )
