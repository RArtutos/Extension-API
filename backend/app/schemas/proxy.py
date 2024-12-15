from pydantic import BaseModel

class ProxyBase(BaseModel):
    host: str
    port: int
    username: str | None = None
    password: str | None = None

class ProxyCreate(ProxyBase):
    pass

class Proxy(ProxyBase):
    id: int

    class Config:
        from_attributes = True