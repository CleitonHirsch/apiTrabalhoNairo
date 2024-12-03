from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from collections import OrderedDict

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_trabalho.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()
    print("Banco de dados inicializado:", db.engine.url)


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(255))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    cep = db.Column(db.String(10))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


@app.route('/clientes', methods=['POST'])
def add_cliente():
    data = request.get_json()
    try:
        
        novo_cliente = Cliente(
            nome=data['nome'],
            sobrenome=data['sobrenome'],
            email=data['email'],
            telefone=data.get('telefone'),
            endereco=data.get('endereco'),
            cidade=data.get('cidade'),
            estado=data.get('estado'),
            cep=data.get('cep'),
            data_cadastro=datetime.utcnow()
        )
        db.session.add(novo_cliente)
        db.session.commit()
        return jsonify({'message': 'Cliente adicionado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@app.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    clientes_list = []
    for cliente in clientes:
        clientes_list.append(OrderedDict({
            'id': cliente.id,
            'nome': cliente.nome,
            'sobrenome': cliente.sobrenome,
            'email': cliente.email,
            'telefone': cliente.telefone,
            'endereco': cliente.endereco,
            'cidade': cliente.cidade,
            'estado': cliente.estado,
            'cep': cliente.cep,
            'data_cadastro': cliente.data_cadastro.strftime('%Y-%m-%d %H:%M:%S')
        }))
    return jsonify(clientes_list)


@app.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    cliente = Cliente.query.get(id)
    if cliente:
        return jsonify({
            'id': cliente.id,
            'nome': cliente.nome,
            'sobrenome': cliente.sobrenome,
            'email': cliente.email,
            'telefone': cliente.telefone,
            'endereco': cliente.endereco,
            'cidade': cliente.cidade,
            'estado': cliente.estado,
            'cep': cliente.cep,
            'data_cadastro': cliente.data_cadastro.strftime('%Y-%m-%d %H:%M:%S')
        })
    else:
        return jsonify({'message': 'Cliente não encontrado!'}), 404


@app.route('/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
    data = request.get_json()
    cliente = Cliente.query.get(id)
    if cliente:
        cliente.nome = data.get('nome', cliente.nome)
        cliente.sobrenome = data.get('sobrenome', cliente.sobrenome)
        cliente.email = data.get('email', cliente.email)
        cliente.telefone = data.get('telefone', cliente.telefone)
        cliente.endereco = data.get('endereco', cliente.endereco)
        cliente.cidade = data.get('cidade', cliente.cidade)
        cliente.estado = data.get('estado', cliente.estado)
        cliente.cep = data.get('cep', cliente.cep)
        db.session.commit()
        return jsonify({'message': 'Cliente atualizado com sucesso!'})
    else:
        return jsonify({'message': 'Cliente não encontrado!'}), 404


@app.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = Cliente.query.get(id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({'message': 'Cliente deletado com sucesso!'})
    else:
        return jsonify({'message': 'Cliente não encontrado!'}), 404


if __name__ == '__main__':
    app.run(debug=True)
