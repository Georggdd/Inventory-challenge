"""
Define la dependencia de autenticación para las rutas de la API.
"""

import os
from fastapi import Depends
from .auth import maybe_auth_dependency

# Devuelve la dependencia que aplica autenticación solo si REQUIRE_AUTH=true

RequireAuth = maybe_auth_dependency  

