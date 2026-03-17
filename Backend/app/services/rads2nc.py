import os
import re
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from utils.arg_mapping import arg_map
from utils.reg_mapping import reg_map


def get_nc():
    return