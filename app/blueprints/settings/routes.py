from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import current_user, login_required

from app.extensions import db
from app.models import PaymentMode, Tag
from app.blueprints.settings.forms import (
    SettingsForm,
    PaymentModeAddForm,
    PaymentModeEditForm,
    TagForm
)

bp = Blueprint('settings', __name__, url_prefix='/settings')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():

    form = SettingsForm(obj=current_user)

    if form.validate_on_submit():
        u = current_user
        u.limit = form.limit.data
        u.allow_decimals = form.allow_decimals.data
        u.ccy_iso = form.ccy_iso.data.upper()
        form_ccode = form.country_code.data.upper()
        if u.country_code != form_ccode:
            u.set_locale(form_ccode)
            u.country_code = form_ccode
        u.ccy_override = form.ccy_override.data.strip()
        db.session.commit()
        flash('Settings updated.', 'success')
        return redirect(url_for('expense.list_expenses'))

    return render_template('settings/settings.html', title='Settings',
                           form=form)


@bp.route('/tags', methods=['GET', 'POST'])
@login_required
def manage_tags():

    form = TagForm()

    if form.validate_on_submit():
        new_tag = Tag(tagname=form.tagname.data.lower())
        current_user.tags.append(new_tag)
        db.session.commit()
        flash('New tag was added.', 'success')
        return redirect(url_for('settings.manage_tags'))

    return render_template('settings/tags.html', title='Expense Tags',
                           form=form)


@bp.route('/tags/delete/<int:id>')
@login_required
def delete_tag(id):

    tag = Tag.query.get(id)
    if tag.user_id != current_user.id:
        abort(403)

    db.session.delete(tag)
    db.session.commit()
    flash('The tag was deleted', 'success')

    return redirect(url_for('settings.manage_tags'))


@bp.route('/modes', methods=['GET', 'POST'])
@login_required
def manage_payment_modes():

    form = PaymentModeAddForm()

    if form.validate_on_submit():
        new_mode = PaymentMode(
            user_id=current_user.id,
            mode=form.mode.data
        )
        db.session.add(new_mode)
        db.session.commit()
        flash('New payment mode was added.', 'success')
        return redirect(url_for('settings.manage_payment_modes'))

    return render_template('settings/payment_mode.html',
                           title='Payment Mode', form=form)


@bp.route('/modes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_mode(id):

    old_mode = PaymentMode.query.get(id)
    if old_mode.user_id != current_user.id:
        abort(403)

    form = PaymentModeEditForm(obj=old_mode)

    if form.validate_on_submit():
        old_mode.mode = form.mode.data
        db.session.commit()
        flash('Payment mode updated.', 'success')
        return redirect(url_for('settings.manage_payment_modes'))

    return render_template('settings/edit_mode.html',
                           title='Edit Mode', id=id, form=form)


@bp.route('/modes/delete/<int:id>')
@login_required
def delete_mode(id):

    mode = PaymentMode.query.get(id)
    if mode.user_id != current_user.id:
        abort(403)

    if mode.expenses.count() > 0:
        flash(
            'The payment mode cannot be deleted as there are linked expenses.',
            'danger'
        )
        return redirect(url_for('settings.manage_payment_modes'))

    db.session.delete(mode)
    db.session.commit()
    flash('Payment mode was deleted.', 'success')

    return redirect(url_for('settings.manage_payment_modes'))
