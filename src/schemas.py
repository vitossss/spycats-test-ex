from pydantic import BaseModel, Field


class SpycatCreate(BaseModel):
    name: str
    years_of_exp: int
    breed: str
    salary: float


class SpycatPublic(SpycatCreate):
    id: int


class SpycatUpdate(BaseModel):
    salary: float | None


class TargetCreate(BaseModel):
    name: str
    country: str
    complete_state: bool = Field(default=False)
    notes: str


class TargetUpdate(BaseModel):
    complete_state: bool = Field(default=False)
    notes: str | None = Field(default=None)


class TargetPublic(TargetCreate):
    id: int


class MissionCreate(BaseModel):
    complete_state: bool = Field(default=False)
    spycat_id: int | None = Field(default=None)
    targets: list[TargetCreate]


class MissionPublic(MissionCreate):
    id: int


class MissionUpdate(BaseModel):
    complete_state: bool = Field(default=False)
    spycat_id: int | None = Field(default=None)


class MissionUpdatePublic(MissionUpdate):
    id: int
