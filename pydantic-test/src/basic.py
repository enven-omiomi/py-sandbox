""" 基本形
"""
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name = 'Jane Doe'

if __name__ == '__main__':
    user = User(id='123')
    print(type(user.id))
