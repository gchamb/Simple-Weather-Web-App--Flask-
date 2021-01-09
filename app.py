
from flask import Flask, request,render_template, url_for
import requests
import os


app = Flask(__name__,template_folder = "templates")
app.static_folder = 'static'

URL ='http://api.weatherapi.com/v1/current.json'
KEY = 'e590a6cc621e49c4a6845113202712'



@app.route("/")
def index():
        return render_template("index.html",)

@app.route('/weather', methods = ["POST", "GET"])
def displayWeather():
      if request.method == 'POST':
        try:
            query = request.form.get('city')
            params = {"key": KEY, "q" : query}
            r = requests.get(URL,params=params)
            data = r.json()

            city = data['location']['name']
            temp = data['current']['temp_f']
            clouds = data['current']['condition']['text']
            feelsLike = data['current']['feelslike_f']
            icon = data['current']['condition']['icon']
            return render_template('weather.html',city=city,temp=temp,clouds=clouds,feelsLike=feelsLike,icon=icon)
        except:
            return render_template("failure.html")

 
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == "__main__":
    app.run(debug = True)