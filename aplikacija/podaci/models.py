from django.db import models

class Beer(models.Model):
    name    = models.CharField(max_length=200)
    rDev    = models.CharField(max_length=20)
    look    = models.CharField(max_length=20)
    smell   = models.CharField(max_length=20)
    taste   = models.CharField(max_length=20)
    feel    = models.CharField(max_length=20)
    overall = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name

class Review(models.Model):
    beer    = models.ForeignKey(Beer)
    user    = models.CharField(max_length=100)
    grade   = models.CharField(max_length=100)
    rDev    = models.CharField(max_length=20)
    look    = models.CharField(max_length=20)
    smell   = models.CharField(max_length=20)
    taste   = models.CharField(max_length=20)
    feel    = models.CharField(max_length=20)
    overall = models.CharField(max_length=20)
    text    = models.TextField()
    data    = models.CharField(max_length=40)
    created = models.DateTimeField('date published')

    def __unicode__(self):
        return self.user + " : " + self.text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class User(models.Model):
    username = models.CharField(max_length=100)
    link     = models.CharField(max_length=200)
    city     = models.CharField(max_length=50)

class UpdateBeer(models.Model):
    beerName = models.CharField(max_length=100)
    date     = models.CharField(max_length=50)

    def __unicode__(self):
        return self.beerName + " : " + self.date

