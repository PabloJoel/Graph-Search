from Solution.Solution import Solution


def test_single_obj():
    solution = Solution()

    solution.add_solution('vf', 1)
    assert solution.get_solution('vf') == [1]

    solution.add_solution('vf', 2)
    assert solution.get_solution('vf') == [1, 2]

    assert solution.get_all_solutions() == [1, 2]


def test_single_obj_all():
    solution = Solution()

    solution.add_solution('*', 1)
    assert solution.get_solution('a') == [1]

    solution.add_solution('*', 2)
    assert solution.get_solution('b') == [1, 2]

    solution.add_solution('*', 3)
    assert solution.get_solution('c') == [1, 2, 3]

    solution.add_solution('*', 1)
    assert solution.get_solution('vf') == [1, 2, 3, 1]

    assert solution.get_all_solutions() == [1, 2, 3, 1]


def test_mult_obj():
    solution = Solution()

    solution.add_solution('v1', 1)
    assert solution.get_solution('v1') == [1]

    solution.add_solution('v2', 2)
    assert solution.get_solution('v2') == [2]

    solution.add_solution('*', 5)
    assert solution.get_solution('v7') == [5]

    solution.add_solution('v1', 2)
    assert solution.get_solution('v1') == [1, 2]

    solution.add_solution('*', 5)
    assert solution.get_solution('v5') == [5,5]

    solution.add_solution('v2', 1)
    assert solution.get_solution('v2') == [2, 1]

    assert solution.get_all_solutions() == [1, 2, 2, 1, 5, 5]


def test_set_sol():
    solution = Solution()

    solution.add_solution('v1', 1)
    assert solution.get_solution('v1') == [1]

    solution.add_solution('v1', 2)
    assert solution.get_solution('v1') == [1, 2]

    solution.set_solution('v1', 5)
    assert solution.get_solution('v1') == [5]