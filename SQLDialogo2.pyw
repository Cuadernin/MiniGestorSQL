import sys
import webbrowser
from DialogoSQL import SQLBaseDialogo
from PyQt5.QtWidgets import *
import mysql.connector
from mysql.connector import Error
from collections import namedtuple
from PyQt5 import *
import pandas as pd
import re
from sqlalchemy import create_engine
import csv

Columna=namedtuple('Columna',['nombre','tipo'])

#primera ventana
class base(QMainWindow):
    def __init__(self):
        super(base,self).__init__()
        self.nombre=''
        self.conexion=''
        self.columnas=[]
        patron='[a-zA-Z]+'
        self.mensajes=QMessageBox(self)
        self.regex=re.compile(patron)
        self.ui=SQLBaseDialogo()
        self.ui.setupUi(self)
        #menu
        self.ui.mni_datos.triggered.connect(self.datos)
        self.ui.mni_informacion.triggered.connect(self.url)
        self.ui.mni_salir.triggered.connect(self.salir)     
        self.ui.mni_contacto.triggered.connect(self.contacto)   
        #primera
        self.ui.btn_crear.clicked.connect(self.crear)
        #segunda
        self.ui.btn_conectar_tabla.clicked.connect(self.conectar_tabla)
        self.ui.btn_columna.clicked.connect(self.columnaB)
        self.ui.btn_crear_tabla.clicked.connect(self.crear_tabla)
        self.ui.btn_avanzado.clicked.connect(self.Avanzado)
        self.ui.btn_avanzado.setEnabled(False)
        #tercera
        self.ui.btn_conectar_modificar.clicked.connect(self.conectar_modificar)
        self.ui.btn_registro.clicked.connect(self.insertar)
        self.ui.btn_eliminar.clicked.connect(self.eliminar)
        #cuarta
        self.ui.btn_consultar.clicked.connect(self.consultar)
        self.ui.btn_personalizada.clicked.connect(self.personalizada)
        self.ui.tbw_consulta.setColumnWidth(0,200)
        self.ui.tbw_consulta.setColumnWidth(1,100)
        self.ui.tbw_consulta.setColumnWidth(2,250)
        self.show()

#primera pestaña
    def crear(self):
        self.nombre=self.ui.txt_nombre.text()
        if len(self.ui.txt_nombre.text())>0:
            try:
                ######################################################
                self.conexion=mysql.connector.connect(host="localhost", 
                                user="root",                                   # CHANGE THIS 
                                passwd="your password")                                                                             
                ######################################################   
                cursor=self.conexion.cursor()
                sql1=f'CREATE DATABASE {nombre}' 
                cursor.execute(sql1) 
                self.ui.label_6.setText("La base de datos ha sido creada")
                self.ui.txt_sentencia_nombre.setText(sql1)
            except Error as e:
                self.ui.label_6.setText("Ha ocurrido un error")
            finally:
                self.conexion.close()
        else:
            mensaje=QMessageBox()
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('Debe escribir el nombre de la base de datos.')
            mensaje.setWindowTitle("Error")
            mensaje.exec_()

