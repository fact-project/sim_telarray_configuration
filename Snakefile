# vim: ft=yaml
import pandas as pd
from runlist import runlist, ceres_file, corsika_file, fact_tools_images, fact_tools_parameters, simtel_images, simtel_parameters

runs = pd.read_csv('build/runlist.csv', dtype='str')


rule all:
    input:
        'build/intensity_migration.png'


rule fact_tools:
    input:
        ceres_file
    output:
        fact_tools_images
    shell:
        'bash run-fact-tools.sh {input} {output}'


rule ctapipe_stage1_fact:
    input:
        fact_tools_images
    output:
        fact_tools_parameters
    conda:
        'envs/ctapipe.yaml'
    shell:
        'bash run-ctapipe-stage1.sh {input} {output}'

rule simtel:
    input:
        corsika_file
    output:
        simtel_images
    shell:
        'bash run-simtel.sh {input} {output}'

rule ctapipe_stage1_simtel:
    input:
        simtel_images
    output:
        simtel_parameters
    conda:
        'envs/ctapipe.yaml'
    shell:
        'bash run-ctapipe-stage1.sh {input} {output}'

rule join_simtel:
    input:
        [simtel_parameters.format(**row) for _, row in runs.iterrows()]
    output:
        'build/simtel.hdf5'
    conda:
        'envs/ctapipe.yaml'
    script:
        'scripts/join_data.py'

rule join_fact_tools:
    input:
        [fact_tools_parameters.format(**row) for _, row in runs.iterrows()]
    output:
        'build/fact_tools.hdf5'
    conda:
        'envs/ctapipe.yaml'
    script:
        'scripts/join_data.py'

rule join_data_runs:
    input:
        fact_tools='build/fact_tools.hdf5',
        simtel='build/simtel.hdf5'
    output:
        'build/data.hdf5'
    conda:
        'envs/ctapipe.yaml'
    script:
        'scripts/join_runs.py'

rule intensity_migration:
    input:
        'build/data.hdf5'
    output:
        'build/intensity_migration.png'
    conda:
        'envs/ctapipe.yaml'
    script:
        'scripts/intensity_migration.py'
