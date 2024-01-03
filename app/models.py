from typing import Optional
from pydantic import BaseModel


# class Character(BaseModel):
#     name: str
#     description: str
#     knowledge_summary: Optional[str] = None
#     knowledge: Optional[str] = None
#     voice: Optional[str] = None
#     image: Optional[str] = None


# export interface CharacterSchema extends VisibilitySchema {
#   user: UserDocument
#   name: string
#   slug: string
#   greeting?: string
#   dialogue?: ChatSchema[]
#   logosData?: LogosData
#   image?: string
#   voice?: string
#   creationCount?: number
#   createdAt?: Date
#   updatedAt?: Date
# }


class CharacterChatMessage(BaseModel):
    character: Character
    message: str

    def __str__(self):
        return f"{self.character.name}: {self.message}"
