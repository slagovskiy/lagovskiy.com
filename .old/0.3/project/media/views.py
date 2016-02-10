import os
from sqlalchemy import func
from uuid import uuid4
from flask import Blueprint, request, redirect, url_for, g
from project.views import ajax_response
from .models import MediaFile, MediaFolder
from project import app, db, logger
from config import UPLOAD_DIR


mod_media = Blueprint(
    'media',
    __name__,
    url_prefix='/media',
    template_folder='templates'
)


@mod_media.route('/upload', methods=['POST'])
def upload():
    form = request.form

    is_ajax = False
    if form.get('__ajax', None) == 'true':
        is_ajax = True
    if g.user.is_authenticated:
        uploaded = []
        for upload in request.files.getlist('file'):
            upload_key = str(uuid4())
            target = UPLOAD_DIR + '/{}'.format(upload_key)
            try:
                os.mkdir(target)
            except:
                if is_ajax:
                    return ajax_response(False, 'Couldn\'t create upload directory: {}'.format(target))
                else:
                    return 'Could\'t create upload directory: {}'.format(target)
            filename = upload.filename.rsplit("/")[0]
            destination = '/'.join([target, filename])

            # select media folder
            mf = MediaFolder.query.get(request.form['upload_folder'])
            if mf is None:
                # if folder not selected - select default
                mf = MediaFile.query.filter(func.lower(MediaFolder.name) == 'default').first()
                if mf is None:
                    # if default not found - create default folder
                    mf = MediaFolder(name='default')
                    mf.rename = False
                    mf.author = g.user
                    db.session.add(mf)
                    db.session.commit()

            # save file on disk
            upload.save(destination)

            # save file information in base
            mf = MediaFile(
                folder=mf,
                name=filename,
                ext=filename[filename.find('.')+1:],
                uuid=upload_key
            )
            mf.author = g.user
            db.session.add(mf)
            db.session.commit()
            uploaded.append(upload_key)
        if is_ajax:
            return ajax_response(True, uploaded)
        else:
            return redirect(url_for('index'))
    else:
        if is_ajax:
            return ajax_response(False, 'User not authenticated.')
        else:
            return 'User not authenticated.'


@mod_media.route('/files', methods=['GET'])
def files():
    return 'ok'
