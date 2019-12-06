from django.db import models
# Create your models here.

class Novel(models.Model):
    name = models.CharField(max_length=30) #小说名字
    author = models.CharField(max_length=30)  #小说作者
    noveltype = models.CharField(max_length=30) #小说类型
    novelindex = models.CharField(max_length=30) #小说文章列表网址

    class Meta:
        verbose_name_plural = "小说"
        db_table = "novel_info"

    def __str__(self):
        return self.name
