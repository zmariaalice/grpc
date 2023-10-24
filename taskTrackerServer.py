import grpc
from google.protobuf.timestamp_pb2 import Timestamp
import TaskTracker_pb2
import TaskTracker_pb2_grpc
from concurrent import futures
import logging

class TaskTrackerServicer(TaskTracker_pb2_grpc.TaskTrackerServicer):
    def __init__(self):
        self.tasks = []

    def CreateTask(self, request, context):
        new_task = TaskTracker_pb2.Task(Title=request.Title, Content=request.Content, Tag=request.Tag)
        new_task.Id = len(self.tasks) + 1
        new_task.Created.GetCurrentTime()
        self.tasks.append(new_task)
        return TaskTracker_pb2.CreateTaskResponse(TaskId=new_task.Id)

    def ListTask(self, request, context):
        response = TaskTracker_pb2.ListTaskResponse(List=self.tasks)
        return response

    def ExecuteTask(self, request, context):
        try:
            task = next(t for t in self.tasks if t.Id == request.TaskId)
            if task.Status == TaskTracker_pb2.DOING:
                return TaskTracker_pb2.ExecuteTaskResponse(Error="Task is already in the 'DOING' status")
            
            task.Status = TaskTracker_pb2.DOING
            task.Started.GetCurrentTime()
            return TaskTracker_pb2.ExecuteTaskResponse(Message="Task moved to 'DOING' status")
        except StopIteration:
            return TaskTracker_pb2.ExecuteTaskResponse(Error="Task not found")

    def FinalizeTask(self, request, context):
        try:
            task = next(t for t in self.tasks if t.Id == request.TaskId)
            if task.Status != TaskTracker_pb2.DOING:
                return TaskTracker_pb2.FinalizeTaskResponse(Error="Task cannot be finalized as it's not in the 'DOING' status")

            task.Status = TaskTracker_pb2.DONE
            task.Ended.GetCurrentTime()
            return TaskTracker_pb2.FinalizeTaskResponse(Message="Task moved to 'DONE' status")
        except StopIteration:
            return TaskTracker_pb2.FinalizeTaskResponse(Error="Task not found")

    def RemoveTask(self, request, context):
        try:
            task = next(t for t in self.tasks if t.Id == request.TaskId)
            self.tasks.remove(task)
            return TaskTracker_pb2.RemoveTaskResponse(Error=0)
        except StopIteration:
            return TaskTracker_pb2.RemoveTaskResponse(Error="Task not found")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    TaskTracker_pb2_grpc.add_TaskTrackerServicer_to_server(TaskTrackerServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()
