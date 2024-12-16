from sqlmodel import Field, SQLModel, Relationship
from typing import Optional


class Spycat(SQLModel, table=True):
    __tablename__ = "spycats"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    years_of_exp: int = Field(default=0, ge=0, le=100)
    breed: str
    salary: float = Field(default=100.0)

    # Bidirectional relation
    mission: Optional["Mission"] = Relationship(
        back_populates="spycat", sa_relationship_kwargs={"uselist": False}
    )


class Mission(SQLModel, table=True):
    __tablename__ = "missions"

    id: int | None = Field(default=None, primary_key=True)
    complete_state: bool = Field(default=False)

    spycat_id: int | None = Field(foreign_key="spycats.id", ondelete="RESTRICT")
    spycat: Spycat = Relationship(back_populates="mission")

    # Bidirectional relation
    targets: list["Target"] = Relationship(back_populates="mission", cascade_delete=True)


class Target(SQLModel, table=True):
    __tablename__ = "targets"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    country: str
    notes: str
    complete_state: bool = Field(default=False)

    mission_id: int | None = Field(foreign_key="missions.id", ondelete="CASCADE")
    mission: Mission = Relationship(back_populates="targets")
