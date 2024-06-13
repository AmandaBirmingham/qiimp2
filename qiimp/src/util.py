import copy
import os
import pandas
import yaml

# config keys
METADATA_FIELDS_KEY = "metadata_fields"
STUDY_SPECIFIC_METADATA_KEY = "study_specific_metadata"
HOST_TYPE_SPECIFIC_METADATA_KEY = "host_type_specific_metadata"
SAMPLE_TYPE_KEY = "sample_type"
QIITA_SAMPLE_TYPE = "qiita_sample_type"
SAMPLE_TYPE_SPECIFIC_METADATA_KEY = "sample_type_specific_metadata"
ALIAS_KEY = "alias"
BASE_TYPE_KEY = "base_type"
DEFAULT_KEY = "default"
REQUIRED_KEY = "required"
ALLOWED_KEY = "allowed"
ANYOF_KEY = "anyof"
TYPE_KEY = "type"
LEAVE_REQUIREDS_BLANK_KEY = "leave_requireds_blank"

# internal code keys
HOSTTYPE_SHORTHAND_KEY = "hosttype_shorthand"
SAMPLETYPE_SHORTHAND_KEY = "sampletype_shorthand"
QC_NOTE_KEY = "qc_note"

# metadata keys
SAMPLE_NAME_KEY = "sample_name"
COLLECTION_TIMESTAMP_KEY = "collection_timestamp"
HOST_SUBJECT_ID_KEY = "host_subject_id"

# constant field values
NOT_PROVIDED_VAL = "not provided"
LEAVE_BLANK_VAL = "leaveblank"
DO_NOT_USE_VAL = "donotuse"


def extract_config_dict(config_fp, starting_fp=None):
    if config_fp is None:
        grandparent_dir = _get_grandparent_dir(starting_fp)
        config_fp = os.path.join(grandparent_dir, "config.yml")

    # read in config file
    config_dict = extract_yaml_dict(config_fp)
    return config_dict


def _get_grandparent_dir(starting_fp=None):
    if starting_fp is None:
        starting_fp = __file__
    curr_dir = os.path.dirname(os.path.abspath(starting_fp))
    grandparent_dir = os.path.join(curr_dir, os.pardir, os.pardir)
    return grandparent_dir


def extract_yaml_dict(yaml_fp):
    with open(yaml_fp, "r") as f:
        yaml_dict = yaml.safe_load(f)
    return yaml_dict


def extract_stds_config(stds_fp):
    if not stds_fp:
        stds_fp = os.path.join(_get_grandparent_dir(), "standards.yml")
    return extract_config_dict(stds_fp)


def deepcopy_dict(input_dict):
    output_dict = {}
    for curr_key, curr_val in input_dict.items():
        if isinstance(curr_val, dict):
            output_dict[curr_key] = deepcopy_dict(curr_val)
        else:
            output_dict[curr_key] = copy.deepcopy(curr_val)
    return output_dict


def load_df_with_best_fit_encoding(an_fp, a_file_separator):
    result = None

    # from https://stackoverflow.com/a/76366653
    encodings = ["utf-8", "utf-8-sig", "iso-8859-1", "latin1", "cp1252"]
    for encoding in encodings:
        try:
            result = pandas.read_csv(an_fp, sep=a_file_separator, encoding=encoding)
            print(f"Chosen encoder: {encoding}")
            break
        except Exception as e:  # or the error you receive
            pass

    if result is None:
        raise ValueError(f"Unable to decode {an_fp} with any available encoder")

    return result
