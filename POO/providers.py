from abc import ABC, abstractmethod

# ── Base (Strategy interface) ──────────────────────────────────────────────────

class NotificationProvider(ABC):
    """Interfaz común para todos los proveedores de notificación."""

    @abstractmethod
    def send(self, user_id: str, message: str) -> dict:
        """Envía la notificación y retorna un dict con el resultado."""
        ...

# ── Concrete strategies ────────────────────────────────────────────────────────

class EmailProvider(NotificationProvider):
    """Proveedor simulado de email."""

    def send(self, user_id: str, message: str) -> dict:
        # Aquí iría la integración real (SendGrid, SES, etc.)
        print(f"[EmailProvider] Enviando email a usuario {user_id}: '{message}'")
        return {
            "provider": "EmailProvider",
            "channel": "email",
            "status": "sent",
            "to": f"{user_id}@example.com",
        }

class SMSProvider(NotificationProvider):
    """Proveedor simulado de SMS."""

    def send(self, user_id: str, message: str) -> dict:
        # Aquí iría la integración real (Twilio, AWS SNS, etc.)
        print(f"[SMSProvider] Enviando SMS a usuario {user_id}: '{message}'")
        return {
            "provider": "SMSProvider",
            "channel": "sms",
            "status": "sent",
            "to": f"+569{user_id}",
        }
