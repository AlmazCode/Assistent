import tools
import warnings
from assistent import Assistent

tools.init()
warnings.filterwarnings("ignore")

del tools
del warnings

assistent = Assistent()
assistent.start()