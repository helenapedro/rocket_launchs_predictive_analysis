import os
import dash
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash import dcc, html, Input, Output
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import time
import cProfile
import pstats

# Function to load data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return None

# Construct the absolute path to the CSV file
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, '../data/dataset_part_2.csv')
xdata_path = os.path.join(base_dir, '../data/dataset_part_3.csv')

# Load datasets
data = load_data(data_path)
X = load_data(xdata_path)
if data is None or X is None:
    raise Exception("Failed to load datasets")

Y = data['Class'].to_numpy()

# Identify and drop non-numeric columns (such as dates) for standardization
numeric_columns = X.select_dtypes(include=[np.number]).columns
X_numeric = X[numeric_columns]

# Standardize the numeric data
scaler = preprocessing.StandardScaler()
X_standardized = scaler.fit_transform(X_numeric)

# Convert non-numeric columns to ordinal values if needed
X_dates = X.select_dtypes(include=['object'])
X_dates_converted = X_dates.apply(lambda col: pd.to_datetime(col, format='%Y-%m-%d', errors='coerce')).fillna(pd.Timestamp('1970-01-01')).map(pd.Timestamp.toordinal)

# Combine standardized numeric data and converted date data
X_combined = pd.concat([pd.DataFrame(X_standardized, columns=numeric_columns), X_dates_converted], axis=1)

# Logging time for each step
start_time = time.time()
X_train, X_test, Y_train, Y_test = train_test_split(X_combined, Y, test_size=0.2, random_state=2)
print(f"Data split in {time.time() - start_time:.2f} seconds")

# Define models and parameters
models = {
    'Logistic Regression': {
        'model': LogisticRegression(max_iter=200, solver='liblinear'),
        'params': {
            'C': [0.01, 0.1, 1],
            'penalty': ['l2']
        }
    },
    'Support Vector Machine': {
        'model': SVC(),
        'params': {
            'C': np.logspace(-3, 3, 5),
            'kernel': ['linear', 'rbf', 'poly', 'sigmoid'],
            'gamma': np.logspace(-3, 3, 5)
        }
    },
    'Decision Tree': {
        'model': DecisionTreeClassifier(),
        'params': {
            'criterion': ['gini', 'entropy'],
            'splitter': ['best', 'random'],
            'max_depth': [2 * n for n in range(1, 10)]
        }
    },
    'K-Nearest Neighbors': {
        'model': KNeighborsClassifier(),
        'params': {
            'n_neighbors': range(1, 11),
            'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
            'p': [1, 2]
        }
    }
}

# Use cProfile to profile the model fitting process
profiler = cProfile.Profile()
profiler.enable()

# Perform GridSearchCV and store results
results = {}
for name, model_info in models.items():
    start_time = time.time()
    grid = GridSearchCV(estimator=model_info['model'], param_grid=model_info['params'], cv=10, n_jobs=-1)
    grid.fit(X_train, Y_train)
    elapsed_time = time.time() - start_time
    print(f"{name} model fit in {elapsed_time:.2f} seconds")
    Y_pred = grid.predict(X_test)
    acc_score = accuracy_score(Y_test, Y_pred)
    conf_matrix = confusion_matrix(Y_test, Y_pred)
    results[name] = {
        'best_params': grid.best_params_,
        'best_score': grid.best_score_,
        'test_score': grid.score(X_test, Y_test),
        'accuracy_score': acc_score,
        'confusion_matrix': conf_matrix,
        'fit_time': elapsed_time
    }


# Print out profiling results
ps = pstats.Stats(profiler).sort_stats('cumtime')
ps.print_stats()

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Machine Learning Model Comparison'),
    dcc.Dropdown(
        id='model-dropdown',
        options=[{'label': name, 'value': name} for name in models.keys()],
        value='Logistic Regression'
    ),
    html.Div(id='model-info'),
    dcc.Graph(id='comparison-graph')
])

@app.callback(
    [Output('model-info', 'children'), Output('comparison-graph', 'figure')],
    [Input('model-dropdown', 'value')]
)
def update_output(selected_model):
    info = results[selected_model]
    model_details = html.Div([
        html.H4(f"{selected_model} Results"),
        html.P(f"Best Parameters: {info['best_params']}"),
        html.P(f"Best Cross-Validation Accuracy: {info['best_score']:.4f}"),
        html.P(f"Test Accuracy: {info['test_score']:.4f}"),
        html.P(f"Accuracy Score: {info['accuracy_score']:.4f}"),
        html.P(f"Confusion Matrix: {info['confusion_matrix']}")
    ])

    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(results.keys()), y=[res['best_score'] for res in results.values()], name='Cross-Validation Accuracy'))
    fig.add_trace(go.Bar(x=list(results.keys()), y=[res['test_score'] for res in results.values()], name='Test Accuracy'))
    fig.update_layout(title='Model Accuracy Comparison', barmode='group', xaxis_title='Model', yaxis_title='Accuracy')

    return model_details, fig

if __name__ == '__main__':
    app.run_server(debug=True)
