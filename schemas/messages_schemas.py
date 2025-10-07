from pydantic import BaseModel, Field


class MessageCreateRequestSchema(BaseModel):
    content: str = Field(description='Текст сообщения')


class MessageUpdateRequestSchema(BaseModel):
    content: str | None = Field(default=None, description='Текст сообщения')


class MessageResponseSchema(BaseModel):
    id: int = Field(description='Уникальный идентификатор сообщения')
    content: str = Field(description='Текст сообщения')


messages_db: list[MessageResponseSchema] = [
    MessageResponseSchema(id=0, content='First post in FastAPI')
]
