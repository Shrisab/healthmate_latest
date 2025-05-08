from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField


# Create your models here.
department = (
    ('Dentistry', "Dentistry"),
    ('Cardiology', "Cardiology"),
    ('ENT Specialists', "ENT Specialists"),
    ('Dietitian', 'Dietitian'),
    ('Endocrinology', 'Endocrinology'),
    ('Blood Screening', 'Blood Screening'),
    ('Eye Care', 'Eye Care'),
    ('Physical Therapy', 'Physical Therapy'),
    ('Neurology', 'Neurology'),
    ('Gynaecology', 'Gynaecology'),
    ('Pediatrics', 'Pediatrics'),
    ('Ophthalmology', 'Ophthalmology'),
    ('Orthopedic', 'Orthopedic'),
    ('Pulmonologist','Pulmonologist'),
    ('Radiologist','Radiologist'),
    ('General Surgeon','General Surgeon')
)


class doctor(models.Model):
    full_name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True,upload_to='healthApp/images')
    description=models.TextField(default="")
    address = models.CharField(max_length=100,default="")
    shift_start_time = models.CharField(max_length=10)
    shift_end_time = models.CharField(max_length=10)
    qualification_name = models.CharField(max_length=100)
    nmc_number = models.CharField(max_length=10, default="")
    education_training = models.TextField(default="")
    hospital_name = models.CharField(max_length=100)
    department = models.CharField(choices=department, max_length=100)
    professional_experience = models.TextField(default="")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name


class consultationform(models.Model):
    consult_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,default="")
    email = models.CharField(max_length=50,default="")
    phone = models.CharField(max_length=30,default="")
    department =models.CharField(max_length=100,default="")
    date = models.CharField(max_length=50,default="")
    time = models.CharField(max_length=50,default="")
    city = models.CharField(max_length=50,default="")
    state =models.CharField(max_length=50,default="")

    def __str__(self):
        return self.name
    



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)

    name = models.CharField(default = 'Update your Name', max_length=20, null=True)

    address = models.CharField(default = 'Update your Address', max_length=100, null=True)
    bio = models.CharField(default = "Update your bio", max_length=200, null=True)
    email = models.CharField(default = "Update your Email", max_length=20, null=True)
    phone = models.CharField(default = "Update your phone no", max_length=20, null=True)

    profile_img =  models.ImageField(default = 'media/default-avatar.png', upload_to = 'media', null = True, blank = True)

    def __str__(self):
        return f"{self.user.username}'s profile"
    


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    short_description = models.TextField()
    content = FroalaField()
    banner_path = models.ImageField(upload_to='news_bannner')
    status = models.CharField(max_length=2, choices=(("1",'Published'), ("2",'Unpublished')), default=2)
    meta_keywords = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,default="")
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.name} - {self.post.title}"  