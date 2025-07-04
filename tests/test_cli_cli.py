from typer.testing import CliRunner

from civic_data_boundaries_us_forests.cli.cli import app

runner = CliRunner()


def test_cli_fetch_runs():
    result = runner.invoke(app, ["fetch"])
    assert result.exit_code == 0
