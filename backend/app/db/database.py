# Agregar estos métodos a la clase Database

def update_user_session(self, email: str, account_id: int, domain: str, timestamp: str) -> bool:
    data = self._read_data()
    user = next((u for u in data["users"] if u["email"] == email), None)
    if not user:
        return False
        
    if "active_sessions" not in user:
        user["active_sessions"] = {}
        
    user["active_sessions"][domain] = timestamp
    self._write_data(data)
    return True

def end_user_session(self, email: str, account_id: int, domain: str) -> bool:
    data = self._read_data()
    user = next((u for u in data["users"] if u["email"] == email), None)
    if not user and "active_sessions" in user:
        return False
        
    user["active_sessions"].pop(domain, None)
    self._write_data(data)
    return True

def extend_user_validity(self, email: str, days: int) -> bool:
    data = self._read_data()
    user = next((u for u in data["users"] if u["email"] == email), None)
    if not user:
        return False
        
    if days == -1:
        user["valid_until"] = None
    else:
        from datetime import datetime, timedelta
        user["valid_until"] = (datetime.utcnow() + timedelta(days=days)).isoformat()
        
    self._write_data(data)
    return True

def get_user_by_email(self, email: str) -> Optional[Dict]:
    data = self._read_data()
    user = next((user for user in data["users"] if user["email"] == email), None)
    if user:
        # Add assigned accounts
        user["assigned_accounts"] = [
            ua["account_id"] for ua in data["user_accounts"] 
            if ua["user_id"] == email
        ]
        
        # Check expiration
        if "valid_until" in user and user["valid_until"]:
            from datetime import datetime
            valid_until = datetime.fromisoformat(user["valid_until"].replace('Z', '+00:00'))
            user["is_expired"] = datetime.utcnow() > valid_until
        else:
            user["is_expired"] = False
            
        # Initialize active sessions if not present
        if "active_sessions" not in user:
            user["active_sessions"] = {}
            
    return user