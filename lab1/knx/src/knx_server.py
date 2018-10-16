import argparse

from flask import Flask, request, jsonify

from KnxnetProtocol import KnxnetProtocol

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("-gwip", "--gateway_ip", help="Gateway ip", required=True)
parser.add_argument("-gwprt", "--gateway_port", help="Gateway port", required=True, type=int)
parser.add_argument("-endport", "--endpoint_port", help="Endpoint port", required=True, type=int)

args = parser.parse_args()

gateway_ip = args.gateway_ip
gateway_port = args.gateway_port
endpoint_port = args.endpoint_port

data_endpoint = ('0.0.0.0', 3672)
control_endpoint = ('0.0.0.0', 3672)

print("Gateway ip: ", gateway_ip)
print("Gateway port: ", gateway_port)


"""
@api {get} /valve/<floor>/<bloc>
@apiName get_valve
@apiGroup Valves

@apiParam {int} floor Floor number
@apiParam {int} bloc Bloc number

@apiSuccess {String} action Action description
@apiSuccess {int} bloc Bloc number
@apiSuccess {int} floor Floor number
@apiSuccess {int} value Valve's value

@apiSuccessExample {json} Example of result in case of success:
{
    "action": "Get valve value",
    "bloc": 2,
    "floor": 4,
    "value": 100
}
@apiDescription Get information on given valve in JSON format

@apiErrorExample {json} Error during knx connection
     {
       "error": "Error occured: knx.connect()"
     }
@apiErrorExample {json} Error during knx read
     {
       "error": "Error occured: knx.read()"
     }
@apiErrorExample {json} Error during knx disconnection
     {
       "error": "Error occured: knx.disconnect()"
     }

"""
"""
@api {post} /valve/<floor>/<bloc>
@apiName set_valve
@apiGroup Valves

@apiParam {int} floor Floor number
@apiParam {int} bloc Bloc number

@apiParamExample {json} Request-Exemple :
    {
        "new_value": 100
    }

@apiSuccess {String} action Action description
@apiSuccess {int} bloc Bloc number
@apiSuccess {int} floor Floor number
@apiSuccess {int} value Valve's value

@apiSuccessExample {json} Example of result in case of success:
{
    "action": "Set valve value",
    "bloc": 2,
    "floor": 4,
    "value": 100
}
@apiDescription Set value of given valve

@apiErrorExample {json} Error during knx connection
     {
       "error": "Error occured: knx.connect()"
     }
@apiErrorExample {json} Error during knx write
     {
       "error": "Error occured: knx.write()"
     }
@apiErrorExample {json} Error during knx disconnection
     {
       "error": "Error occured: knx.disconnect()"
     }

"""
@app.route('/valve/<int:floor>/<int:bloc>', methods=['GET', 'POST'])
def valve(floor, bloc):
    knx = KnxnetProtocol(gateway_ip, gateway_port, endpoint_port, data_endpoint, control_endpoint)
    if knx.connect() == -1:
        return jsonify(error="Error occured: knx.connect()")

    if request.method == 'POST':
        new_value = request.get_json()['new_value']
        grp_addr = '0/' + str(floor) + '/' + str(bloc)
        if knx.write(grp_addr, new_value) == -1:
            return jsonify(error="Error occured: knx.write()")
        value = new_value
        action = "Set valve value"
    else:
        grp_addr = '0/' + str(floor) + '/' + str(bloc)
        valve_value = knx.read(grp_addr)
        if valve_value == -1:
            jsonify(error="Error occured: knx.read()")
        value = valve_value
        action = "Get valve value"

    if knx.disconnect() == -1:
        jsonify(error="Error occured: knx.disconnect()")
    return jsonify(action=action, floor=floor, bloc=bloc, value=value)


