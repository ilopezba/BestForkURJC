# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.core.context_processors import csrf
from django.template import RequestContext
from datetime import datetime, date, timedelta
from smtplib import SMTPRecipientsRefused
import urllib2
import commands
import urllib
import os
import os.path 
import smtplib 
from os import listdir

# Create your views here.
REPOSITORIO= ""
RetroDays = 2000

def Hello(request):
    response = request.get_full_path() #Para usar la url del navegador
    htmlRepo = " "
    htmlRepoFork = " " 
    response = response.split("&email=")
    repositorio = response[0].split("%2F")
    print "HHHHHHHH"+repositorio[3]
    ip = commands.getoutput("ifconfig").split("\n")[17].split()[1][5:]
    #ip = os.system(ifconfig | grep "Direc. inet:")
    #ip = ip.split(" ")
    print ip
    #print "hhhhhhh"+repositorio[len(repositorio)-1]+"uSER: " +repositorio[3]+ "dire " +repositorio[4]
    forks = urllib2.urlopen('https://api.github.com/repos/'+repositorio[3]+'/'+repositorio[4]+'/'+'forks') #construyo enlace
    #print forks
    html = forks.read()
    div = html.split(",")
    file_directory = "/home/ivanlb1/TFG2/"
       
    for lines in div:
        actualizadoRepo = False
        linea = lines.split('":')
        if linea[0].startswith('"full_name'):
            forkName = (linea[1][1:-1])
            #print forkName
            DirName = forkName.split("/")
            REPOSITORIO = DirName[1]
        if linea[0].startswith('"pushed_at'):  
            fecha = (linea[1][1:-11])
            fecha = fecha.split('-')
            #print fecha
            present = datetime.now()
            Ahora =  str(present)
            now = Ahora.split(" ")
            now = now[0].split("-")
            #print now[0]+"--"+now[1]+"--"+now[2]
            c = date(int(now[0]),int(now[1]),int(now[2]))-timedelta(days=RetroDays)
            if c < date(int(fecha[0]),int(fecha[1]),int(fecha[2])): #si la fecha dada es mas actual que hace 2 meses se imprime
                actualizadoRepo = True        
            if not os.path.isdir("/home/ivanlb1/TFG2/"+DirName[1]) and (actualizadoRepo == True):#Si es la primera vez que descarga un repo
                os.mkdir(os.path.join(file_directory,DirName[1])) 
            if not os.path.isdir("/home/ivanlb1/TFG2/"+DirName[1]+"/"+DirName[0]) and (actualizadoRepo == True): #Si hay Forks nuevos
                os.mkdir(os.path.join(file_directory+DirName[1],DirName[0])) 
                os.chdir(file_directory+DirName[1]+"/"+DirName[0])
                os.system("git clone " +"https://github.com/"+DirName[0]+"/"+DirName[1])
                os.chdir(file_directory+DirName[1]+"/"+DirName[0]+"/"+DirName[1])
                AnalizarPython(file_directory+DirName[1]+"/"+DirName[0]+"/"+DirName[1],DirName[1], DirName[0], "")
            else:
                if actualizadoRepo == True:
                    os.chdir(file_directory+DirName[1]+"/"+DirName[0]+"/"+DirName[1])
                    os.system("git pull") #Descargo modificaciones 
                    AnalizarPython(file_directory+DirName[1]+"/"+DirName[0]+"/"+DirName[1],DirName[1], DirName[0], "")
    #Descargo Rama Ppal:
    if os.path.isdir("/home/ivanlb1/TFG2/"+repositorio[4]+"/"+repositorio[3]):
        from prueba.models import HistoricoRepo
        try:
            p = HistoricoRepo.objects.filter(repo=repositorio[3]).get(nameppal=repositorio[4])
            p.delete()
        except HistoricoRepo.DoesNotExist:
            print("No existe Repo")
        p = HistoricoRepo(nameppal=repositorio[4], repo=repositorio[3])
        p.save()
        #print "AÑADO A BASE DE DATOS HISTORIAL"
        os.chdir(file_directory+repositorio[4]+"/"+repositorio[3]+"/"+repositorio[4])
        os.system("git pull") #Descargo modificaciones  
        os.chdir(file_directory+repositorio[4]+"/"+repositorio[3]+"/"+repositorio[4])
        AnalizarPython(file_directory+repositorio[4]+"/"+repositorio[3]+"/"+repositorio[4],repositorio[4], repositorio[3], "") 
    else:
        #print "NO EXISTE RAIZ"
        from prueba.models import HistoricoRepo
        try:
            p = HistoricoRepo.objects.filter(repo=repositorio[3]).get(nameppal=repositorio[4])
            p.delete()
        except HistoricoRepo.DoesNotExist:
            print("No existe Repo")
        p = HistoricoRepo(nameppal=repositorio[4], repo=repositorio[3])
        p.save()
        if not os.path.isdir("/home/ivanlb1/TFG2/"+repositorio[4]):
            os.mkdir(os.path.join(file_directory+repositorio[4]))
        os.mkdir(os.path.join(file_directory+repositorio[4],repositorio[3]))
        os.chdir(file_directory+repositorio[4]+"/"+repositorio[3])
        os.system("git clone " +"https://github.com/"+repositorio[3]+"/"+repositorio[4])
        #print "dirrr: "+ repositorio[3]+"/"+repositorio[4]
        #print "hago clone"
        os.chdir(file_directory+repositorio[4]+"/"+repositorio[3]+"/"+repositorio[4])
        AnalizarPython(file_directory+repositorio[4]+"/"+repositorio[3]+"/"+repositorio[4],repositorio[4], repositorio[3], "")    
       

    #    
    Resultados = Respuesta(repositorio[4])
    Res = Answer(Resultados, repositorio[3],repositorio[4],request, True)
    MandoEmail(response[1], repositorio[3], repositorio[4], ip)
    return render_to_response('recal.html', RequestContext(request, {'nombreppal': Res[0], 'notappal': Res[1],'archppal':Res[2],'name1': Res[3], 'nota1': Res[4],'arch1':Res[5], 'error1':Res[6], 'name2': Res[7], 'nota2': Res[8],'arch2':Res[9],'error2':Res[10], 'name3': Res[11], 'nota3': Res[12],'arch3':Res[13],'error3':Res[14], 'name4': Res[15], 'nota4': Res[16],'arch4':Res[17],'error4':Res[18], 'name5': Res[19], 'nota5': Res[20],'arch5':Res[21],'error5':Res[22], 'name6': Res[23], 'nota6': Res[24],'arch6':Res[25],'error6':Res[26], 'name7': Res[27], 'nota7': Res[28],'arch7':Res[29], 'error7':Res[30],'name8': Res[31], 'nota8': Res[32],'arch8':Res[33],'error8':Res[34], 'name9': Res[35], 'nota9': Res[36], 'arch9':Res[37], 'error9': Res[38], 'warr':Res[39], 'errr':Res[40], 'conn':Res[41], 'reff':Res[42],  'repositorio': Res[43], 'historico':Res[44]}))


