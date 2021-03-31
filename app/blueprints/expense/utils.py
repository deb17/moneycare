from flask_login import current_user

from app.models import Tag


def set_tags_on_expense(taglist, exp):

    for tagname in taglist.split(','):
        if tagname:
            tag = Tag.query.filter_by(
                user_id=current_user.id, tagname=tagname.lower()).first()
            if not tag:
                tag = Tag(user_id=current_user.id, tagname=tagname.lower())
            exp.tags.append(tag)
