import os
from .base import *

if os.path.isfile(os.path.join(os.path.dirname(__file__), 'production.py')):
    from .production import *
elif os.path.isfile(os.path.join(os.path.dirname(__file__), 'development.py')):
    from .development import *
else:
    from .local import *

