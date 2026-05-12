def load_mnist_data():
    from sklearn.datasets import fetch_openml
    import numpy as np
    from sklearn.model_selection import train_test_split

    # Load MNIST dataset
    mnist = fetch_openml('mnist_784', version=1)
    X = np.array(mnist.data)
    y = np.array(mnist.target)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test

def preprocess_data(X):
    # Normalize the data to the range [0, 1]
    X_normalized = X / 255.0
    return X_normalized

def get_class_distribution(y):
    unique, counts = np.unique(y, return_counts=True)
    return dict(zip(unique, counts))