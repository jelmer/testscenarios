#  testscenarios: extensions to python unittest to allow declarative
#  dependency injection ('scenarios') by tests.
#
# Copyright (c) 2009, Robert Collins <robertc@robertcollins.net>
# 
# Licensed under either the Apache License, Version 2.0 or the BSD 3-clause
# license at the users choice. A copy of both licenses are available in the
# project source as Apache-2.0 and BSD. You may not use this file except in
# compliance with one of these two licences.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under these licenses is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# license you chose for the specific language governing permissions and
# limitations under that license.

import unittest

import testscenarios
from testtools.tests.helpers import LoggingResult


class TestTestWithScenarios(unittest.TestCase):

    def test_no_scenarios_no_error(self):
        class ReferenceTest(testscenarios.TestWithScenarios):
            def test_pass(self):
                pass
        test = ReferenceTest("test_pass")
        result = unittest.TestResult()
        test.run(result)
        self.assertTrue(result.wasSuccessful())
        self.assertEqual(1, result.testsRun)

    def test_with_one_scenario_one_run(self):
        class ReferenceTest(testscenarios.TestWithScenarios):
            scenarios = [('demo', {})]
            def test_pass(self):
                pass
        test = ReferenceTest("test_pass")
        log = []
        result = LoggingResult(log)
        test.run(result)
        self.assertTrue(result.wasSuccessful())
        self.assertEqual(1, result.testsRun)
        self.assertEqual(
            'testscenarios.tests.test_testcase.ReferenceTest.test_pass(demo)',
            log[0][1].id())

    def test_with_two_scenarios_two_run(self):
        class ReferenceTest(testscenarios.TestWithScenarios):
            scenarios = [('1', {}), ('2', {})]
            def test_pass(self):
                pass
        test = ReferenceTest("test_pass")
        log = []
        result = LoggingResult(log)
        test.run(result)
        self.assertTrue(result.wasSuccessful())
        self.assertEqual(2, result.testsRun)
        self.assertEqual(
            'testscenarios.tests.test_testcase.ReferenceTest.test_pass(1)',
            log[0][1].id())
        self.assertEqual(
            'testscenarios.tests.test_testcase.ReferenceTest.test_pass(2)',
            log[4][1].id())

    def test_attributes_set(self):
        class ReferenceTest(testscenarios.TestWithScenarios):
            scenarios = [
                ('1', {'foo': 1, 'bar': 2}),
                ('2', {'foo': 2, 'bar': 4})]
            def test_check_foo(self):
                self.assertEqual(self.foo * 2, self.bar)
        test = ReferenceTest("test_check_foo")
        log = []
        result = LoggingResult(log)
        test.run(result)
        self.assertTrue(result.wasSuccessful())
        self.assertEqual(2, result.testsRun)

    def test_scenarios_attribute_cleared(self):
        class ReferenceTest(testscenarios.TestWithScenarios):
            scenarios = [
                ('1', {'foo': 1, 'bar': 2}),
                ('2', {'foo': 2, 'bar': 4})]
            def test_check_foo(self):
                self.assertEqual(self.foo * 2, self.bar)
        test = ReferenceTest("test_check_foo")
        log = []
        result = LoggingResult(log)
        test.run(result)
        self.assertTrue(result.wasSuccessful())
        self.assertEqual(2, result.testsRun)
        self.assertNotEqual(None, test.scenarios)
        self.assertEqual(None, log[0][1].scenarios)
        self.assertEqual(None, log[4][1].scenarios)

    def test_countTestCases_no_scenarios(self):
        class ReferenceTest(testscenarios.TestWithScenarios):
            def test_check_foo(self):
                pass
        test = ReferenceTest("test_check_foo")
        self.assertEqual(1, test.countTestCases())

    def test_countTestCases_empty_scenarios(self):
        class ReferenceTest(testscenarios.TestWithScenarios):
            scenarios = []
            def test_check_foo(self):
                pass
        test = ReferenceTest("test_check_foo")
        self.assertEqual(1, test.countTestCases())

    def test_countTestCases_1_scenarios(self):
        class ReferenceTest(testscenarios.TestWithScenarios):
            scenarios = [('1', {'foo': 1, 'bar': 2})]
            def test_check_foo(self):
                pass
        test = ReferenceTest("test_check_foo")
        self.assertEqual(1, test.countTestCases())

    def test_countTestCases_2_scenarios(self):
        class ReferenceTest(testscenarios.TestWithScenarios):
            scenarios = [
                ('1', {'foo': 1, 'bar': 2}),
                ('2', {'foo': 2, 'bar': 4})]
            def test_check_foo(self):
                pass
        test = ReferenceTest("test_check_foo")
        self.assertEqual(2, test.countTestCases())

    def test_debug_2_scenarios(self):
        log = []
        class ReferenceTest(testscenarios.TestWithScenarios):
            scenarios = [
                ('1', {'foo': 1, 'bar': 2}),
                ('2', {'foo': 2, 'bar': 4})]
            def test_check_foo(self):
                log.append(self)
        test = ReferenceTest("test_check_foo")
        test.debug()
        self.assertEqual(2, len(log))
        self.assertEqual(None, log[0].scenarios)
        self.assertEqual(None, log[1].scenarios)
        self.assertNotEqual(log[0].id(), log[1].id())

