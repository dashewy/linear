import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def numpy_array(*args, shape, show=True):

    array = np.array([*args])

    shaped_array = np.reshape(array, shape)

    if show is True:
      show = print(shaped_array)
      
    return shaped_array
  
def image_to_matrix(image_file, color=True, info=True):
    input_image = Image.open(image_file)

    matrix = np.asarray(input_image)
    if color is True:
      
      red_matrix = matrix[:, :, 0]
      green_matrix = matrix[:, :, 1]
      blue_matrix = matrix[:, :, 2]
      matrixs = [red_matrix, green_matrix, blue_matrix]
      matrixs = [((value - np.min(value)) / (np.max(value) - np.min(value)) * 255) for value in matrixs]
      
      if info is True:
        print(f'the shape is {[matrix.shape for matrix in matrixs]}')
        
      return matrixs
  
    else:
      
      matrix = np.mean(matrix, axis=2)
  
      if info is True:
        print(f'the shape is {matrix.shape}')

      return matrix


def matrix_to_image(matrix, color=True, show=True, save=False):

    if color is True:
      matrix = [((value - np.min(value)) / (np.max(value) - np.min(value)) * 255) for value in matrix]
      # matrix.astype('uint8')
      matrix = [i.astype('uint8') for i in matrix]
      matrix = np.dstack(matrix)
      
      output_image = Image.fromarray(matrix, mode='RGB')
    
    else:
      output_image = Image.fromarray(matrix)
      
    if save is True:
      
      output_image.save(f'file_compressed.jpg')
      
    if show is True:
      plt.imshow(output_image)
      plt.show()
    
    
        
    return output_image


slime = image_to_matrix('slime.jpg', color=False)
slime_back = matrix_to_image(slime, color=False)