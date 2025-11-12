from datetime import datetime

from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

import luigi

from {{ cookiecutter.project_slug }}.tasks import ExampleTask

app = FastAPI(title="Luigi Portal")


# Models
class ExecuteRequest(BaseModel):
    task: str
    date: str
    data_ini: str | None = None
    data_fim: str | None = None


TASKS_MAP: dict[str, type] = {
    "example_task": ExampleTask,
}

executions: list[dict] = []


@app.get("/", response_class=HTMLResponse)
async def root():
    """Interface HTML simples"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Luigi Portal</title>
        <style>
            body { font-family: Arial; margin: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
            h1 { color: #333; }
            select, input, button { padding: 10px; margin: 5px; }
            button { background: #007bff; color: white; border: none; cursor: pointer; }
            button:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Luigi Portal</h1>
            <form onsubmit="executarTask(event)">
                <select id="task" required>
                    <option>Selecione uma task...</option>
                    <option value="task_name">Task Name</option>
                </select>
                <input type="date" id="date" required>
                <button type="submit">▶️ Executar</button>
            </form>
            <h3>Execuções Recentes</h3>
            <div id="history"></div>
        </div>
        <script>
            async function executarTask(e) {
                e.preventDefault();
                const task = document.getElementById('task').value;
                const date = document.getElementById('date').value;
                
                const response = await fetch('/execute', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ task, date })
                });
                const result = await response.json();
                alert(result.status);
                carregarHistorico();
            }
            
            async function carregarHistorico() {
                const response = await fetch('/history');
                const data = await response.json();
                const html = data.map(e => 
                    `<p><strong>${e.task}</strong> - ${e.status} (${e.time})</p>`
                ).join('');
                document.getElementById('history').innerHTML = html;
            }
            
            carregarHistorico();
        </script>
    </body>
    </html>
    """


@app.post("/execute")
async def execute_task(req: ExecuteRequest, background_tasks: BackgroundTasks):
    """Executar task em background"""

    def run_task():
        try:
            task_class = TASKS_MAP.get(req.task)
            if not task_class:
                return {"status": "error", "message": "Task não encontrada"}

            date = datetime.fromisoformat(req.date).date()
            task = task_class(date=date)

            result = luigi.build([task], local_scheduler=True)

            executions.append(
                {
                    "task": req.task,
                    "time": datetime.now().isoformat(),
                    "status": "✅ Sucesso" if result else "❌ Erro",
                }
            )
        except Exception as e:
            executions.append(
                {
                    "task": req.task,
                    "time": datetime.now().isoformat(),
                    "status": f"❌ {str(e)}",
                }
            )

    background_tasks.add_task(run_task)
    return {"status": "⏳ Task iniciada"}


@app.get("/history")
async def get_history():
    """Retornar histórico de execuções"""
    return executions[-10:]  # Últimas 10


@app.get("/tasks")
async def get_tasks():
    """Listar tasks disponíveis"""
    return {"tasks": list(TASKS_MAP.keys())}
