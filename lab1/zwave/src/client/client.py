from time import sleep
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template("index.html")


@app.route('/network.html', methods=['GET', 'POST'])
def network():
    network_info_obj = requests.get('http://192.168.1.2:5000/network/info').json()
    return render_template("network.html", network=network_info_obj, network_size=len(network_info_obj)-1)


@app.route('/networkConfig.html', methods=['GET', 'POST'])
def network_config():
    if request.method == 'POST':
        group1_interval = request.form['group1Interval']
        group1_report = request.form['group1Report']
        wakeup_interval = request.form['wakeupInterval']
        requests.post(
            'http://192.168.1.2:5000/network/set_sensor_nodes_basic_configuration',
            json={
                "Group_Interval": group1_interval,
                "Group_Reports": group1_report,
                "Wake-up_Interval": wakeup_interval
            }
        )
        sleep(5)

    network_obj = requests.get('http://192.168.1.2:5000/network/get_nodes_configuration').json()
    return render_template("networkConfig.html", network=network_obj, network_size=len(network_obj)-1)


@app.route('/nodes.html')
def nodes():
    nodes_obj = requests.get('http://192.168.1.2:5000/nodes/get_nodes_list').json()
    return render_template("nodes.html", nodes=nodes_obj, nodes_len=len(nodes_obj))


@app.route('/sensors.html')
def sensors():
    sensors_obj = requests.get('http://192.168.1.2:5000/sensors/get_sensors_list').json()
    return render_template("sensors.html", nodes=sensors_obj, nodes_len=len(sensors_obj))


@app.route('/nodeMeasures.html')
def sensor_measures():
    node_id = request.args.get("nodeid", 0)
    if node_id != 0:
        node_temperature = requests.get('http://192.168.1.2:5000/sensors/' + str(node_id) + '/get_temperature').json()
        node_humidity = requests.get('http://192.168.1.2:5000/sensors/' + str(node_id) + '/get_humidity').json()
        node_luminance = requests.get('http://192.168.1.2:5000/sensors/' + str(node_id) + '/get_luminance').json()
        node_motion = requests.get('http://192.168.1.2:5000/sensors/' + str(node_id) + '/get_motion').json()
        node_all_measures = requests.get('http://192.168.1.2:5000/sensors/' + str(node_id) + '/get_all_measures').json()
        node = {
            'id': node_id,
            'temperature': node_temperature,
            'luminance': node_luminance,
            'humidity': node_humidity,
            'motion': node_motion,
            'all_measures': node_all_measures
        }
        return render_template("nodeMeasures.html", node=node)


@app.route('/actuatorLevel.html', methods=["GET", "POST"])
def actuator_level():
    node_id = request.args.get("nodeid", 0)
    actuator_obj = requests.get('http://192.168.1.2:5000/dimmers/' + str(node_id) + '/get_level').json()
    node = {
        'id': node_id,
        'actuator': actuator_obj
    }
    if request.method == "POST":
        new_level_val = request.form['actuatorLevel']
        requests.post(
            'http://192.168.1.2:5000/dimmers/set_level',
            json={
                "node_id": node_id,
                "value": new_level_val
            }
        )
        node['actuator']['value'] = new_level_val

    return render_template("actuatorLevel.html", node=node)


@app.route('/actuators.html')
def actuators():
    actuators_obj = requests.get('http://192.168.1.2:5000/dimmers/get_dimmers_list').json()
    return render_template("actuators.html", nodes=actuators_obj, nodes_len=len(actuators_obj))


@app.route('/networkEditConfig.html')
def network_edit_config():
    return render_template("networkEditConfig.html")


@app.route('/404.html')
def page404():
    return render_template("404.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.route('/network/get_nodes_configuration')
def get_nodes_configuration():
    nodes_config = requests.get('http://192.168.1.2:5000/network/get_nodes_configuration').json()
    return jsonify(nodes_config)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3001)

