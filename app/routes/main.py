from flask import Blueprint, render_template, request, redirect, url_for, flash

main_bp = Blueprint('main', __name__)

# Rotas principais aqui
@main_bp.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard"""
    return render_template('index.html')
