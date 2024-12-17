from flask import Flask, render_template, request
from get_weather_api import get_current_weather, get_forecast_weather
from get_coords_by_name import get_coords_by_name
from weather_assessment import weather_assessment


app = Flask(__name__)

@app.route("/")
def start():
    return 'Welcome'

@app.route('/weather', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        depart_city, arrived_city = list(request.form.values())
        try:
            depart_coords = get_coords_by_name(depart_city)
            arrived_coords = get_coords_by_name(arrived_city)
            print(depart_coords, arrived_coords)
        except:
            return 'One of cities not found'
        print(depart_coords.values())
        depart_weather = get_current_weather(*depart_coords.values())
        arrived_weather = get_forecast_weather(*arrived_coords.values())
        depart_assessment = weather_assessment(*depart_weather.values())
        arrived_assessments = [weather_assessment(*i[0].values())for i in arrived_weather]
        data = {
            'depart_city': depart_city,
            'arrived_city': arrived_city,
            'left_title1':'Now',
            'left_item5': f'Result: {depart_assessment}'
        }
        for i, m in enumerate(depart_weather.keys()):
            data['left_item'+str(i + 1)] = f'{m}:  {depart_weather[m]}'


        for i, m in enumerate(arrived_weather):
            data['right_title'+str(i + 1)] = m[1]
            for j, n in enumerate(m[0].keys()):
                data['right_item'+str(i + 1) +"_" + str(j + 1)] = f'{n}: {m[0][n]}'
            data['right_item'+str(i + 1) +"_" + str(j + 2)] = f"Result: {arrived_assessments[i]}"

        return render_template('ans.html', **data)
    return render_template('get_coords_by_city.html')


if __name__ == '__main__':
    app.run(debug=True, port = 5003)
