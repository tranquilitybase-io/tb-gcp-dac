from src.main.python.tranquilitybase.celery_worker import celery_tasks

task_track_started = True
task_ignore_result = False

if __name__ == '__main__':
    celery_tasks.validate()
    imports = 'src.main.python.tranquilitybase.celery_worker.celery_tasks'
