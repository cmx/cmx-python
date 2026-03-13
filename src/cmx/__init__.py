import os

from cmx.utils import F
from cmx.backends.markdown import CommonMark
from . import data as data  # Explicit re-export

doc = CommonMark(root=os.getcwd(), prefix=".")
md = doc
# todo: implement this
csv = F @ doc.csv
# todo: implement this
