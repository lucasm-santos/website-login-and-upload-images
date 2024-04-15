import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .views import signin, register, galeria
from .models import Image
from home.forms import ImageUploadForm
from django.contrib.auth.models import Group

# register

class RegisterTestCase(TestCase):
    def test_valid_form_creates_user_and_redirects_to_login(self):
        
        response = self.client.post(reverse('register'), {
            'username': 'testando',
            'password1': 'clone205',
            'password2': 'clone205',
            'email': 'testando@gmail.com',
            'is_superuser': 1
        })
        
        
        self.assertRedirects(response, reverse('login'))

        
        user = authenticate(username='testando', password='clone205')
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'testando@gmail.com')


# login/signin

class SigninTestCase(TestCase):
    def test_authenticated_user_redirects_to_galeria(self):
        
        user = User.objects.create_user(username='testando', password='clone205')
        
        
        self.client.login(username='testando', password='clone205')
    
       
        response = self.client.get(reverse('login'))
        
      
        self.assertRedirects(response, reverse('galeria'))

    def test_get_request_returns_login_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'login.html')

    def test_valid_credentials_redirects_to_galeria(self):
        
        user = User.objects.create_user(username='testando', password='clone205')
        
        
        response = self.client.post(reverse('login'), {'username': 'testando', 'password1': 'clone205'})
        
        
        self.assertRedirects(response, reverse('galeria'))
        
        
        self.assertTrue(self.client.login(username='testando', password='clone205'))

    def test_invalid_credentials_returns_login_template(self):
        
        response = self.client.post(reverse('login'), {'username': 'testando', 'password1': 'senhaerrada'})
        
        
        self.assertTemplateUsed(response, 'login.html')



# sair

class SairTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tesntando', password='clone205')
        self.client.login(username='testando', password='clone205')

    def test_sair_view(self):
        response = self.client.get(reverse('sair'))

        self.assertFalse(response.wsgi_request.user.is_authenticated)

        self.assertRedirects(response, reverse('login'))

    def tearDown(self):
        self.user.delete()

if __name__ == '__main__':
    unittest.main()

# galeria

class GaleriaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testando', password='clone205')
        self.client.login(username='testando', password='clone205')

    def test_galeria_view(self):
        image = Image.objects.create(titulo='imagem teste', ativo=True, imagem='exemplo de url')

        
        response = self.client.get(reverse('galeria'))

        self.assertEqual(response.status_code, 200)

        self.assertIn(image, response.context['images'])

    def test_galeria_view_with_active_images(self):
        image = Image.objects.create(titulo='Minha Imagem', ativo=True, imagem='url da imagem')

        response = self.client.get(reverse('galeria'))

        self.assertIn(image, response.context['images'])

    def test_galeria_view_with_inactive_images(self):
        image = Image.objects.create(titulo='Minha Imagem', ativo=False, imagem='url da imagem')

        response = self.client.get(reverse('galeria'))

        self.assertNotIn(image, response.context['images'])

    def tearDown(self):
        self.user.delete()

if __name__ == '__main__':
    unittest.main()

# home

class HomeTestCase(TestCase):
    def setUp(self):
        # precisa criar o grupo e setar o usuario nesse grupo, não adianta usar um usuario q ja tenha setado no banco pois o teste nn acessa o banco
        self.noivos_group, created = Group.objects.get_or_create(name='noivos')
        self.noivos_group, created = Group.objects.get_or_create(name='noivos')
        self.user = User.objects.create_user(username='lucasmsantos', password='clone205')
        self.client.login(username='lucasmsantos', password='clone205')
        self.user.groups.add(self.noivos_group)

    def test_home_view_with_valid_data(self):
        with open('C:/Users/pessoal/Downloads/lugia.jpg', 'rb') as image_file:
            data = {
                'titulo': 'lugia',
                'imagem': image_file,
            }
            response = self.client.post(reverse('home'), data)

        self.assertRedirects(response, reverse('home'))

        self.assertTrue(Image.objects.exists())
        
    def test_home_view_with_invalid_data(self):
        data = {
        'titulo': '',
        'imagem': ''
        }
        response = self.client.post(reverse('home'), data)

        
        self.assertEqual(response.status_code, 200)

        self.assertTrue('form' in response.context)
        self.assertFalse(response.context['form'].is_valid())

    def tearDown(self):
        self.user.delete()

if __name__ == '__main__':
    unittest.main()


# excluir_imagem

class ExcluirImagemTestCase(TestCase):
    def setUp(self):
        self.noivos_group, created = Group.objects.get_or_create(name='noivos')
        self.user = User.objects.create_user(username='lucasmsantos', password='clone205')
        self.client.login(username='lucasmsantos', password='clone205')
        self.user.groups.add(self.noivos_group)
        self.image = Image.objects.create(titulo='Minha Imagem', ativo=True, imagem='exemplo de url')

    def test_excluir_imagem_view(self):
        response = self.client.post(reverse('excluir_imagem'), {'image_id': self.image.id})

       
        self.image.refresh_from_db() 
        self.assertFalse(self.image.ativo)

        self.assertRedirects(response, reverse('excluir_imagem'))

    def tearDown(self):
        self.user.delete()
        self.image.delete()

if __name__ == '__main__':
    unittest.main()

# lixeira

class LixeiraTestCase(TestCase):
    def setUp(self):
        self.noivos_group, created = Group.objects.get_or_create(name='noivos')
        self.user = User.objects.create_user(username='lucasmsantos', password='clone205')
        self.client.login(username='lucasmsantos', password='clone205')
        self.user.groups.add(self.noivos_group)
        self.image = Image.objects.create(titulo='Minha Imagem', ativo=False, imagem='exemplo de url')

    def test_lixeira_view(self):
        response = self.client.post(reverse('lixeira'), {'image_id': self.image.id})

        self.image.refresh_from_db()
        self.assertTrue(self.image.ativo)

        self.assertRedirects(response, reverse('galeria'))

    def tearDown(self):
        self.user.delete()
        self.image.delete()

if __name__ == '__main__':
    unittest.main()