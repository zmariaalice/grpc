from flask import Flask, request, jsonify
from enum import Enum
from datetime import datetime

app = Flask('__name__')

class TaskStatus(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

tasks = {}
task_id_counter = 1

def create_task(title, content, tag):
    global task_id_counter
    task_id = task_id_counter
    task = {
        "id": task_id,
        "title": title,
        "content": content,
        "tag": tag,
        "created": datetime.now(),
        "started": None,
        "ended": None,
        "status": TaskStatus.TODO.value
    }
    tasks[task_id] = task
    task_id_counter += 1
    return task_id

@app.route("/CreateTask", methods=["POST"])
def create_task_route():
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    tag = data.get("tag")
    if title is None or content is None or tag is None:
        return jsonify({"error": "Title, content, and tag are required"}), 400
    if not all(char.isalnum() or char in "#$%&/-" for char in title):
        return jsonify({"error": "Title should only contain alphanumeric characters and special symbols"}), 400
    task_id = create_task(title, content, tag)
    return jsonify({"id": task_id})

@app.route("/ListTask", methods=["GET"])
def list_task_route():
    queue = request.args.get("queue", default="todo").lower()
    filter_type = request.args.get("filter", default="all").lower()
    
    if queue not in [TaskStatus.TODO.value, TaskStatus.DOING.value, TaskStatus.DONE.value]:
        return jsonify({"error": "Invalid queue"}), 400
    
    if filter_type not in ["all", "urgent", "priority", "common"]:
        return jsonify({"error": "Invalid filter"}), 400

    filtered_tasks = [task for task in tasks.values() if task["status"] == queue]
    if filter_type != "all":
        filtered_tasks = [task for task in filtered_tasks if task["tag"] == filter_type]

    return jsonify(filtered_tasks)

@app.route("/ExecuteTask/<int:task_id>", methods=["POST"])
def execute_task_route(task_id):
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404
    task = tasks[task_id]
    if task["status"] == TaskStatus.TODO.value:
        task["status"] = TaskStatus.DOING.value
        task["started"] = datetime.now()
        return jsonify({"message": "Task moved to Doing"})
    else:
        return jsonify({"error": "Task cannot be executed"}), 400

@app.route("/FinalizeTask/<int:task_id>", methods=["POST"])
def finalize_task_route(task_id):
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404
    task = tasks[task_id]
    if task["status"] == TaskStatus.DOING.value:
        task["status"] = TaskStatus.DONE.value
        task["ended"] = datetime.now()
        return jsonify({"message": "Task moved to Done"})
    else:
        return jsonify({"error": "Task cannot be finalized"}), 400

@app.route("/RemoveTask/<int:task_id>", methods=["DELETE"])
def remove_task_route(task_id):
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404
    task = tasks[task_id]
    if task["status"] == TaskStatus.TODO.value:
        del tasks[task_id]
        return jsonify({"message": "Task removed"})
    else:
        return jsonify({"error": "Task cannot be removed"}), 400

if __name__ == "__main__":
    app.run(debug=True)
