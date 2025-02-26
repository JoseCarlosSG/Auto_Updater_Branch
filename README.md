Uso:

Ejecuta el script con:

python script.py MyClass /ruta/del/archivo.py my_branch 8228270

Si la clase está hasta el final del archivo, omite el identificador:

python script.py MyClass /ruta/del/archivo.py my_branch

Flujo del script:

    Localiza la clase y la copia en un archivo MyClass_backup.py.
    Ejecuta git pull origin master.
    Si no hay conflictos, hace git commit -m "my_branch: Updating branch".
    Si hay conflictos, usa git checkout --theirs . para mantener los cambios de master, los agrega, hace git commit y luego git push.
