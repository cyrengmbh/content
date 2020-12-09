import os
import argparse
from Tests.Marketplace.marketplace_services import init_storage_client


STORAGE_ID_SET_PATH = 'content/id_set.json'
ARTIFACTS_PATH = '/home/circleci/project/artifacts/'
PRIVATE_ID_SET_FILE = 'private_id_set.json'


def download_private_id_set_from_gcp(public_storage_bucket):
    """Downloads private ID set file from cloud storage.

    Args:
        public_storage_bucket (google.cloud.storage.bucket.Bucket): google storage bucket where private_id_set.json
        is stored.
    Returns:
        str: private ID set file full path.
    """

    index_blob = public_storage_bucket.blob(STORAGE_ID_SET_PATH)

    if not os.path.exists(ARTIFACTS_PATH):
        os.mkdir(ARTIFACTS_PATH)
    index_blob.download_to_filename(f'{ARTIFACTS_PATH}/{PRIVATE_ID_SET_FILE}')

    if os.path.exists(f'{ARTIFACTS_PATH}/{PRIVATE_ID_SET_FILE}'):
        return f'{ARTIFACTS_PATH}/{PRIVATE_ID_SET_FILE}'

    return ''


def option_handler():
    """Validates and parses script arguments.

    Returns:
        Namespace: Parsed arguments object.

    """
    parser = argparse.ArgumentParser(description="Store packs in cloud storage.")
    # disable-secrets-detection-start
    parser.add_argument('-b', '--public_bucket_name', help="CI public bucket name", required=True)
    parser.add_argument('-s', '--service_account',
                        help=("Path to gcloud service account, is for circleCI usage. "
                              "For local development use your personal account and "
                              "authenticate using Google Cloud SDK by running: "
                              "`gcloud auth application-default login` and leave this parameter blank. "
                              "For more information go to: "
                              "https://googleapis.dev/python/google-api-core/latest/auth.html"),
                        required=False)

    # disable-secrets-detection-end
    return parser.parse_args()


def main():
    options = option_handler()
    service_account = options.service_account
    storage_client = init_storage_client(service_account)
    public_bucket_name = options.public_bucket_name
    public_storage_bucket = storage_client.bucket(public_bucket_name)
    private_id_set = download_private_id_set_from_gcp(public_storage_bucket)
    return private_id_set


if __name__ == '__main__':
    main()