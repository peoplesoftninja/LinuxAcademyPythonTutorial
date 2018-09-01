import pytest
from pgbackup import cli
# $ pgbackup postgres://bob@example.com:5432/db_one --driver s3 backups

url = "postgres://bob@example.com:5432/db_one"

@pytest.fixture
def parser():
    return cli.create_parser()

def test_parser_without_driver(parser):
    """
    Without a specified drive (--driver in url) parser will exit
    """
    with pytest.raises(SystemExit):
        parser.parse_args([url])

def test_parser_with_driver(parser):
    """
    The parser will exit if driver given but without destination
    """
    with pytest.raises(SystemExit):
        parser.parse_args([url,"--driver","local"])

def test_passer_with_unknown_driver(parser):
    """
    The parser will exit if driver name is unkown
    """
    with pytest.raises(SystemExit):
        parser.parse_args([url,'--driver','azure','destination'])

def test_parser_with_known_drivers(parser):
    """
    The parser will not exit if driver name is known
    """
    for driver in ['local','s3']:
        assert parser.parse_args([url,'--driver',driver,'destination'])


def test_parser_with_driver_and_destination(parser):
    """
    The parser will not exit if it recives both driver and destination
    """
    args = parser.parse_args([url,'--driver','local','/some/path'])
    assert args.url == url
    assert args.driver == 'local'
    assert args.destination == '/some/path'

