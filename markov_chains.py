import numpy as np
from supplemental_functions import numpy_array


class Markoff_chainz():

  def __init__(self, A):
    self.A = A

  def matrix_power(self, power, show=True):
    count = power
    multi = self.A
    while count > 1:
      multi = multi @ self.A
      count -= 1

    if show is True:
      print(multi)
    return multi

  def time_step_with_initial(self, time_steps ,initial, rounding=4, show=True):
    stepped_A = self.matrix_power(time_steps, show=False)

    if show is True:
      print(np.round((stepped_A @ initial), rounding))
      
    return np.round((stepped_A @ initial), rounding)

  def eigens(self):
    eigenvalue, eigenvector = np.linalg.eig(self.A)
    statement = print(f'the eiginvalues are {eigenvalue} \n the corresponding eiginvectors are {eigenvector}')
    return statement

  def steady_state(self, rounding=4, show=True):

    eigenvalue, eigenvector = np.linalg.eig(self.A)
    try:
      one_value = np.where(np.isclose(eigenvalue, 1))

    except ValueError:
      print('check your matrix is written correctly')

    eigenvector[:, one_value]

    normalized = eigenvector[:, one_value] / np.sum(eigenvector[:, one_value])

    if show is True:
      print(np.round(normalized.real, rounding))

    return np.round(normalized.real, rounding)

  def smallest_k(self, num_iters, initial, rounding=4):
    steady_state = np.reshape(self.steady_state(rounding, show=False), len(self.steady_state(rounding, show=False)))
    initial_attempt = num_iters

    for iter in range(num_iters):
      k_time = np.round(self.time_step_with_initial(iter, initial, show=False), rounding)
      k_time = np.reshape(k_time, len(k_time))

      if np.array_equal(steady_state, k_time):
        statement = print(f'the smallest value of k is {iter}')
        break
        return statement

      elif iter + 1 == initial_attempt and not np.array_equal(steady_state, k_time):
        statement = print(f'Number of iterations too small, increase magnitude, last matrix in step was {k_time} on the {iter + 1} iteration')
        return statement

# Google matrix which uses markov chains to find page ranking, dangling node True when node does not point outward
  def Google(self, alpha, dangling_node=True, show=True):
    if dangling_node is True:
      for i in range(len(self.A)):
        if np.sum(self.A[:,i]) == 0:
          self.A[:,i] = (1/ len(self.A))

    rank = (1/ len(self.A)) * np.ones((len(self.A), len(self.A)))
    G = alpha * rank + (1 - alpha) * self.A

    if show is True:
      print(G)

    return G

  def Google_steady_state(self, alpha, show=True):
    G = self.Google(alpha, show=False)

    eigenvalue, eigenvector = np.linalg.eig(G)

    try:
      one_value = np.where(np.isclose(eigenvalue, 1))


    except ValueError:
      print('check your matrix is written correctly')

    eigenvector[:, one_value]

    normalized = eigenvector[:, one_value] / np.sum(eigenvector[:, one_value])

    if show is True:
      print(np.round(normalized.real, 4))

    return np.round(normalized.real, 4)

  def PageRank(self, alpha, show=True):
    rankings = self.Google_steady_state(alpha, show=False)

    ranked_dict = {x + 1: rankings[x] for x in range(len(rankings))}

    sorted_rankings = sorted(ranked_dict.items(), key=lambda x: x[1], reverse=True)

    ranked_list = list(dict(sorted_rankings).keys())

    if show is True:
        print(ranked_list)
    
    return ranked_list


