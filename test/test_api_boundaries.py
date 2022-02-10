from framework.hashserve import HashServe
from framework.utils import generate_random_string_of_length


def test_that_hash_cannot_be_deleted(framework: HashServe, clean_start, shutdown_hashserve):
    """
    Test that data cannot be deleted by job id
    Steps:
        Restart app
        Post a password
        Assert the post was successful
        Attempt to delete the response by the id provided
        Assert that the response was a 4xx from the API meaning it didn't work
        Validate that the hash is still there
    """
    password = 'lksdjflskdjjlkgdkskeihhswheki'
    response = framework.set_password(password)
    assert response.ok
    response_delete = framework.delete_by_id(response.text)
    assert not response_delete.ok
    response_get = framework.get_password_hash(response.text)
    assert response_get.ok


def test_post_to_stats_not_allowed(framework: HashServe, clean_start, shutdown_hashserve):
    """
    Test to make sure that posting stats is rejected by the api

    """
    sample_stats = {"TotalRequests": 2198, "AverageTime": 56772}
    response = framework.api.post(payload=sample_stats, endpoint='hash')
    assert not response.ok, "Post to hash should have been rejected"


def test_post_hash_with_existing_id(framework: HashServe, clean_start, shutdown_hashserve):
    """
    Test to make sure we cannot post over an existing hash by id
    Steps:
        Refresh hashserve
        Post a password for hashing and get the hash
        Attempt the posting of a different password to the previous postings returned id
        Validate that this is rejected with 4xx response
        Run another get command to inspect that the hash for the id has not changed
    :param framework:
    :return:
    """
    post_response = framework.set_password('testPasswordOne')
    get_first_response = framework.get_password_hash(post_response.text)

    test_pass = {'password': 'testpass'}
    ep = f'hash/{post_response.text}'
    response = framework.api.post(payload=test_pass, endpoint=ep)
    assert not response.ok, "Posting a hash to an id should be rejected"
    get_response = framework.get_password_hash(response.text)
    assert get_first_response.text == get_response.text, "Posting to hash by id was able to change the value " \
                                                         "of the hash"


def test_post_long_passwords(framework: HashServe, clean_start, shutdown_hashserve):
    """
    Any length of string should be handleable by the sha512 algorithm it's unknown if there are restrictions
    placed on the input before it is hashed.
    """
    password_len = 100000
    long_string = generate_random_string_of_length(password_len)
    response = framework.set_password(long_string)
    assert response.ok, f"Could not post a password with string of length {password_len}"

