# coding=utf-8
# Author: Amir Mosquera
# python script: Ejecutar ffmpg en maquinas linux para emitir una transmision de archivos mp3 junto a una imagen usando un bucle infinito.

import os #Importamos el modulo os para trabajar con el sistema operativo
import subprocess #Importamos el modulo subprocess para llamar aplicaciones externas
import eyed3 #Importamos el modulo eyed3 para obtener la metadata del archivo mp3

dir = os.path.dirname(os.path.abspath(__file__)) #Obtenemos la ruta del directorio actual, como el pwd de linux
imagen = 'imagen.jpg' #Imagen que se usara de fondo en el livestream
texto2 = ':fontsize=150:fontcolor=black:x=(w-text_w)/6:y=(h-text_h)/2:font=Arial' 


def streamYoutube(): #Definimos la función
        while True:
            obj = os.listdir(dir) #Creamos una lista con todos los archivos que existen en la ruta actual dir
            obj.sort() #Ordenamos la lista de menor a mayor
            #Ciclo de mandar el ffmpg
            try:
                for fichero in obj: #Recorremos la lista buscando los archivo que son mp3
                    if fichero[-4:] == ".mp3":
                        tagMp3 = eyed3.load(fichero) #Capturamos la metadata del mp3 que se usa para el titulo
                        nombreMp3 = tagMp3.tag.title
                        numeroMp3 = int(fichero[-7:-4])
                        texto1 = f'text={nombreMp3} {numeroMp3}\n\n2do Parrafo'
                        try:
                            #Se usa el programa ffmpeg, previamente instalado en la maquina
                            subprocess.call([
                                'ffmpeg', '-loglevel', 'info', '-y', '-re',
                                '-f', 'image2', '-loop', '1', '-i', f'{imagen}',
                                '-i', f'{fichero}', '-af', 'apad=pad_dur=5',
                                '-c:v', 'libx264', '-preset', 'ultrafast', '-b:v', '2000k', '-maxrate', '2000k', '-bufsize', '4000k',
                                '-framerate', '15', '-s', '1280x720', '-vf', f'drawtext={texto1}{texto2}', '-g', '30', '-shortest', '-strict', 'experimental',
                                '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
                                '-f', 'flv', 'rtmp://a.rtmp.youtube.com/live2/xxxx-xxxx-xxxx-xxxx-xxxx']) #Recuerda cambiar las xxxx por tu codigo del livestream dado por Youtube
                        except:
                            pass
            except KeyboardInterrupt as _e:
                print("Error : {}".format(str(_e)))
                break


if __name__ == '__main__':
    streamYoutube() #Ejecutamos el proceso