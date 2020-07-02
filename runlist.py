import pandas as pd
from pathlib import Path
from tqdm import tqdm

base_path = ''
input_data_dir = base_path + '../data/'
output_data_dir = base_path + 'build/'

corsika_file = input_data_dir + (
    'corsika/76900/epos_urqmd_iact_lapalma_winter/'
    '{particle_type}/{runs}/'
    'corsika_{particle_type}_run_{run_id}'
    '_az{az_min}-{az_max}_zd{zd_min}-{zd_max}'
    '.eventio.zst'
)

ceres_file = input_data_dir + (
    'ceres/r19561/settings_12/epos_urqmd_iact_lapalma_winter/'
    '{particle_type}/{run_type}_{offset}/{runs}/'
    'ceres_{particle_type}_{run_type}_{offset}_run_{run_id}'
    '_az{az_min}-{az_max}_zd{zd_min}-{zd_max}'
    '_Events.fits.gz'
)

fact_tools_images = output_data_dir + (
    'FactTools/1.1.3/'
    '{particle_type}/{run_type}_{offset}/{runs}/'
    'fact-tools_{particle_type}_run_{run_id}'
    '_az{az_min}-{az_max}_zd{zd_min}-{zd_max}'
    '_Images.fits'
)

fact_tools_parameters = output_data_dir + (
    'ctapipe/0.8.0/'
    '{particle_type}/{run_type}_{offset}/{runs}/'
    'ctapipe_fact-tools_{particle_type}_run_{run_id}'
    '_az{az_min}-{az_max}_zd{zd_min}-{zd_max}'
    '.dl1.h5'
)

simtel_images = output_data_dir + (
    'simtel/'
    '{particle_type}/{run_type}_{offset}/{runs}/'
    'simtel_{particle_type}_run_{run_id}'
    '_az{az_min}-{az_max}_zd{zd_min}-{zd_max}'
    '.zst'
)

simtel_parameters = output_data_dir + (
    'ctapipe/0.8.0/'
    '{particle_type}/{run_type}_{offset}/{runs}/'
    'ctapipe_simtel_{particle_type}_run_{run_id}'
    '_az{az_min}-{az_max}_zd{zd_min}-{zd_max}'
    '.dl1.h5'
)


def list_corsika(data_dir):
    d = Path(data_dir) / 'corsika'
    return list(Path(d).glob('**/*.eventio.zst'))


def list_ceres(data_dir):
    d = Path(data_dir) / 'ceres'
    return list(Path(d).glob('**/*.fits.gz'))


def parse_ceres(p):
    _, *f, _ = p.name.split('_')
    az = f[-2]
    zd = f[-1]
    az_min, az_max = az[2:].split('-')
    zd_min, zd_max = zd[2:].split('-')
    d = dict(
        particle_type=f[0],
        run_type=f[1],
        offset=f[2],
        run_id=f[4],
        az_min=az_min,
        az_max=az_max,
        zd_min=zd_min,
        zd_max=zd_max,
        runs=p.parent.name,
    )
    return d


def parse_corsika(p):
    _, *f = p.name.split('_')
    az = f[-2]
    zd = f[-1]
    az_min, az_max = az[2:].split('-')
    zd_min, zd_max = zd[2:].split('-')
    zd_max = zd_max.split('.')[0]
    d = dict(
        particle_type=f[0],
        run_id=f[2],
        runs=p.parent.name,
        az_min=az_min,
        az_max=az_max,
        zd_min=zd_min,
        zd_max=zd_max,
    )
    return d


def runlist():
    """Create runlist for Corsika and Ceres data stored on disk."""
    n_files = 10

    ceres_files = list_ceres(input_data_dir)
    corsika_files = list_corsika(input_data_dir)

    ceres_runs = pd.DataFrame(
        columns=[
            'particle_type',
            'runs',
            'run_id',
            'run_type',
            'offset',
            'az_min',
            'az_max',
            'zd_min',
            'zd_max',
        ]
    )
    corsika_runs = pd.DataFrame(
        columns=[
            'particle_type',
            'runs',
            'run_id',
            'az_min',
            'az_max',
            'zd_min',
            'zd_max',
        ]
    )

    for p in tqdm(ceres_files[:n_files]):
        ceres_runs = ceres_runs.append(parse_ceres(p), ignore_index=True)

    for p in tqdm(corsika_files[:n_files]):
        corsika_runs = corsika_runs.append(parse_corsika(p), ignore_index=True)

    df = ceres_runs.merge(corsika_runs, how='outer').dropna()

    return df


if __name__ == "__main__":
    df = runlist()
    df.to_csv('build/runlist.csv', index=False)
