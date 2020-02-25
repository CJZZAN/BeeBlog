from django.db import models
from DjangoUeditor.models import UEditorField
import os

# Create your models here.



class Relationship(models.Model):
    fan_id =  models.CharField(max_length=50,default="")
    follow_id =  models.CharField(max_length=50,default="")
#

def user_directory_path(instance, filename):
    ext = filename.split('.').pop()
    filename = '{0}{1}.{2}'.format(instance.name, instance.identity_card, ext)
    return os.path.join(instance.major.name, filename)

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50,default="")
    user_email = models.CharField(max_length=100, default="")
    user_password = models.CharField(max_length=30, default="")
    user_sex = models.CharField(max_length=4, default="")
    user_phonenum = models.CharField(max_length=30, default="")
    user_birth = models.CharField(max_length=30, default="")
    user_hobby = models.CharField(max_length=30, default="")
    user_follow = models.IntegerField(default="0")
    user_fan = models.IntegerField(default="0")
    user_header = models.ImageField('头像', upload_to = user_directory_path, blank=True, null=True)
    user_sentence = models.CharField(max_length=200, default="博主很懒，什么都不写")
    # 这里定义一个方法，作用是当用户注册时没有上传照片，模板中调用 [ModelName].[ImageFieldName].url 时赋予一个默认路径
    def photo_url(self):
        if self.user_header and hasattr(self.user_header, 'url'):
            return self.user_header.url
        else:
            return '/media/default/user.jpg'

class Label(models.Model):
    label_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20,default="")
    label_name = models.CharField(max_length=20,default="")


class ArticleLabel(models.Model):
    label_id = models.CharField(max_length=20,default="")
    article_id = models.CharField(max_length=20,default="")




class ArticleType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=20,default="")
    r = models.ManyToManyField("User")





#
#
#
#
class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    usr = models.ForeignKey(User)
    article_type = models.ForeignKey(to='ArticleType',to_field='type_id')
    article_title = models.CharField(max_length=32,default="")
    article_sendtime = models.DateTimeField(auto_now_add=True, null=True)
    article_up = models.IntegerField(default=0)
    article_down = models.IntegerField(default=0)
    article_info = models.CharField(max_length=1000, default="")
    article_content = UEditorField(height=300,width=1000,verbose_name='content',default='')
    article_isdelete = models.IntegerField(default=0)

class Collection(models.Model):
    article_id = models.CharField(max_length=10,default='')
    user_id = models.CharField(max_length=10,default='')
#     # type_choice = (
#     #     (0,'Python'),
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(to='User',to_field='user_id')
    article_id = models.CharField(max_length=10,default='')
    date = models.DateTimeField(auto_now_add=True, null=True)
    content = models.CharField(max_length=150,default="")
    floor = models.IntegerField(default=1)

class Reply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    comment_id = models.ForeignKey(to='Comment',to_field='comment_id')
    reply_to = models.CharField(max_length=20,default="0")
    content = models.CharField(max_length=150,default="")
    user_id = models.ForeignKey(to='User',to_field='user_id')








