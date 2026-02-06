import bpy
from queue import Queue
from traceback import print_exc

_queue = None


def put(callback):
    global _queue
    if _queue:
        _queue.put(callback)


def _timer():
    global _queue
    try:
        callback = _queue.get(block=False)
    except Exception:
        return 0.1
    else:
        try:
            callback()
        except Exception:
            print_exc()
    return 0.0


def register():
    global _queue
    _queue = Queue()
    if not bpy.app.timers.is_registered(_timer):
        bpy.app.timers.register(_timer, persistent=True)


def unregister():
    global _queue
    if bpy.app.timers.is_registered(_timer):
        bpy.app.timers.unregister(_timer)
    _queue = None
