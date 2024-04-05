###### Your ID ######
# ID1: 322548660
# ID2: 211827555
#####################

# imports 
import numpy as np
import pandas as pd

def preprocess(X,y):
    """
    Perform mean normalization on the features and true labels.

    Input:
    - X: Input data (m instances over n features).
    - y: True labels (m instances).

    Returns:
    - X: The mean normalized inputs.
    - y: The mean normalized labels.
    """
    ###########################################################################
    # TODO: Implement the normalization function.                             #
    ###########################################################################
    meanX = np.average(X)
    maxX = np.max(X)
    minX = np.min(X)
    X = (X - meanX)/(maxX - minX) # Replace each instance for features based on mean normalization
    
    meanY = np.average(y)
    maxY = np.max(y)
    minY = np.min(y)
    y = (y - meanY)/(maxY - minY) # Replace each instance for targets based on mean normalization
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return X, y

def apply_bias_trick(X):
    """
    Applies the bias trick to the input data.

    Input:
    - X: Input data (m instances over n features).

    Returns:
    - X: Input data with an additional column of ones in the
        zeroth position (m instances over n+1 features).
    """
    ###########################################################################
    # TODO: Implement the bias trick by adding a column of ones to the data.                             #
    ###########################################################################      
    rows = X.shape[0]
    new_column = np.ones((rows, 1))
    X = np.column_stack((new_column, X))
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return X

def compute_cost(X, y, theta):
    """
    Computes the average squared difference between an observation's actual and
    predicted values for linear regression.  

    Input:
    - X: Input data (m instances over n features).
    - y: True labels (m instances).
    - theta: the parameters (weights) of the model being learned.

    Returns:
    - J: the cost associated with the current set of parameters (single number).
    """
    
    J = 0  # We use J for the cost.
    ###########################################################################
    # TODO: Implement the MSE cost function.                                  #
    ###########################################################################
    m = X.shape[0] # represents the number of instances in X

    MultResult = np.dot(X, theta) # X * Theta
    delta = MultResult - y # h(X) - y
    deltaSquare = delta ** 2 
    J = np.sum((1 / (2 * m)) * deltaSquare)

    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return J

def gradient_descent(X, y, theta, alpha, num_iters):
    """
    Learn the parameters of the model using gradient descent using 
    the training set. Gradient descent is an optimization algorithm 
    used to minimize some (loss) function by iteratively moving in 
    the direction of steepest descent as defined by the negative of 
    the gradient. We use gradient descent to update the parameters
    (weights) of our model.

    Input:
    - X: Input data (m instances over n features).
    - y: True labels (m instances).
    - theta: The parameters (weights) of the model being learned.
    - alpha: The learning rate of your model.
    - num_iters: The number of updates performed.

    Returns:
    - theta: The learned parameters of your model.
    - J_history: the loss value for every iteration.
    """
    
    theta = theta.copy() # optional: theta outside the function will not change
    J_history = [] # Use a python list to save the cost value in every iteration
    ###########################################################################
    # TODO: Implement the gradient descent optimization algorithm.            #
    ###########################################################################
    m = X.shape[0] # represents the number of instances in X

    for i in range(num_iters):
        MultResult = np.dot(X, theta) # Theta*X 
        delta = MultResult - y # h(X) - y
        theta = theta - (alpha / m) * np.dot(X.T, delta) # Theta - (alpha / m) * X^t * (h(X) - y)
        J_history.append(compute_cost(X, y, theta))

    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return theta, J_history

def compute_pinv(X, y):
    """
    Compute the optimal values of the parameters using the pseudoinverse
    approach as you saw in class using the training set.

    #########################################
    #### Note: DO NOT USE np.linalg.pinv ####
    #########################################

    Input:
    - X: Input data (m instances over n features).
    - y: True labels (m instances).

    Returns:
    - pinv_theta: The optimal parameters of your model.
    """
    
    pinv_theta = []
    ###########################################################################
    # TODO: Implement the pseudoinverse algorithm.                            #
    ###########################################################################
    xTransposedTimesX = np.dot(X.T, X) # X^t * X
    pinv = np.dot(np.linalg.inv(xTransposedTimesX), X.T) # (X^t * X)^-1 * X^t
    pinv_theta = np.dot(pinv, y) # pinv * y

    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return pinv_theta

