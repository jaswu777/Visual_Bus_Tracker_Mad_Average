from flask import Flask, render_template, jsonify, url_for, request
import json, requests, urllib2, time, datetime, calendar, urllib, re
app = Flask(__name__) 

@app.route("/")
def first_one():
	return "First one!"

@app.route("/lovely_markers/")
def second_one():
	return render_template('formformat.html')

@app.route("/lovely_markers/", methods = ['POST'])
def third_one():
	name = request.form['name']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	country = request.form['country']
	street = street.replace(" ", "_")
	city = city.replace(" ", "_")
	state = state.replace(" ", "_")
	country = country.replace(" ", "_")
	if name == "" or name == None:
		name = "random ass person"
	location_total = street + "," + city + "," + state + "," + country
	google_url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + location_total + "&sensor=false"
	google_data = json.loads(urllib2.urlopen(google_url).read())
	lat = google_data["results"][0]["geometry"]["location"]["lat"]
	lon = google_data["results"][0]["geometry"]["location"]["lng"]
	link = "http://runextbus.herokuapp.com/locations"
	data_parsed = json.loads(urllib2.urlopen(link).read())
	keys = []
	for i in data_parsed.keys():
		keys.append(i)
	latitude = []
	longitude = []
	bus_name = []
	for j in range(0, len(keys)):
		for i in range(0, len(data_parsed[keys[j]])):
			latitude.append(float(data_parsed[keys[j]][i]["lat"]))
			longitude.append(float(data_parsed[keys[j]][i]["lon"]))
			#return str(data_parsed[keys[j]][i]["lat"])
			#return str(data_parsed[keys[j]][i]["lon"])
			new = str(data_parsed[keys[j]][i]["dirtag"])
			new = re.compile("[^\w']|_").sub(" ", new)
			bus_name.append(new)
	#return str(len(latitude))
	#return jsonify(data_parsed)
	return render_template('mapmarkers.html', name = name, lat = lat, lon = lon, latitude = latitude, longitude = longitude, bus_name = json.dumps(bus_name))

if __name__ == '__main__':
	app.run(debug = True)