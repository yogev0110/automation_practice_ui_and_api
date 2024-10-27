from tests.test_ui import ui_test
from tests.test_api import test_question_two, test_question_one


def run_tests():
    tests_list = [ui_test]
    # tests_list = [ui_test, test_question_one, test_question_two]
    test_amount = len(tests_list)
    tests_failed = []
    print('* ----------------------------- *')
    print(f"Running [{test_amount}] Test")
    print("* ----------------------------- *")
    for test in tests_list:
        if not test():
            tests_failed.append(test.__name__)
    print("* ----------------------------- *")
    print(f"Tests Passed [{test_amount - len(tests_failed)}/{test_amount}]")
    print("* ----------------------------- *")
    if tests_failed:
        print(f"Failed Tests:")
        for test in tests_failed:
            print(test)


if __name__ == "__main__":
    run_tests()
