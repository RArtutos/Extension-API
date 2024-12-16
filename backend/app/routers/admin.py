# Agregar este endpoint al router admin

@router.post("/users/{user_id}/extend")
async def extend_user_validity(
    user_id: str, 
    days: int,
    current_user: dict = Depends(get_current_admin_user)
):
    if not db.extend_user_validity(user_id, days):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User validity extended successfully"}

@router.post("/users/{user_id}/sessions/{account_id}")
async def update_user_session(
    user_id: str,
    account_id: int,
    domain: str,
    timestamp: str,
    current_user: dict = Depends(get_current_user)
):
    if not db.update_user_session(user_id, account_id, domain, timestamp):
        raise HTTPException(status_code=404, detail="User or account not found")
    return {"message": "Session updated successfully"}

@router.delete("/users/{user_id}/sessions/{account_id}")
async def end_user_session(
    user_id: str,
    account_id: int,
    domain: str,
    current_user: dict = Depends(get_current_user)
):
    if not db.end_user_session(user_id, account_id, domain):
        raise HTTPException(status_code=404, detail="User or account not found")
    return {"message": "Session ended successfully"}