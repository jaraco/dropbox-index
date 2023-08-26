import pytest
from jaraco import path


@pytest.fixture
def sample_dir(tmp_path):
    path.build(
        {
            'foo.txt': 'my text',
            'foo.png': b'<imagine image data here>',
            'subdir': {
                'bar.txt': 'other text',
            },
        },
        tmp_path,
    )
    return tmp_path