def Recalcula(request): 
    score = ""
    disable = ""
    options = "Options: "
    file_directory = "/home/ivanlb1/TFG2/"
    response = request.get_full_path()
    print "re:" + response
    print "long " + str(len(response.split("namerepo=")))
    if(len(response.split("namerepo="))>1):
        repositorio = response.split("namerepo=")
        repositorio = repositorio[1].split("%2F")
        repositorio = repositorio[0]
        marcas = request.GET.getlist('checks[]')
        print "HAY NAMEREPO = "+ repositorio
    else:
        repositorio = response.split("%2F")
        marcas = request.GET.getlist('checks[]')
        repositorio = repositorio[len(repositorio)-1]
        print "+++++"  + repositorio[len(repositorio)-1]
        print "NO HAY NAMEREPO = "+ repositorio
    if(len(response.split("nameppal="))>1):
        nombreppal = response.split("nameppal=")
        nombreppal = nombreppal[1].split("%2F")
        nombreppal = nombreppal[0]
        print "NOMBRE PRINCIPAL " + nombreppal

        
    print "numero de checks" + str(len(marcas))
    for i in range(len(marcas)):
        print i
        if marcas[i] == "1":
            disable = disable+" --disable=C0103"
            options = options + "- invalid names "
        elif marcas[i] == "2":
            disable= disable + " --disable=W0312 --disable=W0311"
            options = options + "- tabs/spaces instead of spaces/tabs " 
        elif marcas[i] == "3":
            disable= disable + " --disable=C0303 --disable=C0326 --disable=W0311"
            options = options + "- wrong number of spaces "
        elif marcas[i] == "4":
            disable= disable + " --disable=C0111 "
            options = options + "- No Docstring "
        elif marcas[i] == "5":
            disable= disable + " --disable=W0104 "
            options = options + "- Statement without effect "
        elif marcas[i] == "6":
            disable= disable + " --disable=C0325 "
            options = options + "- Unnecessary parens "
    #if(len(marcas) != 0):
     #   if marcas[0] == "1":
     #       disable = disable+" --disable=C0103"
     #   if marcas[1] == "2":
     #       disable= disable + " --disable=W0312 "
     #   if marcas[2] == "3":
     #       disable= disable + " --disable=C0303 "
        print "::::" + "".join(marcas)+ " disable: " + disable
    for user in listdir(file_directory+"/"+repositorio): 
        print "user now: " + file_directory+repositorio+"/"+user+"/"+repositorio
        os.chdir(file_directory+repositorio+"/"+user+"/"+repositorio)
        AnalizarPython(file_directory+repositorio+"/"+user+"/"+repositorio,repositorio, user, disable)
    Resultados = Respuesta(repositorio)
    Res = Answer(Resultados, nombreppal,repositorio,request, False)
    print Res[23]
    print Res[24]
    print Res[31]
    print "*********************************"
    return render_to_response('recal.html', RequestContext(request, {'nombreppal': Res[0], 'notappal': Res[1],'archppal':Res[2],'name1': Res[3], 'nota1': Res[4],'arch1':Res[5], 'error1':Res[6], 'name2': Res[7], 'nota2': Res[8],'arch2':Res[9],'error2':Res[10], 'name3': Res[11], 'nota3': Res[12],'arch3':Res[13],'error3':Res[14], 'name4': Res[15], 'nota4': Res[16],'arch4':Res[17],'error4':Res[18], 'name5': Res[19], 'nota5': Res[20],'arch5':Res[21],'error5':Res[22], 'name6': Res[23], 'nota6': Res[24],'arch6':Res[25],'error6':Res[26], 'name7': Res[27], 'nota7': Res[28],'arch7':Res[29], 'error7':Res[30],'name8': Res[31], 'nota8': Res[32],'arch8':Res[33],'error8':Res[34], 'name9': Res[35], 'nota9': Res[36], 'arch9':Res[37], 'error9': Res[38], 'warr':Res[39], 'errr':Res[40], 'conn':Res[41], 'reff':Res[42],  'repositorio': Res[43], 'historico':Res[44], 'options': options}))


