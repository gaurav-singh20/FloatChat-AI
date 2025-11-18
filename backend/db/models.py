from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from sqlalchemy import Integer, Float, String, DateTime

Base = declarative_base()

class ArgoRecord(Base):
    __tablename__ = "argo_data"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    time: Mapped[str] = mapped_column(DateTime)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    depth: Mapped[float] = mapped_column(Float)          # dbar
    temperature: Mapped[float] = mapped_column(Float, nullable=True)  # deg C
    salinity: Mapped[float] = mapped_column(Float, nullable=True)     # PSU
    platform: Mapped[str] = mapped_column(String, nullable=True)      # WMO
