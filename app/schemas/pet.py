from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
	id: int = Field(..., description="ID da categoria")
	name: str = Field(..., min_length=1, max_length=100, description="Nome da categoria")


class TagSchema(BaseModel):
	id: int = Field(..., description="ID da tag")
	name: str = Field(..., min_length=1, max_length=100, description="Nome da tag")


class PetBaseSchema(BaseModel):
	category: CategorySchema
	name: str = Field(..., min_length=1, max_length=120)
	photoUrls: list[str] = Field(default_factory=list)
	tags: list[TagSchema] = Field(default_factory=list)
	status: str = Field(default="available", pattern="^(available|pending|sold)$")


class PetCreateSchema(PetBaseSchema):
	pass


class PetUpdateSchema(PetBaseSchema):
	pass


class PetResponseSchema(PetBaseSchema):
	id: int = Field(..., gt=0)
