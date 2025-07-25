from fasthtml.common import *
from fasthtml.oauth import GoogleAppClient, OAuth
from monsterui.all import *


cli = GoogleAppClient(client_id='YOUR_KEY_HERE',
                      client_secret='YOUR_SECRET_HERE')

class Auth(OAuth):
    def get_auth(self, info, ident, session, state):
        email = info.email or ''
        session['email'] = email

        return RedirectResponse('/', status_code=303)

hdrs = (
    Link(rel='stylesheet', href='style.css', type='text/css'),
)
skip = ('/login', '/logout', '/redirect', r'/.*\.(png|jpg|ico|css|js|md|svg)', '/static')

app, rt = fast_app(hdrs=hdrs)
oauth = Auth(app, cli, skip=skip)


@app.get
def index(session):
    email = session.get('email', None)

    return (Title("Git 4 FastHTML"), P(f"Welcome {email}"),)

@app.get('/login')
def login(req): 
    return (
        Title("Git 4 FastHTML"),
        DivVStacked(
            Img(src="https://icons-8e9.pages.dev/favicon-black.svg", width=100),
            DivVStacked(
                H1('Git 4 FastHTML', cls="text-center"),
                P("Track your changes and move fast", cls="text-center"),
                A(Button("Log in with Google"), href=oauth.login_link(req))
            ),
            cls="pt-[20vh]",
        ),
    )

 

# Start server
if __name__ == "__main__":
    serve()
