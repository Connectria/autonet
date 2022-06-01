import os
import pytest


@pytest.fixture
def test_cwd(request):
    fp = ''
    for part in request.path.parts[1:]:
        fp += '/' + part
        if part == 'autonet':
            return fp


@pytest.fixture(autouse=True)
def use_test_config(monkeypatch, test_cwd):
    monkeypatch.chdir(test_cwd)
    monkeypatch.setattr('sys.argv', ['program', '--config-file', './tests/test_config.ini'])


@pytest.fixture
def test_token():
    return 'f19da6fe9db446a3b8b501ad8cecb7d1'


@pytest.fixture
def test_token_hash():
    return '$pbkdf2-sha512$25000$jdFayzlHqPX.PyfEOKdUag$MXXGN/1fM0QNSjHFsRdXLh9CYPTwVtBBPTW8nDwttEOFQ9r2n/VHY4okEGA9DU1hlYTNjIdGxuwbU5ZkNsM2JQ'


@pytest.fixture
def test_auth_header(test_token):
    return {'X-API-Key': f'admin:{test_token}'}


@pytest.fixture
def flask_app():
    from autonet.core.app import flask_app
    flask_app.config.update({
        'TESTING': True
    })

    yield flask_app


@pytest.fixture
def client(flask_app, monkeypatch):
    return flask_app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def db_session(request):
    from sqlalchemy import text
    from autonet.db import Session
    from autonet.db.base import engine, mapper_registry
    mapper_registry.metadata.create_all(bind=engine)
    session = Session()
    populated = request.param if hasattr(request, 'param') else True
    if populated:
        cwd = os.path.dirname(os.path.abspath(__file__))
        for sql_file in [f'{cwd}/tests/sql/users.sql', f'{cwd}/tests/sql/tokens.sql']:
            with open(sql_file, 'r') as sql_fh:
                for sql in sql_fh.readlines():
                    session.execute(text(sql))
        session.commit()

    yield session
    mapper_registry.metadata.drop_all(bind=engine)
