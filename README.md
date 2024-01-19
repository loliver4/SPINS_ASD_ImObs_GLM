# Imitate Observe GLM   

This directory includes code to run the Imitate Observe task GLM on SPINS and SPASD data, including steps after ciftify is run, and associated outputs.  

## Code:  
Activate corresponding python env before running any .py scripts using source /projects/loliver/SPINS_ASD_ImObs_GLM/code/py_venv/bin/activate (see note below re this)  
**cifti_clean_ImObs_*mm_SP*.sh**: Drops 4 TRs and applies 6 or 2 mm smoothing to SPINS or SPASD Imitate Observe task images from ciftify   

**parse_confounds_32p_no_GSR_SPASD.sh** and **parse_confounds_32p_no_GSR_SPINS.sh**: Scripts to run parse_confounds_32p_no_GSR.py  
**parse_confounds_32p_no_GSR.py**: Parses fmriprep confound file for 32 parameter confound regression (no GSR) in GLM  

**ImObs_GLM_*mm_no_GSR_SP*.sh**: Script to run ImObs_GLM_*mm_no_GSR.py on SPASD and SPINS participants, respectively (with 6 or 2 mm smoothed files)  
**ImObs_GLM_*mm_no_GSR_SP*.py**: Imitate Observe task GLM, including contrasts for emo im-obs, neg im-obs, and pos im-obs. There are currently different .py scripts for SPINS and SPASD because SPINS includes run # in the imaging file names by default, whereas SPASD does not.  

**ImObs_GLM_subbrick_extract_SP*.sh**: Script to run ImObs_GLM_subbrick_extract.py on SPASD and SPINS participants  
**ImObs_GLM_subbrick_extract.py**: Extracts 'subbricks' of interest from AFNI GLM output files, including coefficients and t-stats for emotion imitate-observe, negative imitate-observe, and positive imitate-observe contrasts  

## Notes:  
The GLM includes the -stim_times_subtract = -1.5 option for 3dDeconvolve, which subtracts the specified number of seconds from each time encountered in any '-stim_times*' option (or in this case adds 1.5 seconds as TR is 3 s).  The purpose of this option is to make it simple to adjust timing files for the removal of images from the start of each imaging run.  

This was implemented based on the recommendation from this post https://reproducibility.stanford.edu/slice-timing-correction-in-fmriprep-and-linear-modeling, which essentially outlines that fMRIprep registers to the middle slice of a TR for slice timing correction by default but linear modeling using AFNI's 3dDeconvolve (and nilearn) assumes that the data are acquired at time zero.  

The -stim_times_subtract option is included in the model.py script for 3dDeconvolve in nipype  


Im Obs regressor 1D files come from /archive/data/SPINS/metadata/design. They have 12 seconds removed from onset times to align with 4 TRs dropped.  

SPASD CMP0014 had to be run separately as they have two Obs runs (using Run 2 for GLM, but Run 1 being kept in archive because it passed imaging QC and may still be useful to someone who isn’t interested in the task).  


## Virtual environment notes:
The nipype 3dDeconvolve interface doesn’t include some 3dDeconvolve options by default (polort A, xjpeg, residuals and full model), so the corresopnding model.py script in the virtual env needed to be updated accordingly (we do not want the AM2 option here, unlike with EA, as there is no parametric modulation)  
Here, /projects/loliver/SPINS_ASD_ImObs_GLM/code/py_venv/lib/python3.8/site-packages/nipype/interfaces/afni/model.py  
It's probabyly easiest to copy or use this virtual env vs making these changes yourself if you are re-running this.  

polort A addition:  
polort_A = traits.Str(
        desc="Set the polynomial order automatically " "[default: A]",
        argstr="-polort %s",
    )  

Also need to change:  
stim_label = traits.List(
        traits.Tuple(
            traits.Int(desc="k-th input stimulus"), Str(desc="stimulus label")
        ),
        desc="label for kth input stimulus (e.g., Label1)",
        argstr="-stim_label %d %s...",
        requires=["stim_times", "stim_times_AM2"], ## THIS LINE RIGHT HERE
        position=-4,
    )  

xjpeg:  
xjpeg = File(
        desc="specificy name for a JPEG file graphing the X matrix",
        argstr="-xjpeg %s",
    )  

residuals and full model:  
res_file = File(desc="output residual files", argstr="-errts %s")
    full_model = File(
        desc="output the (full model) time series fit to the input data",
        argstr="-fitts %s",
    )  

Also need to comment out REML outputs (different model type):  
class DeconvolveOutputSpec(TraitedSpec):
    out_file = File(desc="output statistics file", exists=True)
    \#reml_script = File(
    \#    desc="automatical generated script to run 3dREMLfit", exists=True
    \#)

\ # outputs["reml_script"] = self._gen_fname(suffix=".REML_cmd", **_gen_fname_opts)  