#segunda pestaña
    def conectar_tabla(self):
        self.nombre=self.ui.txt_nombre_tabla.text()
        if self.regex.match(self.nombre) is not None:
            try:
                self.ui.btn_avanzado.setEnabled(True)
                ######################################################   
                self.conexion=mysql.connector.connect(host="localhost", 
                                    user="root",
                                    passwd="your password",database=self.nombre)
                ######################################################   
                self.ui.txt_nombre_tabla.setEnabled(False)
                self.ui.btn_conectar_tabla.setEnabled(False)
                
                return self.conexion
            except Error as e:
                self.mensajes.setWindowTitle("Error")
                self.mensajes.setIcon(QMessageBox.Warning)
                self.mensajes.setText("La base de datos NO EXISTE") 
                self.mensajes.exec_()
        else:
            self.mensajes.setWindowTitle("Error")
            self.mensajes.setIcon(QMessageBox.Warning)
            self.mensajes.setText("Debes escribir un nombre de base de datos valido") 
            self.mensajes.exec_()
            
    def valor(self):
        return self.nombre
    
    def columnaB(self):
        nombre_columna=self.ui.txt_columna.text().strip()
        if self.regex.match(nombre_columna) is not None:
            tipo_dato=str(self.ui.cbx_tipo.currentText())
            self.columnas.append(Columna(nombre_columna,tipo_dato))
            self.ui.txt_columna.setText('')
        else:
            self.mensajes.setWindowTitle("Error de nombre")
            self.mensajes.setText("Debe escribir un nombre de columna VALIDO (Solo caracteres alfabeticos)") 
            self.mensajes.exec_()        
    
    def crear_tabla(self):
        base=self.ui.txt_nombre_tabla.text().strip()
        tabla=self.ui.txt_tabla.text().strip()
        if self.ui.btn_conectar_tabla.isEnabled():   
            if self.regex.match(base) is not None:
                if self.regex.match(tabla) is not None:
                    if len(self.columnas)>0:
                        sql=f'CREATE TABLE {tabla}('
                        plantilla='{} {}'
                        campos=[]
                        for c in self.columnas:
                            campos.append(plantilla.format(c.nombre,c.tipo))
                        listaC=', '.join(campos)
                        sql+=listaC+ ')'
                    
                        try:
                            ######################################################   
                            self.conexion=mysql.connector.connect(host="localhost", 
                                        user="root",
                                        passwd="your password")   
                            ######################################################   
                            cursor2=self.conexion.cursor()
                            sqlB=f'CREATE DATABASE {base}' 
                            cursor2.execute(sqlB) 
                            cursor2.execute(f'USE {base}')
                            cursor2.execute(sql)
                            self.ui.txt_crear.setText(sql)
                            self.mensajes.setWindowTitle("EUREKA")
                            self.mensajes.setIcon(QMessageBox.Information)
                            self.mensajes.setText("Se ha creado la base de datos así como la tabla y sus columnas") 
                            self.mensajes.exec_() 
                            self.columnas.clear()
                        except Error as e:
                            self.mensajes.setWindowTitle("Error")
                            self.mensajes.setIcon(QMessageBox.Warning)
                            self.mensajes.setText("Hay problemas al crear la base de datos") 
                            self.mensajes.exec_()
                        finally:
                                self.conexion.close() 
                            
                    else:
                        self.mensajes.setWindowTitle("Error")
                        self.mensajes.setIcon(QMessageBox.Warning)
                        self.mensajes.setText("Debe agregar al menos una columna") 
                        self.mensajes.exec_() 
                else:  
                    self.mensajes.setWindowTitle("Error")
                    self.mensajes.setIcon(QMessageBox.Warning)
                    self.mensajes.setText("Debe escribir un nombre de tabla VALIDO (Solo caracteres alfabeticos)") 
                    self.mensajes.exec_() 
            else:
                self.mensajes.setWindowTitle("F en el chat")
                self.mensajes.setIcon(QMessageBox.Warning)
                self.mensajes.setText("Debe escribir un nombre de base de datos VALIDO (Solo caracteres alfabeticos)") 
                self.mensajes.exec_() 
                
        else:
            if self.regex.match(tabla) is not None:
                if len(self.columnas)>0:
                    sql=f'CREATE TABLE {tabla}('
                    plantilla='{} {}'
                    campos=[]
                    for c in self.columnas:
                        campos.append(plantilla.format(c.nombre,c.tipo))
                    listaC=', '.join(campos)
                    sql+=listaC+ ')'
                    sql=sql.replace('VARCHAR','VARCHAR(100)',-1)
                    sql=sql.replace('CHAR','CHAR(100)',-1)
                    self.conexion=self.conectar_tabla()
                    cursor2=self.conexion.cursor()
                    cursor2.execute(sql)
                    self.ui.txt_crear.setText(sql)
                    self.mensajes.setWindowTitle("EUREKA")
                    self.mensajes.setIcon(QMessageBox.Information)
                    self.mensajes.setText("Se ha creado la base de datos así como la tabla y sus columnas") 
                    self.mensajes.exec_()
                    self.ui.txt_nombre_tabla.setEnabled(True)
                    self.ui.btn_conectar_tabla.setEnabled(True)
                    self.ui.btn_avanzado.setEnabled(False)
                    self.columnas.clear()
                    self.conexion.close()
                else:
                    self.mensajes.setWindowTitle("Ups...")
                    self.mensajes.setIcon(QMessageBox.Warning)
                    self.mensajes.setText("Debe agregar al menos una columna") 
                    self.mensajes.exec_()  
            else:
                self.mensajes.setWindowTitle("Error de nombre")
                self.mensajes.setIcon(QMessageBox.Warning)
                self.mensajes.setText("Debe escribir un nombre de tabla") 
                self.mensajes.exec_()     
