import random

from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.six import BytesIO

from PIL import Image
from .models import Photo

def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
   """
   Generate a test image, returning the filename that it was saved as.

   If ``storage`` is ``None``, the BytesIO containing the image data
   will be passed instead.
   """
   data = BytesIO()
   Image.new(image_mode, size).save(data, image_format)
   data.seek(0)
   if not storage:
       return data
   image_file = ContentFile(data.read())
   return storage.save(filename, image_file)

class ImageUploadTest(TestCase):

    def setUp(self):
        self.correct_credentials = {
            'username': 'demo',
            'password': '1$welcome'
        }
        User.objects.create_user(**self.correct_credentials)

    def test_image_upload_with_login(self):
        login = self.client.login(username='demo', password='1$welcome')
        #First login
        self.assertEqual(login, True)

        #Create sample image file
        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
        data = {'photo': avatar_file}

        #POST the data
        response = self.client.post('/photo/', data, follow=True)

        #Assert that the image is uploaded and saved in DB
        self.assertEquals(response.status_code, 200)
        self.assertEqual(Photo.objects.filter(owner_id=User.objects.filter(username='demo')[0].id).count(), 1)
        self.assertTemplateUsed('photo/index.html')

    def test_image_upload_without_login(self):

        #Create sample image file
        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
        data = {'photo': avatar_file}

        #POST the data
        response = self.client.post('/photo/', data, follow=True)

        #Assert that the image is uploaded but NOT saved in DB
        self.assertEquals(response.status_code, 200)
        self.assertEqual(Photo.objects.filter(owner_id=User.objects.filter(username='demo')[0].id).count(), 0)
        self.assertTemplateUsed('photo/index.html')
        self.assertContains(response, "form_login")

    def test_multiple_image_upload_with_login(self):
        login = self.client.login(username='demo', password='1$welcome')
        #First login
        self.assertEqual(login, True)

        count = random.randint(3, 15)

        for i in range(count):
            #Create sample image file
            avatar = create_image(None, 'avatar'+str(i)+'.png')
            avatar_file = SimpleUploadedFile('front'+str(i)+'.png', avatar.getvalue())
            data = {'photo': avatar_file}

            #POST the data
            response = self.client.post('/photo/', data, follow=True)

        #Assert that the image is uploaded properly
        self.assertEquals(response.status_code, 200)

        #Assert that the same number of images is saved in DB
        self.assertEqual(Photo.objects.filter(owner_id=User.objects.filter(username='demo')[0].id).count(), count)

        #Assert that the right template is used to render
        self.assertTemplateUsed('photo/index.html')

    def test_multiple_image_upload_without_login(self):

        count = random.randint(3, 15)

        for i in range(count):
            # Create sample image file
            avatar = create_image(None, 'avatar' + str(i) + '.png')
            avatar_file = SimpleUploadedFile('front' + str(i) + '.png', avatar.getvalue())
            data = {'photo': avatar_file}

            # POST the data
            response = self.client.post('/photo/', data, follow=True)

        #Assert that the image is uploaded but NOT saved in DB
        self.assertEquals(response.status_code, 200)
        self.assertEqual(Photo.objects.filter(owner_id=User.objects.filter(username='demo')[0].id).count(), 0)
        self.assertTemplateUsed('photo/index.html')
        self.assertContains(response, "form_login")