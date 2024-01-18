#!/usr/bin/env python

import argparse
import logging
import os
import subprocess
import sys

import nipype.pipeline.engine as pe
from nipype.interfaces import afni

deconvolve = pe.Node(afni.Deconvolve(), name="3Ddeconvolve")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")

file_handler = logging.FileHandler(
    "/projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/3dDeconvolve_s2.log"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def collect_preprocessed_files(sub_indir, reg_indir):
    in_files = dict()
    # Listing all files in subject directory
    sub_files = os.listdir(sub_indir)
    reg_files = os.listdir(reg_indir)

    # Get input files from the subject directory
    # Change the nii files to your input

    in_files["nii_files"] = sorted(
        [
            os.path.join(sub_indir, f)
            for f in os.listdir(sub_indir)
            if ("s2.nii" in f)
        ]
    )
    in_files["ortvec_file"] = os.path.join(
        sub_indir,
        next(f for f in sub_files if f.endswith("task-imobs_confounds_no_GSR_glm.1D")),
    )

    in_files["stim_times"] = [
        (
            1,
            os.path.join(
                reg_indir,
                next(f for f in reg_files if f.endswith("NE_imit.1D")),
            ),
            "BLOCK(1,1)",
        ),
        (
            2,
            os.path.join(
                reg_indir,
                next(f for f in reg_files if f.endswith("FE_imit.1D")),
            ),
            "BLOCK(1,1)",
        ),
        (
            3,
            os.path.join(
                reg_indir,
                next(f for f in reg_files if f.endswith("SA_imit.1D")),
            ),
            "BLOCK(1,1)",
        ),
        (
            4,
            os.path.join(
                reg_indir,
                next(f for f in reg_files if f.endswith("HA_imit.1D")),
            ),
            "BLOCK(1,1)",
        ),
        (
            5,
            os.path.join(
                reg_indir,
                next(f for f in reg_files if f.endswith("AN_imit.1D")),
            ),
            "BLOCK(1,1)",
        ),
        (
            6,
            os.path.join(
                reg_indir,
                next(f for f in reg_files if f.endswith("FX_imit.1D")),
            ),
            "BLOCK(1,1)",
        ),
        (
            7,
            os.path.join(
                reg_indir,
                next(f for f in reg_files if f.endswith("NE_obs.1D")),
            ),
            "BLOCK(1,1)",
        ),
        (
            8,
            os.path.join(
                reg_indir,
                next(f for f in reg_files if f.endswith("FE_obs.1D")),
            ),
            "BLOCK(1,1)",
        ),
        (
            9,
            os.path.join(
                reg_indir,
                next(f for f in reg_files if f.endswith("SA_obs.1D")),
            ),
            "BLOCK(1,1)",
        ),
        (
            10,
            os.path.join(
                reg_indir,
                next(f for f in reg_files if f.endswith("HA_obs.1D")),
            ),
            "BLOCK(1,1)",
        ),
        (
            11,
            os.path.join(
                reg_indir,
                next(f for f in reg_files if f.endswith("AN_obs.1D")),
            ),
            "BLOCK(1,1)",
        ),
        (
            12,
            os.path.join(
                reg_indir,
                next(f for f in reg_files if f.endswith("FX_obs.1D")),
            ),
            "BLOCK(1,1)",
        ),
    ]

    in_files["stim_label"] = [
        (1, "neutral_imit"),
        (2, "fear_imit"),
        (3, "sad_imit"),
        (4, "happy_imit"),
        (5, "angry_imit"),
        (6, "fixation_imit"),
        (7, "neutral_obs"),
        (8, "fear_obs"),
        (9, "sad_obs"),
        (10, "happy_obs"),
        (11, "angry_obs"),
        (12, "fixation_obs"),
    ]
    return in_files


def collect_3dDeconvolve_outputs(out_dir, subject_id):
    out_files = dict()
    subject_name = "sub-" + subject_id

    # Generate the output files to subject directory
    out_files["bucket"] = os.path.join(
        out_dir, subject_name + "_task-imobs_1stlevel.nii.gz"
    )
    out_files["x1D"] = os.path.join(
        out_dir, subject_name + "_task-imobs_design-matrix-values.mat"
    )
    out_files["xjpeg"] = os.path.join(
        out_dir, subject_name + "_task-imobs_design-matrix-image.jpg"
    )
    out_files["full_model"] = os.path.join(
        out_dir, subject_name + "_task-imobs_1stlevel_explained.nii.gz"
    )
    out_files["residuals"] = os.path.join(
        out_dir, subject_name + "_task-imobs_residuals.nii.gz"
    )
    out_files["cbucket"] = os.path.join(
        out_dir, subject_name + "_task-imobs_1stlevel_coeffs.nii.gz"
    )
    return out_files


def run_3Ddeconvolve(sub_dir, reg_dir, out_dir, sub_id):
    inputs = collect_preprocessed_files(sub_dir, reg_dir)
    outputs = collect_3dDeconvolve_outputs(out_dir, sub_id)
    deconvolve.inputs.in_files = inputs["nii_files"]
    deconvolve.inputs.num_stimts = 12
    deconvolve.inputs.stim_times = inputs["stim_times"]
    deconvolve.inputs.stim_label = inputs["stim_label"]
    deconvolve.inputs.num_glt = 3
    deconvolve.inputs.gltsym = [
        'SYM: +fear_imit +sad_imit +happy_imit +angry_imit -fear_obs -sad_obs -happy_obs -angry_obs',
        'SYM: +fear_imit +sad_imit +angry_imit -fear_obs -sad_obs -angry_obs',
        'SYM: +happy_imit -happy_obs'
    ]
    deconvolve.inputs.glt_label = [(1, "emo_im_vs_obs"),
                                   (2, "neg_im_vs_obs"),
                                   (3, "pos_im_vs_obs")
    ]
    deconvolve.inputs.ortvec = (inputs["ortvec_file"], "ortvec")
    deconvolve.inputs.force_TR = 3
    deconvolve.inputs.polort_A = "A"
    deconvolve.inputs.local_times = True
    deconvolve.inputs.stim_times_subtract = -1.5
    deconvolve.inputs.num_threads = 4
    deconvolve.inputs.fout = True
    deconvolve.inputs.tout = True
    deconvolve.inputs.out_file = outputs["bucket"]
    deconvolve.inputs.x1D = outputs["x1D"]
    deconvolve.inputs.xjpeg = outputs["xjpeg"]
    deconvolve.inputs.full_model = outputs["full_model"]
    deconvolve.inputs.res_file = outputs["residuals"]
    deconvolve.inputs.cbucket = outputs["cbucket"]
    deconvolve.inputs.goforit = 6
    workflow = pe.Workflow(name=sub_id)
    workflow.base_dir = "/projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/tmp/"
    workflow.add_nodes([deconvolve])
    workflow.config["execution"]["crashfile_format"] = "txt"
    workflow.run()
    workflow.write_graph()


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


def main():

    parser = argparse.ArgumentParser(description="Run 3dDeconvolve from AFNI")
    parser.add_argument(
        "input_dir", type=str, help="path to subject preprocessed directory"
    )
    parser.add_argument(
        "reg_dir", type=str, help="path to regressor (1D file) directory"
    )
    parser.add_argument(
        "output_dir", type=str, help="path to subject output directory"
    )
    parser.add_argument("sub_id", type=str, help="a string of subject ID: i.e CMH0012")

    args = parser.parse_args()
    in_path = args.input_dir
    reg_path = args.reg_dir
    out_path = args.output_dir
    sub_id = args.sub_id

    try:
        os.makedirs(out_path)
        # os.chdir(out_path)
        print("Directory ", out_path, " Created ")
    except FileExistsError:
        print("Directory ", out_path, " already exists")

    try:
        run_3Ddeconvolve(in_path, reg_path, out_path, sub_id)
    except ValueError:
        logger.error(
            "run_3Ddeconvolve did not run because of missing inputs at {}".format(
                in_path
            )
        )
    for f in os.listdir(in_path):
        if "task-imi_run-1_desc-preproc_Atlas_s2.dtseries.nii" in f:
            cifti_tmp = os.path.join(in_path, f) # more imi files than obs so used this option - SPINS includes run info right now, whereas SPASD does not, hence different .py files
            logger.debug("Template file found at {}".format(cifti_tmp))
    # Template to convert nifti into cifti
    # cifti_tmp = os.path.join(
    #    in_path,
    #    "sub-"
    #    + sub_id
    #    + "task-obs_run-1_desc-preproc_Atlas_s2.dtseries.nii",
    # )

    if os.path.exists(out_path):
        nifti_files = [
            os.path.join(out_path, f)
            for f in os.listdir(out_path)
            if ("nii.gz" in f)
        ]
    else:
        logger.error("Participant is missing outputs at {}".format(out_path))
        sys.exit(1)

    for f in nifti_files:
        cifti_out = os.path.join(
            out_path, f.rsplit(".", 2)[0] + ".dscalar.nii"
        )
        nifti_to_cifti(f, cifti_tmp, cifti_out)
    return


if __name__ == "__main__":
    main()
