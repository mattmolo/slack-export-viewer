import flask


app = flask.Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)


@app.route("/channel/<name>")
def channel_name(name):
    messages = flask._app_ctx_stack.channels[name]['messages']
    all_channels = [{
            "name": c,
            "archived": flask._app_ctx_stack.channels[c]['archived']
        } for c in list(flask._app_ctx_stack.channels.keys())
    ]
    channels = [c for c in all_channels if not c['archived']]
    archived_channels = [c for c in all_channels if c['archived']]

    return flask.render_template(
        "viewer.html",
        messages=messages,
        name=name.format(name=name),
        channels=sorted(channels, key=lambda x: x['name']),
        archived_channels=sorted(archived_channels, key=lambda x: x['name']))


@app.route("/")
def index():
    channels = list(flask._app_ctx_stack.channels.keys())
    if "general" in channels:
        return channel_name("general")
    else:
        return channel_name(channels[0])
