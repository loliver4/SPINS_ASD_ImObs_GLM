#!/usr/bin/env python

import argparse
import logging
import os
import subprocess
import sys
from fnmatch import fnmatch
import nibabel as nib

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")

file_handler = logging.FileHandler(
    "/projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/GLM_subbrick_extract.log"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def nifti_to_cifti(nifti_path, cifti_temp_path, cifti_path):
    """
    Arguments:
        nifti_path          Full path to the input cifti file
        cifti_temp          Full path to the cifti template file
        cifti_path          Full path to the output nifti file
    """
    wb_cmd = [
        "wb_command",
        "-cifti-convert",
        "-from-nifti",
        "-reset-scalars",
        nifti_path,
        cifti_temp_path,
        cifti_path,
    ]
    subprocess.run(wb_cmd)


# Use 3dinfo -verb to check what the subrick included (on *_glm_imobs_1stlevel.nii.gz)
# AFNI's count starts at 0, whereas ours starts at 1 (so subbrick 0 is 1 here)
def extract_column_from_CIFTI(cifti_out, cifti_in, col):
    """
    Arguments:
        cifti_in            Full path to input CIFTI file with columns
        col                 The desired column number to extract from CIFTI file (i.e 1, 2 ,3)
        cifti_out           Full path to output column from cifti file
    """
    wb_cmd = [
        "wb_command",
        "-cifti-merge",
        cifti_out,
        "-cifti",
        cifti_in,
        "-column",
        col,
    ]
    subprocess.run(wb_cmd)



def main():

    parser = argparse.ArgumentParser(
        description="Extract subricks from AFNI 3dDeconvolve"
    )
    parser.add_argument(
        "input_dir", type=str, help="path to subject GLM directory"
    )
    parser.add_argument(
        "subject_id", type=str, help="a string of subject ID (i.e sub-CMH0012)"
    )

    args = parser.parse_args()
    in_path = args.input_dir
    subject = args.subject_id

    

    try:
        sub_files = os.listdir(in_path)
        subricks_file = os.path.join(
            in_path,
            next(
                f for f in sub_files if f.endswith("imobs_1stlevel.dscalar.nii")
            ),
        )
        logger.debug(f"Subrick file is found at {subricks_file}")
    except FileNotFoundError:
        logger.debug(f"Subrick file is not found")

    
    # Extract emo im-obs, neg im-obs, and pos im-obs coefficients and tstats
    for col in ["38", "39", "41", "42", "44", "45"]:
        if col == "38":
            out_file = os.path.join(
                in_path,
                subject
                + "_task-imobs_emo-coef.dscalar.nii",
            )
            extract_column_from_CIFTI(out_file, subricks_file, col)
            logger.warning(
                f"Imobs emo coef map is being extracted from bucket CIFTI file at {in_path}"
            )
        if col == "39":
            out_file = os.path.join(
                in_path,
                subject
                + "_task-imobs_emo-tstat.dscalar.nii",
            )
            extract_column_from_CIFTI(out_file, subricks_file, col)
            logger.warning(
                f"Imobs emo t-stat map is being extracted from bucket CIFTI file at {in_path}"
            )
        if col == "41":
            out_file = os.path.join(
                in_path,
                subject
                + "_task-imobs_neg-coef.dscalar.nii",
            )
            extract_column_from_CIFTI(out_file, subricks_file, col)
            logger.warning(
                f"Imobs neg coef map is being extracted from bucket CIFTI file at {in_path}"
            )
        if col == "42":
            out_file = os.path.join(
                in_path,
                subject
                + "_task-imobs_neg-tstat.dscalar.nii",
            )
            extract_column_from_CIFTI(out_file, subricks_file, col)
            logger.warning(
                f"Imobs neg t-stat map is being extracted from bucket CIFTI file at {in_path}"
            )
        if col == "44":
            out_file = os.path.join(
                in_path,
                subject
                + "_task-imobs_pos-coef.dscalar.nii",
            )
            extract_column_from_CIFTI(out_file, subricks_file, col)
            logger.warning(
                f"Imobs pos coef map is being extracted from bucket CIFTI file at {in_path}"
            )
        if col == "45":
            out_file = os.path.join(
                in_path,
                subject
                + "_task-imobs_pos-tstat.dscalar.nii",
            )
            extract_column_from_CIFTI(out_file, subricks_file, col)
            logger.warning(
                f"Imobs pos t-stat map is being extracted from bucket CIFTI file at {in_path}"
            )

if __name__ == "__main__":
    main()