try:
    import unittest2
    class TestWithScenariosWithUnittest2(testscenarios.MixableTestWithScenarios, unittest2.TestCase):
        pass

    class TestTestWithScenariosWithInittest2(unittest.TestCase):

        def test_no_scenarios_no_error(self):
            class ReferenceTest(TestWithScenariosWithUnittest2):
                def test_pass(self):
                    pass
            test = ReferenceTest("test_pass")
            result = unittest.TestResult()
            test.run(result)
            self.assertTrue(result.wasSuccessful())
            self.assertEqual(1, result.testsRun)

        def test_with_one_scenario_one_run(self):
            class ReferenceTest(TestWithScenariosWithUnittest2):
                scenarios = [('demo', {})]
                def test_pass(self):
                    pass
            test = ReferenceTest("test_pass")
            log = []
            result = LoggingResult(log)
            test.run(result)
            self.assertTrue(result.wasSuccessful())
            self.assertEqual(1, result.testsRun)
            self.assertEqual(
                'testscenarios.tests.test_testcase.ReferenceTest.test_pass(demo)',
                log[0][1].id())

        def test_with_two_scenarios_two_run(self):
            class ReferenceTest(TestWithScenariosWithUnittest2):
                scenarios = [('1', {}), ('2', {})]
                def test_pass(self):
                    pass
            test = ReferenceTest("test_pass")
            log = []
            result = LoggingResult(log)
            test.run(result)
            self.assertTrue(result.wasSuccessful())
            self.assertEqual(2, result.testsRun)
            self.assertEqual(
                'testscenarios.tests.test_testcase.ReferenceTest.test_pass(1)',
                log[0][1].id())
            self.assertEqual(
                'testscenarios.tests.test_testcase.ReferenceTest.test_pass(2)',
                log[4][1].id())

        def test_attributes_set(self):
            class ReferenceTest(TestWithScenariosWithUnittest2):
                scenarios = [
                    ('1', {'foo': 1, 'bar': 2}),
                    ('2', {'foo': 2, 'bar': 4})]
                def test_check_foo(self):
                    self.assertEqual(self.foo * 2, self.bar)
            test = ReferenceTest("test_check_foo")
            log = []
            result = LoggingResult(log)
            test.run(result)
            self.assertTrue(result.wasSuccessful())
            self.assertEqual(2, result.testsRun)

        def test_scenarios_attribute_cleared(self):
            class ReferenceTest(TestWithScenariosWithUnittest2):
                scenarios = [
                    ('1', {'foo': 1, 'bar': 2}),
                    ('2', {'foo': 2, 'bar': 4})]
                def test_check_foo(self):
                    self.assertEqual(self.foo * 2, self.bar)
            test = ReferenceTest("test_check_foo")
            log = []
            result = LoggingResult(log)
            test.run(result)
            self.assertTrue(result.wasSuccessful())
            self.assertEqual(2, result.testsRun)
            self.assertNotEqual(None, test.scenarios)
            self.assertEqual(None, log[0][1].scenarios)
            self.assertEqual(None, log[4][1].scenarios)

        def test_countTestCases_no_scenarios(self):
            class ReferenceTest(TestWithScenariosWithUnittest2):
                def test_check_foo(self):
                    pass
            test = ReferenceTest("test_check_foo")
            self.assertEqual(1, test.countTestCases())

        def test_countTestCases_empty_scenarios(self):
            class ReferenceTest(TestWithScenariosWithUnittest2):
                scenarios = []
                def test_check_foo(self):
                    pass
            test = ReferenceTest("test_check_foo")
            self.assertEqual(1, test.countTestCases())

        def test_countTestCases_1_scenarios(self):
            class ReferenceTest(TestWithScenariosWithUnittest2):
                scenarios = [('1', {'foo': 1, 'bar': 2})]
                def test_check_foo(self):
                    pass
            test = ReferenceTest("test_check_foo")
            self.assertEqual(1, test.countTestCases())

        def test_countTestCases_2_scenarios(self):
            class ReferenceTest(TestWithScenariosWithUnittest2):
                scenarios = [
                    ('1', {'foo': 1, 'bar': 2}),
                    ('2', {'foo': 2, 'bar': 4})]
                def test_check_foo(self):
                    pass
            test = ReferenceTest("test_check_foo")
            self.assertEqual(2, test.countTestCases())

        def test_debug_2_scenarios(self):
            log = []
            class ReferenceTest(TestWithScenariosWithUnittest2):
                scenarios = [
                    ('1', {'foo': 1, 'bar': 2}),
                    ('2', {'foo': 2, 'bar': 4})]
                def test_check_foo(self):
                    log.append(self)
            test = ReferenceTest("test_check_foo")
            test.debug()
            self.assertEqual(2, len(log))
            self.assertEqual(None, log[0].scenarios)
            self.assertEqual(None, log[1].scenarios)
            self.assertNotEqual(log[0].id(), log[1].id())


except ImportError:
    pass
