from __future__ import unicode_literals

from django.db import models

class Analisis(models.Model):
        username = models.CharField(max_length=100)
        Repo = models.CharField(max_length=100)
        archivo = models.CharField(max_length=100)
        code = models.CharField(max_length=100)
        docstring = models.CharField(max_length=100)
        comment = models.CharField(max_length=100)
        empty = models.CharField(max_length=100)

        convention = models.CharField(max_length=100)
        refactor = models.CharField(max_length=100)
        warning = models.CharField(max_length=100)
        error = models.CharField(max_length=100)

        module = models.CharField(max_length=100)
        clase = models.CharField(max_length=100)
        method = models.CharField(max_length=100)
        function = models.CharField(max_length=100)
        statements = models.CharField(max_length=100)
        def __unicode__(self):
                return self.username +": es del repo:" + self.Repo + "errores: " + self.error

class Historial(models.Model):
        nameppal = models.CharField(max_length=100)
        notappal = models.CharField(max_length=100)
        archppal = models.CharField(max_length=100)
        name1 = models.CharField(max_length=100)
        nota1 = models.CharField(max_length=100)
        arch1 = models.CharField(max_length=100)
        error1 = models.CharField(max_length=1000)        
        name2 = models.CharField(max_length=100)
        nota2 = models.CharField(max_length=100)
        arch2 = models.CharField(max_length=100)  
        error2= models.CharField(max_length=1000)             
        name3 = models.CharField(max_length=100)
        nota3 = models.CharField(max_length=100)
        arch3 = models.CharField(max_length=100)
        error3= models.CharField(max_length=1000)        
        name4 = models.CharField(max_length=100)
        nota4 = models.CharField(max_length=100)
        arch4 = models.CharField(max_length=100)
        error4= models.CharField(max_length=1000)        
        name5 = models.CharField(max_length=100)
        nota5 = models.CharField(max_length=100)
        arch5 = models.CharField(max_length=100)
        error5= models.CharField(max_length=1000)       
        name6 = models.CharField(max_length=100)
        nota6 = models.CharField(max_length=100)
        arch6 = models.CharField(max_length=100)
        error6 = models.CharField(max_length=1000)        
        name7 = models.CharField(max_length=100)
        nota7 = models.CharField(max_length=100)
        arch7 = models.CharField(max_length=100)
        error7= models.CharField(max_length=1000)     
        name8 = models.CharField(max_length=100)
        nota8 = models.CharField(max_length=100)
        arch8 = models.CharField(max_length=100)
        error8 = models.CharField(max_length=1000)      
        name9 = models.CharField(max_length=100)
        nota9 = models.CharField(max_length=100)
        arch9 = models.CharField(max_length=100)
        error9= models.CharField(max_length=1000)       
        war = models.CharField(max_length=100)
        err = models.CharField(max_length=100)
        con = models.CharField(max_length=100)
        ref = models.CharField(max_length=100)
        repo = models.CharField(max_length=100)

        def __unicode__(self):
                return self.nameppal +": es del repo:" + self.repo

class HistoricoRepo(models.Model):
        nameppal = models.CharField(max_length=100)
        repo = models.CharField(max_length=100)
        def __unicode__(self):
                return "Repo: "  + self.repo+"/"+self.nameppal

# Create your models here. p1 = Analisis(username="ivan", Repo="prueba", code="1", docstring="1", comment="1", empty="3", convention="2", refactor="3", warning="0", error="0", module="0", clase="0", method="3", function="1")
# NOTA 10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10)


