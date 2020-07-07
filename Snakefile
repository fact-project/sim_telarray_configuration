# vim: ft=yaml
import pandas as pd
from runlist import runlist, ceres_file, corsika_file, fact_tools_images, fact_tools_parameters, simtel_images, simtel_parameters

runs = pd.read_csv('build/runlist.csv', dtype='str')


rule all:
    input:
        'build/intensity_migration.png',
        'build/intensity_distribution.png',
        'build/hist_hillas.pdf',
        'build/hist_impars.pdf',
        'build/kstest.png'


rule fact_tools:
    input:
        ceres_file
    output:
        fact_tools_images
    shell:
        'bash run-fact-tools.sh {input} {output}'


rule ctapipe_stage1_fact:
    input:
        data=fact_tools_images,
        script='run-ctapipe-stage1.sh'
    output:
        fact_tools_parameters
    conda:
        'envs/ctapipe.yaml'
    shell:
        'bash {input.script} {input.data} {output}'

rule simtel:
    input:
        data=corsika_file,
        script='run-simtel.sh',
        config='config/FACT.cfg'
    output:
        simtel_images
    shell:
        'bash {input.script} {input.data} {output}'

rule ctapipe_stage1_simtel:
    input:
        data=simtel_images,
        script='run-ctapipe-stage1.sh'
    output:
        simtel_parameters
    conda:
        'envs/ctapipe.yaml'
    shell:
        'bash {input.script} {input.data} {output}'

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

rule intensity_distribution:
    input:
        'build/data.hdf5'
    output:
        'build/intensity_distribution.png'
    conda:
        'envs/ctapipe.yaml'
    script:
        'scripts/intensity_distribution.py'

rule hillas_hist:
    input:
        data='build/data.hdf5',
        script='scripts/hist_hillas.py'
    output:
        'build/hist_hillas.pdf'
    conda:
        'envs/ctapipe.yaml'
    shell:
        'python {input.script} {input.data} {output}'

rule kstest:
    input:
        data='build/data.hdf5',
        script='scripts/ks_test.py'
    output:
        'build/kstest.png'
    conda:
        'envs/ctapipe.yaml'
    shell:
        'python {input.script} {input.data} {output}'

rule impars_hist:
    input:
        data='build/data.hdf5',
        script='scripts/hist_impars.py'
    output:
        'build/hist_impars.pdf'
    conda:
        'envs/ctapipe.yaml'
    shell:
        'python {input.script} {input.data} {output}'

