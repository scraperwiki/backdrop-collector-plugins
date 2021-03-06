import re

class ComputeDepartmentKey(object):
    """
    Adds a 'department' key to a dictionary by looking up the department from the specified, key_name.
    It takes the first department code of form <[code]> from document[key_name].
    """
    def __init__(self, key_name):
        self.key_name = key_name

    def __call__(self, documents):
        def compute_department(department):
            assert self.key_name in document, (
                'key "{}" not found "{}"'.format(self.key_name, document))
            department_codes = document[self.key_name]
            department_code = take_first_department_code(department_codes)
            document["department"] = DEPARTMENT_MAPPING.get(department_code, department_code)
            return document

        return [compute_department(document) for document in documents]

def take_first_department_code(department_codes):
    get_first_re = re.compile("^(<[^>]+>).*$")
    match = get_first_re.match(department_codes)
    assert match is not None
    (department_code, ) = match.groups()
    return department_code


DEPARTMENT_MAPPING = {
    "<D1>": "AGO",
    "<D2>": "CO",
    "<D3>": "BIS",
    "<D4>": "DCLG",
    "<D5>": "DCMS",
    "<D6>": "DfE",
    "<D7>": "Defra",
    "<D8>": "DFID",
    "<D9>": "DFT",
    "<D10>": "DWP",
    "<D11>": "DECC",
    "<D12>": "DH",
    "<D13>": "FCO",
    "<D15>": "HMT",
    "<D16>": "HO",
    "<D17>": "MOD",
    "<D18>": "MOJ",
    "<D19>": "NIO",
    "<D20>": "OAG",
    "<D25>": "HMRC",
    "<D102>": "FSA",
    "<OT532>": "No 10",
    "<OT537>": "ODPM",
}

def test_mapping():
    from nose.tools import assert_equal, assert_in

    plugin = ComputeDepartmentKey("key_name")
    documents = [{"key_name":"<D10>"}]
    (transformed_document, ) = plugin(documents)

    assert_in("department", transformed_document)
    assert_equal(transformed_document["department"], "DWP")


def test_fail_if_no_key_name_in_document():
    from nose.tools import assert_raises

    plugin = ComputeDepartmentKey("key_name")
    documents = [{"foo":"<D10>"}]

    with assert_raises(AssertionError):
        plugin(documents)

def test_unknown_department_code():
    from nose.tools import assert_equal

    plugin = ComputeDepartmentKey("key_name")
    documents = [{"key_name":"<D30>"}]
    (transformed_document, ) = plugin(documents)

    assert_equal(transformed_document["department"], "<D30>")

def test_takes_first_code():
    from nose.tools import assert_equal

    plugin = ComputeDepartmentKey("key_name")
    documents = [{"key_name":"<D10><D9>"}]
    (transformed_document, ) = plugin(documents)

    assert_equal(transformed_document["department"], "DWP")
    