# Hashserve Test Project

## Summary
In the time that I was able to spend on this I built out a small framework focusing on the 
functionality of the app itself and also the api it provides. With more time I'd spend more
time cleaning up comments and adding docstrings where needed, following the python google syle
guide. 

I'd write the setup.py file so that the package could be built and deployed to pypi and made 
installable via pip. 

To make this framework cross platform I mocked up what I'd do to extend the HashServe class to be
compatible with windows. Then a simple factory class could be used to detect the current os
and return the correct object. NOTE: This was only tested on MacOS. 

## Running Tests  

Install the requirements: `pip3 install -r requirements.txt`  

Then to run you can either run `make test` or simply run `pytest <path to tests dir>`  
The following command line params exist to adjust default variables when running pytest. 
`--ip <ip address of hashserve> --port <port to run run hashserve on> --local_exe <path where exe is locally>` 

It's recommended that a python virtual environment be used and to set the src directory as the PYTHONPATH

## Testing Choices  
I chose to implement a breadth of smoke tests to validate the stated functionality in the design
spec. This is a good route because some of the more focused testing would likely fail because of failures
found in this test set. 

Time was of consideration as well. Having 4 days to complete this project but really only hours to spend on
it due to current obligations I felt this was an appropriate demonstration of how I'd start such a project.

I documented a few of the test cases in the docstrings of them as far as steps go. Maybe these would be
better articulated in jira? 

## Additional Commentary 

### Testing I would do if I had more time 
- There's a lot more boundary testing to do, i.e. post, get, delete, put on the endpoints to validate
what should be allowed vs what is.
- More around the functionality of the app itself. I didn't write a test verifying the graceful shutdown of the app but
I would also run tests where the user attempts to start it in different threads/terminals, attempts to start it using
different ports or attempts to change the port variable while the app is running. 
- I don't know a ton on the topic but pen testing would be interesting. 
- Lastly, I'd build out thorough tests for all the api features. 


## Known Bugs
Test case definitions demonstrating bugs:  
- test_post_to_stats_not_allowed
  - Testing found that posting data to the stats endpoint returns a 200 code and should be rejected. Stats should be
  internally generated.
- test_post_hash_with_existing_id
  - Testing found that if you attempt to post a hash to an existing job id you can corrupt the data.
  The request is rejected with a 400 code but the previous hash that mapped to the job id is altered to be
  part of the error that is returned.
- test_post_integer_password 
  - Hashserve should be able to handle integers and convert them to strings. Posting an error returns a
  malformed input error but the input is valid json. The error is both confusing and the app
  should handle ints.
- test_post_incorrect_json_returns_valid_400
  - Posting incorrect json i.e. {'username': 'user'} is accepted. The key of 'password' is not validated
- test_post_malformed_json_retuns_valid_json
  - Posting of malformed content returns invalid json. The 'malformed input' string returned has a newline in it
  which is not valid json
- test_post_empty_password
  - User should not be able to post an empty password, but they can.
- test_sha512_integrity
  - Unsure on this one. Locally if you encode a string, hash it, and encode it as base64 I get a
  different output. In practice I'd validate this before assuming the test is valid.
- test_get_stats_validate_output
  - Stats returns incorrect average time data. The spec says it returns in ms, and you'd expect
  each request to take around 5s to complete but stats returns invalid timing numbers.