import grpc
from google.protobuf.timestamp_pb2 import Timestamp
import TaskTracker_pb2
import TaskTracker_pb2_grpc
import logging
from datetime import datetime as Datetime

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = TaskTracker_pb2_grpc.TaskTrackerStub(channel)

        print("===== CreateTask =====")
        request1 = TaskTracker_pb2.CreateTaskRequest(Title="Task1", Content="Task 1 is first task", Tag=TaskTracker_pb2.TP_COMMON)
        response1 = stub.CreateTask(request1)
        print(f"Creating Task 1 - ID: {response1.TaskId}")

        request2 = TaskTracker_pb2.CreateTaskRequest(Title="Task2", Content="Task 2 is second task", Tag=TaskTracker_pb2.TP_URGENT)
        response2 = stub.CreateTask(request2)
        print(f"Creating Task 2 - ID: {response2.TaskId}")

        request3 = TaskTracker_pb2.CreateTaskRequest(Title="Task3", Content="Task 3 is third task", Tag=TaskTracker_pb2.TP_PRIORITY)
        response3 = stub.CreateTask(request3)
        print(f"Creating Task 3 - ID: {response3.TaskId}")

        print("===== RemoveTask =====")
        removeTaskRequest = TaskTracker_pb2.RemoveTaskRequest(TaskId=2)
        response_remove = stub.RemoveTask(removeTaskRequest)
        if response_remove.Error == 0:
            print("Task 2 removed successfully")
        else:
            print(f"Failed to remove Task 2: {response_remove.Error}")

        print("===== ListTask =====")
        listTaskRequest = TaskTracker_pb2.ListTaskRequest(Queue=TaskTracker_pb2.TQ_TODO, Filter=TaskTracker_pb2.TF_ALL)
        response_list = stub.ListTask(listTaskRequest)
        for task in response_list.List:
            created = task.Created
            created_datetime = Datetime.utcfromtimestamp(created.seconds) + Datetime.microsecond // 1000
            print(f"Id: {task.Id}")
            print(f"Title: {task.Title}")
            print(f"Content: {task.Content}")
            print(f"Tag: {task.Tag}")
            print(f"Created: {created_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    logging.basicConfig()
    run()
