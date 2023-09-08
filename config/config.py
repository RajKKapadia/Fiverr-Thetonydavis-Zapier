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
