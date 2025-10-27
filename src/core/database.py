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

class Template(Base):
    __tablename__ = 'templates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    structure = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Change(Base):
    __tablename__ = 'changes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    change_type = Column(String, nullable=False)
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="changes")

class DatabaseManager:
    def __init__(self, db_path: str = 'project_structure.db'):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

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

    def save_template(self, name: str, structure: Dict[str, Any]) -> None:
        session = self.Session()
        try:
            template = Template(name=name, structure=structure)
            session.add(template)
            session.commit()
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Failed to save template: {e}")
        finally:
            session.close()

    def get_templates(self) -> List[Dict[str, Any]]:
        session = self.Session()
        try:
            templates = session.query(Template).all()
            return [{'id': t.id, 'name': t.name, 'structure': t.structure} for t in templates]
        except Exception as e:
            raise RuntimeError(f"Failed to get templates: {e}")
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