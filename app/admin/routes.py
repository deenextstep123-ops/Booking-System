from flask import render_template, request, redirect, url_for
from flask_login import login_required

from app.admin import admin
from app.admin.forms import ServiceSettingsForm
from app.extensions import db
from app.models import Service


@admin.route("/service-settings", methods=["GET", "POST"])
@login_required
def service_settings():

    # There should only ever be one Service record.
    service = Service.query.first()

    if request.method == "POST":

        form = ServiceSettingsForm(request.form)

        if form.validate():

            service.name = form.name
            service.duration_minutes = form.duration_minutes

            db.session.commit()

            return redirect(
                url_for("admin.service_settings")
            )

        return render_template(
            "admin/service_settings.html",
            form=form,
            service=service
        )

    return render_template(
        "admin/service_settings.html",
        service=service
    )