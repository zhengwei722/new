from flask import Flask, request, jsonify
import threading
import queue
import time
import uuid
import json
import os
from datetime import datetime
import requests
app = Flask(__name__)

# 文件路径，用于持久化任务数据
TASKS_FILE = 'tasks.json'
QUEUE_FILE = 'queue.json'
FAIL_TASKS_FILE = 'fail_tasks.json'

# 任务队列
task_queue = queue.Queue()

# 存储任务状态和结果的字典
tasks = {}
fail_tasks = {}


def save_tasks():
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)


def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_fail_tasks():
    with open(FAIL_TASKS_FILE, 'w') as f:
        json.dump(fail_tasks, f)


def load_fail_tasks():
    if os.path.exists(FAIL_TASKS_FILE):
        with open(FAIL_TASKS_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_queue():
    with open(QUEUE_FILE, 'w') as f:
        json.dump(list(task_queue.queue), f)


def load_queue():
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, 'r') as f:
            for task_id in json.load(f):
                task_queue.put(task_id)


# 任务处理函数
def process_tasks():
    while True:
        task_id = task_queue.get()
        if task_id is None:
            break

        # 模拟任务处理
        print(f"正在处理任务： {task_id}")
        tasks[task_id]['status'] = 'processing'
        tasks[task_id]['start_time'] = datetime.now().timestamp()
        save_tasks()  # 保存任务状态

        a = int(tasks[task_id]['details']['id'])
        port = int(tasks[task_id]['details']['port'])
        time.sleep(a)  # 模拟任务处理时间
        url = 'http://127.0.0.1:'
        response = requests.post(f'{url}{port}/forward', json=tasks[task_id]).json()
        # 检查任务是否已经处理超过20秒
        elapsed_time = time.time() - tasks[task_id]['start_time']
        if elapsed_time > 10:
            print(f"任务 {task_id} 超时，将其重新放回队列")
            tasks[task_id]['status'] = 'queued'
            tasks[task_id]['timeout_count'] = tasks[task_id].get('timeout_count', 0) + 1
            if tasks[task_id]['timeout_count'] > 3:
                print(f"任务 {task_id} 超时超过3次，标记为失败")
                tasks[task_id]['status'] = 'failed'
                fail_tasks[task_id] = tasks[task_id]
                save_fail_tasks()
            else:
                task_queue.put(task_id)
            save_tasks()
            save_queue()
        else:
            tasks[task_id]['status'] = 'completed'
            tasks[task_id]['result'] = response['received_data']
            save_tasks()  # 保存任务结果
            task_queue.task_done()
            save_queue()  # 保存队列状态
            print(f"任务已完成： {task_id}")


# 后台线程来处理任务
def start_task_processor():
    thread = threading.Thread(target=process_tasks)
    thread.daemon = True
    thread.start()
    return thread


# 加载持久化的任务和队列数据
tasks = load_tasks()
fail_tasks = load_fail_tasks()
load_queue()

# 启动任务处理线程
start_task_processor()


@app.route('/add_task', methods=['POST'])
def add_task():
    task_id = str(uuid.uuid4())
    task_details = request.json if request.json else {}
    tasks[task_id] = {'status': 'queued', 'result': None, 'details': task_details, 'timeout_count': 0}
    task_queue.put(task_id)
    save_tasks()  # 保存任务状态
    save_queue()  # 保存队列状态
    return jsonify({'task_id': task_id})


@app.route('/get_task/<task_id>', methods=['GET'])
def get_task(task_id):
    task = tasks.get(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'task_id': task_id, 'status': task['status'], 'result': task['result'], 'details': task['details']})


@app.route('/queue_status', methods=['GET'])
def queue_status():
    queued_tasks = [task_id for task_id, task in tasks.items() if task['status'] == 'queued']
    processing_tasks = [task_id for task_id, task in tasks.items() if task['status'] == 'processing']
    completed_tasks = [task_id for task_id, task in tasks.items() if task['status'] == 'completed']
    failed_tasks = [task_id for task_id, task in tasks.items() if task['status'] == 'failed']

    return jsonify({
        'queued_tasks': [{'task_id': task_id, 'details': tasks[task_id]['details'], 'result': tasks[task_id]['result']} for task_id in queued_tasks],
        'processing_tasks': [{'task_id': task_id, 'details': tasks[task_id]['details'], 'result': tasks[task_id]['result']} for task_id in processing_tasks],
        'completed_tasks': [{'task_id': task_id, 'details': tasks[task_id]['details'], 'result': tasks[task_id]['result']} for task_id in completed_tasks],
        'failed_tasks': [{'task_id': task_id, 'details': tasks[task_id]['details'], 'result': tasks[task_id]['result']} for task_id in failed_tasks]
    })


if __name__ == '__main__':
    app.run(debug=True)
