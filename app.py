from flask import Flask, render_template, request, session
import sklearn
import pickle
import secrets

with open('House_Price_Model.pkl', 'rb') as file:
    lin_reg = pickle.load(file)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route("/", methods=['GET', 'POST'])
def Home():
    # Retrieve the input values from the session
    input_values = session.pop('input_values', {})
    session.clear()
    session.modified = True
    return render_template('index.html', input_values=input_values)

@app.route('/prediction', methods=['POST'])
def Predict():
    bd = request.form.get('bedrooms')
    bth = request.form.get('bathrooms')
    slvng = request.form.get('sqftLiving')
    sl = request.form.get('sqftLot')
    fl = request.form.get('floors')
    wf = request.form.get('waterfront')
    vw = request.form.get('view')
    con = request.form.get('condition')
    sbsmnt = request.form.get('sqftBasement')
    yblt = request.form.get('yearBuilt')
    yrnvt = request.form.get('yearRenovated')

    # Store the input values in the session
    input_values = {
        'bedrooms': bd,
        'bathrooms': bth,
        'sqftLiving': slvng,
        'sqftLot': sl,
        'floors': fl,
        'waterfront': wf,
        'view': vw,
        'condition': con,
        'sqftBasement': sbsmnt,
        'yearBuilt': yblt,
        'yearRenovated': yrnvt
    }

    session['input_values'] = input_values

    try:
        bd = float(bd)
        bth = float(bth)
        slvng = float(slvng)
        sl = float(sl)
        fl = float(fl)
        wf = float(wf)
        vw = float(vw)
        con = float(con)
        sbsmnt = float(sbsmnt)
        yblt = float(yblt)
        yrnvt = float(yrnvt)

        input_data = [[bd, bth, slvng, sl, fl, wf, vw, con, sbsmnt, yblt, yrnvt]]
        predict = lin_reg.predict(input_data)

        # Pass the 'prediction' variable to the template
        return render_template('index.html', input_values=input_values, prediction=predict[0]*10)

    except ValueError as e:
        print(f"Error converting values to float: {e}")
        return "Error in form data. Please enter valid numerical values."

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
