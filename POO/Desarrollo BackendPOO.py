from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from typing import Literal, List
from datetime import datetime
from providers import EmailProvider, SMSProvider
from history import NotificationHistory
 
app = FastAPI(title="Notification API")
history = NotificationHistory()
 
# ---------- Schemas ----------
 
class NotificationRequest(BaseModel):
    userId: str
    message: str
    channel: Literal["email", "sms"]
 
    @field_validator("userId", "message")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v
 
class NotificationRecord(BaseModel):
    userId: str
    message: str
    channel: str
    status: str
    timestamp: str
 
class NotificationListResponse(BaseModel):
    data: List[NotificationRecord]
 
# ---------- Strategy: provider selector ----------
 
PROVIDERS = {
    "email": EmailProvider(),
    "sms":   SMSProvider(),
}
 
def get_provider(channel: str):
    provider = PROVIDERS.get(channel)
    if not provider:
        raise HTTPException(status_code=400, detail=f"Canal '{channel}' no soportado")
    return provider
 
# ---------- Endpoints ----------
 
@app.post("/notifications", status_code=201)
def send_notification(body: NotificationRequest):
    provider = get_provider(body.channel)
    result = provider.send(body.userId, body.message)
 
    record = NotificationRecord(
        userId=body.userId,
        message=body.message,
        channel=body.channel,
        status=result["status"],
        timestamp=datetime.utcnow().isoformat() + "Z",
    )
    history.save(record)
 
    return {
        "message": "Notificación enviada",
        "detail": result,
        "record": record,
    }
 
@app.get("/notifications", response_model=NotificationListResponse)
def get_notifications():
    return {"data": history.all()}