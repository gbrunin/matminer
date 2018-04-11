"""
Functions used for auto-generating featurizer tables.
"""
import numpy as np
import pandas as pd
from matminer.featurizers import structure
from matminer.featurizers import dos
from matminer.featurizers import bandstructure
from matminer.featurizers import site
from matminer.featurizers import composition
from matminer.featurizers import base
from matminer.featurizers import function
from matminer.featurizers.base import BaseFeaturizer

__authors__ = 'Alex Dunn <ardunn@lbl.gov>'

def generate_tables():
    """
    Generate nicely formatted tables of all features in RST format.

    Args:
        None

    Returns:
        tables ([str]): A list of formatted strings, where each entry is a
            separate table representing one module.
    """

    mmfeat = "===========\nfeaturizers\n===========\n"
    mmdes = "Below, you will find a description of each featurizer, listed in " \
            "tables grouped by module.\n"
    tables = [mmfeat, mmdes]
    subclasses = []
    for sc in BaseFeaturizer.__subclasses__() + [BaseFeaturizer]:
        scdict = {"name": sc.__name__}
        scdict["doc"] = sc.__doc__.splitlines()[1].lstrip()
        scdict["module"] = sc.__module__
        scdict["type"] = sc.__module__.split(".")[-1]
        subclasses.append(scdict)

    df = pd.DataFrame(subclasses)

    for ftype in np.unique(df['type']):
        dftable = df[df['type'] == ftype]
        namelen = max([len(n) for n in dftable['name']])
        doclen = max([len(d) for d in dftable['doc']])
        borderstr = "=" * namelen + "   " + "=" * doclen + "\n"
        headerstr = "Name" + " " * (namelen - 1) + "Description\n"
        tablestr = ""
        for i, n in enumerate(dftable['name']):
            tablestr += n + " " * (namelen - len(n) + 3) + \
                        dftable['doc'].iloc[i] + "\n"

        ftype_border = "\n" + "-" * len(ftype) + "\n"
        tables.append(ftype_border + ftype + ftype_border + borderstr + headerstr + borderstr +
                      tablestr + borderstr)

    return tables

if __name__ == "__main__":
    for t in generate_tables():
        print(t)