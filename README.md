# pytest-data-suites

Class-based test cases for `pytest`.

## Usage example

```python
from pytest_data_suites import DataSuite


class MultiplicationDataSuite(DataSuite):
    # Using TypedDict instead of dict here could clarify your code, but that's just a demo
    positive_operands = dict(left_operand=2, right_operand=2, operation_result=4)
    negative_operands = dict(left_operand=-3, right_operand=-7, operation_result=21)


@MultiplicationDataSuite.parametrize
def test_multiplication(left_operand: float, right_operand: float, operation_result: float) -> None:
    assert left_operand * right_operand == operation_result

```
