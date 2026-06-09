from pydantic import BaseModel, ConfigDict

# Utilise ConfigDict pour que Pydantic accepte les objets SQLAlchemy
class ScanPortBase(BaseModel):
    port: int
    statut: str
    mac_appareil: str

class ScanPortCreate(ScanPortBase):
    pass

class ScanPort(ScanPortBase):
    id: int
    model_config = ConfigDict(from_attributes=True) # C'est le point crucial