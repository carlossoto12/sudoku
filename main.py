from flask import Flask, request, jsonify
from sudoku.sudoku import Sudoku
from send_email.send_email import Send_email

app = Flask(__name__)
data_send_email = {
    'message': None,
    'recipient': "carlosst4510@gmail.com",
    'subject_line': "Tablero del sudoku en juego"
}


@app.route('/play', methods=['POST'])
def insert_value():
    info_request = request.get_json()
    new_game = Sudoku()
    new_game.set_board(info_request["tablero"])
    if new_game.check_elements(info_request):
        respuesta = {
            "mensaje_1": "The element is allowed"
        }
        if new_game.insert_element(info_request):
            respuesta["mensaje_2"] = "the element was correctly inserted"
            info_request = new_game.get_info_position()
            data_send_email['message'] = info_request["tablero"]
            respuesta["mensaje_3"] = send_email_message(data_send_email)
    else:
        respuesta = {
            "mensaje": "The element is not allowed"
        }
    return jsonify(respuesta)


def send_email_message(data_send_email):
    se = Send_email(data_send_email['message'], data_send_email['recipient'], data_send_email['subject_line'])
    if se.send_the_email():
        respuesta = {
            "mensaje": "the message has been sent"
        }
    else:
        respuesta = {
            "mensaje": "the message could not be sent"
        }
    return respuesta


if __name__ == '__main__':
    app.run(debug=True)