def Historial(request): 
    response = request.get_full_path() #Para usar la url del navegador
    print "HHHHHHHH"+response
    repositorio = response.split("___")
    user = repositorio[1]
    repo = repositorio[2]
    print user
    print repo
    from prueba.models import Historial
    nameppal = str(Historial.objects.filter(repo = repo, nameppal = user).values('nameppal'))
    nameppal = nameppal.split(":")
    nameppal = nameppal[1][3:-3]
    notappal = str(Historial.objects.filter(repo = repo, nameppal = user).values('notappal'))
    notappal = notappal.split(":")
    notappal = notappal[1][3:-3]
    archppal = str(Historial.objects.filter(repo = repo, nameppal = user).values('archppal'))
    archppal = archppal.split(":")
    archppal = archppal[1][3:-3]
    name1 = str(Historial.objects.filter(repo = repo, nameppal = user).values('name1'))
    name1 = name1.split(":")
    name1 = name1[1][3:-3]
    nota1 = str(Historial.objects.filter(repo = repo, nameppal = user).values('nota1'))
    nota1 = nota1.split(":")
    nota1 = nota1[1][3:-3]
    arch1 = str(Historial.objects.filter(repo = repo, nameppal = user).values('arch1'))
    arch1 = arch1.split(":")
    arch1 = arch1[1][3:-3]
    error1 = str(Historial.objects.filter(repo = repo, nameppal = user).values('error1'))
    error1 = error1.split(": u")
    if len(error1) > 1:
        if len(error1[1]) >20:
            error1 = error1[1][:-15]
    else:
        error1 = "No Errors"
    name2 = str(Historial.objects.filter(repo = repo, nameppal = user).values('name2'))
    name2 = name2.split(":")
    name2 = name2[1][3:-3]
    nota2 = str(Historial.objects.filter(repo = repo, nameppal = user).values('nota2'))
    nota2 = nota2.split(":")
    nota2 = nota2[1][3:-3]
    arch2 = str(Historial.objects.filter(repo = repo, nameppal = user).values('arch2'))
    arch2 = arch2.split(":")
    arch2 = arch2[1][3:-3]
    error2 = str(Historial.objects.filter(repo = repo, nameppal = user).values('error2'))
    error2 = error2.split(": u")
    if len(error2) > 1:
        if len(error2[1]) >20:
            error2 = error2[1][:-15]
    else:
        error2 = "No Errors"
    name3 = str(Historial.objects.filter(repo = repo, nameppal = user).values('name3'))
    name3 = name3.split(":")
    name3 = name3[1][3:-3]
    nota3 = str(Historial.objects.filter(repo = repo, nameppal = user).values('nota3'))
    nota3 = nota3.split(":")
    nota3 = nota3[1][3:-3]
    arch3 = str(Historial.objects.filter(repo = repo, nameppal = user).values('arch3'))
    arch3 = arch3.split(":")
    arch3 = arch3[1][3:-3]
    error3 = str(Historial.objects.filter(repo = repo, nameppal = user).values('error3'))
    error3 = error3.split(": u")
    if len(error3) > 1:
        if len(error3[1]) >20:
            error3 = error3[1][:-15]
    else:
        error3 = "No Errors"
    name4 = str(Historial.objects.filter(repo = repo, nameppal = user).values('name4'))
    name4 = name4.split(":")
    name4 = name4[1][3:-3]
    nota4 = str(Historial.objects.filter(repo = repo, nameppal = user).values('nota4'))
    nota4 = nota4.split(":")
    nota4 = nota4[1][3:-3]
    arch4 = str(Historial.objects.filter(repo = repo, nameppal = user).values('arch4'))
    arch4 = arch4.split(":")
    arch4 = arch4[1][3:-3]
    error4 = str(Historial.objects.filter(repo = repo, nameppal = user).values('error4'))
    error4 = error4.split(": u")
    if len(error4) > 1:
        if len(error4[1]) >20:
            error4 = error4[1][:-15]
    else:
        error4 = "No Errors"
    name5 = str(Historial.objects.filter(repo = repo, nameppal = user).values('name5'))
    name5 = name5.split(":")
    name5 = name5[1][3:-3]
    nota5 = str(Historial.objects.filter(repo = repo, nameppal = user).values('nota5'))
    nota5 = nota5.split(":")
    nota5 = nota5[1][3:-3]
    arch5 = str(Historial.objects.filter(repo = repo, nameppal = user).values('arch5'))
    arch5 = arch5.split(":")
    arch5 = arch5[1][3:-3]
    error5 = str(Historial.objects.filter(repo = repo, nameppal = user).values('error5'))
    error5 = error5.split(": u")
    if len(error5) > 1:
        if len(error5[1]) >20:
            error5 = error5[1][:-15]
    else:
        error5 = "No Errors"
    name6 = str(Historial.objects.filter(repo = repo, nameppal = user).values('name6'))
    name6 = name6.split(":")
    name6 = name6[1][3:-3]
    nota6 = str(Historial.objects.filter(repo = repo, nameppal = user).values('nota6'))
    nota6 = nota6.split(":")
    nota6 = nota6[1][3:-3]
    arch6 = str(Historial.objects.filter(repo = repo, nameppal = user).values('arch6'))
    arch6 = arch6.split(":")
    arch6 = arch6[1][3:-3]
    error6 = str(Historial.objects.filter(repo = repo, nameppal = user).values('error6'))
    error6 = error6.split(": u")
    if len(error6) > 1:
        if len(error6[1]) >20:
            error6 = error6[1][:-15]
    else:
        error6 = "No Errors"
    name7 = str(Historial.objects.filter(repo = repo, nameppal = user).values('name7'))
    name7 = name7.split(":")
    name7 = name7[1][3:-3]
    nota7 = str(Historial.objects.filter(repo = repo, nameppal = user).values('nota7'))
    nota7 = nota7.split(":")
    nota7 = nota7[1][3:-3]
    arch7 = str(Historial.objects.filter(repo = repo, nameppal = user).values('arch7'))
    arch7 = arch7.split(":")
    arch7 = arch7[1][3:-3]
    error7 = str(Historial.objects.filter(repo = repo, nameppal = user).values('error7'))
    error7 = error7.split(": u")
    if len(error7) > 1:
        if len(error7[1]) >20:
            error7 = error7[1][:-15]
    else:
        error7 = "No Errors"
    name8 = str(Historial.objects.filter(repo = repo, nameppal = user).values('name8'))
    name8 = name8.split(":")
    name8 = name8[1][3:-3]
    nota8 = str(Historial.objects.filter(repo = repo, nameppal = user).values('nota8'))
    nota8 = nota8.split(":")
    nota8 = nota8[1][3:-3]
    arch8 = str(Historial.objects.filter(repo = repo, nameppal = user).values('arch8'))
    arch8 = arch8.split(":")
    arch8 = arch8[1][3:-3]
    error8 = str(Historial.objects.filter(repo = repo, nameppal = user).values('error8'))
    error8 = error8.split(": u")
    if len(error8) > 1:
        if len(error8[1]) >20:
            error8 = error8[1][:-15]
    else:
        error8 = "No Errors"
    name9 = str(Historial.objects.filter(repo = repo, nameppal = user).values('name9'))
    name9 = name9.split(":")
    name9 = name9[1][3:-3]
    nota9 = str(Historial.objects.filter(repo = repo, nameppal = user).values('nota9'))
    nota9 = nota9.split(":")
    nota9 = nota9[1][3:-3]
    arch9 = str(Historial.objects.filter(repo = repo, nameppal = user).values('arch9'))
    arch9 = arch9.split(":")
    arch9 = arch9[1][3:-3]
    error9 = str(Historial.objects.filter(repo = repo, nameppal = user).values('error9'))
    error9 = error9.split(": u")
    if len(error9) > 1:
        if len(error9[1]) >20:
            error9 = error9[1][:-15]
    else:
        error8 = "No Errors"
    war = str(Historial.objects.filter(repo = repo, nameppal = user).values('war'))
    war = war.split(":")
    war = war[1][3:-3]
    err = str(Historial.objects.filter(repo = repo, nameppal = user).values('err'))
    err = err.split(":")
    err = err[1][3:-3]
    con = str(Historial.objects.filter(repo = repo, nameppal = user).values('con'))
    con = con.split(":")
    con = con[1][3:-3]
    ref = str(Historial.objects.filter(repo = repo, nameppal = user).values('ref'))
    ref = ref.split(":")
    ref = ref[1][3:-3]
    repo = str(Historial.objects.filter(repo = repo, nameppal = user).values('repo'))
    repo = repo.split(":")
    repo = repo[1][3:-3]
    print repo
    historial = GetHistorial()
    return render_to_response('hist.html', RequestContext(request, {'nombreppal': nameppal, 'notappal': notappal,'archppal':archppal,'name1': name1, 'nota1': nota1,'arch1':arch1, 'error1': error1, 'name2': name2, 'nota2': nota2,'arch2':arch2, 'error2':error2,'name3': name3, 'nota3': nota3,'arch3':arch3, 'error3':error3, 'name4': name4, 'nota4': nota4,'arch4':arch4, 'error4':error4, 'name5': name5, 'nota5': nota5,'arch5':arch5, 'error5':error5, 'name6': name6, 'nota6': nota6,'arch6':arch6, 'error6':error6,'name7': name7, 'nota7': nota7,'arch7':arch7, 'error7':error7,'name8': name8, 'nota8': nota8,'arch8':arch8, 'error8':error8, 'name9': name9, 'nota9': nota9,'arch9':arch9, 'error9':error9, 'warr': war, 'errr':err, 'conn':con, 'reff':ref,  'repositorio': repo,'historico': historial}))


