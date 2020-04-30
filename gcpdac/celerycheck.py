from flask import request, jsonify

import config
from celery_worker import add_together_two
logger = config.logger

def add_together():
    logger.info("ADD TOGETHER")
    result = add_together_two.delay(23, 42)
    result.wait()

    x = int(request.args.get("x", 1))
    y = int(request.args.get("y", 2))
    res = add_together_two.apply_async((x, y))
    context = {"id": res.task_id, "x": x, "y": y}
    result = "add((x){}, (y){})".format(context['x'], context['y'])
    goto = "{}".format(context['id'])

    return jsonify(result=result, goto=goto)

def add_together_result(taskid):
    logger.info("ADD TOGETHER RESULT %s",format(taskid))
    retval = add_together_two.AsyncResult(taskid).get(timeout=1.0)
    return {"sum": str(repr(retval))}
