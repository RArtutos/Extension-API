# Account Manager API Documentation

## Overview
This document describes the API endpoints available in the Account Manager backend service.

## Base URL
```
https://api.artutos.us.kg
```

## Authentication
All endpoints except `/api/auth/login` require authentication using a Bearer token.

```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication

#### Login
- **POST** `/api/auth/login`
- **Body**: `username=<email>&password=<password>` (form-urlencoded)
- **Response**: 
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

#### Validate Token
- **GET** `/api/auth/validate`
- **Response**:
```json
{
  "email": "string",
  "is_admin": boolean
}
```

### Accounts

#### Get All Accounts
- **GET** `/api/accounts`
- **Response**: Array of accounts
```json
[
  {
    "id": number,
    "name": "string",
    "group": "string",
    "cookies": [
      {
        "domain": "string",
        "name": "string",
        "value": "string",
        "path": "string"
      }
    ],
    "max_concurrent_users": number
  }
]
```

#### Get Account Session Info
- **GET** `/api/accounts/{account_id}/session`
- **Response**:
```json
{
  "active_sessions": number,
  "max_concurrent_users": number
}
```

### Analytics

#### Get User Analytics
- **GET** `/api/analytics/user/{user_id}`
- **Response**:
```json
{
  "user_id": "string",
  "sessions": [],
  "account_usage": [],
  "total_time": number,
  "current_sessions": number
}
```

#### Get Account Analytics
- **GET** `/api/analytics/account/{account_id}`
- **Response**:
```json
{
  "account_id": number,
  "total_users": number,
  "active_users": number,
  "total_sessions": number,
  "current_sessions": number,
  "usage_by_domain": [],
  "user_activities": []
}
```

### Admin Endpoints
These endpoints require admin privileges.

#### Users Management
- **GET** `/api/admin/users` - Get all users
- **POST** `/api/admin/users` - Create new user
- **DELETE** `/api/admin/users/{user_id}` - Delete user

#### Presets Management
- **GET** `/api/admin/presets` - Get all presets
- **POST** `/api/admin/presets` - Create new preset
- **PUT** `/api/admin/presets/{preset_id}` - Update preset
- **DELETE** `/api/admin/presets/{preset_id}` - Delete preset

## Extension Integration Notes

The extension should use the following endpoints:

1. For authentication:
   - `/api/auth/login` for user login
   - `/api/auth/validate` for token validation

2. For account management:
   - `/api/accounts` to get available accounts
   - `/api/accounts/{account_id}/session` to check session limits

3. For analytics:
   - `/api/analytics/user/{user_id}` to track user activity
   - `/api/analytics/account/{account_id}` to track account usage

The extension's API calls should be updated to match these endpoints exactly. Current code review shows some mismatches in the session management endpoints that need to be corrected.