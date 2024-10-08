from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100000000)
    email = models.CharField(max_length=70000000, default="")
    phone = models.CharField(max_length=7000000, default="")
    msg = models.CharField(max_length=50000000, default="")

    def __str__(self):
        return self.name


class Video(models.Model):
    video_id = models.AutoField
    video_name = models.CharField(max_length=5000000)
    desc = models.TextField()
    show_desc = models.CharField(max_length=68, null=True)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="Home/images", default="")
    video = models.URLField(unique=True)
    download_links = models.TextField(default="")

    def __str__(self):
        return self.video_name




class Comment(models.Model):
    post = models.ForeignKey(Video , on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', null=True, related_name="replies" , on_delete=models.CASCADE)
    content = models.TextField(max_length=160 , default="")
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '{}-{}'.format(self.post.video_name, str(self.user.username))

