from django.db import models

class Lesson(models.Model):
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=500)
    length = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    lessons = models.ManyToManyField(Lesson)

    def __str__(self):
        return self.product_name

class User(models.Model):
    username = models.CharField(max_length=200)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.username

class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    time = models.DateTimeField("Viewing time")
    duration = models.IntegerField(default=0)
    viewed = models.BooleanField(default=False)

    def viewed_check(self):
        self.viewed = float(self.duration) >= float(0.8 * self.lesson.length)
        return self.viewed

    def __str__(self):
        return f"%s's lesson: %s" %(self.user, self.lesson)


# Create your models here.
