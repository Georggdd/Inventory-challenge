import os
from fastapi import Depends
from .auth import maybe_auth_dependency

RequireAuth = maybe_auth_dependency  # alias to be explicit
