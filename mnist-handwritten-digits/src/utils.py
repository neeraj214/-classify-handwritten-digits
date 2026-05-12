def plot_accuracy_vs_depth(depths, accuracies):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    plt.plot(depths, accuracies, marker='o')
    plt.title('Accuracy vs. Depth of Decision Tree')
    plt.xlabel('Depth of Decision Tree')
    plt.ylabel('Accuracy')
    plt.grid()
    plt.show()

def save_model(model, filename):
    import joblib
    joblib.dump(model, filename)

def load_model(filename):
    import joblib
    return joblib.load(filename)

def print_classification_report(y_true, y_pred):
    from sklearn.metrics import classification_report
    report = classification_report(y_true, y_pred)
    print(report)