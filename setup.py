import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="match_sim-ckear",
  version="0.0.1",
  author="Conor Kearney",
  author_email="ckear@example.com",
  description="A small example package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/ckear/match_sim",
  packages=setuptools.find_packages(),
  package_data={
    'match_sim': ['data/defaults/*.txt', 'data/formations/*.txt'],
  },
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)
