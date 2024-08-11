from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import gspread

app = Flask(__name__)
socketio = SocketIO(app)

# Configuração do Google Sheets
gc = gspread.service_account(filename='credentials.json')
sheet = gc.open('gerenciador').sheet1

@app.route('/')
def index():
    data = sheet.get_all_records()
    return render_template('index.html', data=data)

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    id_orcamento = data['id']
    column = data['column']
    value = data['value']

    # Atualiza o Google Sheets com base na coluna
    cell = sheet.find(id_orcamento)
    if column == 'Revisor Atuando':
        sheet.update_cell(cell.row, 2, value)
    elif column == 'Status':
        sheet.update_cell(cell.row, 3, value)
    elif column == 'Abordar':
        sheet.update_cell(cell.row, 4, value)
    elif column == 'Finalizar Atendimento':
        sheet.update_cell(cell.row, 5, value)

    # Emite o evento de atualização para todos os clientes conectados
    socketio.emit('update_data', data)

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    socketio.run(app, debug=True)
