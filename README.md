# Install
## Ubuntu
1. You should have python and git installed.
  - You can run `python3 --version` to check the version of python. You may want
    to update to `3.11` with `sudo apt install python3.11`
  - You may need to install the `venv` and `pip` modules for python with
    `sudo apt install python3.10-venv` and
    `sudo apt install python3.10-pip`.
3. Run `git clone git@github.com:einargs/tnhimss-bill.git`. This will create a
  folder `tnhimss-bill` in the source code directory you ran it in.
  - Enter that directory.
4. Run `source start-python.sh`. Do this every time you need to run python code.
5. Run `pip install -r requirements.txt` This installs all of the package
  dependencies.
  - Now you can run the python server with: `hypercorn app:asgi -b localhost:5000`
  - You can also run python code with `python3 ./filename.py`. You can use this
    to test out stuff like `fhir_test.py`
6. Install node with `brew install node`
7. Install pnpm `npm install -g pnpm`
8. change to the `bill-site` directory and run `pnpm install`. Now you can run
  the website with `pnpm run dev`. To do this you need to be in the `bill-site`
  directory.

## MacOS
1. Install [homebrew](https://brew.sh/)
2. Install git with `brew install git`
3. Run `git clone git@github.com:einargs/tnhimss-bill.git`. This will create a
  folder `tnhimss-bill` in the source code directory you ran it in.
4. Run `source ./start-python.sh`. Do this every time you need to run python code.
  It's important that you run `source` and not `bash` or `sh`.
5. Run `pip install -r requirements.txt` This installs all of the package
  dependencies.
  - Now you can run the python server with: `hypercorn app:asgi -b localhost:5000`
  - You can also run python code with `python3 ./filename.py`. You can use this
    to test out stuff like `fhir_test.py`
6. Install node with `brew install node`
7. Install pnpm `npm install -g pnpm`
8. change to the `bill-site` directory and run `pnpm install`. Now you can run
  the website with `pnpm run dev`.

# FHIR Documentation
You can run a python documentation server locally with `pydoc -b` or
`python -m pydoc -b`.  This will open up a web page that lists all of the
installed python modules. `fhir` should be in there. We're using the `R4B`
format, so look under the `fhir.resources.R4B` module. You can also use the
`help()` function by calling it on e.g. a class.

The [FHIR website](https://www.hl7.org/fhir/) provides more information about
the structure of each class. I generally just google FHIR + whatever resource
type I need to know about.

# Running Parts
## Run backend
To run the backend locally, run:
```
hypercorn app:asgi -b localhost:5000
```

## Run frontend
To run the frontend server locally, cd to the `bill-site` directory and
run:
```
pnpm run dev
```
