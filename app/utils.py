from fastapi import HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.settings import settings
from app.schemas import ActivityBaseSchema, ActivitySchema, ActivityTreeSchema
from app.models import Activity
import re
import unidecode

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
def transliterate(name: str) -> str:
    """
    Преобразует слово на кириллице в латинницу.
    """
    name = unidecode.unidecode(name)  # транслитерация
    name = name.lower()
    name = re.sub(r'\s+', '_', name)  # пробелы в _
    name = re.sub(r'[^a-z0-9_]', '', name)  # только допустимые символы
    return name

async def get_path(activity_data: ActivityBaseSchema, db: AsyncSession) -> str:
    """
    Генерирует путь для древовидной структуры на основе имени.
    """
    MAX_ACTIVITY_DEPTH = 3  # Максимальный 3 уровня вложенности

    parent_id = getattr(activity_data, "parent_id", None)
    node_name = transliterate(activity_data.name)

    if parent_id:
        parent_activity = await db.scalar(select(Activity).where(Activity.id == parent_id))
        if not parent_activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Родительская деятельность с id={parent_id} не найдена."
            )

        parent_depth = len(str(parent_activity.path).split('.'))
        if parent_depth >= MAX_ACTIVITY_DEPTH:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Максимальная глубина дерева ({MAX_ACTIVITY_DEPTH}) превышена."
            )

        ltree_path = f"{parent_activity.path}.{node_name}"
    else:
        ltree_path = node_name

    existing = await db.scalar(select(Activity).where(Activity.path == ltree_path))
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Деятельность с путем '{ltree_path}' уже существует."
        )
    
    return ltree_path

async def build_activity_tree(activities: List[ActivitySchema], root_path: str) -> ActivitySchema:
    """
    Строит древовидную структуру видов деятельности из плоского списка по path
    и сразу возвращает корень с path == root_path.
    """
    path_to_node = {}

    for activity in activities:
        node = ActivityTreeSchema(
            id=activity.id,
            name=activity.name,
            path=activity.path,
            children=[]
        )
        path_to_node[activity.path] = node

        # Добавляем в children родителя, если есть
        if '.' in activity.path:
            parent_path = '.'.join(activity.path.split('.')[:-1])
            parent_node = path_to_node.get(parent_path)
            if parent_node:
                parent_node.children.append(node)

    activity_tree = path_to_node.get(root_path)
    if not activity_tree:
        raise ValueError(f"Root activity with path {root_path} not found")
    
    return activity_tree





