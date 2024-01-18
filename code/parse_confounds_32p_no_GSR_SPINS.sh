#!/usr/bin/env bash
#SBATCH --partition=low-moby
#SBATCH --array=1-438
#SBATCH --nodes=1
#SBATCH --cpus-per-task=2
#BSATCH --mem-per-cpu=1G
#SBATCH --time=1:00:00
#SBATCH --export=ALL
#SBATCH --job-name="parse_confounds_32p_no_GSR_SPINS"
#SBATCH --output=/projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/SPINS/logs/parse_confounds_32p_no_GSR_SPINS.txt

sublist="/projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/SPINS/3dDeconvolve_sublist.txt"

index () {
	  head -n $SLURM_ARRAY_TASK_ID $sublist \
	  | tail -n 1
	 }

sub_indir="/archive/data/SPINS/pipelines/fmriprep_20.2.7/fmriprep"
sub_outdir="/projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/SPINS"
sub_id="sub-`index`"
python3 /projects/loliver/SPINS_ASD_ImObs_GLM/code/parse_confounds_32p_no_GSR.py ${sub_indir}/${sub_id}/ses-0*/func "`index`" ${sub_outdir}/${sub_id}/
