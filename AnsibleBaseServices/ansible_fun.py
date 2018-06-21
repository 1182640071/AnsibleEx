#coding: utf-8
#!/usr/bin/env python

import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C

class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def __init__(self , result):
        self.result = result


    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        # print(json.dumps({host.name: result._result}, indent=4))
        # self.result = json.dumps({host.name: result._result}, indent=4)
        self.result.append({host.name: result._result})

class AnsibleApi():
    '''
    ansible的基本api
    '''
    def fun(self , user , passwd , hosts , module , args):
        # since API is constructed for CLI it expects certain options to always be set, named tuple 'fakes' the args parsing options object
        Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])
        options = Options(connection='smart', module_path=['/to/mymodules'], forks=10, become=None, become_method=None, become_user=None, check=False, diff=False)

        # initialize needed objects
        loader = DataLoader() # Takes care of finding and reading yaml, json and ini files
        passwords = dict(vault_pass='secret')

        # Instantiate our ResultCallback for handling results as they come in. Ansible expects this to be one of its main display outlets
        results_callback = ResultCallback([])

        # create inventory, use path to host config file as source or hosts in a comma separated string
        # 如没有明确指定inventory（如下的参数），那么会默认从/etc/ansible/hosts中读取hosts
        inventory = InventoryManager(loader=loader, sources=['hosts.conf'])

        # variable manager takes care of merging all the different sources to give you a unifed view of variables available in each context
        variable_manager = VariableManager(loader=loader, inventory=inventory)

        variable_manager.extra_vars={"ansible_ssh_user":user , "ansible_ssh_pass":passwd}

        # create datastructure that represents our play, including tasks, this is basically what our YAML loader does internally.
        play_source = {"name":"Ansible Ad-Hoc","hosts":hosts,"gather_facts":"no","tasks":[{"action":{"module":module,"args":args}, "register":"shell_out"}]}
        #play_source =  dict(
        #        name = "Ansible Play",
        #        hosts = 'wmltest',
        #        gather_facts = 'no',
        #        tasks = [
        #            dict(action=dict(module='shell', args='ls'), register='shell_out'),
        #            dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
        #         ]
        #    )

        # Create play object, playbook objects use .load instead of init or new methods,
        # this will also automatically create the task objects from the info provided in play_source
        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

        # Run it - instantiate task queue manager, which takes care of forking and setting up all objects to iterate over host list and tasks
        tqm = None
        try:
            tqm = TaskQueueManager(
                      inventory=inventory,
                      variable_manager=variable_manager,
                      loader=loader,
                      options=options,
                      passwords=passwords,
                      stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
                  )
            result = tqm.run(play) # most interesting data for a play is actually sent to the callback's methods
            print result
        finally:
            # we always need to cleanup child procs and the structres we use to communicate with them
            if tqm is not None:
                tqm.cleanup()

             # Remove ansible tmpdir
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

        return results_callback.result