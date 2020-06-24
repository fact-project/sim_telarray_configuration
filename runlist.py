import pandas as pd

input_data_dir = '../data/'
output_data_dir = 'build/'

corsika_file = (input_data_dir +
    'Corsika/76900/epos_urqmd_iact_lapalma_winter/'
    '{particle_type}/{runs}/'
    'corsika_{particle_type}_run_{run_id}'
    '_az{az_min}-{az_max}_zd{zd_min}-{zd_max}'
    '.eventio.zst'
)

ceres_file = (input_data_dir +
    'Ceres/r19561/settings_12/epos_urqmd_iact_lapalma_winter/'
    '{particle_type}/{run_type}_{offset}/{runs}/'
    'ceres_{particle_type}_{run_type}_{offset}_run_{run_id}'
    '_az{az_min}-{az_max}_zd{zd_min}-{zd_max}'
    '_Events.fits.gz'
)

fact_tools_images = (output_data_dir +
    'FactTools/1.1.3/'
    '{particle_type}/{run_type}_{offset}/{runs}/'
    'fact-tools_{particle_type}_run_{run_id}'
    '_az{az_min}-{az_max}_zd{zd_min}-{zd_max}'
    '_Images.fits'
)

fact_tools_parameters = (output_data_dir +
    'ctapipe/0.8.0/'
    '{particle_type}/{run_type}_{offset}/{runs}/'
    'ctapipe_fact-tools_{particle_type}_run_{run_id}'
    '_az{az_min}-{az_max}_zd{zd_min}-{zd_max}'
    '.dl1.h5'
)

simtel_images = (output_data_dir +
    'simtel/'
    '{particle_type}/{run_type}_{offset}/{runs}/'
    'simtel_{particle_type}_run_{run_id}'
    '_az{az_min}-{az_max}_zd{zd_min}-{zd_max}'
    '.zst'
)

simtel_parameters = (output_data_dir +
    'ctapipe/0.8.0/'
    '{particle_type}/{run_type}_{offset}/{runs}/'
    'ctapipe_simtel_{particle_type}_run_{run_id}'
    '_az{az_min}-{az_max}_zd{zd_min}-{zd_max}'
    '.dl1.h5'
)


def runlist():
    ceres_runs = pd.read_csv(input_data_dir + 'Ceres/runlist.csv', dtype='str')
    corsika_runs = pd.read_csv(input_data_dir + 'Corsika/runlist.csv', dtype='str')

    df = ceres_runs.merge(corsika_runs, how='outer').dropna()

    return df


if __name__ == "__main__":
    df = runlist()
    df.to_csv('build/runlist.csv', index=False)
