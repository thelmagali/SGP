from sqlalchemy import Table, Integer, ForeignKey, String, Column, Date, create_engine
from sqlalchemy import Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


"""Modulo contenedor de las clases de las entidades"""  
__author__ = 'Grupo 5'
__date__ = '23/04/13'
__version__ = '1.0'
__credits__ = 'none'
__text__ = 'Modulo con las clases y las tablas relacionadas entre si'
__file__ = 'Modelo.py' 

engine = create_engine('postgresql+psycopg2://admin:admin@localhost/sgptest')
Base = declarative_base()

"""------------------------TABLAS DE RELACION---------------------------------------"""
RolPermiso = Table('rolpermiso', Base.metadata,
    Column('idrol', Integer, ForeignKey('rol.idrol'),primary_key=True),
    Column('idpermiso', Integer, ForeignKey('permiso.idpermiso'),primary_key=True)
)

RolUsuario = Table('rolusuario', Base.metadata,
    Column('idusuario', Integer, ForeignKey('usuario.idusuario'),primary_key=True),
    Column('idrol', Integer, ForeignKey('rol.idrol'),primary_key=True)
)

RolFase = Table('rolfase', Base.metadata,
    Column('idrol', Integer, ForeignKey('rol.idrol'),primary_key=True),
    Column('idfase', Integer, ForeignKey('fase.idfase'),primary_key=True)
)

ComiteCambios = Table('comitecambios', Base.metadata,
    Column('idusuario', Integer, ForeignKey('usuario.idusuario'),primary_key=True),
    Column('idproyecto', Integer, ForeignKey('proyecto.idproyecto',
                                             onupdate="CASCADE",
                                            ondelete="CASCADE"),
                                            primary_key=True)
)

TipoItemFase = Table('tipoitemfase',Base.metadata,
    Column('idtipoitem', Integer, ForeignKey('tipoitem.idtipoitem'),primary_key=True),
    Column('idfase', Integer, ForeignKey('fase.idfase'),primary_key=True)
)

"""------------------------USUARIO---------------------------------------""" 
class Usuario(Base):
    __tablename__ = 'usuario'
    idusuario = Column(Integer,primary_key = True)
    username = Column(String(45),unique = True)
    passwrd = Column(String(160))
    nombre = Column(String(45))
    apellido = Column(String(45))
    telefono = Column(String(45))
    ci = Column(Integer)
    roles = relationship("Rol",secondary=RolUsuario)   
     
    def __init__(self, idusuario, username, passwrd, nombre, apellido, telefono, ci):
        self.idusuario = idusuario
        self.username = username
        self.passwrd = passwrd
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.ci = ci
 
    def __repr__(self):
        return "<Usuario '%s' '%s' '%s' '%s' '%s' '%s' '%s'>" % self.idusuario, self.username, self.passwrd, self.nombre, self.apellido, self.telefono, self.ci 

"""------------------------ROL---------------------------------------"""
class Rol(Base):
    __tablename__ = 'rol'
    idrol = Column(Integer,primary_key=True)
    nombre = Column(String(160))
    descripcion = Column(String(300))
    permisos = relationship("Permiso", secondary=RolPermiso)
 
    def __init__(self, idrol,nombre, descripcion):
        self.idrol = idrol
        self.nombre = nombre
        self.descripcion = descripcion
 
 
    def __repr__(self):
        return "<Rol '%s' '%s' '%s'>" % self.idrol, self.nombre, self.descripcion

"""------------------------PERMISO---------------------------------------"""
class Permiso(Base):
    __tablename__ = 'permiso'
    idpermiso = Column(Integer,primary_key = True)
    nombre = Column(String(160))
    descripcion = Column(String(400))
   
    def __init__(self, idpermiso,nombre, descripcion):
        self.idpermiso = idpermiso
        self.nombre = nombre
        self.descripcion = descripcion
 
    def __repr__(self):
        return "<Permiso '%s' '%s' '%s'>" % self.idpermiso, self.nombre, self.descripcion 

