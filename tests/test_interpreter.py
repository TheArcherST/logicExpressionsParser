from interpreter import Interpreter


def _check(expression: str, excepted: int) -> bool:
    return Interpreter(expression).expr() == excepted


def test_truth_table():
    assert _check('0 -> 0', 1)
    assert _check('1 -> 0', 0)
    assert _check('0 -> 1', 1)
    assert _check('1 -> 1', 1)

    assert _check('0 & 0', 0)
    assert _check('1 & 0', 0)
    assert _check('0 & 1', 0)
    assert _check('1 & 1', 1)

    assert _check('0 || 0', 0)
    assert _check('1 || 0', 1)
    assert _check('0 || 1', 1)
    assert _check('1 || 1', 1)

    assert _check('0 == 0', 1)
    assert _check('0 == 1', 0)
    assert _check('1 == 0', 0)
    assert _check('1 == 1', 1)

    assert _check('!0', 1)
    assert _check('!1', 0)


def test_order():
    assert _check('0 -> 0 == 0', 0)
    assert _check('0 == !0 || 0', 0)
