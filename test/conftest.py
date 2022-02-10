import pytest
from framework.hashserve import HashServe


def pytest_addoption(parser):
    parser.addoption("--ip", action="store", default="127.0.0.1", help="IP address of the hashserve app")
    parser.addoption("--port", action="store", default="8088", help="Port hashserve will listen for http requests")
    parser.addoption("--local_exe", action="store",
                     default="/usr/local/bin/broken-hashserve",
                     help="Full path to the hashserve executable")


@pytest.fixture(scope='session')
def framework(request):
    return HashServe(ip=request.config.getoption('--ip'),
                     port=request.config.getoption('--port'),
                     path_to_exe=request.config.getoption('--local_exe'),
                     )


@pytest.fixture(scope='function')
def clean_start(request, framework: HashServe):
    framework.refresh_hashserve()
    yield  # Run the test


@pytest.fixture(scope='function')
def shutdown_hashserve(request, framework: HashServe):
    yield  # Run the test
    framework.shutdown()



