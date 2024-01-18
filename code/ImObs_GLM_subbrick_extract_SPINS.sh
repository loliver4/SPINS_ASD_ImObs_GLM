#!/usr/bin/env bash

#SBATCH --job-name ImObs_GLM_SPINS_subbrick
#SBATCH --partition=low-moby
#SBATCH --cpus-per-task=2
#SBATCH --export=ALL
#SBATCH --output=/projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/SPINS/ImObs_GLM_subbrick_SPINS.txt
#SBATCH --error=/projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/SPINS/ImObs_GLM_subbrick_SPINS.err

module load connectome-workbench/1.4.1

sublist=$(ls -d -- /projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/SPINS/sub*/*mm*/)
#sublist=$(ls -d -- /projects/loliver/SPINS_ASD_ImObs_GLM/data/outputs_2023/SPINS/sub-CMP0002/*mm*/)

for dir in ${sublist}; do
    subid=$(basename ${dir})
    if [ ! -f ${dir}/*pos-tstat.dscalar.nii ]; then
    python3 /projects/loliver/SPINS_ASD_ImObs_GLM/code/ImObs_GLM_subbrick_extract.py ${dir} ${subid}
    fi
done


