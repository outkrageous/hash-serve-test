from framework.hashserve import HashServe
from framework.utils import run_api_calls_in_threads


def test_multiple_posts_in_parallel(framework: HashServe, clean_start, shutdown_hashserve):
    """
    Test that we can run multiple calls in parallel to hashserve
    """
    passwords = [f'kdsjglksdjglksjdlkfjsldklksdjflksjd{i}' for i in range(20)]
    job_ids = []

    # This is just a wrapper so that we can get results back from the calls made in threads
    def post_password(password):
        response = framework.set_password(password)
        job_ids.append(response.json())

    run_api_calls_in_threads(post_password, passwords)
    framework.shutdown_if_running()
    assert len(job_ids) == 20, "number of job ids returned did not match the number of passwords sent to be hashed"


def test_multiple_get_hash_in_parallel(framework: HashServe, clean_start, shutdown_hashserve):
    """
    Test that multiple get requests can be run in parallel
    """
    passwords = [f'kdsjglksdjglksjdlkfjsldklksdjflksjd{i}' for i in range(20)]
    job_ids = []
    hashes = []

    # This is just a wrapper so that we can get results back from the calls made in threads
    def post_password(password):
        response = framework.set_password(password)
        job_ids.append(response.json())

    def get_hash(job_id):
        response = framework.get_password_hash(job_id)
        hashes.append(response.text)

    run_api_calls_in_threads(post_password, passwords)
    run_api_calls_in_threads(get_hash, job_ids)
    assert len(hashes) == 20

