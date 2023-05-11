from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship


class Base(DeclarativeBase):
    pass


class Simulations(Base):
    __tablename__ = "simulations"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(30))
    date: Mapped[datetime] = mapped_column(default=sa.func.current_timestamp())

    datapoints: Mapped[list["Datapoints"]] = relationship(back_populates="simulation")


class Datapoints(Base):
    __tablename__ = "datapoints"
    id: Mapped[int] = mapped_column(primary_key=True)
    pos_x: Mapped[float]
    pos_y: Mapped[float]
    pos_z: Mapped[float]
    volume: Mapped[float]
    cell_type: Mapped[int]
    intra_oxy: Mapped[float]
    intra_glu: Mapped[float]
    intra_lac: Mapped[float]
    intra_energy: Mapped[float]
    simulation_id: Mapped[int] = mapped_column(sa.ForeignKey("simulations.id"))

    simulation: Mapped[Simulations] = relationship(back_populates="datapoints")


engine = sa.create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    sim_1 = Simulations(name="MySim #1")
    dp_1 = Datapoints(
        pos_x=1,
        pos_y=2,
        pos_z=3,
        volume=3.5,
        cell_type=1,
        intra_oxy=3.4,
        intra_glu=3.5,
        intra_lac=3.6,
        intra_energy=3.7,
        simulation=sim_1,
    )
    dp_2 = Datapoints(
        pos_x=3,
        pos_y=1,
        pos_z=3,
        volume=3.2,
        cell_type=1,
        intra_oxy=3.2,
        intra_glu=3.4,
        intra_lac=3.5,
        intra_energy=3.6,
        simulation=sim_1,
    )
    session.add_all([sim_1, dp_1, dp_2])
    session.commit()

    mydata = session.query(Datapoints).first()
    print(mydata)
