from circus.commands.base import AsyncCommand


class Stop(AsyncCommand):
    """\
        Stop the arbiter or a watcher
        =============================

        This command stop all the process in a watcher or all watchers.

        ZMQ Message
        -----------

        ::

            {
                "command": "stop",
                "propreties": {
                    "name": "<name>",
                    "async": True
                }
            }

        The response return the status "ok".

        If the property name is present, then the stop will be applied
        to the watcher.

        If async is False the graceful period will be blocking the
        call and the circusd daemon. (defaults: True).

        Otherwise the call will return immediatly after
        calling SIGTERM on each process and call asynchronously
        SIGKILL after the delay of some processes are still up.


        Command line
        ------------

        ::

            $ circusctl stop [<name>]

        Options
        +++++++

        - <name>: name of the watcher
        - <async>: asynchronous stop
    """

    name = "stop"

    def message(self, *args, **opts):
        if len(args) >= 1:
            return self.make_message(name=args[0])
        return self.make_message()

    def execute(self, arbiter, props):
        if 'name' in props:
            watcher = self._get_watcher(arbiter, props['name'])
            watcher.stop()
        else:
            arbiter.stop_watchers()
