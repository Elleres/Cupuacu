from enum import Enum


class UserType(Enum):
    admin = "admin"
    gerente_laboratorio = "gerente_laboratorio"
    empresa = "empresa"

class UserStatusType(Enum):
    active = "active"
    deleted = "deleted"
    on_hold = "on_hold"

class InventionType(Enum):
    desenho_industrial = "desenho_industrial"
    marca = "marca"
    modelo_de_utilidade = "modelo_de_utilidade"
    patente_de_invencao = "patente_de_invencao"
    programa_de_computador = "programa_de_computador"

class InventionStatusType(Enum):
    arquivado = "arquivado"
    arquivado_definitivamente = "arquivado_definitivamente"
    concedido_registrado = "concedido_registrado"
    indeferido = "indeferido"
    numeracao_anulada = "numeracao_anulada"
    pedido_de_protecao_depositado = "pedido_de_protecao_depositado"
    rejeitado = "rejeitado"
    titularidade_transferida = "titularidade_transferida"

class UnitType(Enum):
    insituto = "insituto"
    faculdade = "faculdade"
    escola = "escola"
    secretaria = "secretaria"
    pro_reitoria = "pro_reitoria"