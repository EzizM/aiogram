import httpx
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv('API_URL').rstrip('/')

async def register_user(name:str, email: str) -> bool:
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(f'{API_URL}/reg', json={"name": name, "email": email})
            return res.status_code == 200
        except httpx.RequestError as e:
            print(f"An error occurred while registering the user: {e}")
            return False

async def get_all_users(order_by = 'id', direction = 'asc') -> list:
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(f'{API_URL}/users', params={'order_by': order_by, 'direction': direction})
            if res.status_code == 200:
                return res.json()
            return []
        except httpx.RequestError as e:
            print(f"An error occurred while fetching users: {e}")
            return []

async def get_user_by_id(user_id: int):
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(f'{API_URL}/users/{user_id}')
            if res.status_code == 200:
                return res.json()
            return None
        except httpx.RequestError as e:
            print(f"An error occurred while fetching the user: {e}")
            return None

async def update_user_by_id(user_id: int, name: str, email: str):
    async with httpx.AsyncClient() as client:
        try:
            res = await client.put(f'{API_URL}/users/{user_id}', json={"name": name, "email": email})
            return res.status_code == 200
        except httpx.RequestError as e:
            print(f"An error occurred while updating the user: {e}")
            return None

async def delete_user_by_id(user_id: int):
    async with httpx.AsyncClient() as client:
        try:
            res = await client.delete(f'{API_URL}/users/{user_id}')
            return res.status_code == 200
        except httpx.RequestError as e:
            print(f"An error occurred while deleting the user: {e}")
            return None