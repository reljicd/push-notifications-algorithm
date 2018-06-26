from typing import List, Any

import yaml


def load_tests(file: str,
               tests_list_key: str = None,
               exclude_tests: List = None,
               category_property: str = 'test_category') -> List:
    """ Util method for loading tests

    Args:
        file: input file
        tests_list_key: if provided, looks for the list of test
            criteria within the value associated with this key.
            If not provided, then assumes tests are a top-level
            value within the yaml.
        exclude_tests: Insert "test_category"(s) to ignore here.
            Useful while known functionality is not implemented
        category_property: category property
    Returns:
        list of tests
    """

    if exclude_tests is None:
        exclude_tests = []

    with open(file, 'r') as yml_file:
        tests = yaml.safe_load(yml_file)

    if tests_list_key:
        tests = tests[tests_list_key]

    # exclude any tests we aren't ready for yet
    tests = [t for t in tests if category_property in t and t[category_property] not in exclude_tests]

    return tests


def filter_tests_by_category(tests: List,
                             cat: str,
                             category_property: str = 'test_category'
                             ) -> List[Any]:
    """Filter tests by category"""

    return [t for t in tests if t[category_property] == cat]
