import logging
log = logging.getLogger('nwdaf-secure.nssf')

async def enforce(action: str, data: dict) -> str:
    # Mock slice steering via NSSF
    log.info(f"NSSF enforce: {action} {data}")
    return 'OK'
