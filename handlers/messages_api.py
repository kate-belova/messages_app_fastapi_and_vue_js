from fastapi import APIRouter, HTTPException

from schemas import (
    messages_db,
    MessageResponseSchema,
    MessageCreateRequestSchema,
    MessageUpdateRequestSchema,
)

msg_router = APIRouter()


async def next_id() -> int:
    return max((msg.id for msg in messages_db), default=-1) + 1


async def get_index(msg_id: int) -> int:
    for idx, msg in enumerate(messages_db):
        if msg.id == msg_id:
            return idx
    return -1


@msg_router.get(
    '/messages',
    summary='Получить все сообщения',
    response_model=list[MessageResponseSchema],
)
async def read_messages() -> list[MessageResponseSchema]:
    return messages_db


@msg_router.post(
    '/messages',
    summary='Отправить новое сообщение',
    response_model=MessageResponseSchema,
    status_code=201,
)
async def create_message(
    payload: MessageCreateRequestSchema,
) -> MessageResponseSchema:
    msg_id = await next_id()
    new_message = MessageResponseSchema(id=msg_id, content=payload.content)
    messages_db.append(new_message)
    return new_message


@msg_router.get(
    '/messages/{msg_id}',
    summary='Получить сообщение по его id',
    response_model=MessageResponseSchema,
)
async def get_message(msg_id: int) -> MessageResponseSchema | None:
    message = next((msg for msg in messages_db if msg.id == msg_id), None)

    if message is None:
        raise HTTPException(status_code=404, detail='Message not found')
    return message


@msg_router.patch(
    '/messages/{msg_id}',
    summary='Частично обновить сообщение по его id',
    response_model=MessageResponseSchema,
)
async def update_message(
    msg_id: int, payload: MessageUpdateRequestSchema
) -> MessageResponseSchema | None:
    idx = await get_index(msg_id)
    if idx < 0:
        raise HTTPException(status_code=404, detail='Message not found')

    if payload.content is not None:
        messages_db[idx].content = payload.content

    return messages_db[idx]


@msg_router.put(
    '/messages/{msg_id}',
    summary='Полностью обновить (заменить) сообщение по его id',
    response_model=MessageResponseSchema,
)
async def replace_message(
    msg_id: int, payload: MessageCreateRequestSchema
) -> MessageResponseSchema | None:
    idx = await get_index(msg_id)

    if idx < 0:
        raise HTTPException(status_code=404, detail='Message not found')

    updated_message = MessageResponseSchema(id=idx, content=payload.content)
    messages_db[idx] = updated_message

    return updated_message


@msg_router.delete(
    '/messages/{msg_id}',
    summary='Удалить сообщение по его id',
    status_code=204,
)
async def delete_message(msg_id: int) -> None:
    idx = await get_index(msg_id)

    if idx < 0:
        raise HTTPException(status_code=404, detail='Message not found')

    messages_db.pop(idx)
