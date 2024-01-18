#!/bin/bash
#SBATCH --partition=low-moby
#SBATCH --job-name cifti_clean_ImObs_2mm
#SBATCH --cpus-per-task=2
#SBATCH --output=/projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/SPINS/logs/cifti_clean_ImObs_2mm.txt
#SBATCH --error=/projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/SPINS/logs/cifti_clean_ImObs_2mm.err
#SBATCH --array=1-438

module load ciftify
module load connectome-workbench/1.4.1
shopt -s extglob

# cifti clean ImObs data, including 2 mm smoothing and dropping 4 TRs (no actual cleaning)
sublist=/projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/SPINS/cifti_clean_sublist.txt
#sublist = sub-CMH0002
index() {
   head -n $SLURM_ARRAY_TASK_ID $sublist \
   | tail -n 1
}

input=/archive/data/SPINS/pipelines/fmriprep_20.2.7/ciftify
output=/projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/SPINS
mkdir -p ${output}/`index`/

task_dirs=$(ls -d ${input}/`index`/MNINonLinear/Results/ses-0?_task-[!e]??_*desc-preproc)
# updated to grab files with three letter names that do not start with e to bypass emp
for dir in ${task_dirs}; do
    run_dir=$(basename ${dir})
    if [ ! -f ${output}/`index`/`index`_${run_dir}_Atlas_s2.dtseries.nii ]; then
      ciftify_clean_img  \
      --output-file=${output}/`index`/`index`_${run_dir}_Atlas_s2.dtseries.nii \
      --no-cleaning \
      --smooth-fwhm=2   --drop-dummy-TRs=4 \
      --left-surface=${input}/`index`/MNINonLinear/fsaverage_LR32k/`index`.L.midthickness.32k_fs_LR.surf.gii  \
      --right-surface=${input}/`index`/MNINonLinear/fsaverage_LR32k/`index`.R.midthickness.32k_fs_LR.surf.gii  \
      ${input}/`index`/MNINonLinear/Results/${run_dir}/${run_dir}_Atlas_s0.dtseries.nii
    fi
    
    #Convert cifti back to nifti
    wb_command -cifti-convert -to-nifti ${output}/`index`/`index`_${run_dir}_Atlas_s2.dtseries.nii \
                                   ${output}/`index`/`index`_${run_dir}_Atlas_s2.nii
done

