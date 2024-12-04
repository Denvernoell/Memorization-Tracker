from fasthtml.common import *


def _not_found(req, exc):
    return Titled("Oh no!", Div("We could not find that page :("))


from shared.database import bware

app = FastHTML(
    before=bware,
    # These are the same as Starlette exception_handlers, except they also support `FT` results
    exception_handlers={404: _not_found},
    routes=[],
    hdrs=(
        picolink,
        Html(data_theme="emerald"),
        Script(src="https://cdn.tailwindcss.com"),
        Link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css",
        ),
        # Have a look at fasthtml/js.py to see how these Javascript libraries are added to FastHTML.
        # They are only 5-10 lines of code each, and you can add your own too.
        # SortableJS(".sortable"),
        # Html(data_theme="dark"),
        Style("""
			"""),
    ),
)
# from shared.paths import paths


# app.mount(
#     path="/well_files",
#     app=StaticFiles(
#         directory=paths["well_info"].as_posix(),
#     ),
#     name="well_files",
# )
# app.mount(
#     "/stc",
#     StaticFiles(
#         directory="shared/static",
#         # html=True,
#     ),
#     name="stc",
# )

# navbar = Div(
#     cls="navbar bg-base-100",
# )(
#     A(cls="navbar-brand", href="/")("Tranquillity District"),
#     Div(cls="navbar-start")(
#         Ul(
#             cls="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow",
#         )(
#             Li(cls="navbar-item")(A(cls="navbar-link", href="/")("Home")),
#             Li(cls="navbar-item")(
#                 A(cls="navbar-link", href="/board")("Board Packages")
#             ),
#             Li(cls="navbar-item")(A(cls="navbar-link", href="/wells")("Wells")),
#             Li(cls="navbar-item")(A(cls="navbar-link", href="/sgma")("SGMA")),
#             # Li(cls="navbar-item")(
#             #     A(cls="navbar-link", href="/well_files")("Well Files")
#             # ),
#         ),
#     ),
# )


rt = app.route
