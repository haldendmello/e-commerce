from django.contrib.auth.models import User
from django.db import models



class listcomment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)
    listname = models.CharField(max_length=64)

    def __str__(self):
        return f' {self.user} , {self.comment} '



class listing(models.Model):
    status=[
        ('active','active'),
        ('close','close')
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    category = models.CharField(max_length=64)
    startbid = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    listimage = models.ImageField(upload_to='media',null=True,blank=True)
    description = models.TextField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=64,choices=status,default='active')

    @property
    def imageURL(self):
        try:
            url = self.listimage.url
        except:
            url = ''
        return url

  
class currbid(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    listbid = models.ForeignKey(listing,on_delete=models.CASCADE,blank=True)




class watchlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    watchpage = models.ForeignKey(listing,on_delete=models.CASCADE)


