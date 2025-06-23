from enum import Enum


class UserType(Enum):
    admin = "admin"
    gerente_laboratorio = "gerente_laboratorio"
    empresa = "empresa"

class UserStatusType(Enum):
    active = "active"
    deleted = "deleted"
    on_hold = "on_hold"
