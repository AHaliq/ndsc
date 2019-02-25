import pandas as pd
import re

def data_addgroup(d):
    def _strtogroup(s):
        if re.search('^mobile', s):
            return 0
        elif re.search('^fashion', s):
            return 1
        return 2
    d['group'] = d.apply(lambda row: _strtogroup(row['image_path']), axis=1)
    return d