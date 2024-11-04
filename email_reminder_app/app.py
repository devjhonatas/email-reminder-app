from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from config import Config
from tasks import enviar_email_task

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Modelo de Lembrete
class Lembrete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    assunto = db.Column(db.String(200), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    agendado_para = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'assunto': self.assunto,
            'mensagem': self.mensagem,
            'agendado_para': self.agendado_para
        }

# Modelo de Usuário (para autenticação)
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    username = dados.get('username')
    password = dados.get('password')
    usuario = Usuario.query.filter_by(username=username).first()

    if usuario and usuario.password == password:  # Em produção, use hashing de senha.
        access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Usuário ou senha incorretos"}), 401

@app.route('/lembretes', methods=['POST'])
@jwt_required()
def criar_lembrete():
    dados = request.json
    if not dados.get('email') or not dados.get('assunto') or not dados.get('mensagem'):
        return jsonify({'msg': 'Todos os campos obrigatórios devem ser preenchidos'}), 400

    try:
        agendado_para = datetime.fromisoformat(dados['agendado_para']) if dados.get('agendado_para') else None
    except ValueError:
        return jsonify({'msg': 'Formato de data inválido'}), 400

    novo_lembrete = Lembrete(
        email=dados['email'],
        assunto=dados['assunto'],
        mensagem=dados['mensagem'],
        agendado_para=agendado_para
    )
    db.session.add(novo_lembrete)
    db.session.commit()

    if novo_lembrete.agendado_para:
        enviar_email_task.apply_async(
            (novo_lembrete.email, novo_lembrete.assunto, novo_lembrete.mensagem),
            eta=novo_lembrete.agendado_para
        )

    return jsonify(novo_lembrete.to_dict()), 201

@app.route('/lembretes', methods=['GET'])
@jwt_required()
def listar_lembretes():
    lembretes = Lembrete.query.all()
    return jsonify([l.to_dict() for l in lembretes]), 200

@app.route('/lembretes/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_lembrete(id):
    lembrete = Lembrete.query.get_or_404(id)
    db.session.delete(lembrete)
    db.session.commit()
    return jsonify({'msg': 'Lembrete excluído com sucesso'}), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)