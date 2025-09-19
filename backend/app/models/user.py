from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from .base import Base  

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  
    email = Column(String(100), unique=True, index=True)   
    hashed_password = Column(String(255))  
    is_active = Column(Boolean, default=True)
    full_name = Column(String(200))  
    is_superuser = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=func.now())
    ultimo_login = Column(DateTime)
    departamento = Column(String(50))
    rol_sistema = Column(String(30))  # admin, usuario, solo-lectura


    empleado_id = Column(Integer, ForeignKey('empleados.id')) #fk
    
    # Relación
    empleado = relationship(
        "Empleado", 
        back_populates="user",
        foreign_keys=[empleado_id]
    )
    
    def __repr__(self):
        return f"<User(username='{self.username}')>"
    
    def __str__(self):
        return self.username

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)
    
    def get_password_hash(self, password):
        return pwd_context.hash(password)