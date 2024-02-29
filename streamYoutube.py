# coding=utf-8
# Author: Amir Mosquera
# python script: Ejecutar ffmpg en maquinas linux para emitir una transmision de archivos
# mp3 junto a una imagen usando un buble infinito.

import os #Importamos el modulo os para trabajar con el sistema operativo
import subprocess #Importamos el modulo subprocess para llamar aplicaciones externas
import eyed3 #Importamos el modulo eyed3 para obtener la metadata del archivo mp3
import random #Importamos el modulo ramdom para crear numeros aleatorios

dir = os.path.dirname(os.path.abspath(__file__)) #Obtenemos la ruta del directorio actual, como el pwd de linux

def streamYoutube(): #Definimos la función streamYoutube
        while True: #Ciclo while para que se repoduzca una y otra vez
            obj = os.listdir(dir) #Creamos una lista con todos los archivos que existen en la ruta actual dir
            obj.sort() #Ordenamos la lista de menor a mayor
            list = [] #Creamos una lista vacia
            for i in obj: #Creamos un ciclo for para validar si los archivos son .mp3 y si es asi los agrege a la lista list.
                if i[-4:] == ".mp3": #Para cuestiones de orden le dimos formato al nombre de los mp3 como 001.mp3, 255.mp3
                    list.append(i)

            #Ciclo de mandar el ffmpg
            try:
                for fichero in list:
                    if fichero[-4:] == ".mp3":
                        tagMp3 = eyed3.load(fichero) #Capturamos la metadata del mp3 que se usa para el titulo, artista y track
                        nombreMp3 = tagMp3.tag.title
                        artistMp3 = tagMp3.tag.artist
                        comment = tagMp3.tag.comments[0].text
                        try:
                            if os.path.exists(f'{fichero[:3]}.jpg'): #Identificamos la imagen para cambiarla en cada mp3
                                imagen = f'{fichero[:3]}.jpg'
                            else:
                                rand = random.randint(1, 30) #Para este ejemplo tenemos 30 imagenes, formato 1.jpg, 30.jpg
                                imagen = f'{rand}.jpg'
                                        
                            #Se inicia el proceso del ffmpeg, debe instalarse en linux o windows (https://ffmpeg.org/)
                            subprocess.call([
                                'ffmpeg.exe', '-loglevel', 'info', '-y', '-re',
                                '-f', 'image2', '-loop', '1', '-i', f'{imagen}',
                                '-i', f'{fichero}', '-af', 'apad=pad_dur=5',
                                '-c:v', 'libx264', '-preset', 'ultrafast', '-b:v', '2000k', '-maxrate', '2000k', '-bufsize', '4000k',
                                '-framerate', '15', '-s', '1280x720', '-vf',f"\
                                drawtext=font=Arial:text='{nombreMp3}':fontcolor=black:fontsize=70:x=(w-text_w)/2:y=(h-text_h)/2,\
                                drawtext=font=Arial:text='Himno # {int(fichero[:3])}':fontcolor=black:fontsize=50:x=(w-text_w)/2:y=h-th-450,\
                                drawtext=font=Arial:text='Letra, {artistMp3}\nMúsica, {comment}':fontcolor=black:fontsize=50:x=w-tw-10:y=h-th-10",
                                '-g', '30', '-shortest', '-strict', 'experimental',
                                '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
                                '-f', 'flv', 'rtmp://a.rtmp.youtube.com/live2/xxxx-xxxx-xxxx-xxxx-xxxx']) #Recuerda cambiar las xxxx por tu codigo del livestream dado por Youtube
                        except Exception as _e:
                            print("Error : {}".format(str(_e)))
                            break
            except KeyboardInterrupt as _e:
                print("Error : {}".format(str(_e)))
                break


if __name__ == '__main__':
    streamYoutube()