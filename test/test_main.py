import pytest

from git_templates import commands
from git_templates.main import main


# Test for the help message, ensures `-h` works
@pytest.fixture
def main_module():
    return "git_templates.main"


@pytest.fixture
def mock_sys(mocker, main_module):
    return mocker.patch(f"{main_module}.sys")


@pytest.fixture
def mock_print(mocker, main_module):
    return mocker.patch(f"{main_module}.print")


@pytest.fixture
def mock_commands(mocker, main_module):
    cmds = mocker.patch(f"{main_module}.commands")
    cmds.__all__ = commands.__all__
    for cmd in commands.__all__:
        setattr(cmds, cmd, mocker.MagicMock())
    return cmds


@pytest.mark.parametrize(
    "command", ["script -h", "script --help", "script help", "script other"]
)
def test_unsupported_commands(command, mock_sys, mock_print):
    mock_sys.argv = command.split()
    main()
    mock_print.assert_called_once_with(f"Usage: {', '.join(commands.__all__)}")


@pytest.mark.parametrize(
    "command", ["script add something", "script update something", "script remove"]
)
def test_supported_commands(command, mock_sys, mock_commands):
    mock_sys.argv = command.split()
    main()
    getattr(mock_commands, mock_sys.argv[1]).assert_called_with(*mock_sys.argv[2:])
