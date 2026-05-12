# MNIST Handwritten Digits Classification

This project aims to classify handwritten digits from the MNIST dataset using machine learning models, specifically Decision Trees and Random Forests. The project is structured to facilitate both exploratory data analysis and hyperparameter tuning for optimal model performance.

## Project Structure

- **notebooks/**: Contains Jupyter notebooks for data exploration and model tuning.
  - `mnist_exploration.ipynb`: Exploratory data analysis and initial model training.
  - `hyperparameter_tuning.ipynb`: Hyperparameter tuning for Decision Tree and Random Forest models.

- **src/**: Contains source code for data handling, model definitions, and utility functions.
  - `data.py`: Functions for loading and preprocessing the MNIST dataset.
  - `model.py`: Model definitions and training functions for classifiers.
  - `utils.py`: Utility functions for data visualization and model evaluation.

- **requirements.txt**: Lists the dependencies required for the project.

- **.gitignore**: Specifies files and directories to be ignored by Git.

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/neeraj214/-classify-handwritten-digits.git
   cd -classify-handwritten-digits
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Launch Jupyter Notebook:
   ```
   jupyter notebook
   ```

4. Open the notebooks in the `notebooks/` directory to start exploring the data and tuning the models.

## Usage

- Use `mnist_exploration.ipynb` for initial data analysis and to understand the dataset.
- Use `hyperparameter_tuning.ipynb` to perform hyperparameter tuning on the Decision Tree and Random Forest models, including plotting accuracy vs. depth and generating classification reports.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.