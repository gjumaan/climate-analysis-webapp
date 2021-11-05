# Import dependencies
from flask import Flask, request, redirect, render_template, jsonify
from sqlalchemy.sql.expression import null

# Import route functions
from routes import precipitation, stations, tobs, start_date, start_end_date

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#Create a welcome page route
@app.route("/")
def welcome():
    return render_template(
        "index.html"
    )

#Create a route that shows precipitation data
@app.route('/api/v1.0/precipitation')
def call_precipitation():
    return (
        jsonify(precipitation())
    )

#Create a route that shows all available stations
@app.route('/api/v1.0/stations')
def call_stations():
    return (
        jsonify(stations())
    )

#Create a route that shows TOBS data for the most active station
@app.route('/api/v1.0/tobs')
def call_tobs():
    return (
        jsonify(tobs())
    )

#Create a function that accepts either a single date input or a ranged date input from the front-end and re-directs to the appropirate route 
@app.route('/', methods=['GET','POST'])
def get_start_date_input():
    print(request.form.get('date'))
    if request.form['action'] == 'start':
        if bool(request.form.get('date').strip()):
            date = request.form.get('date')
            return redirect('/api/v1.0/' + date)
        return ('',204)
    elif request.form['action'] == 'start-end':
        if bool(request.form.get('start-date').strip() and request.form.get('end-date').strip()):
            date_1 = request.form.get('start-date')
            date_2 = request.form.get('end-date')
            return redirect(f'/api/v1.0/{date_1}/{date_2}')
        return ('', 204)

#Create a route that shows TMIN, TMAX, TAVG for a given start-date input
@app.route('/api/v1.0/<start>')
def call_start_date(start):
    return (
        jsonify(start_date(start))
    )

#Create a route that shows TMIN, TMAX, TAVG for a given start-end date input
@app.route('/api/v1.0/<start>/<end>')
def call_start_end_date(start, end):
    return (
        jsonify(start_end_date(start, end))
    )

if __name__ == '__main__':
   app.run(debug=True)

