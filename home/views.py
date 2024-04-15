from django.shortcuts import render
from PIL import Image
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from home.models import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required   
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator
from .forms import ImageUploadForm
from .models import Image
import unittest
import cgi, cgitb
from flask import Flask, render_template, request, jsonify
import pickle
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)


@login_required(login_url="login")
@has_role_decorator('noivos')
def home(request):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

        else:
            form = ImageUploadForm()

        return render(request, 'home.html', {'form': form})


def excluir_imagem(request):
    images = Image.objects.filter(ativo=True)
   #  images = Image.objects.all()
    # bucket_name = 'konoalucardtesteimagens'
    
    if request.method == "POST":
        image_id = request.POST.get("image_id")
        # essa parte é pra excluir a imagem do banco do amazon s3, mas a perm nn ta direito pq teria q mudar a região do bucket
        # s3 = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')
        excluirImagemPorId(image_id)

        
    return render(request, 'galeria.html', {'images': images})


def excluirImagemPorId(id):
    try:
        images = Image.objects.get(id=id)
        
        # essa parte é pra excluir a imagem do banco do amazon s3, mas a perm nn ta direito pq teria q mudar a região do bucket
        # s3.delete_object(Bucket=bucket_name, Key=images.imagem.name)
        
        # caso queria deletar a imagem direto ao inves de mandar pra lixeira
        # images.delete()
        images.ativo = False
        images.save()
        
        return redirect('excluir_imagem')
    except Image.DoesNotExist:
        
        pass

def lixeira(request):
    images = Image.objects.filter(ativo=False)
   
    
    if request.method == "POST":
        image_id = request.POST.get("image_id")
        restaurarImagemPorId(image_id)
    return render(request, 'lixeira.html', {'images': images})


def restaurarImagemPorId (id):
        try:
            images = Image.objects.get(id=id)
            images.ativo = True
            images.save()
            
            return redirect('galeria')
        
        except Image.DoesNotExist:
            
            pass

def generate_user_url(username, is_superuser):
    base_url = "http://127.0.0.1:8000/galeria/"

    if is_superuser:
        return f"{base_url}noivo/{username}"
    else:
        return f"{base_url}user/{username}"
    





@login_required(login_url="login/")
def galeria(request):
    images = Image.objects.filter(ativo=True)
    return render(request, "galeria.html", {'images': images},)

    

def signin (request):
   if request.user.is_authenticated:
       return redirect('galeria')
   if request.method == "GET":
      return render (request,"login.html")
   else:
      username = request.POST.get('username')
      password = request.POST.get('password1')

      user = authenticate(username=username, password=password)
      if user:  
       login_django(request, user)
       if remember_me:
                user.remember_me = True
                user.save()
       return redirect('galeria')
         
      #    return redirect ('home')
   return render (request, "login.html")
    


    
def register(request):
    if request.user.is_authenticated:
       return redirect('galeria')
    if request.method == 'POST':
       form = UserCreationForm(request.POST)
       if form.is_valid():
          username = form.cleaned_data.get("username")
          password = form.cleaned_data.get("password1")
          email = form.cleaned_data.get("email")
          is_superuser = form.cleaned_data.get("is_superuser")
          if User.objects.filter(email=email).exists():
             print ("exists")
             return
         #  user = User(username=username, password=password, email=email)
         #  login_django(request, user)
          user2 = User.objects.create_user(username=username, password=password, email=email, is_superuser=is_superuser)
          user_url = generate_user_url(username, is_superuser)
          print("Generated URL:", user_url)
          if is_superuser == 1:
             assign_role(user2, 'noivos')
          user2.save()
        #   return redirect('login')
          return render(request, 'registration_success.html', {'user_url': user_url})
       else:
          return render(request, 'register.html') 
    else:
      form = UserCreationForm()
      return render(request, 'register.html')


def save_login_info(username, password1):
    login_info = {'username': username, 'password': password1}
    with open('login_info.pkl', 'wb') as file:
        pickle.dump(login_info, file)

def load_login_info():
    try:
        with open('login_info.pkl', 'rb') as file:
            login_info = pickle.load(file)
            return login_info['username'], login_info['password']
    except FileNotFoundError:
        return None, None
    

def remember_me():
    if request.method == 'POST':
        if request.form['remember'] == 'true':
            username, password = load_login_info()
            if username and password:
                return jsonify({'status': 'success', 'username': username, 'password': password})
            else:
                return jsonify({'status': 'error', 'message': 'No login details found.'})
    return jsonify({'status': 'error', 'message': 'Invalid request.'})




def index (request):
   return render (request, "index.html")


def sair(request):
   logout(request)
   return redirect('login')


def testes (request):

   return render(request, "testes.html")



    
    
 
