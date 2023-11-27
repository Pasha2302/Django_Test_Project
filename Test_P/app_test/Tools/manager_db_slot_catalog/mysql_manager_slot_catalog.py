from __future__ import annotations

# import asyncio
# import os
import aiomysql
from aiomysql.cursors import DictCursor

from .create_all_tables import create_tables
# from server_slot_catalog.paths_app import *


class DatabaseManagerSlotCatalog:
    def __init__(self, host, port, user, password, database="slot_catalog"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.pool = None

    async def connect(self):
        if self.pool is not None:
            self.pool.close()
            await self.pool.wait_closed()

        self.pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.database,
            autocommit=True,
            cursorclass=DictCursor,  # Устанавливаем DictCursor (Получение данных из базы в формате dict().)
        )

    async def create_database(self, database = None):
        if database: self.database = database
        async with aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            autocommit=True,
        ) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")

    async def create_tables_db(self):
        if self.pool is None: raise TypeError("\nНет Подключения к Базе Данных !!!")
        await create_tables(self.pool)

    async def close(self):
        if self.pool is not None:
            self.pool.close()
            await self.pool.wait_closed()

    @staticmethod
    def __replace_space(_string: str):
        if 'type' == _string.lower():
            _string = "game_type"
        return _string.replace('.', '').replace(' ', '_')

    async def delete_rows_table(self, table_name, condition: str | None = None):
        """Удаляет все строки из таблицы, или конкретную строку по условию, например: (WHERE id = 2)"""
        where = condition if condition else ''
        query = f"DELETE FROM {table_name} {where}"
        await self.execute_query(query)

    async def get_column_names(self, table_name):
        columns = await self.execute_query(query=f"DESCRIBE {table_name}", fetch=True)
        column_names = [column['Field'] for column in columns]
        return column_names

    async def delete_row_from_table(self, table_name, condition):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                query = f"DELETE FROM {table_name} WHERE {condition}"
                await cur.execute(query)

    async def insert_data_default(self, table, data: dict):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                table_name = table
                column_names = ', '.join(map(self.__replace_space ,data.keys()))
                placeholders = ', '.join(['%s' for _ in data.values()])
                query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
                try:
                    await cur.execute(query, tuple(data.values()))
                except aiomysql.IntegrityError as err_duplicate:
                    if 'Duplicate' in str(err_duplicate): pass
                    else: raise
                except aiomysql.DataError as err_data:
                    print(f"{err_data}\n{data}")
                    raise

    async def execute_query(self, query, fetch=False):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query)
                if fetch:
                    result = await cur.fetchall()
                    return result

    async def select_data(self, table, columns, condition=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                cur: aiomysql.Cursor
                query = f"SELECT {', '.join(columns)} FROM {table}"
                if condition:
                    query += f" WHERE {condition}"
                await cur.execute(query)
                result = await cur.fetchall()
                return result
