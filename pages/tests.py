import sys

sys.path.append("..")
import arrow

from fasthtml.common import *
from fapp import app, rt
from shared.fh.tables import *
from shared.fh.utils import *
import polars as pl
from datetime import date


@rt("/tests", methods=["GET", "POST"])
def tests_home(request):
    if request.method == "POST":
        # Handle test taking logic here
        # ...test logic...
        return redirect("/tests")
    current_tests = []  # Fetch current tests from database
    return Titled(
        "Tests",
        H2("Current Tests"),
        Table(current_tests),
        Form(
            # Form fields for taking tests
            Button("Start Test", type="submit")
        ),
    )
