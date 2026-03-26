from fastapi import HTTPException, status


def verify_resource_owner(resource_user_id: int, current_user_id: int) -> None:
    """
    Verify that the current user is the owner of the resource.
    
    Raises HTTP 403 Forbidden if the user is not the owner.
    """
    if resource_user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access or modify this resource",
        )
