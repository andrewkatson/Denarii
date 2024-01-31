import argparse

# The artifact if found is deleted
DELETE = "DELETE"
# The artifact if found is left where it is
SKIP = "SKIP"

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--existing_artifact_delete_policy', type=str,
                    help='What to do when an artifact exists. This does not apply to creating the BUILD files and folders. Valid values are {DELETE}, {SKIP}')

args = parser.parse_args()
