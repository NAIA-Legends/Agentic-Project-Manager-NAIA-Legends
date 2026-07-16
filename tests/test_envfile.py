import os

from apm.envfile import load_env_files


def test_sets_missing_skips_existing_and_comments(tmp_path, monkeypatch):
    env = tmp_path / ".env"
    env.write_text(
        "# comment\n"
        "\n"
        "APM_TEST_NEW=abc\n"
        'APM_TEST_QUOTED="with spaces"\n'
        "APM_TEST_EXISTING=from-file\n"
        "not a kv line\n",
        encoding="utf-8",
    )
    monkeypatch.delenv("APM_TEST_NEW", raising=False)
    monkeypatch.delenv("APM_TEST_QUOTED", raising=False)
    monkeypatch.setenv("APM_TEST_EXISTING", "from-shell")

    applied = load_env_files(env)

    assert os.environ["APM_TEST_NEW"] == "abc"
    assert os.environ["APM_TEST_QUOTED"] == "with spaces"
    assert os.environ["APM_TEST_EXISTING"] == "from-shell"  # shell wins
    assert set(applied) == {"APM_TEST_NEW", "APM_TEST_QUOTED"}

    for k in ("APM_TEST_NEW", "APM_TEST_QUOTED"):
        del os.environ[k]


def test_missing_file_is_noop(tmp_path):
    assert load_env_files(tmp_path / "nope.env") == []
