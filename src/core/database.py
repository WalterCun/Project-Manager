# import os
# from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, JSON
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.pool import NullPool
# from datetime import datetime
# from typing import Optional, Dict, List, Any
# from pathlib import Path
#
# Base = declarative_base()
#
# class Project(Base):
#     __tablename__ = 'projects'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String, nullable=False)
#     structure = Column(JSON, nullable=False)
#     path = Column(String, nullable=True)  # Path where the project structure is generated
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     changes = relationship("Change", back_populates="project")
#
#
# class Change(Base):
#     __tablename__ = 'changes'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     project_id = Column(Integer, ForeignKey('projects.id'))
#     change_type = Column(String, nullable=False)
#     details = Column(Text)
#     timestamp = Column(DateTime, default=datetime.utcnow)
#     project = relationship("Project", back_populates="changes")
#
# class Template(Base):
#     __tablename__ = 'templates'
#     __table_args__ = {'extend_existing': True}
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     nombre = Column(String, nullable=False)
#     contenido = Column(Text, nullable=False)
#     padre_id = Column(Integer, ForeignKey('templates.id'), nullable=True)
#     extension = Column(String, nullable=False)
#     project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     padre = relationship("Template", remote_side=[id], backref="hijos")
#     project = relationship("Project", backref="templates")
#
# class DatabaseManager:
#     def __init__(self, db_path: str = 'project-manager.db'):
#         self.db_path = db_path
#
#         # Ensure the SQLite file exists to avoid teardown FileNotFoundError in tests
#         try:
#             if self.db_path and self.db_path != ':memory:' and not os.path.exists(self.db_path):
#                 # Create the file (empty); SQLite will use it
#                 open(self.db_path, 'a').close()
#         except Exception:
#             # Non-fatal; continue
#             pass
#
#         self.engine = create_engine(f'sqlite:///{db_path}', echo=False, poolclass=NullPool)
#
#         # Create all tables (including new columns)
#         try:
#             Base.metadata.create_all(self.engine)
#         except Exception as e:
#             # Handle potential column addition issues
#             print(f"Warning: Database schema update issue: {e}")
#             # Try to continue anyway
#             pass
#
#         self.Session = sessionmaker(bind=self.engine)
#
#         # Optionally auto-initialize templates when explicitly enabled
#         if os.getenv('PSM_INIT_BASE_TEMPLATES') == '1':
#             try:
#                 from .base_templates import initialize_base_templates
#                 initialize_base_templates(self)
#             except Exception as e:
#                 print(f"Warning: Failed to initialize base templates: {e}")
#             try:
#                 from .external_templates import initialize_external_templates
#                 initialize_external_templates()
#             except Exception as e:
#                 print(f"Warning: Failed to initialize external templates: {e}")
#
#     def dispose(self) -> None:
#         """Dispose the SQLAlchemy engine to release file handles (especially on Windows)."""
#         try:
#             if hasattr(self, 'engine') and self.engine:
#                 self.engine.dispose()
#         except Exception:
#             pass
#
#     def __del__(self):
#         # Best-effort cleanup
#         self.dispose()
#
#     def save_project(self, name: str, structure: Dict[str, Any], path: Optional[str] = None) -> int:
#         session = self.Session()
#         try:
#             # Handle case where path column might not exist in older databases
#             try:
#                 project = Project(name=name, structure=structure, path=path)
#                 session.add(project)
#                 session.commit()
#                 self.log_change(project.id, 'CREATE', f'Project {name} created at {path or "default location"}')
#                 return project.id
#             except Exception:
#                 # Fallback for databases without path column
#                 project = Project(name=name, structure=structure)
#                 session.add(project)
#                 session.commit()
#                 if path:
#                     print(f"Warning: Path column not available in database. Project created without path tracking.")
#                 self.log_change(project.id, 'CREATE', f'Project {name} created')
#                 return project.id
#         except Exception as e:
#             session.rollback()
#             raise RuntimeError(f"Failed to save project: {e}")
#         finally:
#             session.close()
#
#     def update_project(self, project_id: int, structure: Optional[Dict[str, Any]] = None, path: Optional[str] = None) -> None:
#         session = self.Session()
#         try:
#             # Try to query with path column first
#             try:
#                 project = session.query(Project).filter_by(id=project_id).first()
#                 if project:
#                     if structure is not None:
#                         project.structure = structure
#                     # Only try to update path if the column exists
#                     if path is not None and hasattr(project, 'path'):
#                         project.path = path
#                     project.updated_at = datetime.utcnow()
#                     session.commit()
#                     action = 'Structure and path updated' if structure and path else ('Structure updated' if structure else 'Path updated')
#                     self.log_change(project_id, 'UPDATE', action)
#             except Exception:
#                 # Fallback for databases without path column
#                 project = session.query(Project).filter_by(id=project_id).first()
#                 if project:
#                     if structure is not None:
#                         project.structure = structure
#                     project.updated_at = datetime.utcnow()
#                     session.commit()
#                     self.log_change(project_id, 'UPDATE', 'Structure updated')
#         except Exception as e:
#             session.rollback()
#             raise RuntimeError(f"Failed to update project: {e}")
#         finally:
#             session.close()
#
#     def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
#         session = self.Session()
#         try:
#             # Try to query with path column first
#             try:
#                 project = session.query(Project).filter_by(id=project_id).first()
#                 if project:
#                     return {
#                         'id': project.id,
#                         'name': project.name,
#                         'structure': project.structure,
#                         'path': getattr(project, 'path', None),
#                         'created_at': project.created_at.isoformat() if project.created_at else None,
#                         'updated_at': project.updated_at.isoformat() if project.updated_at else None
#                     }
#             except Exception:
#                 # Fallback for databases without path column
#                 project = session.query(Project.id, Project.name, Project.structure, Project.created_at, Project.updated_at).filter_by(id=project_id).first()
#                 if project:
#                     return {
#                         'id': project.id,
#                         'name': project.name,
#                         'structure': project.structure,
#                         'path': None,
#                         'created_at': project.created_at.isoformat() if project.created_at else None,
#                         'updated_at': project.updated_at.isoformat() if project.updated_at else None
#                     }
#             return None
#         except Exception as e:
#             raise RuntimeError(f"Failed to get project: {e}")
#         finally:
#             session.close()
#
#     def list_projects(self) -> List[Dict[str, Any]]:
#         session = self.Session()
#         try:
#             # Try to query with path column first
#             try:
#                 projects = session.query(Project).all()
#                 return [{'id': p.id, 'name': p.name, 'path': getattr(p, 'path', None), 'updated_at': p.updated_at.isoformat() if p.updated_at else None} for p in projects]
#             except Exception:
#                 # Fallback for databases without path column
#                 projects = session.query(Project.id, Project.name, Project.updated_at).all()
#                 return [{'id': p.id, 'name': p.name, 'path': None, 'updated_at': p.updated_at.isoformat() if p.updated_at else None} for p in projects]
#         except Exception as e:
#             raise RuntimeError(f"Failed to list projects: {e}")
#         finally:
#             session.close()
#
#     def get_project_by_name(self, project_name: str) -> Optional[Dict[str, Any]]:
#         """Get project by name."""
#         session = self.Session()
#         try:
#             # Try to query with path column first
#             try:
#                 project = session.query(Project).filter_by(name=project_name).first()
#                 if project:
#                     return {
#                         'id': project.id,
#                         'name': project.name,
#                         'structure': project.structure,
#                         'path': getattr(project, 'path', None),
#                         'created_at': project.created_at.isoformat() if project.created_at else None,
#                         'updated_at': project.updated_at.isoformat() if project.updated_at else None
#                     }
#             except Exception:
#                 # Fallback for databases without path column
#                 project = session.query(Project.id, Project.name, Project.structure, Project.created_at, Project.updated_at).filter_by(name=project_name).first()
#                 if project:
#                     return {
#                         'id': project.id,
#                         'name': project.name,
#                         'structure': project.structure,
#                         'path': None,
#                         'created_at': project.created_at.isoformat() if project.created_at else None,
#                         'updated_at': project.updated_at.isoformat() if project.updated_at else None
#                     }
#             return None
#         except Exception as e:
#             raise RuntimeError(f"Failed to get project by name: {e}")
#         finally:
#             session.close()
#
#     def check_duplicate_name(self, project_name: str) -> bool:
#         """Check if a project name already exists."""
#         projects = self.list_projects()
#         return any(p['name'] == project_name for p in projects)
#
#     @staticmethod
#     def check_path_exists(path: str) -> bool:
#         """Check if a directory exists at the given path."""
#         import os
#         return os.path.exists(path)
#
#     def check_project_path_conflict(self, project_name: str, path: str) -> Optional[str]:
#         """Check if there's a conflict with an existing project path."""
#         full_path = os.path.join(path, project_name)
#         existing_project = self.get_project_by_name(project_name)
#         if existing_project and existing_project['path']:
#             if existing_project['path'] in (full_path, path):
#                 return "same_path"  # Same project, same path (accept stored full path or provided base path)
#             elif os.path.exists(full_path):
#                 if os.listdir(full_path):
#                     return "path_exists_with_files"  # Directory exists with files
#                 else:
#                     return "path_exists_empty"  # Directory exists but is empty
#         elif os.path.exists(full_path):
#             if os.listdir(full_path):
#                 return "path_exists_with_files"  # Directory exists with files
#             else:
#                 return "path_exists_empty"  # Directory exists but is empty
#         return None  # No conflict
#
#
#     def log_change(self, project_id: int, change_type: str, details: str) -> None:
#         session = self.Session()
#         try:
#             change = Change(project_id=project_id, change_type=change_type, details=details)
#             session.add(change)
#             session.commit()
#         except Exception as e:
#             session.rollback()
#             raise RuntimeError(f"Failed to log change: {e}")
#         finally:
#             session.close()
#
#     def get_change_history(self, project_id: int) -> List[Dict[str, str]]:
#         session = self.Session()
#         try:
#             changes = session.query(Change).filter_by(project_id=project_id).order_by(Change.timestamp.desc()).all()
#             return [{'change_type': c.change_type, 'details': c.details, 'timestamp': c.timestamp.isoformat() if c.timestamp else None} for c in changes]
#         except Exception as e:
#             raise RuntimeError(f"Failed to get change history: {e}")
#         finally:
#             session.close()
#
#     def save_template(self, nombre: str, contenido: str, extension: str, padre_id: Optional[int] = None, project_id: Optional[int] = None) -> int:
#         session = self.Session()
#         try:
#             template = Template(nombre=nombre, contenido=contenido, extension=extension, padre_id=padre_id, project_id=project_id)
#             session.add(template)
#             session.commit()
#             return template.id
#         except Exception as e:
#             session.rollback()
#             raise RuntimeError(f"Failed to save template: {e}")
#         finally:
#             session.close()
#
#     def update_template(self, template_id: int, nombre: Optional[str] = None, contenido: Optional[str] = None, extension: Optional[str] = None, padre_id: Optional[int] = None, project_id: Optional[int] = None) -> None:
#         session = self.Session()
#         try:
#             template = session.query(Template).filter_by(id=template_id).first()
#             if template:
#                 if nombre is not None:
#                     template.nombre = nombre
#                 if contenido is not None:
#                     template.contenido = contenido
#                 if extension is not None:
#                     template.extension = extension
#                 if padre_id is not None:
#                     template.padre_id = padre_id
#                 if project_id is not None:
#                     template.project_id = project_id
#                 template.updated_at = datetime.utcnow()
#                 session.commit()
#         except Exception as e:
#             session.rollback()
#             raise RuntimeError(f"Failed to update template: {e}")
#         finally:
#             session.close()
#
#     def get_template(self, template_id: int) -> Optional[Dict[str, Any]]:
#         session = self.Session()
#         try:
#             template = session.query(Template).filter_by(id=template_id).first()
#             if template:
#                 return {
#                     'id': template.id,
#                     'nombre': template.nombre,
#                     'contenido': template.contenido,
#                     'padre_id': template.padre_id,
#                     'extension': template.extension,
#                     'project_id': template.project_id,
#                     'created_at': template.created_at.isoformat() if template.created_at else None,
#                     'updated_at': template.updated_at.isoformat() if template.updated_at else None
#                 }
#             return None
#         except Exception as e:
#             raise RuntimeError(f"Failed to get template: {e}")
#         finally:
#             session.close()
#
#     def list_templates(self, project_id: Optional[int] = None) -> List[Dict[str, Any]]:
#         session = self.Session()
#         try:
#             query = session.query(Template)
#             if project_id is not None:
#                 query = query.filter_by(project_id=project_id)
#             templates = query.all()
#             return [{
#                 'id': t.id,
#                 'nombre': t.nombre,
#                 'extension': t.extension,
#                 'padre_id': t.padre_id,
#                 'project_id': t.project_id,
#                 'updated_at': t.updated_at.isoformat() if t.updated_at else None
#             } for t in templates]
#         except Exception as e:
#             raise RuntimeError(f"Failed to list templates: {e}")
#         finally:
#             session.close()
#
#     def delete_template(self, template_id: int) -> None:
#         session = self.Session()
#         try:
#             template = session.query(Template).filter_by(id=template_id).first()
#             if template:
#                 session.delete(template)
#                 session.commit()
#         except Exception as e:
#             session.rollback()
#             raise RuntimeError(f"Failed to delete template: {e}")
#         finally:
#             session.close()