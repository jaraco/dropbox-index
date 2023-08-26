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
                'dir-info': '<span>some dir info</span>',
            },
        },
        tmp_path,
    )
    return tmp_path


@pytest.fixture
def template_file(tmp_path):
    path.build(
        {
            'template.html': '<html><head></head><body>my template</body></html>',
        },
        tmp_path,
    )
    return tmp_path / 'template.html'
