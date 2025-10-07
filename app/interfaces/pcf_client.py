import logging
log = logging.getLogger('nwdaf-secure.pcf')

async def enforce(action: str, data: dict) -> str:
    # Mock policy tweak via PCF
    log.info(f"PCF enforce: {action} {data}")
    return 'OK'
