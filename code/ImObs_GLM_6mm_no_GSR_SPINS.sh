#!/usr/bin/env bash
#SBATCH --partition=low-moby
#SBATCH --array=1-438
#SBATCH --nodes=1
#SBATCH --cpus-per-task=2
#BSATCH --mem-per-cpu=1G
#SBATCH --time=24:00:00
#SBATCH --export=ALL
#SBATCH --job-name="ImObs_GLM_6mm_no_GSR_SPINS"
#SBATCH --output=/projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/SPINS/logs/ImObs_GLM_6mm_no_GSR_SPINS.txt

module load connectome-workbench/1.4.1
module load AFNI/2017.07.17

sublist="/projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/SPINS/3dDeconvolve_sublist.txt"
index () {
	  head -n $SLURM_ARRAY_TASK_ID $sublist \
	  | tail -n 1
	 }

sub_in=/projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/SPINS/sub-`index`
reg_in=/projects/loliver/SPINS_ASD_ImObs_GLM/data
sub_out=/projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/SPINS/sub-`index`/6_mm_no_GSR

if [ ! -f ${sub_out}/*task-imobs_1stlevel.dscalar.nii ]; then
   python3 /projects/loliver/SPINS_ASD_ImObs_GLM/code/ImObs_GLM_6mm_no_GSR_SPINS.py ${sub_in} ${reg_in} ${sub_out} `index`
fi
