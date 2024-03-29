from glue.config import importer
from glue_qt.dialogs.data_wizard import data_wizard


@importer("Import from directory")
def directory_importer():
    return data_wizard(mode='directories')
