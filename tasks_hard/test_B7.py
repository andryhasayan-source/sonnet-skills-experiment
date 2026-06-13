# -*- coding: utf-8 -*-
from conftest import load_solution
sol = load_solution("B7")

def test_parse_duration():
    assert sol.parse_duration("15m") == 900
    assert sol.parse_duration("2h") == 7200
    assert sol.parse_duration("30s") == 30
    assert sol.parse_duration("1d") == 86400

def test_parse_duration_invalid():
    for bad in ["0m", "1.5h", "h", "10", "10x", "", "-5m", "m10"]:
        assert sol.parse_duration(bad) is None, bad

def test_parse_command_basic():
    r = sol.parse_command("/remind 15m купить хлеб")
    assert r["command"] == "remind"
    assert r["args"] == ["15m", "купить", "хлеб"]
    assert r["flags"] == set()

def test_parse_command_flags():
    r = sol.parse_command("/remind 15m текст --silent --loud")
    assert r["args"] == ["15m", "текст"]
    assert r["flags"] == {"silent", "loud"}

def test_parse_command_flags_mixed_and_dedup():
    r = sol.parse_command("/cmd --a arg1 --a arg2 --b")
    assert r["args"] == ["arg1", "arg2"]
    assert r["flags"] == {"a", "b"}

def test_parse_command_invalid():
    for bad in ["", "   ", "remind 15m", "/", "/cmd --", "/cmd --Bad",
                "/cmd --a-b"]:
        assert sol.parse_command(bad) is None, bad

def test_parse_command_extra_spaces():
    r = sol.parse_command("/cmd   arg1    arg2")
    assert r["args"] == ["arg1", "arg2"]

def test_build_reminder_ok():
    r = sol.build_reminder("/remind 15m купить хлеб")
    assert r == {"seconds": 900, "message": "купить хлеб", "silent": False}

def test_build_reminder_silent():
    r = sol.build_reminder("/remind 1h позвонить --silent")
    assert r["seconds"] == 3600
    assert r["message"] == "позвонить"
    assert r["silent"] is True

def test_build_reminder_invalid():
    assert sol.build_reminder("/other 15m text") is None
    assert sol.build_reminder("/remind notime text") is None
    assert sol.build_reminder("/remind 15m") is None        # нет текста
    assert sol.build_reminder("/remind 15m --silent") is None  # текст пуст
