import logging, sys

def setup_logging(level: str = 'INFO'):
    lvl = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=lvl,
        format='[%(asctime)s] %(levelname)s %(name)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger('nwdaf-secure')
