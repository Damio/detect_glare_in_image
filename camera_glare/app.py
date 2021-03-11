from flask import Flask, jsonify, Flask, redirect, render_template, url_for, request
from flask_expects_json import expects_json

# Custom class built for project
from camera_glare.glare_checker import GlareCheck

app = Flask(__name__)

# define a schema to ensure valid input data
schema = {

    'type': 'object',
    'properties': {
        'lat': {'type': 'number', 'minimum': -90, 'maximum': 90},
        'lon': {'type': 'number', 'minimum': -180, 'maximum': 180},
        'epoch': {'type': 'number', 'minimum': 0},
        'orientation': {'type': 'number', 'minimum': -180, 'maximum': 180}
        },
    'required': ['lat', 'lon', 'epoch', 'orientation']
    
    }

# homepage to test random entry input
@app.route("/")
def index():
    """ Renders the index.html page"""

    return render_template("index.html")

@app.route('/result/<result>')
def result(result):
   return render_template("result.html", result=result)


@app.route("/detect_glare" , methods=["POST", "GET"])
#pects_json(schema)
def check_glare():
    """ Recieves a request to process if there is glare in an image
    using the metadata provided. Return the result, using the custom 
    GlareCheck class"""
    if request.method == "POST":
        # read the data
        json_data = request.json
        lat = json_data["lat"]
        lon = json_data["lon"]
        epoch = json_data["epoch"]
        orientation = json_data["orientation"]

        # create an instance of the GlareCheck class 
        # & get the az, and alt
        az, alt = GlareCheck(lat, lon, epoch, orientation).altittude_azimuth()
        
        # check if Az diff is <30 and sun alt is < 45, then 
        glare = True if az<30 and alt<45 else False
        
        return jsonify({
            "glare": glare
            })

    # checks if this comes from our webpage
    if request.method == "GET":
        json_data = request.args
        lat = float(json_data["lat"])
        lon = float(json_data["lon"])
        epoch = float(json_data["epoch"])
        orientation = float(json_data["ori"])

        print(lat,lon,epoch,orientation)

        az, alt = GlareCheck(lat, lon, epoch, orientation).altittude_azimuth()

        glare = True if az<30 and alt<45 else False
        
        return redirect(url_for('result',result = glare))




# for testing
@app.route("/ping")
def ping():
    """ responds with a simple json to test the API"""

    return jsonify({"res": "pong"})


@app.route('/find_glare_web',methods = ['POST'])
def find_glare_web():
    lat = request.form['lat']
    lon = request.form['lon']
    epoch = request.form['epoch']
    orientation = request.form['ori']

    return redirect(url_for('result',result = "fish"))



if __name__ == "__main__":
    app.run(debug=True)