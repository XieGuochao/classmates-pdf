# Classmates Project: PDF Generator

## Quick Start

Note: You should pass your data in `in` directory and your output file will be written to `out` directory.

You should follow the template of input and output in the `in` and `out` directory.

### Docker

A dockerfile is provided. You can build the container and run with the following instructions:

1. `docker build -t classmates-pdf .`
2. `docker run --rm -v $(PWD)/in:/in -v $(PWD)/out:/out classmates-pdf`


### Install Manually

Prerequisite: `python3` (test on `python3.8`).

1. `python3 -m pip install -r src/requirements.txt`: install dependency.
2. `python3 src/main.py`: run.

### As a Component of Classmates Project

We also implement several things to connect with the Classmates projects:

1. `redis` as a message queue.
2. Retrieve and upload data from MySQL Database.
3. Upload pdf to cloud storage.
4. Send email to notify users.

## Developers

Feel free to modify python codes. You may need to pay attention to the licenses of the fonts.

## Contact

Contact me on [gx@apartsa.com](mailto:gx@apartsa.com).
