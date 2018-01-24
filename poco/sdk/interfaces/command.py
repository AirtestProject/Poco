# coding=utf-8

__author__ = 'lxn3032'


class CommandInterface(object):
    """
    This is one of the main communication interfaces. This interface defines command-level behaviours providing 
    abilities to control remote runtime by sending self-defined command. The provided command can be various type -
    from string type to specific structure of a dict.
    """

    def command(self, cmd, type):
        """
        Emit a command to remote runtime (target device). 

        Args:
            cmd: any json serializable data.
            type (:obj:`str`): a string value indicated the command type (command tag).

        Returns:
            None (recommended).
        """

        pass
