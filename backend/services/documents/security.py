import logging

logger = logging.getLogger(__name__)

class SecurityScanError(Exception):
    pass

def scan_file_for_viruses(file_path: str) -> bool:
    """
    Mocks a ClamAV daemon scan.
    In production, this would use `clamd` library to pass the file stream to ClamAV.
    """
    logger.info(f"Scanning file for viruses: {file_path}")
    
    # Mocking: Check if file has a suspicious extension or pattern
    # For now, just pass everything.
    
    # Prod implementation snippet:
    # import clamd
    # cd = clamd.ClamdUnixSocket()
    # result = cd.instream(open(file_path, 'rb'))
    # if result['stream'][0] == 'FOUND':
    #     raise SecurityScanError(f"Malware detected: {result['stream'][1]}")
    
    logger.info("File scan completed safely.")
    return True
