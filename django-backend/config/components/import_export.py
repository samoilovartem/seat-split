from config.components.global_settings import DEBUG

IMPORT_EXPORT_EXPORT_PERMISSION_CODE = 'export'
IMPORT_EXPORT_IMPORT_PERMISSION_CODE = 'import'
IMPORT_EXPORT_TMP_STORAGE_CLASS = 'import_export.tmp_storages.MediaStorage'
IMPORT_EXPORT_CHUNK_SIZE = 150 if DEBUG else 75