"""------------------------PROYECTO---------------------------------------"""
class Proyecto(Base):
    __tablename__ = 'proyecto'
    idproyecto = Column(Integer,primary_key = True)
    nombre = Column(String(45))
    descripcion = Column(String(200))
    fechacreacion = Column(Date)
    complejidad = Column(Integer)
    estado = Column(String(45))
    usuariolider = Column(Integer, ForeignKey('usuario.idusuario'))
    usuario = relationship("Usuario")
    presupuesto = Column(Integer)
    
    comitecambios = relationship("Usuario", secondary=ComiteCambios)

     
    def __init__(self,idproyecto,nombre,descripcion,fechacreacion,complejidad,estado,usuariolider,presupuesto):
        self.idproyecto = idproyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechacreacion = fechacreacion
        self.complejidad = complejidad
        self.estado = estado
        self.usuariolider = usuariolider
        self.presupuesto = presupuesto
 
    def __repr__(self):
        return "<Proyecto '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s'>" % self.idproyecto, self.nombre, self.descripcion, self.fechacreacion, self.complejidad, self.estado, self.usuariolider, self.presupuesto

"""------------------------FASE---------------------------------------"""
class Fase(Base):

    __tablename__ = 'fase'
    idfase = Column(Integer,primary_key = True)
    idproyecto = Column(Integer,ForeignKey('proyecto.idproyecto',
                                            onupdate="CASCADE",
                                            ondelete="CASCADE"))
    proyecto = relationship("Proyecto")
    posicionfase = Column(Integer)
    nombre = Column(String(45))
    descripcion = Column(String(45))
    roles = relationship("Rol", secondary=RolFase)
    tipositems = relationship("TipoItem", secondary=TipoItemFase)
    
    def __init__(self, idfase, idproyecto, posicionfase, nombre, descripcion):
        self.idfase = idfase
        self.idproyecto = idproyecto
        self.posicionfase = posicionfase
        self.nombre = nombre
        self.descripcion = descripcion


    def __repr__(self):
        return "<Fase '%s' '%s' '%s' '%s' '%s' '%s' '%s'>" % self.idfase, self.idproyecto, self.posicionfase, self.nombre, self.descripcion 

"""------------------------TIPO DE ITEM---------------------------------------"""
class TipoItem(Base):
    __tablename__ = 'tipoitem'
    idtipoitem = Column(Integer,Sequence('sec_idtipoitem'),primary_key=True)
    nombre = Column(String(160))
    descripcion = Column(String(300))
    atributos = relationship("AtributoTipo")
 
    def __init__(self,nombre, descripcion):
        #self.idtipoitem = idtipoitem #La secuencia se encargara de esto
        self.nombre = nombre
        self.descripcion = descripcion
 
 
    def __repr__(self):
        return "<TipoItem '%s' '%s' '%s'>" % self.idtipoitem, self.nombre, self.descripcion
    
"""------------------------ATRIBUTO POR TIPO DE ITEM---------------------------------------"""
class AtributoTipo(Base):
    __tablename__ = 'atributotipo'
    idatributo = Column(Integer,Sequence('sec_atributotipo'),primary_key=True)
    idtipoitem = Column(Integer,ForeignKey('tipoitem.idtipoitem',
                                        onupdate="CASCADE",
                                        ondelete="CASCADE"))
    nombre = Column(String(160))
    tipo = Column(String(45))
    valordefecto = Column(String(45))

    def __init__(self,idtipoitem, nombre, tipo, valordefecto):
        self.idtipoitem = idtipoitem
        self.nombre = nombre
        self.tipo = tipo
        self.valordefecto = valordefecto

    def __repr__(self):
        return "<AtributoTipo '%s' '%s' '%s' '%s' '%s'>" % self.idatributo, self.idtipoitem, self.nombre, self.tipo, self.valordefecto
        
