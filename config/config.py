import os
import tempfile
import uuid

TEXT_FILE_PATH = os.path.join(
    tempfile.gettempdir(),
    f'{uuid.uuid1()}.txt'
)

CSV_FILE_PATH = os.path.join(
    tempfile.gettempdir(),
    f'{uuid.uuid1()}.csv'
)

HCE_AMOUNT = 130000
HCE_OWNERSHIP_PERCENTAGE = 5
HCE_FAMILY_RELATIONSHIP = 'Yes'

DP_MAXIMUM_COMPENSATION = 305000
