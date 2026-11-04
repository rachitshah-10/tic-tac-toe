import builtins

import pytest

import main


class StopGame(Exception):
    """Raised by the fake AI so main() stops right after the menu."""


def run_menu_with_inputs(monkeypatch, inputs, ai_name):
    """Run main() with scripted menu input; return the AI class chosen.

    The named AI class in main is replaced by a fake that records its
    construction and then aborts, so the game loop never starts.
    """
    created = []

    def fake_ai(*args, **kwargs):
        created.append(ai_name)
        raise StopGame

    monkeypatch.setattr(main, ai_name, fake_ai)
    answers = iter(inputs)
    monkeypatch.setattr(builtins, "input", lambda *a: next(answers))

    with pytest.raises(StopGame):
        main.main()
    return created


def test_difficulty_menu_offers_medium(monkeypatch, capsys):
    """Verify the difficulty menu lists a Medium option."""
    run_menu_with_inputs(monkeypatch, ["1", "3"], "MediumAI")
    assert "3 - Medium" in capsys.readouterr().out


def test_choosing_medium_creates_medium_ai(monkeypatch):
    """Verify single player + option 3 builds a MediumAI."""
    assert run_menu_with_inputs(monkeypatch, ["1", "3"], "MediumAI") == ["MediumAI"]


def test_easy_and_hard_options_still_work(monkeypatch):
    """Verify adding Medium did not change options 1 and 2."""
    assert run_menu_with_inputs(monkeypatch, ["1", "1"], "EasyAI") == ["EasyAI"]
    assert run_menu_with_inputs(monkeypatch, ["1", "2"], "HardAI") == ["HardAI"]
