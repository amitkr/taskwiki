import sys
import vim

from tasklib.task import TaskWarrior, Task

# Insert the taskwiki on the python path
sys.path.insert(0, vim.eval("s:plugin_path") + '/taskwiki')

import cache
import util
import task

"""
How this plugin works:

    1.) On startup, it reads all the tasks and syncs info TW -> Vimwiki file. Task is identified by their
        uuid.
    2.) When saving, the opposite sync is performed (Vimwiki -> TW direction).
        a) if task is marked as subtask by indentation, the dependency is created between
"""


tw = TaskWarrior()
cache = cache.TaskCache(tw)


def update_from_tw():
    """
    Updates all the incomplete tasks in the vimwiki file if the info from TW is different.
    """

    cache.load_buffer()
    cache.update_tasks()
    cache.update_buffer()
    cache.evaluate_viewports()


def update_to_tw():
    """
    Updates all tasks that differ from their TaskWarrior representation.
    """

    cache.reset()
    cache.load_buffer()
    cache.update_tasks()
    cache.save_tasks()
    cache.update_buffer()
    cache.evaluate_viewports()

class CurrentTask(object):
    def __init__(self):
        self.task = task.VimwikiTask.from_current_line(cache)
        self.tw = tw

    def info(self):
        info = self.tw.execute_command([self.task['uuid'], 'info'])
        util.show_in_split(info)

    def link(self):
        path = util.get_absolute_filepath()
        self.task.task.add_annotation("wiki: {0}".format(path))
        print("Task \"{0}\" linked.".format(self.task['description']))

if __name__ == '__main__':
    update_from_tw()