"""
Define la dependencia de autenticación para las rutas de la API.
"""

import os
from fastapi import Depends
from .auth import maybe_auth_dependency

RequireAuth = maybe_auth_dependency  
