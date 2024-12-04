import sys

sys.path.append("..")
import arrow

from fasthtml.common import *
from fapp import app, rt
from shared.fh.tables import *
from shared.fh.utils import *
import polars as pl
from datetime import date
import shared.database as db
from starlette.responses import RedirectResponse as redirect

channel_id = 4


@rt("/terms", methods=["POST"])
def new_term(params: dict):
    print(
        db.supabase.table("terms")
        .insert(
            [
                {
                    "term_text": params["term"],
                    "answer_text": params["answer"],
                    "channel_id": channel_id,
                }
            ]
        )
        .execute()
    )
    # Save term to database
    # ...save logic...
    return redirect("/terms", status_code=303)


@rt("/terms", methods=["GET"])
def terms_home(request: Request):
    current_terms = pl.DataFrame(
        db.supabase.table("terms")
        .select("term_text", "answer_text")
        .eq("channel_id", channel_id)
        .execute()
        .data
    )

    return Titled(
        "Terms",
        Div(
            id="terms",
            name="terms",
        )(
            H2("Current Terms"),
            Table()(
                Th(
                    Td("Term"),
                    Td("Answer"),
                ),
                *[
                    Tr(
                        Td(term["term_text"]),
                        Td(term["answer_text"]),
                    )
                    for term in current_terms.to_dicts()
                ],
            ),
            Form(
                hx_post="/terms",
                hx_swap="outerHTML",
                hx_target="#terms",
            )(
                Input(name="term", type="text", placeholder="Term"),
                Input(name="answer", type="text", placeholder="Answer"),
                Button(
                    "Add Term",
                    type="submit",
                    # action="/terms",
                    # method="post",
                ),
            ),
        ),
    )
