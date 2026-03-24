import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random


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

  
  
def alpha_num_dict(lower=True, upper=False):
  first_lower = ord('a')
  first_upper = ord('A')
  
  lowercase = {}
  uppercase = {}
  
  for i in range(26):
    lowercase[chr(i + first_lower)] = (ord(chr(i + first_lower)) - first_lower)
    uppercase[chr(i + first_upper)] = (ord(chr(i + first_upper)) - first_upper) 
    
  if lower is True:
    return lowercase

  elif upper is True:
    return uppercase

  else:
    return lowercase, uppercase
  
  
def num_alpha_dict(lower=True, upper=False):
  first_lower = ord('a')
  first_upper = ord('A')
  
  lowercase = {}
  uppercase = {}
  
  for i in range(26):
    lowercase[(ord(chr(i + first_lower)) - first_lower)] = chr(i + first_lower)
    uppercase[(ord(chr(i + first_upper)) - first_upper)] =  chr(i + first_upper)
    
  if lower is True:
    return lowercase

  elif upper is True:
    return uppercase

  else:
    return lowercase, uppercase
  

def alpha_bin_dict(lower=False, upper=False):
  first_lower = ord('a')
  first_upper = ord('A')
  
  lowercase = {}
  uppercase = {}
  
  for i in range(26):
    lowercase[chr(i + first_lower)] = bin(i + first_lower)[2:].zfill(8)
    uppercase[chr(i + first_upper)] = bin(i + first_upper)[2:].zfill(8)

    
  if lower is True:
    return lowercase
  
  elif upper is True:
    return uppercase
  
  else:
    return lowercase, uppercase
  
def bin_alpha_dict(lower=False, upper=False):
  first_lower = ord('a')
  first_upper = ord('A')
  
  lowercase = {}
  uppercase = {}
  
  for i in range(26):
    lowercase[bin(i + first_lower)[2:].zfill(8)] = chr(first_lower + i)
    uppercase[bin(i + first_upper)[2:].zfill(8)] = chr(first_upper + i)
    
  if lower is True:
    return lowercase
  elif upper is True:
    return uppercase
  else:
    lowercase, uppercase  

def blocker(word, block_size, show=True):
   
  lower = alpha_num_dict()

  word_to_matrix = []
  for i in word:
    word_to_matrix.append(lower[i])
  
  word_to_matrix = np.array(word_to_matrix)
  
  block_dim = np.prod((block_size, np.ceil(len(word_to_matrix) / block_size)))
 
  nan_need = int(np.ceil(len(word_to_matrix) / block_size))
  
  null_pad = np.pad(word_to_matrix, pad_width=(0, (int(block_dim) - len(word_to_matrix))), mode='constant', constant_values= 0)
  # FIX so that every non square matrix comes through in column break down instread of row break down.......
  word_to_matrix = null_pad.reshape(block_size, nan_need).T  
  
  
  if show is True:
    print(word_to_matrix)
    
  return word_to_matrix


def hill_scramber_key(size, show=True):
  
  lower = list(alpha_num_dict())
  
  matrix_size = size * size
      
  scramble = []
  for i in range(matrix_size):
    scramble.append(random.choice(lower))

  key = np.reshape(scramble, (size, size))
  if show is True:
    print(key)
    
  return key


def brute_reccurance(array):
  
  for i in range(2, len(array)): 
    try:
      m_build_size = i * i 
      m_build =  array[0:m_build_size]
      m_build_reshape = np.reshape(m_build, (i, i))
      det_m = np.ceil(np.linalg.det(m_build_reshape)) % 2
      print(m_build_reshape.shape, det_m)
    except:
      print('last square matrix able to make')
      break

def stream_scambeler(length=16, show=True):
  lower = list(alpha_bin_dict(lower=True))
  
  key = []
  
  for i in range(length):
    key.append(random.choice(lower))
  
  if show is True:
    print(key)
    
  return key


# keep this to test hill cipher

# E = blocker('hillcipher', 3)
# hill_scramber_key(3)
# Y = blocker('hfzcljljvbpugnng', 4)
# M = numpy_array(3, 4, 5, 2, 1, 3, 2, 5, 13, 2, 5, 19, 7, 8, 2, 15, shape=(4, 4))

# print((M @ E) % 26)
# adjoint = np.conjugate(M).T
# print(adjoint)
# M_inv = ((pow(int(np.linalg.det(M)), -1, 26)) * adjoint) % 26

# decode = (Y @ M_inv) % 26
# print(decode)
# word = decode.flatten(order='F')
# print(word)

# word_tot = [num_alpha_dict()[(i)] for i in word]
# print(word_tot)

# print(num_alpha_dict()[1])

# rec = np.array([1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1,
# 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1,
# 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1,
# 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0])

# brute_reccurance(rec)

# stream_scambeler()