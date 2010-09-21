from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(
    name="OFS",
    version="0.1",
    description="OFS - provides plugin-orientated low-level blobstore.",
    long_description="""OFS - provides plugin-orientated low-level blobstore. """,
    maintainer="Ben O'Steen",
    maintainer_email="bosteen@gmail.com",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    packages=find_packages(),
    test_suite = "test.test.TestPairtreeOFS",
    entry_points="""
    [ofs.backend]
    pairtree = ofs.local.pairtreestore:OFS
    s3 = ofs.remote.botostore:S3OFS
    google = ofs.remote.botostore:GSOFS
    archive.org = ofs.remote.botostore:ArchiveOrgOFS
    reststore = ofs.remote.reststore:RESTOFS
    """
    )

