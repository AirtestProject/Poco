__version = (1, 10, 3)

__version__ = version = '.'.join(map(str, __version))
__project__ = PROJECT = __name__

from .manager import JSONRPCResponseManager
from .dispatcher import Dispatcher

dispatcher = Dispatcher()

# lint_ignore=W0611,W0401
