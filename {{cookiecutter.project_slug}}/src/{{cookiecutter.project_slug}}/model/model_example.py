from calendar import c

from sqlalchemy import (
    JSON,
    Column,
    Date,
    DateTime,
    Double,
    Integer,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Model(Base):
    __tablename__ = "little_table"

    __table_args__ = (
        PrimaryKeyConstraint("idContrato", "idOperacao", name="pk_refins"),
    )

    nr_contrato = Column(String, nullable=False)
    nr_operacao = Column(String, nullable=False)
    status_consulta = Column(String, nullable=False)
    descricao_consulta = Column(String, nullable=False)
    label_contrato = Column(String, nullable=False)
    status_contrato = Column(String, nullable=False)
    descricao_contrato = Column(String, nullable=False)

    dt_consulta = Column(Date, nullable=False)

    nome_cliente = Column(String, nullable=False)
    cpf_cliente = Column(String, nullable=False)
    dt_contratacao_inicio = Column(Date, nullable=False)
    dt_contratacao_fim = Column(Date, nullable=False)

    escritorio_cobranca = Column(String, nullable=False)

    agencia = Column(String, nullable=False)
    situacao = Column(String, nullable=False)
    indexadra = Column(String, nullable=False)
    empresa = Column(String, nullable=False)
    plano_contratado = Column(Integer, nullable=False)
    vlr_contratado = Column(Double, nullable=False)
    plataforma = Column(String, nullable=False)
    taxa_juros = Column(Double, nullable=False)
    tipo_cobranca = Column(String, nullable=False)
    cluster = Column(String, nullable=False)
    risco_credito = Column(String, nullable=False)
    qtd_parcelas_pagas = Column(Integer, nullable=False)
    qtd_parcelas_pagas_atrasadas = Column(Integer, nullable=False)
    qtd_parcelas_atrasadas = Column(Integer, nullable=False)
    nr_media_atraso = Column(Integer, nullable=False)
    dt_maior_atraso = Column(Date, nullable=False)
    maior_atraso = Column(JSON, nullable=False)
    parcelas = Column(JSON, nullable=False)
    nr_parc_maior_atraso = Column(Integer, nullable=False)
    vlr_maior_atraso = Column(Double, nullable=False)
    conta_corrente = Column(String, nullable=False)
    desc_class_revenda = Column(String, nullable=False)
    vlr_quitacao = Column(Double, nullable=False)
    vlr_reneg = Column(Double, nullable=False)
    vlr_atraso = Column(Double, nullable=False)
    vlr_principal_vencido = Column(Double, nullable=False)
    vlr_total_vencido = Column(Double, nullable=False)
    vlr_principal_venc_vinc = Column(Double, nullable=False)
    vlr_total_venc_vinc = Column(Double, nullable=False)
    dt_atualizacao = Column(DateTime, nullable=False)
    vlr_juridico = Column(Double, nullable=False)
    flag_entrada = Column(String, nullable=False)

    @property
    def ctt_op(self):
        return f"{self.nr_contrato}/{self.nr_operacao}"
    