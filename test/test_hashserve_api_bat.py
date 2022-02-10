"""
Pytest module containing basic acceptance tests for the hashserve API

These tests simply verify happy paths and expected behavior
"""

from framework.hashserve import HashServe
import hashlib
import base64


def test_post_password(framework: HashServe, clean_start, shutdown_hashserve):
    """
    Basic test to validate that posting a single password to hashserve returns a
    2xx code and a job id.

    Note: we expect the job id to be 1 here because we start
    with a freshly started app.
    Steps:
        Post a simple password
        Validate that an ok status is returned
        Validate we get a job_id back that is accurate.
    """

    response = framework.set_password(password='myBoringPassword')
    assert response.ok, f"Post command failed. Details: {response.json()}"
    assert response.json() == 1, f"expected a job id of 1 but got {response.json()}"


def test_sha512_hash_and_base64_encoding_len(framework: HashServe, clean_start, shutdown_hashserve):
    """
    A base64 encoded sha512 hash should be 86 or 88 chars long.
    """
    test_password = 'testSha512TestPassword'
    post_response = framework.set_password(test_password)
    assert post_response.ok, f'post of test password failed. Details: {post_response.json()}'
    get_response = framework.get_password_hash(post_response.text)
    assert get_response.ok, f'get of password hash using job id {post_response.text} failed. ' \
                            f'Details {get_response.json()}'
    length_of_hash = len(get_response.text)

    assert length_of_hash == 88 or length_of_hash == 86, 'A base64 encoded sha512 hash should be 88 or 86 characters ' \
                                                         f'long this was {length_of_hash} chars'


def test_post_integer_password(framework: HashServe, clean_start, shutdown_hashserve):
    """
    Post a password as an integer
    Steps:
        Set a password of type int
        Assert that the app handles the int and reports 200
    :param framework:
    :return:
    """
    password = 1234567989
    response = framework.set_password(password)
    assert response.ok, "Integer password was not posted correctly"


def test_post_incorrect_json_returns_valid_400(framework: HashServe, clean_start, shutdown_hashserve):
    """
    Test validates that posting data that doesn't conform to the input schema is rejected
    Steps:
        Post data without password as a key
        Assert the returned data is json type
        Assert that the post was rejected with a non-ok response
    """
    invalid_input = {"username": "bob"}
    response = framework.api.post(payload=invalid_input, endpoint='hash')
    assert response.json(), "Unable to return proper json object"
    assert not response.ok, "API should have rejected the data but did not"


def test_post_malformed_json_retuns_valid_json(framework: HashServe, clean_start, shutdown_hashserve):
    """
    Test that if we attempt to send malformed json data to the API it is rejected cleanly. We
    expect returned errors to be json objects
    Steps:
        Post a non dict type to the api
        Assert that the response returns non-ok status
        Assert that the response can be json decoded.
    """
    invalid_json = 'potatoe'

    response = framework.api.post(payload=invalid_json, endpoint='hash')
    assert not response.ok, "api should not have accepted invalid payload but did"
    assert response.json(), f"json cannot be decoded inspect {response.text}"


def test_post_empty_password(framework: HashServe, clean_start, shutdown_hashserve):
    """
    Posting an empty string to hashserve should return a 4xx. We assume empty strings should be rejected
    """
    password = ''
    response = framework.set_password(password)
    assert not response.ok, "Hashserve accepted an empty string"


def test_sha512_integrity(framework: HashServe, clean_start, shutdown_hashserve):
    """
    Test that the hashserve app is hashing with the expected algorithm. Hashing the same string locally
    should produce the same result in the app.

    TODO: Check how the string is encoded before running it through sha512. This implementation detail would be needed
    """
    password = 'TestPasswork88'
    response = framework.set_password(password)
    get_response = framework.get_password_hash(response.text)
    result = base64.b64encode(hashlib.sha512(password.encode('utf-8')).digest())
    assert result == get_response.text, "Output of hashserve does not match expected value"


def test_get_stats_validate_output(framework: HashServe, clean_start, shutdown_hashserve):
    """
    Test that we can pull stats from the API and validate that the output is as expected.
    Steps:
        Post two passwords
        Pull the stats from the API in json
        Expected average time is in ms so we divide by 1000 to convert to seconds
        We assert that the average time should be between 5 and 6 seconds
        We assert that there should be two requests processed.

    :param framework:
    :return:
    """

    pw1 = 'slkjdflskjdfskkeiidj'
    pw2 = 'weoiuiuyrtiuyweoiruwpoie'

    post_response_1 = framework.set_password(pw1)
    assert post_response_1.ok, "posting pw1 caused a problem"

    post_response_2 = framework.set_password(pw2)
    assert post_response_2.ok, "posting pw2 caused a problem "

    response = framework.get_stats()
    assert response.ok, "there was a problem getting stats"
    response_json = response.json()
    average_time = response_json['AverageTime']
    average_time_seconds = average_time / 1000
    assert 6 > average_time_seconds > 5, "average time to process request should be between 5 and 6 seconds"
    assert response['TotalRequests'] == 2, "Expected 2 requests"
