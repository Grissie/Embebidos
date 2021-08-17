#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Proyecto  final de la asignatura de Fundamentos de Sistemas Embebidos
Centro Multimedia 
Autores:
        Gutiérrez Silvestre Griselda
        Mayen Palmillas Marco Antonio
        Santillan Garcia Josue 
        
        MIT license       
        
"""

#Módulopara el control y reproducción de audios 
import pygame
#Librería para el control y generación de hilos 
import threading
#Módulo para el control y visualización de videos y fotos 
import vlc
#Módulo para acceder a los directorios del sistema
import os
#Módulo para la creación de la interfaz 
from tkinter import*
#Módulo para acceder al navegador web 
import webbrowser


def validaExtension(lista, archivo):
    """
    Función que verifica la extensión de un archivo con una lista de extensiones
    permitidas. Si la extensión del archivo esta en la lista regresa un True, de
    lo contrario regresa un False.
    """
    #Recorre la lista
    for i in range(len(lista)):
        #Compara la extensión del archivo con el elemento actual de la lista
        if archivo.endswith(lista[i]):
            #Si la extensión esta en la lista, regresa un valor verdadero
            return True
    #De lo contrario regresa un valor falso
    return False

    
def encontrar(entrada):
    """
    Función que analiza el contenido de la memoria USB (directorio /media/pi),
    si no hay contenido regresa una lista vacía. De lo contrario se verifica
    que sea un archivo y con la función validaExtension() se verifica que la extensión
    sea válida. Si cumple con ambas se agrega a una lista nueva y al final esta
    lista se regresa.
    """
    #Crea una lista con los elementos del directorio
    listaArchivos=os.listdir('/media/pi/')
    #Verifica si la lista esta vacía
    if len(listaArchivos)==0:
        return listaArchivos
    #Si no está vacía, es porque tiene conectada la memoria USB, se lee el contenido de la primer USB
    listaArchivos2=os.listdir('/media/pi/'+listaArchivos[0])
    #Arreglo que contiene los archivos con extensiones válidas
    listaArchivosValidos=[]
    #Recorre la lista de archivos de la memoria USB
    for archivo in listaArchivos2:
        #Es archivo y tiene extensión válida se agrega al nuevo arreglo
        if os.path.isfile(os.path.join('/media/pi/'+listaArchivos[0], archivo)) and validaExtension(entrada,archivo):
            listaArchivosValidos.append(archivo)
    #Regresar lista final 
    return listaArchivosValidos


class VentanaPrincipal:
    """
    Ventana principal del sistema, permite al usuario elegir entre Netflix, Spotify,
    la memoria USB o salir. 
    """
    def __init__(self, principal):
        """Constructor de la ventana principal y creación de botones"""
        self.principal=principal
        self.opcion=0
        principal.title("CENTRO MULTIMEDIA")
        
        #Instanciamos botones para cada opción
        self.botonNetflix=Button(principal,text="NETFLIX",command=self.netflix,width=12,height=3,anchor="center",relief="groove",borderwidth=5)
        self.botonNetflix.pack(padx=50,pady=30)
        self.botonSpotify=Button(principal,text="SPOTIFY",command=self.spotify,width=12,height=3,anchor="center",relief="groove",borderwidth=5)
        self.botonSpotify.pack(padx=50,pady=30)
        self.botonMemoria=Button(principal,text="MEMORIA USB",command=self.memoria, width=12,height=3,anchor="center",relief="groove",borderwidth=5)
        self.botonMemoria.pack(padx=50,pady=30)
        self.botonSalir=Button(principal,text="SALIR",command=self.salir,width=12,height=3,anchor="center",relief="groove",borderwidth=5)
        self.botonSalir.pack(padx=50,pady=30)

    #Funciones asignadas según el botón que elija el usuario 
    def netflix(self):
        """El usuario elige la opción de Netflix, entonces eliminar la ventana principal"""
        self.opcion=1
        self.principal.destroy()

    def spotify(self):
        """El usuario elige la opción de Spotify, entonces eliminar la ventana principal"""
        self.opcion=2
        self.principal.destroy()

    def memoria(self):
        """El usuario elige la opción de Memoria USB, entonces eliminar la ventana principal"""
        self.principal.destroy()

    def salir(self):
        """El usuario elige la opción de Salir, entonces eliminar la ventana principal"""
        self.opcion=4
        self.principal.destroy()

    def getOpcion(self):
        """Regresa el valor de la variable opción"""
        return self.opcion


class VentanaMemoria:
    """
    Ventana para seleccionar los archivos multimedia de la memoria USB, el usuario
    puede elegir entre música, fotos, audio o simplemente salir.
    """
    def __init__(self,principal,opcion):
        """Constructor de la ventana"""
        self.principal=principal
        principal.title("CONTENIDO MEMORIA USB")
        #Lista con la extensión de audio aceptada
        audio=[".mp3"]
        #Lista de archivos con extensión mp3 
        listaAudios=encontrar(audio)
        #Lista con la extensión de video aceptado
        video=[".mp4"]
        #Lista de archivos con extensión mp4
        listaVideos=encontrar(video)
        #Lista con la extensión de foto aceptado
        foto=[".jpg",".png",".jfif"]
        #Lista de archivos con extensión jpg, png, jfif 
        listaFotos=encontrar(foto)

        if (len(listaAudios)==0 and len(listaVideos)==0 and len(listaFotos)==0):
            """
            Si no hay elementos en las listas de audio, video y fotos, entonces la USB
            esta vacía, el usuario sale con el botón de salir.
            """
            self.mensaje=Label(principal,text="¡ NO SE ENCONTRO CONTENIDO !")
            self.mensaje.pack()
            self.botonSalir=Button(principal,text="SALIR",command=self.salir,width=12,height=3,anchor="center",relief="groove",borderwidth=5)
            self.botonSalir.pack(padx=50,pady=50)

        #Sí hay elementos en cada lista entonces se asigna un botón para cada lista
        if (len(listaAudios)!=0):
            self.boton=Button(principal,text="MÚSICA",command=self.musica,width=12,height=3,anchor="center",relief="groove",borderwidth=5)
            self.boton.pack(padx=50,pady=40)
        if (len(listaFotos)!=0):
            self.boton=Button(principal,text="FOTOS",command=self.fotos,width=12,height=3,anchor="center",relief="groove",borderwidth=5)
            self.boton.pack(padx=50,pady=40)
        if (len(listaVideos)!=0):
            self.boton=Button(principal,text="VIDEOS",command=self.videos,width=12,height=3,anchor="center",relief="groove",borderwidth=5)
            self.boton.pack(padx=50,pady=40)

    #Si se elige cualquiera de las 4 opciones se elimina la ventana principal
    def musica(self):
        self.opcion=1
        self.principal.destroy()
    def fotos(self):
        self.opcion=2
        self.principal.destroy()
    def videos(self):
        self.opcion=3
        self.principal.destroy()
    def salir(self):
        self.opcion=5
        self.principal.destroy()

    def getOpcion(self):
        """Regresa el valor de la variable opción"""
        return self.opcion


class VentanaAudio:
    """
    Ventana para el control de archivos de audio de la memoria usb 
    """
    def __init__(self,principal,tamano):
        """Constructor de la ventana, recibe el tamaño de la lista de archivos de audio """
        self.principal=principal
        self.indice=0
        self.tamano=tamano
        self.bandera=True
        self.auxiliar=True
        #Título de la ventana 
        principal.title("MÚSICA")
        #Cargar archivo de audio
        pygame.mixer.music.load(self.tamano[self.indice])
        #Reproducción del audio 
        pygame.mixer.music.play()

        #Botón para pausar 
        self.botonPausa=Button(principal,text="PAUSA",command=self.pausarReproducir,width=12,height=3,anchor="center",relief="groove",borderwidth=5)
        self.botonPausa.pack(padx=50,pady=20)
        #Botón para adelantar
        self.botonAdelante=Button(principal,text="ADELANTE",command=self.adelante,width=12,height=3,anchor="center",relief="groove",borderwidth=5)
        self.botonAdelante.pack(padx=50,pady=20)
        #Botón para atrasar
        self.botonAtras=Button(principal,text="ATRÁS",command=self.atras,width=12,height=3,anchor="center",relief="groove",borderwidth=5)
        self.botonAtras.pack(padx=50,pady=30)
        #Botón para salir 
        self.botonSalir=Button(principal,text="SALIR",command=self.salir,width=12,height=3,anchor="center",relief="groove",borderwidth=5)
        self.botonSalir.pack(padx=50,pady=20)

    def pausarReproducir(self):
        """Función para pausar o reproducir el audio actual"""
        #Si bandera=True, entonces esta en reproducción 
        if (self.bandera==True):
            pygame.mixer.music.pause()
            self.bandera=False
        #Si bandera=False, entonces esta pausado 
        else:
            pygame.mixer.music.unpause()
            self.bandera=True

    def adelante(self):
        """
        Función para cargar el siguiente audio y reproducirlo. Sí se llega al final de la lista,
        se regresa al valor inicial de la misma.
        """
        #Valor siguiente
        self.indice=self.indice+1
        #Mientras la posición actual sea menor al tamaño de la lista
        if (self.indice<len(self.tamano)):
            #Detiene el audio actual
            pygame.mixer.music.stop()
            #Se carga el audio siguiente 
            pygame.mixer.music.load(self.tamano[self.indice])
            #Se reproduce el audio siguiente
            pygame.mixer.music.play()
        else:
            #Se regresa al inicio de la lista 
            self.indice=0
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.tamano[self.indice])
            pygame.mixer.music.play()
    
    def atras(self):
        """
        Función para cargar el audio anterior y reproducirlo. Sí se llega al inicio de la lista,
        se regresa al valor final de la misma.

        """      
        #Valor anterior
        self.indice=self.indice-1
        #Mientras la posición actual sea mayor o igual a cero 
        if (self.indice>=0):
            #Detiene el audio actual
            pygame.mixer.music.stop()
            #Se carga el audio anterior
            pygame.mixer.music.load(self.tamano[self.indice])
            #Se reproduce el audio anterior 
            pygame.mixer.music.play()
        else:
            #Se regresa al final de la lista
            self.indice=len(self.tamano)-1 
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.tamano[self.indice])
            pygame.mixer.music.play()
        
    def salir(self):
        """Función que sale de la ventana de reproducción de audio"""
        #Elimina la ventana 
        self.principal.destroy()
        #Variable para terminar la secuencia de hilos 
        self.auxiliar=False
        #Detiene el audio actual 
        pygame.mixer.music.stop()

    def getAuxiliar(self):
        """Función que regresa el valor de auxiliar"""
        return self.auxiliar

    def getIndice(self):
        """Función que regresa la posición actual de la lista"""
        return self.indice

    def setIndice(self,a):
        """Función que modifica el valor de la posición de la lista"""
        self.indice=a


def rutaArchivo(n):
    """
    Función que recorre la lista de entrada de la memoria usb, cada elemento
    se le concatena la ruta absoluta de su ubicación y se regresa dicha lista 
    """
    for i in range(len(n)):
        #Obtiene el contenido del directorio /media/pi
        contenido=os.listdir('/media/pi/')
        #Obtiene la ruta absoluta del archivo 
        n[i]="/media/pi/"+contenido[0]+"/"+n[i]
    return n  


class VentanaFoto:
    """Ventana para el control de fotos de la memoria usb"""

    def __init__(self,principal,tamano):
        """Constructor de la ventana, recibe el tamaño de la lista de fotos""" 
        self.principal=principal
        self.tamano=tamano
        self.indice=0

        principal.title("FOTOS")
        #Crear un objeto de MediaPlayer 
        self.media=vlc.MediaPlayer(self.tamano[self.indice])
        #Visualizar la foto 
        self.media.play()

        #Botón adelantar
        self.botonAdelante=Button(principal,text="ADELANTE",command=self.adelante,width=12,height=2,anchor="center",relief="groove",borderwidth=5)
        self.botonAdelante.pack(padx=30,pady=20)
        #Botón atrasar 
        self.botonAtras=Button(principal,text="ATRÁS",command=self.atras,width=12,height=2,anchor="center",relief="groove",borderwidth=5)
        self.botonAtras.pack(padx=30,pady=20)
        #Botón salir
        self.botonSalir=Button(principal,text="SALIR",command=self.salir,width=12,height=2,anchor="center",relief="groove",borderwidth=5)
        self.botonSalir.pack(padx=30,pady=20)

    def adelante(self):
        """
        Función que muestra la siguiente foto, si llega la final de la lista,
        se regresa al primer valor de la lista 
        """
        #Detiene la foto actual
        self.media.stop()
        #Foto siguiente 
        self.indice=self.indice+1
        #Mientras la posición actual sea menor al tamaño de la lista
        if (self.indice<len(self.tamano)):
            #Cargar foto actual 
            self.media=vlc.MediaPlayer(self.tamano[self.indice])
            #Visualizar foto
            self.media.play()
        else:
            #Regresa a la posición inicial de la lista 
            self.indice=0
            self.media=vlc.MediaPlayer(self.tamano[self.indice])
            self.media.play()

    def atras(self):
        """
        Función que muestra la foto anterior, si llega al inicio de la lista,
        se regresa al último valor de la lista 
        """
        #Posición anterior
        self.indice=self.indice-1
        #Detiene la foto 
        self.media.stop()
        #Mientras la posición sea mayor o igual a cero 
        if (self.indice>=0):
            #Crea un objeto media y se carga a foto actual 
            self.media=vlc.MediaPlayer(self.tamano[self.indice])
            #Visualiza la foto
            self.media.play()
        else:
            #Obtiene el último elemento de la lista 
            self.indice=len(self.tamano)-1
            self.media=vlc.MediaPlayer(self.tamano[self.indice])
            self.media.play()

    def salir(self):
        """Función para salir de la ventana de visualización de fotos"""
        self.principal.destroy()
        #Se detiene la foto actual 
        self.media.stop()


class VentanaVideo:
    """Ventana para el control de videos de la memoria usb"""

    def __init__(self,principal,tamano):
        """Constructor de la ventana, recibe el tamaño de la lista de videos"""
        self.principal=principal
        self.tamano=tamano
        self.indice=0
        self.bandera=True
        self.auxiliar=True

        #Título de la ventana
        principal.title("VIDEOS")
        #Crea un objeto del tipo MediaPlayer y se carga el actual video 
        self.media=vlc.MediaPlayer(self.tamano[self.indice])
        self.media.play()

        #Botón pausar
        self.botonPausa=Button(principal,text="PAUSA",command=self.pausa,width=12,height=1,anchor="center",relief="groove",borderwidth=5)
        self.botonPausa.pack(padx=50,pady=10)
        #Botón adelantar
        self.botonAdelante=Button(principal,text="ADELANTA",command=self.adelanta,width=12,height=1,anchor="center",relief="groove",borderwidth=5)
        self.botonAdelante.pack(padx=50,pady=10)
        #Botón atrasar
        self.botonAtras=Button(principal,text="ATRÁS",command=self.atras,width=12,height=1,anchor="center",relief="groove",borderwidth=5)
        self.botonAtras.pack(padx=50,pady=10)
        #Botón salir 
        self.botonSalir=Button(principal,text="SALIR",command=self.salir,width=12,height=1,anchor="center",relief="groove",borderwidth=5)
        self.botonSalir.pack(padx=50,pady=10)

    def pausa(self):
        """Función que pausa o reanuda el video, según el valor de la bandera"""
        #Si bandera=True el video se está reproduciendo
        if (self.bandera==True):
            #Pausar video
            self.media.set_pause(1)
            self.bandera=False
        #Si bandera=False el video está pausado 
        else:
            #Reanudar video
            self.media.play()
            self.bandera=True

    def adelanta(self):
        """
        Función que reproduce el siguiente video, si llega al final de la lista, 
        entonces se regresa al primer elemento de la lista
        """
        #Detiene el actual video 
        self.media.stop()
        #Siguiente video
        self.indice=self.indice+1
        #Mientras la posición actual sea menor al tamaño de la lista
        if (self.indice<len(self.tamano)):
            #Crear un nuevo objeto y cargar el video en la posición actual 
            self.media=vlc.MediaPlayer(self.tamano[self.indice])
            #Reproducir video 
            self.media.play()
        else:
            #Caso contrario, regresar al primer elemento de la lista 
            self.indice=0
            self.media=vlc.MediaPlayer(self.tamano[self.indice])
            self.media.play()

    def atras(self):
        """
        Función que reproduce el video anterior, si llega al inicio de la lista, 
        entonces se regresa al último elemento de la lista
        """
        #Anterior video
        self.indice=self.indice-1
        #Detiene el actual video 
        self.media.stop()
        #Mientras la posición actual sea mayor o igual a cero
        if (self.indice>=0):
            #Crea un objeto media y se le carga el video actual 
            self.media=vlc.MediaPlayer(self.tamano[self.indice])
            #Reproducir video
            self.media.play()
        else:
            #Caso contrario, regresar al último elemento de la lista 
            self.indice=len(self.tamano)-1
            self.media=vlc.MediaPlayer(self.tamano[self.indice])
            self.media.play()           

    def salir(self):
        """Función para salir de la ventana de visualización de videos"""
        self.principal.destroy()
        #Se detiene el video actual 
        self.media.stop()


def incrementar(num,**datos):
    """
    Función que utiliza un hilo para cambiar al siguiente audio, cuando el actual audio ha terminado 
    """
    #Cuando se da clic en el botón salir, getAuxiliar() regresa un false
    while (datos['inicio'].getAuxiliar()):
        #¿Algo se está reproduciendo?
        if(pygame.mixer.music.get_busy()==0):
            #Obtiene el valor del índice actual y lo guarda en a 
            a=datos['inicio'].getIndice()
            #Se verifica que el índice llegue a la última posición
            if(a==len(datos['arreglo'])-1):
                a=-1
            #Obtiene el siguiente audio 
            a=a+1
            #Modifica el valor del índice, pasandole el valor de a, esto permite que los botones 
            #se usen en el nuevo audio 
            datos['inicio'].setIndice(a)
            #Carga el archivo actual de audio 
            pygame.mixer.music.load(datos['arreglo'][a])
            #Reproducción del audio 
            pygame.mixer.music.play()
    #Detiene el audio 
    pygame.mixer.music.stop()
    #Elimina el objeto
    pygame.mixer.quit()


"""
Función principal de todo el proyecto. Se crea un ciclo, mientras la bandera sea verdadera.
Se crea una primer ventana y dependiendo de la elección del usuario se crean otras ventanas secundarias,
este proceso se repite hasta que el usuario de clic en el botón salir de la ventana principal.
"""
bandera=True
while(bandera):
    #Creación del objeto
    root=Tk()
    tipoArchivo=0
    root.attributes()
    #Modo pantalla completa
    root.attributes("-zoomed",True)
    root.configure(bg="black")
    #Creación de un objeto de la ventana principal y se lempasa el objeto root como parámetro
    ventana=VentanaPrincipal(root)
    #Se pone la ventana en ciclo 
    root.mainloop()
    #Obtenemos el valor de la opción elegida por el usuario en la ventana principal 
    opcion=ventana.getOpcion()

    #Dependiendo de la opción elegida por el usuario, se irá a Netflix, Spotify, memoria USB o salir
        
    if opcion==0:
        """Eligió la memoria USB"""
        #Recordar que la funcion encontrar() valida que la extension de un archivo este dentro de una lista
        #de extensiones permitidas 
        formatosAudio=[".mp3"]
        listaAudio=encontrar(formatosAudio)
        formatosVideo=[".mp4"]
        listaVideo=encontrar(formatosVideo)
        formatosFoto=[".jpg",".png",".jfif"]
        listaFoto=encontrar(formatosFoto)

        #Verifica que solo contiene un tipo de archivo (video, audio o foto) la memoria usb

        #Solo audios
        if len(listaAudio)!=0 and len(listaVideo)==0 and len(listaFoto)==0:
            tipoArchivo=1
        #Solo videos
        elif len(listaAudio)==0 and len(listaVideo)!=0 and len(listaFoto)==0:
            tipoArchivo=3
        #Solo fotos
        elif len(listaAudio)==0 and len(listaVideo)==0 and len(listaFoto)!=0:
            tipoArchivo=2

        #Archivos de los 3 tipos
        else:
            root=Tk()
            tipoArchivo=0
            root.attributes("-zoomed",True)
            root.configure(bg="black")
            #Se crea un objeto de la venta de memoria y se pasa el parámetro root y el tipo de archivo 
            ventana=VentanaMemoria(root,tipoArchivo)
            root.mainloop()
            #Devuelve el tipo de archivo a reproducir 
            tipoArchivo=ventana.getOpcion()
            
        #Verificamos el tipo de archivo
        #Es audio
        if tipoArchivo==1:
            #Instancia del reproductor de audio 
            reproductor=pygame.mixer.init()
            #Lista de formatos permitidos
            formatosAudio=[".mp3"]
            #La función encontrar() valida la extensión de cada archivo y regresa una lista con audios
            #con el formato permitido 
            listaAudio=encontrar(formatosAudio)
            root=Tk()
            
            root.attributes("-topmost",True)
            tipoArchivo=0
            #La función rutaAbsoluta() obtiene la ruta completa de cada audio 
            listaAudio=rutaArchivo(listaAudio)
            #Creación del objeto del tipo VentanaAudio, pasar como parámetro a root y la lista de audios 
            ventana=VentanaAudio(root,listaAudio)
            #Creación de hilo, para reproducir el siguiente audio, esto siempre y cuando haya terminado el actual
            inicia=threading.Thread(target=incrementar,args=(2,),kwargs={'inicio':ventana,'arreglo':listaAudio})
            #Inicia el hilo
            inicia.start()
            #Mantiene la ventana hasta que se elimine
            root.mainloop()

        #Es foto
        if tipoArchivo==2:
            #Lista de formatos permitidos para las fotos 
            formatosFoto=[".jpg",".png",".jfif"]
            #Lista de fotos con formato válido 
            listaFoto=encontrar(formatosFoto)
            root=Tk()
            root.attributes("-topmost",True)
            tipoArchivo=0
            #Obtener la ruta absoluta de cada foto 
            listaFoto=rutaArchivo(listaFoto)
            #Se crea un objeto del tipo VentanaFoto y se le pasa como parámetro root y la lista de fotos 
            ventana=VentanaFoto(root,listaFoto)
            root.mainloop()

        #Es video
        if tipoArchivo==3:
            #Lista de formatos permitidos para video
            formatosVideo=[".mp4"]
            #Archivos que cumplen con la extensión 
            listaVideo=encontrar(formatosVideo)
            root=Tk()
            root.attributes("-topmost",True)
            tipoArchivo=0
            #Obtener la ruta absoluta de cada video
            listaVideo=rutaArchivo(listaVideo)
            #Crear objeto del tipo VentanaVideo
            ventana=VentanaVideo(root,listaVideo)
            root.mainloop()
        
    elif opcion==1:
        """Se eligió Netflix"""
        #Accede a la ruta absoluta del navegador 
        rutaNavegador="/usr/bin/firefox %s"
        #Se obtiene la ruta del navegador 
        navegador=webbrowser.get(rutaNavegador)
        #Se registra el navegador 
        webbrowser.register("firefox",None,navegador)
        #Se obtiene el ejecutable del navegador 
        navegador=webbrowser.get("firefox")
        #Enlace al sitio oficial de Netflix 
        navegador.open("https://www.netflix.com/mx/login")

            
    elif opcion==2:
        """Eligió Spotify"""
        #Agregar la ruta absoluta del navegador 
        rutaNavegador="/usr/bin/firefox %s"
        #Obtener la ruta del navegador
        navegador=webbrowser.get(rutaNavegador)
        #Registro el navegador 
        webbrowser.register("firefox",None,navegador)
        #Se obtiene el navegador para usarlo
        navegador=webbrowser.get("firefox")
        #Enlace a la página oficial 
        navegador.open("https://accounts.spotify.com/es/login/?continue=https:%2F%2Fwww.spotify.com%2Fapi%2Fgrowth%2Fl2l-redirect&_locale=es-MX")

        
    else:
        """Se eligió salir del programa"""
        #Sale del ciclo while 
        bandera=False
