import numpy as np
from supplemental_functions import numpy_array
from supplemental_functions import image_to_matrix
from supplemental_functions import matrix_to_image



class SVD():

  def __init__(self, A):
    self.A = A

  def least(self, b):
    least = np.linalg.lstsq(self.A, b)

    return least

  def ATA(self, show=True):

    lefty = self.A.T @ self.A

    statement = str(f'A.T @ A is {lefty}')
    if show is True:
      print(statement)

    return lefty

  def AAT(self, show=True):

    righty = self.A @ self.A.T

    statement = str(f'A @ A.T is {righty}')
    if show is True:
      print(statement)

    return righty

  def eigens(self, show=True):

    right_eigenvalue, right_eigenvector = np.linalg.eig(self.ATA())
    left_eigenvalue, left_eigenvector = np.linalg.eig(self.AAT())

    statement = print(f'for A.T @ A the eiginvalues are {right_eigenvalue} \n the eiginvectors are {right_eigenvector} \n for A @ A.T the eiginvalues are {left_eigenvalue} and the eigenvector is {left_eigenvector}')

    if show is True:
      print(statement)
    return right_eigenvalue, right_eigenvector, left_eigenvalue, left_eigenvector


  def norm(self):
    norm = np.linalg.norm(self.A)
    return norm


  def checker(self, show=True):

    U, S, V = np.linalg.svd(self.A)

    if show is True:
      print(f'numpy svd output U = {U}, S = {S}, V = {V}')
    return U, S, V

  def U(self, show=True):
    U = self.checker(show=False)[0]

    return U

  def Alt_U(self, show=True):
    pass


  def S(self, recon_matrix=None ,show=True):
    if recon_matrix is None:
      S = self.checker(show=False)[1]

      full_S = np.zeros_like(self.A)

      for i in range(len(S)):
        full_S[i, i] = S[i]

      if show is True:
        print(full_S)
    else:
      S = recon_matrix
      
      full_S = np.zeros_like(self.A)

      for i in range(len(S)):
        full_S[i, i] = S[i]
        
      if show is True:
        print(full_S)
    return full_S

  def V(self, show=True):
    V = self.checker(show=False)[2]
    if show is True:
      print(V)
    return V

  def reconstructor(self, reduced_S=None,show=True):
    if reduced_S is None:
      matrix = self.U(show=False) @ self.S(show=False) @ self.V(show=False)
        
    else:
      matrix = self.U(show=False) @ reduced_S @ self.V(show=False)
      
    if show is True:
      print(matrix)
    return matrix

  def smallest_reduction(self, norm_value, show=True):

    S = self.checker(show=False)[1]
    full_S = self.S(show=False)
    k = []

    for i in reversed(range(len(S))):
      full_S[i, i] = 0

      Ak = self.U(show=False) @ full_S @ self.V(show=False)

      error = np.linalg.norm(self.A - Ak)

      if error < norm_value:
         k.append([error, i, Ak])

    statement = str(f'the error is {k[-1][0]}, \n k is {k[-1][1]}, \n Ak is {k[-1][2]}')

    print(statement)
    

  def min_singular_compression(self, target_percent, singular_values=None, show=True):

    if singular_values is None:

      singular_values = [x**2 for x in self.checker(show=False)[1]]

      number_values = len(singular_values)

      total = np.sum(singular_values)

      percent = []
      for i in reversed(range(len(singular_values) - 1 )):

        singular_values = np.delete(singular_values, -1)

        current_percent = (np.sum(singular_values) / total)

        if target_percent < current_percent:
          percent.append([np.sum(singular_values) / total, i + 1])


      try:
        statement = str(f'The quality retained is {percent[-1][0]}% \n The number of singular values retained is {percent[-1][1]} out of {number_values}')

        if show is True:
          print(statement)
      except:
        print('No rows could be deleted, try lower target percent')

    else:
      singular_values = [x**2 for x in singular_values]

      number_values = len(singular_values)

      total = np.sum(singular_values)
      # print(total)
      percent = []
      for i in reversed(range(len(singular_values) - 1)):

        singular_values = np.delete(singular_values, -1)

        current_percent = (np.sum(singular_values) / total)
        # print(current_percent)
        if target_percent < current_percent:
          percent.append([np.sum(singular_values) / total, i + 1])

      try:
        statement = str(f'The quality retained is {percent[-1][0]}% \n The number of singular values retained is {percent[-1][1]} out of {number_values}')

        if show is True:
          print(statement)
      except:
        print('No rows could be deleted, try lower target percent')
        

  def k_many_reduction_variance(self, k, singular_values=None, rebuild=True, show=True):

      if singular_values is None:
        
          singular_values = [x**2 for x in self.checker(show=False)[1]]

          k_to_reduce = len(singular_values) - k

          total = np.sum(singular_values)

          current_percent = (np.sum(singular_values[0:k]) / total)
          
          statement = (f'The quality retained is {current_percent}% \n The number of singular values retained is {k}')
          
          retained_values = [x**(1/2) for x in singular_values]
          
          if show is True:
            print(statement)
          
          if rebuild is True:
            return(retained_values)
             
      else:
          if k < len(singular_values):
            singular_values = [x**2 for x in singular_values]

            k_to_reduce = len(singular_values) - k

            total = np.sum(singular_values)

            for i in range(k_to_reduce):
              singular_values = np.delete(singular_values, -1)

            current_percent = (np.sum(singular_values) / total)

            statement = (f'The quality retained is {current_percent}% \n The number of singular values retained is {k}')

            if show is True:
              print(statement)
              
  def image_compression(self , k, color=False, show=True, save=False):
    
    if color is True:
      
      singular_values = []
      U_values = []
      V_values = []
      for matrix in self.A:
        
        U_image, S_image, V_image = np.linalg.svd(matrix)
        singular_values.append(S_image)
        U_values.append(U_image)
        V_values.append(V_image)
        
        
      matricies = [np.array(matrix[0:k]) for matrix in singular_values]
      
      back_to_fool = []
      for i in range(len(matricies)):
        
        S = matricies[i]
      
        full_S = np.zeros_like(self.A[0])

        for j in range(len(S)):
          full_S[j, j] = S[j]
        back_to_fool.append(full_S)
        
      to_be_stacked = [U_values[i] @ back_to_fool[i] @ V_values[i] for i in range(len(back_to_fool))]
        
      image_reduced = matrix_to_image(to_be_stacked, color=True, show=True, save=save)
      
    
      
    else:
       
      reduced_to_k = self.k_many_reduction_variance(k, show=False)
    
      reduced = self.S(recon_matrix=reduced_to_k, show=False)
    
      reduced_image_matrix = self.reconstructor(reduced_S=reduced, show=False)
      
      image_reduced = matrix_to_image(reduced_image_matrix, color=color)



