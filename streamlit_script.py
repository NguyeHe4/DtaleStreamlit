# import typing as T
# from streamlit.web.server import Server

# def get_streamlit_server() -> T.Optional[Server]:
#     """
#     Get the active streamlit server object. Must be called within a running
#     streamlit session.

#     Easy access to this object was removed in streamlit 1.12:
#         https://github.com/streamlit/streamlit/pull/4966
#     """
#     # In the run() method in `streamlit/web/bootstrap.py`, a signal handler is registered
#     # with the server as a closure. Fetch that signal handler.
#     streamlit_signal_handler = signal.getsignal(signal.SIGQUIT)

#     # Iterate through the closure variables and return the server if found.
#     for cell in streamlit_signal_handler.__closure__:
#         if isinstance(cell.cell_contents, Server):
#             return cell.cell_contents

#     return None

from streamlit.web.cli import main
from streamlit.web.server import Server as streamlit_server
import sys
from tornado.wsgi import WSGIContainer
from tornado.web import FallbackHandler

from dtale.app import build_app
from dtale.cli.clickutils import run


orig_start_listening = streamlit_server.start_listening


def _override_start_listening(app):
    dtale_app_obj = build_app(reaper_on=False)

    tr = WSGIContainer(dtale_app_obj)
    app.add_handlers(r".*", [(".*dtale.*", FallbackHandler, dict(fallback=tr))])
    orig_start_listening(app)


streamlit_server.start_listening = _override_start_listening

# we need to stop XSRF protection since dash won't work otherwise
additional_args = []
if "--server.enableCORS" not in sys.argv:
    additional_args += ["--server.enableCORS", "false"]
if "--server.enableXsrfProtection" not in sys.argv:
    additional_args += ["--server.enableXsrfProtection", "false"]
sys.argv += additional_args

if __name__ == "__main__":
    run(main)
