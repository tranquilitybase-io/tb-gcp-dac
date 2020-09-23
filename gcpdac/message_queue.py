import config

logger = config.logger

import time


def mqtest():
    # Create controller.
    # In this case we are specifying the host and default redis_queue_controller name
    # redis_queue_controller = RedisSMQ(host="127.0.0.1", qname="myqueue")
    # redis_queue_controller = RedisSMQ(host="redis", qname="eaglequeue")
    redis_queue_controller = config.get_redis_queue_controller()

    # # Delete Queue if it already exists, ignoring exceptions
    # redis_queue_controller.deleteQueue().exceptions(False).execute()
    #
    # # Create Queue with default visibility timeout of 20 and delay of 0
    # # demonstrating here both ways of setting parameters
    # redis_queue_controller.createQueue(delay=0).vt(20).execute()

    queues: set = redis_queue_controller.listQueues()
    logger.info("number of queues {}".format(len(queues)))
    if len(queues) == 0:
        logger.info("Creating Queue")
        redis_queue_controller.createQueue(delay=0).vt(20).execute()


    # Send a message with a 2 second delay
    message_id = redis_queue_controller.sendMessage(delay=2).message("Hello World").execute()

    logger.debug({'queue_status': redis_queue_controller.getQueueAttributes().execute()})

    # Try to get a message - this will not succeed, as our message has a delay and no other
    # messages are in the redis_queue_controller
    msg = redis_queue_controller.receiveMessage().exceptions(False).execute()

    # Message should be False as we got no message
    logger.debug({"Message": msg})

    logger.debug("Waiting for our message to become visible")
    # Wait for our message to become visible
    time.sleep(2)

    logger.debug({'queue_status': redis_queue_controller.getQueueAttributes().execute()})
    # Get our message
    msg = redis_queue_controller.receiveMessage().execute()

    # Message should now be there
    logger.debug({"Message": msg})

    # Delete Message
    redis_queue_controller.deleteMessage(id=msg['id'])

    logger.debug({'queue_status': redis_queue_controller.getQueueAttributes().execute()})
    # delete our redis_queue_controller
    redis_queue_controller.deleteQueue().execute()

    # No action
    redis_queue_controller.quit()

    return 200
