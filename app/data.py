from pathlib import Path
from typing import Dict
from xml.etree import ElementTree
from scipy import io as sio

import pandas as pd
from physicool import processing


def get_file_name(time: int) -> str:
    """
    Returns the expected PhysiCell output file name for the given time point.

    >>> get_file_name(0)
    'output00000000_cells.mat'
    >>> get_file_name(20)
    'output00000020_cells.mat'
    """
    return f"output{str(time).zfill(8)}_cells_physicell.mat"


def get_max_cell_num(output_path: str) -> int:
    number_of_cell_files = int(processing.get_cell_file_num(output_path=Path(output_path), version="1.10.2"))
    file_name = get_file_name(number_of_cell_files - 1)
    return len(sio.loadmat(f"{output_path}/{file_name}")["cells"][0])


def get_variables_idx(output_path: str = "output") -> Dict[str, int]:
    """Returns the cell data variables and their indices from the initial.xml file."""
    tree = ElementTree.parse(f"{output_path}/initial.xml")
    stem = "cellular_information/cell_populations/cell_population/custom/simplified_data[@source='PhysiCell']/labels"
    variables_idx = {label.text: int(label.attrib["index"])
                     for label in tree.find(stem).findall("label")}

    position_idx = variables_idx.pop("position")
    for i, coordinate in enumerate(["x", "y", "z"]):
        variables_idx[f"position_{coordinate}"] = position_idx + i

    return variables_idx


def get_simulation_time_interval(output_path: str = "output") -> float:
    """Returns the current time at the first simulation time point (excluding time point 0)."""
    tree = ElementTree.parse(f"{output_path}/output00000001.xml")
    return float(tree.find("metadata/current_time").text)


def get_time(output_path: str = "output") -> pd.Series:
    """Returns a map of the simulation time points and corresponding file number."""
    frames = int(
        processing.get_cell_file_num(output_path=Path(output_path), version="1.10.2")
    )
    time_interval = get_simulation_time_interval(output_path=output_path)
    return pd.Series([frame * time_interval for frame in range(frames)])


def extract_data(output_path: str = "output") -> pd.DataFrame:
    """Extracts the internal cell data into a Pandas DataFrame."""
    time = get_time(output_path)
    cell_variables = get_variables_idx(output_path=output_path)
    max_cell_num = get_max_cell_num(output_path)
    data = list()

    for time_idx, time_value in time.items():
        path_name = f"{output_path}/{get_file_name(time_idx)}"
        cells = sio.loadmat(path_name)["cells"]
        df = pd.DataFrame(
            0.0, index=range(max_cell_num),
            columns=list(cell_variables.keys())
        )

        # Save data into the DataFrame
        df["ID"] = df.index
        mask = df["ID"].isin(cells[0])
        for variable, var_idx in cell_variables.items():
            df.loc[mask, variable] = cells[var_idx]

        df["time"] = time_value

        data.append(df)

    return pd.concat(data, ignore_index=True)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
