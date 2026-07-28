"""Helpers de data/hora.

O projeto guarda tudo em UTC *naive*: as colunas sao `DateTime` sem
`timezone=True`, entao o banco devolve datetimes sem tzinfo. Manter essa
convencao em um lugar so evita o erro
"can't compare offset-naive and offset-aware datetimes" nas comparacoes
entre valor vindo do banco e horario atual.
"""

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Agora em UTC, sem tzinfo.

    Substitui `datetime.utcnow()`, que esta deprecado desde o Python 3.12 e
    marcado para remocao. O valor retornado e identico ao dele.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


def to_naive_utc(value: datetime | None) -> datetime | None:
    """Converte um datetime com fuso para UTC naive, preservando o instante.

    Datetimes que chegam pela API podem vir com offset (`...T10:00:00-03:00`).
    Sem essa conversao o SQLAlchemy apenas descarta o offset ao gravar numa
    coluna `DateTime`, guardando 10:00 onde o instante correto e 13:00 UTC.
    Valores que ja sao naive passam intactos.
    """
    if value is None or value.tzinfo is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)
