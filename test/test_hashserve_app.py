"""
The tests in this module test the app functionality itself.

For this implementation the app is expected to be running locally.
"""
import requests
from framework.hashserve import HashServe


def test_basic_shutdown_behavior(framework: HashServe):
    """
    Basic test to check that shutdown happens as expected.
    Steps:
        Shutdown the app if it is running
        Launch the app
        Run shutdown command
        Validate 200 response
        Attempt to post to the app and validate exception with attempt
        Validate the process is no longer running on the system

    """
    framework.shutdown_if_running()
    framework.launch()
    response = framework.shutdown()
    assert response.ok, f"shutdown was not performed gracefully, details: {response.json()}"
    try:
        framework.set_password('dothethings')
    except requests.ConnectionError:
        assert True, "Expected a ConnectionError when attempting to post to Hashserve"
    assert not framework.is_hashserve_running(), "Hashserve was running and it was not supposed to be"


def test_restart_behavior(framework: HashServe):
    """
    Test that hashserve restarts properly and that data doesn't persist after shutdown
    Steps:
        Shutdown hashserve if it's running
        Launch hashserve
        Post a pw
        Run shutdown command
        Attempt to get the hash using the job idea from the previous post
        Validate that no hash is found
    """
    framework.shutdown_if_running()
    framework.launch()
    response = framework.set_password('kldsjgiwoeruieriuiw')
    response_shutdown = framework.shutdown()
    assert response_shutdown.ok
    framework.launch()
    response_get = framework.get_password_hash(response.text)
    assert not response_get.ok


def test_hashserve_on_non_default_port(framework: HashServe):
    pass
