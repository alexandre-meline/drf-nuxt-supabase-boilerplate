from __future__ import annotations
from .base import env

# Supabase JWT secret
SUPABASE_JWT_SECRET = env.str('SUPABASE_JWT_SECRET')
SUPABASE_WEBHOOK_SECRET = env.str('SUPABASE_WEBHOOK_SECRET')