#Tercera pestaña
    def conectar_modificar(self):
        base=self.ui.txt_base_modificar.text()
        if len(base)>0:
            try:
                ######################################################   
                self.conexion=mysql.connector.connect(host="localhost", 
                                    user="root",
                                    passwd="your password",database=base)
                ######################################################   
                self.ui.txt_base_modificar.setEnabled(False)
                self.ui.btn_conectar_modificar.setEnabled(False)
            except Error as e:
                self.mensajes.setWindowTitle("Error")
                self.mensajes.setIcon(QMessageBox.Warning)
                self.mensajes.setText("Ocurrio un error. Verifica que la base de datos existe") 
                self.mensajes.exec_()
        else:
            self.mensajes.setWindowTitle("HEY")
            self.mensajes.setIcon(QMessageBox.Warning)
            self.mensajes.setText("Debe escribir una base de datos") 
            self.mensajes.exec_()
        return self.conexion
    
    def insertar(self):
        texto=self.ui.txt_sentencia1.toPlainText()
        if len(texto)>0 and len(self.ui.txt_base_modificar.text())>0:
            try:
                self.conexion=self.conectar_modificar()
                cursor3=self.conexion.cursor()
                cursor3.execute(texto)
                self.mensajes.setWindowTitle("EUREKA")
                self.mensajes.setIcon(QMessageBox.Information)
                self.mensajes.setText("Se han insertado los valores satisfactoriamente") 
                self.mensajes.exec_()
                self.ui.txt_sentencia1.setText('')
                self.ui.txt_base_modificar.setEnabled(True)
                self.ui.btn_conectar_modificar.setEnabled(True)
            
            except:
                self.mensajes.setWindowTitle("Error")
                self.mensajes.setIcon(QMessageBox.Warning)
                self.mensajes.setText("Tenemos un problema, amigo.") 
                self.mensajes.exec_()
        else:
            self.mensajes.setWindowTitle("ALERTA")
            self.mensajes.setIcon(QMessageBox.Warning)
            self.mensajes.setText("Debe escribir la sentencia") 
            self.mensajes.exec_()
    
    def eliminar(self):
        texto=self.ui.txt_sentencia2.toPlainText()
        if len(texto)>0 and len(self.ui.txt_base_modificar.text())>0:
            try:
                self.conexion=self.conectar_modificar()
                cursor3=self.conexion.cursor()
                sql=texto
                cursor3.execute(sql)
                self.mensajes.setWindowTitle("EUREKA")
                self.mensajes.setIcon(QMessageBox.Information)
                self.mensajes.setText("Se han eliminado los valores satisfactoriamente") 
                self.ui.txt_sentencia1.setText('')
                self.ui.txt_base_modificar.setEnabled(True)
                self.ui.btn_conectar_modificar.setEnabled(True)
                self.mensajes.exec_()
            except:
                self.mensajes.setWindowTitle("Error")
                self.mensajes.setIcon(QMessageBox.Warning)
                self.mensajes.setText("Tenemos un problema, amigo.") 
                self.mensajes.exec_()
        else:
            self.mensajes.setWindowTitle("Ups...")
            self.mensajes.setIcon(QMessageBox.Warning)
            self.mensajes.setText("Debe escribir la sentencia") 
            self.mensajes.exec_()
            
#segunda ventana (modo avanzado)
    def Avanzado(self):
        seleccion,ok=QInputDialog.getMultiLineText(self, "Escribe la sentencia SQL", "CREATE TABLE [TABLE NAME]()")
        self.conexion=self.conectar_tabla()
        cursor2=self.conexion.cursor()
        if len(seleccion)>0:
            try:
                cursor2.execute(seleccion)
                self.ui.txt_crear.setText(seleccion)
                self.mensajes.setWindowTitle("EUREKA")
                self.mensajes.setIcon(QMessageBox.Information)
                self.mensajes.setText("Se ha creado la tabla") 
                self.mensajes.exec_()
                self.ui.txt_nombre_tabla.setEnabled(True)
                self.ui.btn_conectar_tabla.setEnabled(True)
                self.ui.btn_avanzado.setEnabled(False)
                self.conexion.close()
            except Error as e:
                self.mensajes.setWindowTitle("CUIDADO")
                self.mensajes.setIcon(QMessageBox.Warning)
                self.mensajes.setText("Escribiste mal la sentencia. Intentalo de nuevo") 
                self.mensajes.exec_()
        else:
            self.mensajes.setWindowTitle("HEY")
            self.mensajes.setIcon(QMessageBox.Warning)
            self.mensajes.setText("Debes escribir la sentencia, amigo") 
            self.mensajes.exec_()
            
