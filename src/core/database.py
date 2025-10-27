from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from typing import Optional, Dict, List, Any

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    structure = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    changes = relationship("Change", back_populates="project")


class Change(Base):
    __tablename__ = 'changes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    change_type = Column(String, nullable=False)
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="changes")

class Template(Base):
    __tablename__ = 'templates'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    contenido = Column(Text, nullable=False)
    padre_id = Column(Integer, ForeignKey('templates.id'), nullable=True)
    extension = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    padre = relationship("Template", remote_side=[id], backref="hijos")
    project = relationship("Project", backref="templates")

class DatabaseManager:
    def __init__(self, db_path: str = 'project-manager.db'):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        # Initialize base templates (import here to avoid circular import)
        from .base_templates import initialize_base_templates
        initialize_base_templates(self)

    def save_project(self, name: str, structure: Dict[str, Any]) -> int:
        session = self.Session()
        try:
            project = Project(name=name, structure=structure)
            session.add(project)
            session.commit()
            self.log_change(project.id, 'CREATE', f'Project {name} created')
            return project.id
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Failed to save project: {e}")
        finally:
            session.close()

    def update_project(self, project_id: int, structure: Dict[str, Any]) -> None:
        session = self.Session()
        try:
            project = session.query(Project).filter_by(id=project_id).first()
            if project:
                project.structure = structure
                project.updated_at = datetime.utcnow()
                session.commit()
                self.log_change(project_id, 'UPDATE', 'Structure updated')
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Failed to update project: {e}")
        finally:
            session.close()

    def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        session = self.Session()
        try:
            project = session.query(Project).filter_by(id=project_id).first()
            if project:
                return {
                    'id': project.id,
                    'name': project.name,
                    'structure': project.structure,
                    'created_at': project.created_at.isoformat() if project.created_at else None,
                    'updated_at': project.updated_at.isoformat() if project.updated_at else None
                }
            return None
        except Exception as e:
            raise RuntimeError(f"Failed to get project: {e}")
        finally:
            session.close()

    def list_projects(self) -> List[Dict[str, Any]]:
        session = self.Session()
        try:
            projects = session.query(Project).all()
            return [{'id': p.id, 'name': p.name, 'updated_at': p.updated_at.isoformat() if p.updated_at else None} for p in projects]
        except Exception as e:
            raise RuntimeError(f"Failed to list projects: {e}")
        finally:
            session.close()


    def log_change(self, project_id: int, change_type: str, details: str) -> None:
        session = self.Session()
        try:
            change = Change(project_id=project_id, change_type=change_type, details=details)
            session.add(change)
            session.commit()
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Failed to log change: {e}")
        finally:
            session.close()

    def get_change_history(self, project_id: int) -> List[Dict[str, str]]:
        session = self.Session()
        try:
            changes = session.query(Change).filter_by(project_id=project_id).order_by(Change.timestamp.desc()).all()
            return [{'change_type': c.change_type, 'details': c.details, 'timestamp': c.timestamp.isoformat() if c.timestamp else None} for c in changes]
        except Exception as e:
            raise RuntimeError(f"Failed to get change history: {e}")
        finally:
            session.close()

    def save_template(self, nombre: str, contenido: str, extension: str, padre_id: Optional[int] = None, project_id: Optional[int] = None) -> int:
        session = self.Session()
        try:
            template = Template(nombre=nombre, contenido=contenido, extension=extension, padre_id=padre_id, project_id=project_id)
            session.add(template)
            session.commit()
            return template.id
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Failed to save template: {e}")
        finally:
            session.close()

    def update_template(self, template_id: int, nombre: Optional[str] = None, contenido: Optional[str] = None, extension: Optional[str] = None, padre_id: Optional[int] = None, project_id: Optional[int] = None) -> None:
        session = self.Session()
        try:
            template = session.query(Template).filter_by(id=template_id).first()
            if template:
                if nombre is not None:
                    template.nombre = nombre
                if contenido is not None:
                    template.contenido = contenido
                if extension is not None:
                    template.extension = extension
                if padre_id is not None:
                    template.padre_id = padre_id
                if project_id is not None:
                    template.project_id = project_id
                template.updated_at = datetime.utcnow()
                session.commit()
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Failed to update template: {e}")
        finally:
            session.close()

    def get_template(self, template_id: int) -> Optional[Dict[str, Any]]:
        session = self.Session()
        try:
            template = session.query(Template).filter_by(id=template_id).first()
            if template:
                return {
                    'id': template.id,
                    'nombre': template.nombre,
                    'contenido': template.contenido,
                    'padre_id': template.padre_id,
                    'extension': template.extension,
                    'project_id': template.project_id,
                    'created_at': template.created_at.isoformat() if template.created_at else None,
                    'updated_at': template.updated_at.isoformat() if template.updated_at else None
                }
            return None
        except Exception as e:
            raise RuntimeError(f"Failed to get template: {e}")
        finally:
            session.close()

    def list_templates(self, project_id: Optional[int] = None) -> List[Dict[str, Any]]:
        session = self.Session()
        try:
            query = session.query(Template)
            if project_id is not None:
                query = query.filter_by(project_id=project_id)
            templates = query.all()
            return [{
                'id': t.id,
                'nombre': t.nombre,
                'extension': t.extension,
                'padre_id': t.padre_id,
                'project_id': t.project_id,
                'updated_at': t.updated_at.isoformat() if t.updated_at else None
            } for t in templates]
        except Exception as e:
            raise RuntimeError(f"Failed to list templates: {e}")
        finally:
            session.close()

    def delete_template(self, template_id: int) -> None:
        session = self.Session()
        try:
            template = session.query(Template).filter_by(id=template_id).first()
            if template:
                session.delete(template)
                session.commit()
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Failed to delete template: {e}")
        finally:
            session.close()