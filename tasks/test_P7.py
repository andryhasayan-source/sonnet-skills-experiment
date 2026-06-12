# -*- coding: utf-8 -*-
"""Тесты задачи P7: интервалы занятости."""
from conftest import load_solution

sol = load_solution("P7")


def test_merge_overlapping_and_touching():
    assert sol.merge_intervals([(60, 120), (100, 150), (150, 180)]) == [(60, 180)]


def test_merge_disjoint_sorted_output():
    assert sol.merge_intervals([(300, 360), (60, 120)]) == [(60, 120), (300, 360)]


def test_merge_empty():
    assert sol.merge_intervals([]) == []


def test_free_slots_basic():
    free = sol.free_slots([(540, 600), (660, 720)], 480, 780)
    assert free == [(480, 540), (600, 660), (720, 780)]


def test_free_slots_unsorted_overlapping_clipped():
    free = sol.free_slots([(700, 900), (100, 560)], 480, 780)
    assert free == [(560, 700)]


def test_free_slots_fully_busy():
    assert sol.free_slots([(0, 1440)], 480, 780) == []


def test_find_slot_earliest():
    slot = sol.find_slot([(540, 600), (660, 720)], 45, 480, 780)
    assert slot == (480, 525)


def test_find_slot_skips_small_gaps():
    slot = sol.find_slot([(540, 600)], 90, 480, 780)
    assert slot == (600, 690)  # первый зазор (480-540) мал, берём следующий


def test_find_slot_none():
    assert sol.find_slot([(480, 770)], 30, 480, 780) is None
