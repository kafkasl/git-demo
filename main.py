from fasthtml.common import *

hdrs = (
    Link(rel='stylesheet', href='style.css', type='text/css'),
    Script("htmx.logAll();") # debug HTMX events
)

app, rt = fast_app(hdrs=hdrs)

@rt("/")
def get():
    return Titled("FastHTML Demo",
        P("Welcome to FastHTML!"),
        P("This is NOT simple demo for the Git workshop."),
        Button("Click me!", hx_post="/clicked", hx_target="#result"),
        Div(id="result")
    )

@rt("/clicked")
def post():
    return P("You clicked the button! 🎉", cls="text-green-600")

serve()