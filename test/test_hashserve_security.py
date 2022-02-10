from framework.hashserve import HashServe


def test_post_xml_instead_of_json(framework: HashServe, clean_start, shutdown_hashserve):
    """
    Test to make sure xml cannot be posted
    Steps:
        Restart app if needed
        Attempt posting of xml data to /hash
        Validate 400 response
    """
    xml_data = '<?xml version="1.0" encoding="UTF-8" ?> ' \
               '<password>testpassword42</password>'

    response = framework.api.post(data=xml_data, headers={'headers': 'application/xml'}, payload=None, endpoint='hash')
    assert not response.ok


def test_for_injection_attacks(framework: HashServe, clean_start, shutdown_hashserve):
    pass
