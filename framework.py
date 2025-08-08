import json
from collections.abc import Callable
from typing import List, TypeAlias, Any
from pint import UnitRegistry

ureg = UnitRegistry()

class Test:
    pass


Strategy: TypeAlias = Callable[[Test], dict]
TestCase: TypeAlias = dict[str, Any]


class Test:
    #Ez még nincs sanitizolva.
    #egy diszrét teszt egy JSON object, ami pythonban egy dict
    def __init__(self, rawTest: TestCase):
        self.strategyList : list[Strategy] = list()
        self.rawTest = rawTest
        self.strategyResults: list(dict) =list()
        populateStrategy(self)

    def performTests(self):
        for strategy in self.strategyList:
            self.strategyResults.append(strategy(self))

class RequiredFieldStrategy:
    def __call__(self, test: Test) -> dict:
        strategyResult={
            "strategy" : "Required_Field"
        }
        data = test.rawTest.get("data", None)
        config = test.rawTest.get("config", {})

        if data is None and not config.get("allow_null", False):
            strategyResult["result"] = False
            strategyResult["errormessage"] = "'data' is null and 'allow_null' is not set in config"
            strategyResult["suggestion"] = "Set 'allow_null': true in config or provide a non-null 'data'"
        else:
            strategyResult["result"] = True
        return strategyResult

class TypeCheckStrategy:
    def __call__(self, test: Test) -> dict:
        result = {
            "strategy": "TypeCheck",
            "result": True,
            "errormessage": "",
            "suggestion": ""
        }

        data = test.rawTest.get("data", None)
        config = test.rawTest.get("config", {})

        required_type_str = config.get("expected_type", None)

        if required_type_str is None:
            result["result"] = False
            result["errormessage"] = "Missing 'expected_type' in config"
            result["suggestion"] = "Add 'expected_type' (e.g., 'int', 'str') to config"
            return result

        # Map string to actual Python type
        str_to_type = {
            "int": int,
            "float": float,
            "str": str,
            "bool": bool
        }

        expected_type = str_to_type.get(required_type_str.lower(), None)

        if expected_type is None:
            result["result"] = False
            result["errormessage"] = f"Unsupported expected_type: '{required_type_str}'"
            result["suggestion"] = f"Use one of: {', '.join(str_to_type.keys())}"
            return result

        # Check only if data is a primitive (not list/dict)
        if isinstance(data, (int, float, str, bool)):
            if not isinstance(data, expected_type):
                result["result"] = False
                result["errormessage"] = f"Type mismatch: expected {required_type_str}, got {type(data).__name__}"
                result["suggestion"] = f"Convert data to {required_type_str}"
        else:
            result["result"] = False
            result["errormessage"] = "Data is not a primitive type or is null"
            result["suggestion"] = "Type checks only apply to int, float, str, or bool"

        return result


#Basic strategy
class CheckFieldsStrategy:
    mustHaveKeys={"case_id","type","data"}
    def __call__(self, test: Test) -> dict:
        strategyResult=dict()
        if self.mustHaveKeys.issubset(test.rawTest.keys()):
            strategyResult["result"]=True
        else:
            strategyResult["result"]=False
            missing_keys = self.mustHaveKeys - test.rawTest.keys()
            strategyResult["errormessage"] = f"Missing key(s): {', '.join(missing_keys)}"
        return strategyResult


class UnitConversionStrategy:

    def __call__(self, test: Test) -> dict:
        strategyResult = {"strategy": "UnitConversionStrategy"}
        data = test.rawTest.get("data", {})
        config = test.rawTest.get("config", {})

        try:
            value = data["value"]
            unit = data["unit"]
            expected_unit = config["expected_unit"]
            min_value = config.get("min", None)

            # Create a quantity with pint
            quantity = value * ureg(unit)

            # Convert to expected unit
            converted = quantity.to(expected_unit)

            # Check if above min
            if min_value is not None and converted.magnitude < min_value:
                strategyResult["result"] = False
                strategyResult["errormessage"] = (
                    f"Converted value {converted.magnitude} {expected_unit} "
                    f"is less than minimum {min_value} {expected_unit}"
                )
                strategyResult["suggestion"] = "Provide a higher value or adjust minimum"
            else:
                strategyResult["result"] = True
                strategyResult["errormessage"] = ""
                strategyResult["suggestion"] = ""

        except Exception as e:
            strategyResult["result"] = False
            strategyResult["errormessage"] = f"Exception occurred: {str(e)}"
            strategyResult["suggestion"] = "Ensure valid value/unit/expected_unit fields"

        return strategyResult


#Appends strategies to the test.strategyList, based on the test.rawTest["type"] value.
#Can be expanded into a Strategy Factory class
def populateStrategy(test: Test) -> None:
    testTypes={'type_check','required_field','unit_conversion'}
    # The fields check is obvious
    test.strategyList.append(CheckFieldsStrategy())
    match test.rawTest.get("type"):
        case "required_field":
            test.strategyList.append(RequiredFieldStrategy())
        case "type_check":
            test.strategyList.append(TypeCheckStrategy())
        case "unit_conversion":
            test.strategyList.append(UnitConversionStrategy())


class TestFramework:
    #A JSON gyökér formája array alapú, ami pythonban egy list, diszkrét tesztekből áll
    def __init__(self, testcases: list[dict]):
        self.testCases: list[Test] = []
        for testcase in testcases:
            test = Test(testcase)
            test.performTests()
            self.testCases.append(test)

    def summary(self):
        passed_tests = []
        failed_tests = []
        for test in self.testCases:
            case_id = test.rawTest.get("case_id", "<unknown>")
            failed_results = [r for r in test.strategyResults if not r.get("result", False)]

            if not failed_results:
                passed_tests.append(case_id)
                print(f"Test '{case_id}' passed.")
            else:
                failed_tests.append(case_id)
                print(f"Test '{case_id}' failed:")
                for failure in failed_results:
                    strategy = failure.get("strategy", "<unknown strategy>")
                    error = failure.get("errormessage", "<no error message>")
                    suggestion = failure.get("suggestion", "")
                    print(f"   - Strategy: {strategy}")
                    print(f"     Error   : {error}")
                    if suggestion:
                        print(f"     Suggest : {suggestion}")

        print("\nSummary:")
        print(f"Total tests     : {len(self.testCases)}")
        print(f"Passed        : {len(passed_tests)}")
        print(f"Failed        : {len(failed_tests)}")

obj=json.load(open("test_cases_input.json"))
framework=TestFramework(obj)
framework.summary()

