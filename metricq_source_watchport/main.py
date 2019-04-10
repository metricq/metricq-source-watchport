import click
import click_log
import click_completion

from metricq.logging import get_logger

from .source import WatchPortSource

logger = get_logger()

click_log.basic_config(logger)
logger.setLevel('INFO')

click_completion.init()


@click.command()
@click.option('--server', default='amqp://localhost/')
@click.option('--token', default='source-watchport')
@click_log.simple_verbosity_option(logger)
def source(server, token):
    src = WatchPortSource(token=token, management_url=server)
    src.run()


if __name__ == '__main__':
    source()
