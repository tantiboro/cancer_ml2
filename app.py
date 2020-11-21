import flask
import pickle
import pandas as pd

# Use pickle to load in the pre-trained model
with open(f'cancer_model', 'rb') as f:
    model = pickle.load(f)

# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')

# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('index.html'))
    
    if flask.request.method == 'POST':
        # Extract the input
        concave_points_worst = flask.request.form['concave_points_worst']
        area_worst = flask.request.form['area_worst']
        radius_worst = flask.request.form['radius_worst']
        perimeter_worst = flask.request.form['perimeter_worst']
        concave_points_mean = flask.request.form['concave_points_mean']

        # Make DataFrame for model
        input_variables = pd.DataFrame([[concave_points_worst, area_orst, radius_worst, perimeter_worst, concave_points_mean]],
                                       columns=['concave_point_worst', 'area_worst', 'radius_worst', 'perimeter_worst', 'concave_points_mean'],
                                       dtype=float,
                                       index=['input'])

        # Get the model's prediction
        prediction = model.predict(input_variables)[0]
    
        # Render the form again, but add in the prediction and remind user
        # of the values they input before
        return flask.render_template('main.html',
                                     original_input={'concave_points_worst':concave_points_worst,
                                                     'area_worst':area_worst,
                                                     'radius_worst':radius_worst,
                                                     'perimeter_worst':perimeter_worst,
                                                     'concave_points_mean':concave_points_mean},
                                     result=prediction,
                                     )

if __name__ == '__main__':
    app.run()