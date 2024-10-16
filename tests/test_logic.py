from atsbindings import get_sdk_version, get_driver_version



def test_sdk_version_format():
    version = get_sdk_version()
    assert isinstance(version, tuple)
    assert all(isinstance(v, int) for v in version)


def test_driver_version_format():
    version = get_driver_version()
    assert isinstance(version, tuple)
    assert all(isinstance(v, int) for v in version)