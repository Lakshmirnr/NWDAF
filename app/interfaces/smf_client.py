import logging
log = logging.getLogger('nwdaf-secure.smf')

async def enforce(action: str, data: dict) -> str:
    # Mock enforcement with SMF
    log.info(f"SMF enforce: {action} {data}")
    return 'OK'
