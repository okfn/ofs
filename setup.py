from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name="OFS",
      version="0.1",
      description="OFS - provides plugin-orientated low-level blobstore.",
      long_description="""OFS - provides plugin-orientated low-level blobstore. """,
      maintainer="Ben O'Steen",
      maintainer_email="bosteen@gmail.com",
      license="http://www.apache.org/licenses/LICENSE-2.0",
      packages=find_packages(),
      test_suite = "tests.test.TestPairtreeOFS",
      )