"""------------------------ATRIBUTO DE ITEM POR TIPO DE ITEM---------------------------------------"""
class AtributoItemPorTipo(Base):
    __tablename__ = 'atributoitemportipo'
    iditem = Column(Integer, ForeignKey('item.iditem'),primary_key=True)
    idatributo = Column(Integer,ForeignKey('atributotipo.idatributo'),primary_key=True)
    valor = Column(String(45))
       
    def __init__(self, iditem, idatributo, valor):
        self.iditem = iditem
        self.idatributo = idatributo
        self.valor = valor
 
    def __repr__(self):
        return "<AtributoItemPorTipo '%s' '%s' '%s' '%s'>" % self.iditem, self.idatributo, self.valor
       
"""------------------------ITEM---------------------------------------"""
class Item(Base):
    __tablename__ = 'item'
    iditem = Column(Integer,primary_key=True)
    nombre = Column(String(160))
    estado = Column(String(45))
    idtipoitem = Column(Integer, ForeignKey('tipoitem.idtipoitem'))
    idfase = Column(Integer, ForeignKey('fase.idfase'))        
    idlineabase = Column (Integer,ForeignKey ('lineabase.idlineabase'))
 
    def __init__(self, iditem, nombre, estado, idtipoitem,idfase):
        self.iditem = iditem
        self.nombre = nombre 
        self.estado = estado
        self.idtipoitem = idtipoitem
        self.idfase = idfase
        self.idlineabase = idlineabase               
 
 
    def __repr__(self):
        return "<Item '%s' '%s' '%s' '%s' '%s' '%s' '%s'>" % self.idtipoitem, self.nombre,self.estado, self.idtipoitem, self.idfase, self.lineabase
        
"""------------------------VERSION DEL ITEM---------------------------------------"""
class VersionItem(Base):
    __tablename__ = 'versionitem'
    idversionitem = Column(Integer, primary_key=True)   
    iditem = Column(Integer,ForeignKey('item.iditem')) 
    idusuario = Column (Integer, ForeignKey('usuario.idusuario'))
    descripcion = Column(String(160))
    complejidad = Column(Integer)
    prioridad = Column(Integer)
    costo = Column(Integer)                   

    def __init__(self, idversionitem, iditem, idusuario,descripcion,complejidad,prioridad,costo):
        self.idversionitem = idversionitem
        self.iditem = iditem
        self.idusuario = idusuario
        self.descripcion = descripcion
        self.complejidad = complejidad
        self.prioridad = prioridad
        self.costo = costo        

    def __repr__(self):
        return "<Item '%s' '%s' '%s' '%s' '%s' '%s' '%s'>" % self.idversionitem, self.iditem, self.idusuario, self.descripcion, self.complejidad, self.prioridad, self.costo
    
"""------------------------RELACION ENTRE ITEMS---------------------------------------"""
class Relacion(Base):
    __tablename__ = 'relacion'
    delitem = Column(Integer,ForeignKey('item.iditem'), primary_key=True)   
    alitem = Column(Integer,ForeignKey('item.iditem'), primary_key=True)
    tipo = Column(String(45))

    def __init__(self, delitem, alitem,tipo):
        self.delitem = delitem
        self.alitem = alitem
        self.tipo = tipo

    def __repr__(self):
        return "<Item '%s' '%s' '%s'>" % self.delitem, self.alitem, self.tipo
 
"""------------------------LINEA BASE---------------------------------------"""
class LineaBase(Base):
    __tablename__ = 'lineabase'
    idlineabase = Column(Integer,primary_key=True)   
    idfase = Column(Integer,ForeignKey('fase.idfase'))
    estado = Column(String(45))
    numero = Column(Integer)
    
    def __init__(self, idlineabase, idfase, estado,numero):
        self.idlineabase = idlineabase
        self.idfase = idfase
        self.estado = estado
        selnumero = numero


    def __repr__(self):
        return "<LineaBase'%s' '%s' '%s' '%s'>" % self.idlineabase, self.idfase, self.estado, self.numero
        
Base.metadata.create_all(engine)  