"""
@api {get} /blind/<floor>/<bloc>
@apiName get_blind
@apiGroup Blinds

@apiParam {int} floor Floor number
@apiParam {int} bloc Bloc number

@apiSuccess {String} action Action description
@apiSuccess {int} bloc Bloc number
@apiSuccess {int} floor Floor number
@apiSuccess {int} value Valve's value

@apiSuccessExample {json} Example of result in case of success:
{
    "action": "Get blind value",
    "bloc": 2,
    "floor": 4,
    "value": 100
}
@apiDescription Get information on given valve in JSON format

@apiErrorExample {json} Error during knx connection
     {
       "error": "Error occured: knx.connect()"
     }
@apiErrorExample {json} Error during knx read
     {
       "error": "Error occured: knx.read()"
     }
@apiErrorExample {json} Error during knx disconnection
     {
       "error": "Error occured: knx.disconnect()"
     }

"""
"""
@api {post} /blind/<floor>/<bloc>
@apiName set_blind
@apiGroup Blinds

@apiParam {int} floor Floor number
@apiParam {int} bloc Bloc number

@apiParamExample {json} Request-Exemple :
    {
        "new_value": 100
    }

@apiSuccess {String} action Action description
@apiSuccess {int} bloc Bloc number
@apiSuccess {int} floor Floor number
@apiSuccess {int} value Valve's value

@apiSuccessExample {json} Example of result in case of success:
{
    "action": "Set blind value",
    "bloc": 2,
    "floor": 4,
    "value": 100
}
@apiDescription Set value of given blind

@apiErrorExample {json} Error during knx connection
     {
       "error": "Error occured: knx.connect()"
     }
@apiErrorExample {json} Error during knx write
     {
       "error": "Error occured: knx.write()"
     }
@apiErrorExample {json} Error during knx disconnection
     {
       "error": "Error occured: knx.disconnect()"
     }

"""
@app.route('/blind/<int:floor>/<int:bloc>', methods=['GET', 'POST'])
def blind(floor, bloc):
    knx = KnxnetProtocol(gateway_ip, gateway_port, endpoint_port, data_endpoint, control_endpoint)
    if knx.connect() == -1:
        return jsonify(error="Error occured: knx.connect()")
    if request.method == 'POST':
        new_value = request.get_json()['new_value']
        grp_addr = '3/' + str(floor) + '/' + str(bloc)
        if knx.write(grp_addr, new_value) == -1:
            return jsonify(error="Error occured: knx.write()")
        value = new_value
        action = "Set blind value"
    else:
        grp_addr = '4/' + str(floor) + '/' + str(bloc)
        blind_value = knx.read(grp_addr)
        if blind_value == -1:
            return jsonify(error="Error occured: knx.read()")
        value = blind_value
        action = "Get blind value"

    if knx.disconnect() == -1:
        return jsonify(error="Error occured: knx.disconnect()")
    return jsonify(action=action, floor=floor, bloc=bloc, value=value)


"""
@api {post} /fullCloseBlind/<floor>/<bloc>
@apiName full_close_blind
@apiGroup Blinds

@apiParam {int} floor Floor number
@apiParam {int} bloc Bloc number

@apiSuccess {String} action Action description
@apiSuccess {int} bloc Bloc number
@apiSuccess {int} floor Floor number

@apiSuccessExample {json} Example of result in case of success:
{
    "action": "Full close blind",
    "bloc": 2,
    "floor": 4,
}
@apiDescription Set value of given blind

@apiErrorExample {json} Error during knx connection
     {
       "error": "Error occured: knx.connect()"
     }
@apiErrorExample {json} Error during knx write
     {
       "error": "Error occured: knx.write()"
     }
@apiErrorExample {json} Error during knx disconnection
     {
       "error": "Error occured: knx.disconnect()"
     }

"""
@app.route('/fullCloseBlind/<int:floor>/<int:bloc>', methods=['POST'])
def close_blind(floor, bloc):
    knx = KnxnetProtocol(gateway_ip, gateway_port, endpoint_port, data_endpoint, control_endpoint)
    if knx.connect() == -1:
        return jsonify(error="Error occured: knx.connect()")

    value = 1
    grp_addr = '1/' + str(floor) + '/' + str(bloc)
    if knx.write(grp_addr, value) == -1:
        return jsonify(error="Error occured: knx.write()")

    if knx.disconnect() == -1:
        return jsonify(error="Error occured: knx.disconnect()")
    return jsonify(action="Full close blind", floor=floor, bloc=bloc)



"""
@api {post} /fullOpenBlind/<floor>/<bloc>
@apiName full_open_blind
@apiGroup Blinds

@apiParam {int} floor Floor number
@apiParam {int} bloc Bloc number

@apiSuccess {String} action Action description
@apiSuccess {int} bloc Bloc number
@apiSuccess {int} floor Floor number

@apiSuccessExample {json} Example of result in case of success:
{
    "action": "Full open blind",
    "bloc": 2,
    "floor": 4,
}
@apiDescription Set value of given blind

@apiErrorExample {json} Error during knx connection
     {
       "error": "Error occured: knx.connect()"
     }
@apiErrorExample {json} Error during knx write
     {
       "error": "Error occured: knx.write()"
     }
@apiErrorExample {json} Error during knx disconnection
     {
       "error": "Error occured: knx.disconnect()"
     }

"""
@app.route('/fullOpenBlind/<int:floor>/<int:bloc>', methods=['POST'])
def open_blind(floor, bloc):
    knx = KnxnetProtocol(gateway_ip, gateway_port, endpoint_port, data_endpoint, control_endpoint)
    if knx.connect() == -1:
        return jsonify(error="Error occured: knx.connect()")

    value = 0
    grp_addr = '1/' + str(floor) + '/' + str(bloc)
    if knx.write(grp_addr, value) == -1:
        return jsonify(error="Error occured: knx.write()")

    if knx.disconnect() == -1:
        return jsonify(error="Error occured: knx.disconnect()")
    return jsonify(action="Full open blind", floor=floor, bloc=bloc)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3002)
