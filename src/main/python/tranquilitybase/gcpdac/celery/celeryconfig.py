from src.main.python.tranquilitybase.gcpdac.core import celery_tasks

task_track_started = True
task_ignore_result = False

if __name__ == '__main__':
    celery_tasks.validate()
    imports = 'main.python.tranquilitybase.gcpdac.core.celery_tasks'
