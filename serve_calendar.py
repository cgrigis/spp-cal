"""
Generate shift calendar for La Fève
"""
import datetime
import io
import logging
import logging.config
import os
import subprocess
import tempfile

from quart import (
    Quart,
    make_response,
    request,
    render_template,
    send_file,
    send_from_directory,
)

from gen_spp_cal import gen_calendar

logging_config = {
    "version": 1,
    "formatters": {
        "simple": {"format": "%(asctime)s [%(name)-10s] %(levelname)-10s %(message)s"}
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        }
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
}

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


app = Quart(__name__)


@app.route("/", methods=["GET"])
async def index():
    current_year = datetime.datetime.now().year

    return await render_template("index.html", current_year=current_year)

@app.route("/cal/svg", methods=["POST"])
async def gen_cal_svg():
    args = await request.values
    year, week_id = int(args['year']), int(args['week_id'])

    svg_data = gen_calendar(year, week_id)

    response = await send_file(
            io.BytesIO(svg_data.encode('utf8')),
            mimetype="image/svg+xml",
            )

    return response

@app.route("/cal/download", methods=["POST"])
async def redirect_to_pdf():
    args = await request.values
    year, week_id = int(args['year']), int(args['week_id'])

    response = await make_response("")
    response.headers['HX-Redirect'] = f"/cal/pdf?year={year}&week_id={week_id}"

    return response

@app.route("/cal/pdf", methods=["GET"])
async def gen_cal_pdf():
    args = await request.values
    year, week_id = int(args['year']), int(args['week_id'])

    svg_data = gen_calendar(year, week_id)

    with tempfile.TemporaryDirectory() as tmpdirname:
        with open(os.path.join(tmpdirname, "cal.svg"), 'w', encoding='utf-8') as f:
            f.write(svg_data)

        subprocess.run([
            "rsvg-convert",
            "--format", "pdf",
            "--output", os.path.join(tmpdirname, "cal.pdf"),
            os.path.join(tmpdirname, "cal.svg"),
            ], check=True)

        with open(os.path.join(tmpdirname, "cal.pdf"), 'rb') as f:
            pdf_data = f.read()

    response_filename = f"calendrier_spp_{year}.pdf"
    response = await send_file(io.BytesIO(pdf_data),
            mimetype="application/pdf",
            as_attachment=True,
            attachment_filename=response_filename)

    return response

@app.route("/lib/htmx", methods=["GET"])
async def serve_htmx():
    lib_dir = os.path.join(app.root_path, "lib")

    return await send_from_directory(lib_dir, "htmx.min.js")
