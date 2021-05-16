import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="match_sim-ckear",
  author="Conor Kearney",
  author_email="ckear@example.com",
  description="A small example package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/ckear/match_sim",
  packages=setuptools.find_packages(),
  package_data={
    'match_sim': ['data/defaults/*.txt', 'data/formations/*.txt', 'data/settings/*.json'],
  },
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
  python_requires=">=2.7",
  extras_require={
    "run": [
    ],
    "dev": [
      "pyfiglet>=0.8",
      "progressbar>=2.5",
      "numpy>=1.16.6",
      "tqdm>=4.46.1",
      "prettytable>=0.7.2",
      "names>=0.3.0",
      "python-dateutil>=2.8.1",
      "barnum>=0.5.1",
      "dill>=0.3.1.1",
      "wxPython>=4.1.0",
      "pytest>=3.5",
    ],
    "gen_tests": [
    ]   
  },
  use_scm_version=True,
  setup_requires=["setuptools_scm"],
)