def Answer(Resultados, User, RepositorioD, request, MeterHistorial):
    score = ""
    file_directory = "/home/ivanlb1/TFG2/"
    print "*****************"
    print Resultados[0][3]
    print "*****************"
    nota1= Resultados[0][0]
    name1= Resultados[0][1]
    arch1= Resultados[0][2]
    error1= Resultados[0][3]   
    nota2= Resultados[1][0]
    name2= Resultados[1][1]
    arch2= Resultados[1][2]
    error2= Resultados[1][3]   
    nota3= Resultados[2][0]
    name3= Resultados[2][1]
    arch3= Resultados[2][2]
    error3= Resultados[2][3]   
    nota4= Resultados[3][0]
    name4= Resultados[3][1]
    arch4= Resultados[3][2]
    error4= Resultados[3][3]       
    nota5= Resultados[4][0]
    name5= Resultados[4][1]
    arch5= Resultados[4][2]
    error5= Resultados[4][3]   
    nota6= Resultados[5][0]
    name6= Resultados[5][1]
    arch6= Resultados[5][2]
    error6= Resultados[5][3]   
    nota7= Resultados[6][0]
    name7= Resultados[6][1]
    arch7= Resultados[6][2]
    error7= Resultados[6][3]   
    nota8= Resultados[7][0]
    name8= Resultados[7][1]
    arch8= Resultados[7][2]
    error8= Resultados[7][3]   
    nota9= Resultados[8][0]
    name9= Resultados[8][1]
    arch9= Resultados[8][2]
    error9= Resultados[8][3]   

    for j in Resultados:
        if j[1] ==User:
            Nameppal=j[1]
            Notappal=j[0]
            Archppal=j[2]
    for i in Resultados:
        #print str(i[1]) +" "+ str(i[0])
        score = score+ "<br>" + str(i[1]) +" "+ str(i[0])
    os.chdir(file_directory+"/mysite/prueba/templates")
    from prueba.models import Analisis
    c = Analisis.objects.filter(Repo = RepositorioD)
    c.delete()
    AnadirBaseDatos(User,RepositorioD)
    repositorio = RepositorioD
    from prueba.models import Analisis
    war = Analisis.objects.exclude(warning='0   ').count()
    err = Analisis.objects.exclude(error='0   ').count()
    con = Analisis.objects.exclude(convention='0   ').count()
    ref = Analisis.objects.exclude(refactor='0   ').count()
    print(str(war)+" "+str(err)+" "+str(con)+" "+str(ref))
    if MeterHistorial:
        from prueba.models import Historial  
        c = Historial.objects.filter(repo = repositorio)
        c.delete()  
        p = Historial(nameppal=Nameppal, notappal=Notappal,archppal=Archppal, name1=name1, nota1=nota1, arch1=arch1,error1=error1, name2=name2, nota2=nota2, arch2=arch2,error2=error2, name3=name3, nota3=nota3, arch3=arch3,error3=error3, name4=name4, nota4=nota4, arch4=arch4, error4=error4, name5=name5, nota5=nota5, arch5=arch5, error5=error5, name6=name6, nota6=nota6, arch6=arch6, error6=error6, name7=name7, nota7=nota7, arch7=arch7, error7=error7, name8=name8, nota8=nota8,arch8=arch8, error8=error8, name9=name9,nota9=nota9,arch9=arch9, error9=error9, war=war, err=err,con=con, ref=ref, repo=repositorio)
        p.save()
    historial = GetHistorial()
    Response = [Nameppal, Notappal, Archppal, name1, nota1,arch1,error1, name2, nota2,arch2,error2, name3, nota3,arch3, error3,  name4, nota4, arch4,error4, name5,nota5,arch5, error5, name6, nota6,arch6, error6 ,name7, nota7,arch7, error7, name8, nota8,arch8, error8, name9, nota9, arch9, error9, war, err, con, ref,repositorio, historial]

    return Response

