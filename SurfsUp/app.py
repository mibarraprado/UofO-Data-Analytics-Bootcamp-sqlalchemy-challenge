# 1. import Flask
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Honolulu,Hawaii climate analysis!"


@app.route("/api/v1.0/precipitation")
def precipitations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query last 12 months of precipitations
    recent_date = max(session.query(Measurement.date).all())
    most_recent_date= datetime.strptime(recent_date[0], '%Y-%m-%d').date()
    year_ago = most_recent_date - relativedelta(months=12)
    sel = [Measurement.date, Measurement.prcp]
    data = session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) > year_ago).all()
    session.close()
    # Create a dictionary from the row data and append to a list of all_precipitations
    L12M_precipitations = []
    for date, prcp in data:
        precipitations_data_dict = {}
        precipitations_data_dict["date"] = date
        precipitations_data_dict["prcp"] = prcp
        L12M_precipitations.append(precipitations_data_dict)

    return jsonify(L12M_precipitations)

@app.route("/api/v1.0/stations")
def station_names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all passengers
    results = session.query(Station.name).all()
    session.close()

    # Convert list of tuples into normal list
    all_station_names = list(np.ravel(results))

    return jsonify(all__station_names)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query last 12 months of TOBs for most-active station
    recent_date = max(session.query(Measurement.date).all())
    most_recent_date= datetime.strptime(recent_date[0], '%Y-%m-%d').date()
    year_ago = most_recent_date - relativedelta(months=12)
    sel = [Measurement.date, Measurement.tobs]
    data_temp = session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) > year_ago).\
    filter(Measurement.station=='USC00519281').all()
    # Create a dictionary from the row data and append to a list of all_precipitations
    L12M_tobs = []
    for date, tobs in data_temp:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        L12M_tobs.append(tobs_dict)

    return jsonify(L12M_tobs)

@app.route("/api/v1.0/<start>")
def start_date():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query of TOBs for most-active station form start_date
    
    start_date = dt.datetime(2011, 5, 31)
    sel = [Measurement.station,
       func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)
      ]
    station_USC00519281 = session.query(*sel).group_by(Measurement.station).\
    filter(Measurement.date >= start_date).\
    filter(Measurement.station == 'USC00519281').all()
    # Create a dictionary from the row data and append to a list of all_precipitations
    LM_tobs = []
    for station,tmin,tmax,tavg in station_USC00519281:
        tobs_dict = {}
        tobs_dict["station"] = date
        tobs_dict["Tmin"] = Tmin
        tobs_dict["Tmax"] = Tmax
        tobs_dict["Tavg"] = Tavg
        LM_tobs.append(tobs_dict)

    return jsonify(LM_tobs)

@app.route("/api/v1.0/<start>/<end>")
def start_date():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query of TOBs for most-active station form start_date
    
    start_date = dt.datetime(2011, 5, 31)
    end_date = dt.datetime(2011, 5, 31)
    sel = [Measurement.station,
       func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)
      ]
    station_USC00519281 = session.query(*sel).group_by(Measurement.station).\
    filter(Measurement.date >= start_date && Measurement.date < end_date ).\
    filter(Measurement.station == 'USC00519281').all()
    # Create a dictionary from the row data and append to a list of all_precipitations
    LM_tobs = []
    for station,tmin,tmax,tavg in station_USC00519281:
        tobs_dict = {}
        tobs_dict["station"] = date
        tobs_dict["Tmin"] = Tmin
        tobs_dict["Tmax"] = Tmax
        tobs_dict["Tavg"] = Tavg
        LM_tobs.append(tobs_dict)

    return jsonify(LM_tobs)

if __name__ == '__main__':
    app.run(debug=True)