#cuarta pestaña  
    def consultar(self):
        lista=[]
        base=self.ui.txt_nombre_consulta.text()
        tabla=self.ui.txt_consulta_tabla.text()
        if len(base)>0 and len(tabla)>0:
            try:
                ######################################################   
                self.conexion=mysql.connector.connect(host="localhost", 
                                        user="root",
                                        passwd="your password",database=base)
                ######################################################   
                cursor1=self.conexion.cursor()
                sql1=f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tabla}';"
                cursor1.execute(sql1)
                for i in cursor1:
                    lista.append(str(i))
                lista=[line.split(',')[3] for line in lista]
                lista2=[]
                for l in lista:
                    if ' ' in l:
                        lista2.append(l[2:len(l)-1])
                        self.ui.tbw_consulta.setHorizontalHeaderLabels(lista2)
                lon=len(lista2)
                sq3=f'SELECT count(*) FROM {tabla}'
                cursor1.execute(sq3)
                for p in cursor1:
                    p=str(p)
                    p=p[1:len(p)-2]  
                sql=f"SELECT * FROM {tabla}"
                cursor1.execute(sql)
                self.ui.tbw_consulta.setRowCount(int(p)+1)
                #self.ui.tbw_consulta.setColumnCount(3)
                tablerow=0
                for row in cursor1:
                    row=list(row)
                    for i in range(len(row)):
                        celda=QTableWidgetItem(str(row[i]))
                        self.ui.tbw_consulta.setItem(tablerow,i,celda)
                    tablerow+=1
            except Error as e:
                self.mensajes.setWindowTitle("CUIDADO")
                self.mensajes.setIcon(QMessageBox.Warning)
                self.mensajes.setText("Algo ha pasado") 
                self.mensajes.exec_()
        else:
            self.mensajes.setWindowTitle("Alerta")
            self.mensajes.setIcon(QMessageBox.Warning)
            self.mensajes.setText("Debes rellenar los datos") 
            self.mensajes.exec_()
        
    def personalizada(self):
        lista=[]
        base=self.ui.txt_nombre_consulta.text()
        tabla=self.ui.txt_consulta_tabla.text()
        if len(base)>0 and len(tabla)>0:
            seleccion,ok=QInputDialog.getMultiLineText(self, "Escribe la sentencia SQL", f"SELECT * FROM {tabla}")
            if len(seleccion)>0:
                try:
                    ######################################################   
                    self.conexion=mysql.connector.connect(host="localhost", 
                                            user="root",
                                            passwd="your password",database=base)
                    ######################################################   
                    cursor1=self.conexion.cursor()
                    sq3=f'SELECT count(*) FROM {tabla}'
                    cursor1.execute(sq3)
                    for p in cursor1:
                        p=str(p)
                        p=p[1:len(p)-2] 
                    self.ui.tbw_consulta.setRowCount(int(p)+1) 
                    tablerow=0
                    cursor1.execute(seleccion)
                    for row in cursor1:
                        row=list(row)
                        for i in range(len(row)):
                            celda=QTableWidgetItem(str(row[i]))
                            self.ui.tbw_consulta.setItem(tablerow,i,celda)
                        tablerow+=1
                except Error as e:
                    self.mensajes.setWindowTitle("Error")
                    self.mensajes.setIcon(QMessageBox.Warning)
                    self.mensajes.setText("Hubo un error. Lo siento") 
                    self.mensajes.exec_()
        else:
            self.mensajes.setWindowTitle("Ups...")
            self.mensajes.setIcon(QMessageBox.Warning)
            self.mensajes.setText("Debes rellenar los datos") 
            self.mensajes.exec_()
#menu          
    def salir(self):
        sys.exit(0)
    
    def url(self):
        webbrowser.open('https://github.com/Cuadernin/MiniGestorSQL')   
        
    def datos(self):
        archivo=QFileDialog.getOpenFileName(self,'Abrir archivo','C:\\','CSV UTF-8 (delimitado por comas) (*.csv)')
        df=[]
        if archivo[0]!='':
            df=pd.read_csv(archivo[0],header=None)
            base,ok=QInputDialog.getText(self,'Base de datos','Escriba la base de datos: ') 
            tabla,ok=QInputDialog.getText(self,'Tabla','Escriba la tabla a la que desea importar los datos: ') 
            if len(base)>0 and len(tabla)>0:
                try:
                ############################################################################################
                        ############################### CODIGO ###############################
                ############################################################################################
                    self.mensajes.setWindowTitle("Informacion")
                    self.mensajes.setIcon(QMessageBox.Information)
                    self.mensajes.setText("Esta opcion no esta habilitada. No obstante, puedes habilitarla modificando el codigo fuente.") 
                    self.mensajes.exec_()
                except Error as e:
                    self.mensajes.setWindowTitle("Error")
                    self.mensajes.setIcon(QMessageBox.Warning)
                    self.mensajes.setText("Ocurrio algo. Lo siento, amigo.") 
                    self.mensajes.exec_()
            else:
                self.mensajes.setWindowTitle("Ups...")
                self.mensajes.setIcon(QMessageBox.Warning)
                self.mensajes.setText("Debes rellenar los datos") 
                self.mensajes.exec_()
                
    def contacto(self):       
        webbrowser.open('https://www.youtube.com/watch?v=fVdL3P_8MQM')              
        
if __name__ == '__main__':
    app=QApplication(sys.argv)
    ventana=base()
    ventana.show()
    sys.exit(app.exec_())