def GetHistorial():
    from prueba.models import HistoricoRepo
    p = HistoricoRepo.objects.count()
    historico =""
    for i in range (p):
        Hist = str(HistoricoRepo.objects.all()[i:i+1])
        print Hist
        Hist = Hist.split(" Repo:")
        print Hist[1]
        Hist = Hist[1][1:-2]
        Hist = Hist.split("/")
        historico = historico + '<a href='+'"'+"http://localhost:8000/hist.html___"+Hist[0]+"___"+Hist[1]+'">'+Hist[0]+"/"+Hist[1]+'</a> <br>'
    return historico

def AnalizarPython(directorio,repositorio, person, opciones):
    for  root, dirs, files in os.walk(directorio): 
        for archivo in files:
            if archivo.endswith(".py"):
                print "OPCIONES: "+ opciones
                print "Python encontrado "+ archivo
                print(os.path.join(root, archivo))
                os.chdir(root)
                os.system("pylint "+"--disable=E1101 "+opciones+" "+archivo+" > /home/ivanlb1/TFG2/"+repositorio+"/"+person+"/"+"puntuacion"+person+archivo+".txt")

def Respuesta(Repo):
    
    arr = []
    arr = [[(-999) for x in range(4)] for x in range(8)]
    for carpeta in listdir("/home/ivanlb1/TFG2/"+Repo):
        score=0
        i=0 
        Errors = ""
        IsError = False
        #print "CARPETA"+carpeta+ " Repo: " + Repo
        for archivo in listdir("/home/ivanlb1/TFG2/"+Repo+"/"+carpeta):
            if (archivo.endswith(".txt")): 
                i=i+1
                resultado = open("/home/ivanlb1/TFG2/"+Repo+"/"+carpeta+"/"+archivo)
                line = True
                while line:
                    line = resultado.readline()
                    if (line.startswith("Report")):
                        IsError = False                    
                    if IsError:
                        Errors = Errors+line+"<br>"
                        IsError = False   
                    if (line.startswith("************* Module")):
                        IsError = True
                        longname = len(carpeta) + 10
                        Errors = Errors+"Errors in "+carpeta+" "+ archivo[longname:-7] + "<br>"  
                    if "Your code has been" in line:
                        score =(score + float(line.split()[6][:-3]))
                        print "num de archivos" + str(i)+" "+Repo+" "+carpeta+" "+archivo +" " +str(float(line.split()[6][:-3]))
                        #arr.append([])
                        #arr[carpeta].append(float(line.split()[6][:-3]))
                        #print "SCORE:"+score 
                        #score = score+ "<br>"+ carpeta+"=" + line.split()[6][:-3]
                resultado.close()
        print carpeta + "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        if i > 0:
            score = score/i
        score = score + 100
        if i == 0:
            score = 0
        arr.append([score, carpeta, i,Errors])
    arr.sort(reverse=True)
    #for i in arr:.css("display","non
    #    print arr
    #    score = score+ "<br>"+ "".join(str(i))
    
    return arr

