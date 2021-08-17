Proyecto final de la asignatura de Fundamentos de Sistemas Embebidos
Centro Multimedia
Autores: Gutiérrez Silvestre Griselda, Mayen Palmillas Marco Antonio y Santillan Garcia Josue 

Pasos para la ejecución:
    1.  Instalación del navegador Mozilla Firefox.
            Descargar desde su máquina virtual el navegador mozilla firefox para linux en su versión de 32 bits. 
            https://www.mozilla.org/es-MX/firefox/all/#product-desktop-release
            
            Generalmente se descarga en Downloads, después descomprimir con el comando:
            tar -xjvf Downloads/<nombre_descarga>
            
            Mover el directorio descomprimido a /opt/ con el comando:
            sudo mv Downloads/firefox /opt/

            Creación de la liga simbólica.
            sudo ln -s /opt/firefox/firefox/ /usr/bin/firefox

            Creación del archivo test.desktop.
            touch test.desktop

            Redirigir entrada de echo al archivo creado.
            echo -e "[Desktop Entry]\nName=Firefox\nComment=Navegador web\nGenericName=Web Browser\nX-GNOME-FullName=Firefox ''Su versión'' Web Browser\nExec=/opt/firefox/firefox %u\nTerminal=false\nX-MultipleArgs=false\nType=Application\nIcon=/opt/firefox/browser/chrome/icons/default/default128.png\nCategories=Network;WebBrowser;\nMimeType=text/html;text/xml;application/xhtml+xml;application/xml;application/vnd.mozilla.xul+xml;application/rss+xml;application/rdf+xml;image/gif;image/jpeg;image/png;x-scheme-handler/http;x-scheme-handler/https;\nStartupWMClass=Firefox\nStartupNotify=true\nPath=" > test.desktop

            Finalmente mover el archivo anterior al directorio de aplicaciones. 
            sudo mv test.desktop /usr/share/applications/firefox.desktop

    2.  Descargue el código del repositorio con el comando:
        git clone https://github.com/Grissie/Embebidos.git 

    3.  Cambiarse al directorio.
        cd Embebidos 

    4.  Instalar módulo vlc con el comando:
        pip3 install python-vlc

    5   Ejecutar el programa con el comando:
        python3 centro-multimedia.py 


