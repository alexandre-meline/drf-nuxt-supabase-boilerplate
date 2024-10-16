from __future__ import annotations
from .base import env


FRONTEND_URL=env.str('FRONTEND_URL', default='http://localhost:3000')