def MandoEmail(destino, User, Repo, ip):

    print destino
    destino = destino.split("%40")
    fromaddr = 'bestforkpython@gmail.com'
    toaddrs  = destino[0]+"@"+destino[1]
    print toaddrs
    msg = 'Correo enviado desde BestFork. \n Visite:+'+ip+":8000/hist.html___"+User+"___"+Repo
     
     
    # Datos
    username = 'bestforkivan@gmail.com'
    password = '987656789'
     
    # Enviando el correo
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def AnadirBaseDatos(User, Repo):
    print "Repo: " + Repo
    for carpeta in listdir("/home/ivanlb1/TFG2/"+Repo): 
        User = carpeta
        #print "CARPETA"+carpeta+ " Repo: " + Repo
        for archivo in listdir("/home/ivanlb1/TFG2/"+Repo+"/"+carpeta):
            if (archivo.endswith(".txt")): 
                resultado = open("/home/ivanlb1/TFG2/"+Repo+"/"+carpeta+"/"+archivo)
                line = True
                while line:
                    if (archivo.endswith(".txt")): 
                        line = resultado.readline()
                        if "|convention |" in line:
                            print archivo +" "+ line.split("|")[2][:-3]
                            convention = line.split("|")[2][:-3]
                        elif "|refactor   |" in line:
                            print archivo +" ref "+ line.split("|")[2][:-3]
                            refactor = line.split("|")[2][:-3]
                        elif "|warning    |" in line:
                            print archivo +" war "+ line.split("|")[2][:-3]
                            warning = line.split("|")[2][:-3]
                        elif "|error      |" in line:
                            print archivo +" err "+ line.split("|")[2][:-3]
                            error = line.split("|")[2][:-3]
                        elif "|code      |" in line:
                            print archivo +" cod "+ line.split("|")[2][:-3]
                            codes = line.split("|")[2][:-3]
                        elif "|docstring |" in line:
                            print archivo +" doc "+ line.split("|")[2][:-3]
                            docstring = line.split("|")[2][:-3]
                        elif "|comment   |" in line:
                            print archivo +" comm "+ line.split("|")[2][:-3]
                            comment = line.split("|")[2][:-3]
                        elif "|empty     |" in line:
                            print archivo +" empt "+ line.split("|")[2][:-3]
                            empty = line.split("|")[2][:-3]
                        elif "|module   |" in line:
                            print archivo +" mod "+ line.split("|")[2][:-3]
                            module = line.split("|")[2][:-3]
                        elif "|class    |" in line:
                            print archivo +" cla "+ line.split("|")[2][:-3]
                            clase = line.split("|")[2][:-3]
                        elif "|method   |" in line:
                            print archivo +" met "+ line.split("|")[2][:-3]
                            method = line.split("|")[2][:-3]
                        elif "|function |" in line:
                            print archivo +" func "+ line.split("|")[2][:-3]
                            function = line.split("|")[2][:-3]
                        elif "statements" in line:
                            print "statements " + line.split(" ")[0]
                            statements= line.split(" ")[0]
                if (archivo.endswith(".txt")): 
                    print archivo
                    from prueba.models import Analisis
                    p = Analisis(username=User, Repo=Repo,archivo=archivo, code=codes, docstring=docstring, comment=comment, empty=empty, convention=convention, refactor=refactor, warning=warning, error=error, module=module, clase=clase, method=method, function=function, statements = statements)
                    p.save()
def Help(request):
    response = request.get_full_path()
    return render_to_response('help.html')           
def home(request):
    return render_to_response('index.html', {'variable': 'world'})
def inicio(request):
    return render_to_response('inicio.html') 
