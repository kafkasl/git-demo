from fasthtml.common import *
from monsterui.all import *
from fasthtml.oauth import GoogleAppClient, OAuth
from dotenv import load_dotenv


load_dotenv()

cli = GoogleAppClient(client_id=os.environ["CLIENT_ID"],
                      client_secret=os.environ["CLIENT_SECRET"])

class Auth(OAuth):
    def get_auth(self, info, ident, session, state):
        email = info.email or ''
        session['email'] = email

        return RedirectResponse('/', status_code=303)

hdrs = (
    Theme.blue.headers(),
    Link(rel='stylesheet', href='style.css', type='text/css'),
    # Script("htmx.logAll();") # debug HTMX events
)
skip = ('/login', '/logout', '/redirect', r'/.*\.(png|jpg|ico|css|js|md|svg)', '/static')

app, rt = fast_app(hdrs=hdrs)
oauth = Auth(app, cli, skip=skip)

def UserMenu(email: str): return DivHStacked(P(email), A("Logout", href="/logout"))

def NavBar(email):
    return Div(
        A(            
            Img(src="https://icons-8e9.pages.dev/favicon-black.svg", width=40),
            H1('Git 4 FastHTML', href="/"), 
            href="/"
        ),
        UserMenu(email),
        cls="header-container"
    )

@app.get
def index(session):
    email = session.get('email', None)

    return (Title("Git 4 FastHTML"),
                Container(
                    NavBar(email)
                )
            )

@app.get('/login')
def login(req): 
    return (
        Title("Git 4 FastHTML"),
        DivVStacked(
            Img(src="https://icons-8e9.pages.dev/favicon-black.svg", width=100),
            DivVStacked(
                H1('Git 4 FastHTML', cls="text-center"),
                P("Track your changes and move fast", cls=TextPresets.muted_sm + " text-center"),
                A(Button("Log in with Google"), href=oauth.login_link(req))
            ),
            cls="pt-[20vh]",
        ),
    )

@app.get('/logout')
def logout(session):
    session.pop('auth', None)
    return RedirectResponse('/login', status_code=303)

 

# Start server
if __name__ == "__main__":
    serve()
