'''

Cell image classifier

Input: Image of a Sudoku cell
Output: Number that is in the image
'''

#Images used for training were pre-processed as follows: convert to grayscale, threshold to either black or white, resize to 50 x 50

#Import relevent modules
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers.core import Dense, Flatten
from keras.optimizers import Adam

#Path to training data. Both training and validation folder consist of the subfolders 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 each containing images of the corresponding numbers
training_path = 'C:\\Users\user\Documents\digits\training'
validation_path = 'C:\\Users\user\Documents\digits\validation'

#Generate the batches of training/validation data with size 50x50
datagen = ImageDataGenerator()

training_data = datagen.flow_from_directory(training_path, target_size=(50,50), classes=['0','1','2','3','4','5', '6', '7', '8', '9'])
validation_data = datagen.flow_from_directory(validation_path, target_size=(50,50), classes=['0','1','2','3','4','5', '6', '7', '8', '9'])

#A simple Multi-layer perception model is built, as it proved to be sufficient for the task
model = Sequential()
model.add(Dense(10, input_shape=(50,50,3), activation="sigmoid"))
model.add(Dense(5, activation="sigmoid"))
model.add(Flatten())
model.add(Dense(5, activation="softmax")) #activation function of output layer is softmax function to squeeze the 5 outputs between 0 and 1 and the total sum is 1

#Adam as optimizer and loss_function categorical_crossentropy as this is a multi-classification task
model.compile(Adam(lr=0.001), loss = 'categorical_crossentropy', metrics = ['accuracy'])

#The model goes through the training set 70 times
model.fit_generator(training_data,validation_data = validation_data, epochs= 70, verbose = 1)


#After training, the model achieved an accuracy of 97%


#Save the trained model so you can use it again later
model.save('C:\\Users\user\Documents/my_model.h5')  # creates a HDF5 file 'my_model.h5'


'''
#For every cell image, predict the number (or zero) inside using Neural network and append to array that represents the Sudoku

#Input: images of all the cells of a Sudoku
#Output: Array representation of Sudoku
'''
def get_cells_values(sudoku_cells):
    cells_values = []
    for i in range(len(sudoku_cells)):
        cell_image = cv2.resize(sudoku_cells[i],(50,50))
        cell_image_3d = np.stack((cell_image,)*3, axis=-1)
        cell_image_tensor = np.expand_dims(cell_image_3d, axis=0)
        cells_values.append(model.predict_classes(cell_image_tensor))
    square_root = int(np.sqrt(len(cells_values)))
    cells_values = np.asarray(cells_values)
    cells_values = cells_values.reshape(square_root, square_root)
    return cells_values