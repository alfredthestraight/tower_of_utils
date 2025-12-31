import pandas as pd
import pickle


def get_var_name_as_string(*variable, pos=0):
    """Return the name of a global variable referencing the provided object.

    Args:
        *variable: The variable (object reference) to resolve the global name for. Only the first is used.
        pos: Index to select when multiple global names reference the same object.
    Returns:
        The global variable name as a string.
    Note:
        This scans globals() and is intended for interactive sessions; not reliable across modules.
    """
    return [k for k, v in globals().items() if v is variable[0]][pos]


def pickle_save(
    obj, filename="", filename_path=".", check_for_duplicate_references=True
):
    """Serialize an object to a pickle file with optional name inference.

    Args:
        obj: The Python object to serialize.
        filename: Base filename without extension. If empty, attempts to infer from global var name.
        filename_path: Directory path where the pickle file will be written.
        check_for_duplicate_references: If True, warns when multiple globals reference the same object.
    Behavior:
        Writes '<filename>.pickle' using pickle.HIGHEST_PROTOCOL.
    """
    if check_for_duplicate_references:
        objs_df = pd.DataFrame(
            {
                "obj_name": [k for k in sorted(globals())],
                "mem_address": [eval("id(" + k + ")") for k in sorted(globals())],
            }
        )
        identical_endpoint_references = objs_df[
            objs_df.mem_address == id(obj)
        ].obj_name.tolist()
        if len(identical_endpoint_references) > 1:
            print(
                "ERROR: Variable is referencing an object referenced by other varialbes ("
                + ", ".join(identical_endpoint_references)
                + "). Please supply a filename"
            )
            return
    if filename == "":
        filename = filename_path + "/" + get_var_name_as_string(obj)
    with open(filename + ".pickle", "wb") as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)


def pickle_load(filename_with_or_without_pickle_extention, filename_path="."):
    """Load a pickled object from disk.

    Args:
        filename_with_or_without_pickle_extention: Filename with or without the '.pickle' suffix.
        filename_path: Directory containing the pickle file.
    Returns:
        The deserialized Python object.
    """
    filename = filename_with_or_without_pickle_extention.split(".pickle")[0]
    with open(filename_path + "/" + filename + ".pickle", "rb") as handle:
        return pickle.load(handle)
