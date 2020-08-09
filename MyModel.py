from keras.models import load_model
import DataGenerator
from keras import layers
from keras import models
from keras import optimizers
import matplotlib.pyplot as plt

tot_char = 3755
_epochs = 200
test_samples_per_class = 60

def train(model, img_size = (64, 64), charset_size=3755, validationRate = 0.3, pickedNumber = 240, batch_size = 128):
    dg = DataGenerator.DataGenerator()
    train_sample_count = dg.pick_small_dataset(char_number=charset_size, picked_number=pickedNumber, validation_rate=validationRate)
    train_generator, validation_generator, test_generator = dg.data_gen(batchSize=batch_size)

    _steps_per_epoch = charset_size * train_sample_count // batch_size
    _validation_steps = charset_size * (pickedNumber - train_sample_count) // batch_size

    # print(_steps_per_epoch)
    # print(_validation_steps)

    # return

    model.compile(loss='categorical_crossentropy',
        optimizer='rmsprop',
        metrics=['acc'])
    
    history = model.fit(
        train_generator,
        steps_per_epoch = _steps_per_epoch,
        epochs = _epochs,
        validation_data = validation_generator,
        validation_steps = _validation_steps
    )
    model.save('char_recognition.h5')

    display(history)

    return test_generator, charset_size * test_samples_per_class // batch_size
  
def display(history):
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(1, len(acc) + 1)

    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()

    plt.figure()

    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()

    plt.show()

    

def build(img_shape = (64, 64, 1), charset_size=3755):
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=img_shape))
    model.add(layers.MaxPool2D(2, 2))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPool2D(2, 2))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPool2D(2, 2))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPool2D(2, 2))
    model.add(layers.Flatten())
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(1024, activation='relu'))
    model.add(layers.Dense(charset_size, activation='softmax'))

    return model






# 加载model
# model = load_model('char_recognition.h5')

# dg = DataGenerator.DataGenerator()

# # dg.pick_small_dataset(char_number=charset_size, picked_number=pickedNumber, validation_rate=validationRate)
# train_generator, validation_generator, test_generator = dg.data_gen(batchSize=32)

# test_loss, test_acc = model.evaluate(test_generator, steps=18)

# print('test acc: ', test_acc)

model = build(charset_size=50)
test_generator, _steps = train(model, charset_size=50)

test_loss, test_acc = model.evaluate(test_generator, steps=_steps)
print('test acc: ', test_acc)