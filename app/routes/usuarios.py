from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import User, Permissao

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('/', methods=['GET'])
def listar():
    """Lista todos os usuários"""
    usuarios = User.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@usuarios_bp.route('/criar', methods=['GET', 'POST'])
def criar():
    """Cria um novo usuário"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        role = request.form.get('role', 'usuario')
        
        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'danger')
            return redirect(url_for('usuarios.criar'))
        
        usuario = User(nome=nome, email=email, role=role, ativo=True)
        usuario.set_password(senha)
        
        db.session.add(usuario)
        db.session.commit()
        
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('usuarios.editar_permissoes', usuario_id=usuario.id))
    
    return render_template('usuarios/criar.html')

@usuarios_bp.route('/<int:usuario_id>/editar', methods=['GET', 'POST'])
def editar(usuario_id):
    """Edita um usuário"""
    usuario = User.query.get_or_404(usuario_id)
    
    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        usuario.role = request.form.get('role')
        usuario.ativo = request.form.get('ativo') == 'on'
        
        db.session.commit()
        flash('Usuário atualizado!', 'success')
        return redirect(url_for('usuarios.listar'))
    
    return render_template('usuarios/editar.html', usuario=usuario)

@usuarios_bp.route('/<int:usuario_id>/permissoes', methods=['GET', 'POST'])
def editar_permissoes(usuario_id):
    """Gerencia permissões do usuário"""
    usuario = User.query.get_or_404(usuario_id)
    todas_permissoes = Permissao.query.all()
    
    if request.method == 'POST':
        # Limpar permissões atuais
        usuario.permissoes.clear()
        
        # Adicionar permissões selecionadas
        permissoes_ids = request.form.getlist('permissoes')
        for perm_id in permissoes_ids:
            perm = Permissao.query.get(perm_id)
            if perm:
                usuario.permissoes.append(perm)
        
        db.session.commit()
        flash('Permissões atualizadas!', 'success')
        return redirect(url_for('usuarios.listar'))
    
    return render_template('usuarios/permissoes.html', usuario=usuario, todas_permissoes=todas_permissoes)

@usuarios_bp.route('/<int:usuario_id>/deletar', methods=['POST'])
def deletar(usuario_id):
    """Deleta um usuário"""
    usuario = User.query.get_or_404(usuario_id)
    
    # Não permitir deletar o admin
    if usuario.role == 'admin':
        flash('Não é possível deletar um admin!', 'danger')
        return redirect(url_for('usuarios.listar'))
    
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário deletado!', 'success')
    return redirect(url_for('usuarios.listar'))
