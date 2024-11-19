# read file
def input_file(file_name):
  with open(file_name) as f:
    learning_rate = float(f.readline().strip("\n"))
    threshold = float(f.readline().strip("\n"))
    bias = int(f.readline().strip("\n"))

    training_data = [[int(x) for x in line.split()] for line in f]

  return learning_rate, threshold, bias, training_data

def separate_data(item, z_list, bias):
  z_item = item.pop()
  z_list.append(z_item)
  item.append(bias)

# compute for perceptron value, a
def compute_perceptron(item, weights, outer_index, a_list):
  a_sum = 0
  a_index = 0
  for data in item:
    a_sum += (data*weights[outer_index][a_index])
    a_index += 1

  a_list.append(a_sum)

  return a_sum

# compute for y-value
def compute_y(y_list, a_sum, threshold):
  y_data = 1 if a_sum >= threshold else 0
  y_list.append(y_data)

  return y_data

# will just be appended to the list of weights (2d list)
def adjust_weights(weights, outer_index, item, learning_rate, z_list, y_data):
  new_weights = []
  weights_index = 0
  for x_sub_p in item:
    wc = weights[outer_index][weights_index]
    # print(f"w{weights_index} = {weights[outer_index][weights_index]} + ({learning_rate})({x_sub_p})({z_list[outer_index]}-{y_data})")
    # rounding off after the value is computed
    new_weights.append(round(wc + learning_rate * x_sub_p * (z_list[outer_index] - y_data), 2))
    weights_index += 1

  weights.append(new_weights)

# check per column (first row not included) if equal using the second row as basis
def check_if_converges(weights):
  weight_converges = True
  compare_weights = weights[1]
  for i in range(2, len(weights)):
    if compare_weights != weights[i]:
      return not weight_converges
    
  return weight_converges

# reset weights and the last row will be the first data of the weights list
def did_not_converge(weights):
  final_adjusted_weight = weights.pop()
  weights = []
  weights.append(final_adjusted_weight)

  return weights 

def print_data(data):
  for i in data:
    print(i)