def efficient_gradient_descent(X, y, theta, alpha, num_iters):
    """
    Learn the parameters of your model using the training set, but stop 
    the learning process once the improvement of the loss value is smaller 
    than 1e-8. This function is very similar to the gradient descent 
    function you already implemented.

    Input:
    - X: Input data (m instances over n features).
    - y: True labels (m instances).
    - theta: The parameters (weights) of the model being learned.
    - alpha: The learning rate of your model.
    - num_iters: The number of updates performed.

    Returns:
    - theta: The learned parameters of your model.
    - J_history: the loss value for every iteration.
    """
    
    theta = theta.copy() # optional: theta outside the function will not change
    J_history = [] # Use a python list to save the cost value in every iteration
    ###########################################################################
    # TODO: Implement the efficient gradient descent optimization algorithm.  #
    ###########################################################################
    m = X.shape[0] # represents the number of instances in X

    for i in range(num_iters):
        MultResult = np.dot(X, theta) # X * Theta 
        delta = MultResult - y # h(X) - y
        theta = theta - (alpha / m) * np.dot(X.T, delta) # Theta - (alpha / m) * X^t * (h(X) - y)
        J_history.append(compute_cost(X, y, theta))

        if (len(J_history) > 1 and (J_history[-2] - J_history[-1] < 1e-8)): # Check if the diffrences between the 2 last costs is less then 1e-8
            break

    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return theta, J_history

def find_best_alpha(X_train, y_train, X_val, y_val, iterations):
    """
    Iterate over the provided values of alpha and train a model using 
    the training dataset. maintain a python dictionary with alpha as the 
    key and the loss on the validation set as the value.

    You should use the efficient version of gradient descent for this part. 

    Input:
    - X_train, y_train, X_val, y_val: the training and validation data
    - iterations: maximum number of iterations

    Returns:
    - alpha_dict: A python dictionary - {alpha_value : validation_loss}
    """
    
    alphas = [0.00001, 0.00003, 0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, 2, 3]
    alpha_dict = {} # {alpha_value: validation_loss}
    ###########################################################################
    # TODO: Implement the function and find the best alpha value.             #
    ###########################################################################
    base_theta = np.random.random(X_train.shape[1]) # getting a random 2D list of n features as guessed theta

    for alpha in alphas:
        theta, J_history = efficient_gradient_descent(X_train, y_train, base_theta, alpha, iterations)
        alpha_dict[alpha] = compute_cost(X_val, y_val, theta) 
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return alpha_dict

def forward_feature_selection(X_train, y_train, X_val, y_val, best_alpha, iterations):
    """
    Forward feature selection is a greedy, iterative algorithm used to 
    select the most relevant features for a predictive model. The objective 
    of this algorithm is to improve the model's performance by identifying 
    and using only the most relevant features, potentially reducing overfitting, 
    improving accuracy, and reducing computational cost.

    You should use the efficient version of gradient descent for this part. 

    Input:
    - X_train, y_train, X_val, y_val: the input data without bias trick
    - best_alpha: the best learning rate previously obtained
    - iterations: maximum number of iterations for gradient descent

    Returns:
    - selected_features: A list of selected top 5 feature indices
    """
    selected_features = []
    #####c######################################################################
    # TODO: Implement the function and find the best alpha value.             #
    ###########################################################################
    for round in range(5):
        costs_features_dict = {} # {feature: cost}
        min_cost_feature = -1
        base_theta = np.random.random(round + 2) # Needs to be changed each round since the amout of features is increasing by 1

        for feature in range(X_train.shape[1]):
            if feature not in selected_features:
                selected_features.append(feature) # Adding the feature into selected features table - temp

                train_feature, test_feature = X_train[:,selected_features], X_val[:,selected_features] # Selects only the columns based on the selected features 
                train_feature, test_feature = apply_bias_trick(train_feature), apply_bias_trick(test_feature) # Applying the bais trick

                theta, J_history = efficient_gradient_descent(train_feature, y_train, base_theta, best_alpha, iterations)
                costs_features_dict[feature] = compute_cost(test_feature, y_val, theta)

                selected_features.remove(feature) # Remove the feature from the selected features table

                if min_cost_feature == -1 or costs_features_dict[min_cost_feature] > costs_features_dict[feature]: # Maintaining the minimal cost feature
                    min_cost_feature = feature
        selected_features.append(min_cost_feature)
                
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return selected_features

def create_square_features(df):
    """
    Create square features for the input data.

    Input:
    - df: Input data (m instances over n features) as a dataframe.

    Returns:
    - df_poly: The input data with polynomial features added as a dataframe
               with appropriate feature names
    """

    df_poly = df.copy()
    ###########################################################################
    # TODO: Implement the function to add polynomial features                 #
    ###########################################################################
    pass
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return df_poly
