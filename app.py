from flask import Flask, render_template, url_for, request
import mysql.connector as mc
import joblib

app = Flask(__name__)

model = joblib.load('./models/randomforest_model.lb')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/project_form')
def project_form():
    return render_template('project.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        age = float(request.form.get('age', 0))
        bmi = float(request.form.get('bmi', 0))
        child = int(request.form.get('child', 0))
        gender = request.form.get('gender', 'unknown')
        gender_male = 1 if gender == 'Male' else 0

        smoker_yes = int(request.form.get('smoker_yes', 0))
            
        region_type = request.form.get('region', 'unknown')

        region_northwest = 0
        region_southeast = 0
        region_southwest = 0
            
        if region_type == 'northwest':
                region_northwest = 1
        elif region_type == 'southeast':
                region_southeast = 1
        elif region_type == 'southwest':
                region_southwest = 1

        UNSEEN_DATA = [[
                age, bmi, child, gender_male, smoker_yes,
                region_northwest, region_southeast, region_southwest
            ]]

        prediction = model.predict(UNSEEN_DATA)[0]

        return render_template('output.html', 
                age=age, 
                bmi=bmi, 
                child=child, 
                gender_male=gender_male, 
                smoker_yes=smoker_yes, 
                region_northwest=region_northwest, 
                region_southeast=region_southeast, 
                region_southwest=region_southwest, 
                insurance_charges=prediction
        )

if __name__ == '__main__':
    app.run(debug=True)
