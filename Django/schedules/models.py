from django.db import models

# Create your models here.

class Article(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000)
    homepage = models.CharField(max_length=1000)
    time = models.DateTimeField()
    
    class Meta:
        db_table = 'article'


    def __str__(self):
        return self.title

class Job(models.Model):
    id = models.IntegerField(primary_key=True)
    company = models.CharField(max_length=1000)
    title = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)
    end_date = models.CharField(max_length=1000)
    time = models.DateTimeField()
    class Meta:
        db_table = 'job'
    def __str__(self):
        return self.title