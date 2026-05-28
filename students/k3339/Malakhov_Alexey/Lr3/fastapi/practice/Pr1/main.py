from fastapi import FastAPI

app: FastAPI = FastAPI()

temp_bd: list[dict] = [
    {
        "id": 1,
        "title": "Подготовить презентацию",
        "description": "Сделать слайды для встречи с клиентом",
        "status": "in_progress",
        "priority": 1,
        "category": {"id": 1, "title": "Работа", "description": "Рабочие задачи"},
        "tags": [{"id": 1, "name": "срочно", "color": "#ff0000"}, {"id": 2, "name": "клиент", "color": "#00ff00"}],
    },
    {
        "id": 2,
        "title": "Купить продукты",
        "description": "Молоко, хлеб, яйца",
        "status": "pending",
        "priority": 2,
        "category": {"id": 2, "title": "Личное", "description": "Личные задачи"},
        "tags": [{"id": 3, "name": "быт", "color": "#0000ff"}],
    },
]


@app.get("/")
def hello() -> str:
    return "Hello, [username]!"


@app.get("/tasks_list")
def tasks_list() -> list[dict]:
    return temp_bd


@app.get("/task/{task_id}")
def task_by_id(task_id: int) -> list[dict]:
    return [task for task in temp_bd if task.get("id") == task_id]


@app.post("/task")
def task_create(task: dict) -> dict:
    temp_bd.append(task)
    return {"status": 200, "data": task}


@app.delete("/task/delete/{task_id}")
def task_delete(task_id: int) -> dict:
    for i, task in enumerate(temp_bd):
        if task.get("id") == task_id:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}


@app.put("/task/{task_id}")
def task_update(task_id: int, task: dict):
    for i, task in enumerate(temp_bd):
        if task.get("id") == task_id:
            temp_bd[i] = task
    return temp_bd
