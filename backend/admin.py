# =====================================================
# ADMIN MODULE
# =====================================================
#
# The actual Admin Blueprint is located in:
#
# backend/admin/__init__.py
#
# Flask uses that Blueprint.
#
# This file is intentionally kept empty so that
# two different "admin" Blueprints are not registered.
# =====================================================


def admin_module_loaded():
    """
    Compatibility function.
    The actual admin routes are inside
    admin/__init__.py.
    """
    return True