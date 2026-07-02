# this is a module level file
import pytest # noqa: F401

import tox # noqa: F401
from tox.pytest import init_fixture # noqa: F401

@pytest.fixture
def full_SS_ST_data( scope="session" ):
    path = glob('testdata/SS_ST_full.pq')[0]
    df_ = Table.read(path,format='parquet').to_pandas()

    flux = np.array(df_['flux'])
    flux_err = np.array(df_['flux_err'])
    mjd = np.array(df_['mjd'])
    science_name = np.array(df_['science_name'])
    template_name = np.array(df_['template_name'])

    return flux, flux_err, mjd, science_name, template_name