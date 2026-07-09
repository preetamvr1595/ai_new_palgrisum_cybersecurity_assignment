import pytest
from fastapi import HTTPException
from backend.api.dependencies import require_role
from backend.db.models.user import User

def test_require_role_allowed():
    # Mock a User with "admin" role
    user = User(role="admin", is_active=True)
    
    # create the dependency factory
    role_checker = require_role(["admin", "super_admin"])
    
    # Should not raise an exception
    returned_user = role_checker(current_user=user)
    assert returned_user.role == "admin"

def test_require_role_forbidden():
    # Mock a User with "free_user" role
    user = User(role="free_user", is_active=True)
    
    role_checker = require_role(["admin", "super_admin"])
    
    with pytest.raises(HTTPException) as excinfo:
        role_checker(current_user=user)
        
    assert excinfo.value.status_code == 403
    assert excinfo.value.detail == "You do not have enough privileges"

def test_super_admin_bypass():
    # Mock a User with "super_admin" role
    user = User(role="super_admin", is_active=True)
    
    # Even if "super_admin" is not explicitly in allowed_roles, 
    # the require_role logic allows super_admin to bypass.
    role_checker = require_role(["free_user", "premium_user"])
    
    returned_user = role_checker(current_user=user)
    assert returned_user.role == "super_admin"
