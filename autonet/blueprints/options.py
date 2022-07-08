from flask import Blueprint, current_app, jsonify

blueprint = Blueprint('options', __name__)


@blueprint.route('/', methods=['OPTIONS'])
def get_root_options():
    options = {}
    omit_options = [
        '/static/<path:filename>'
    ]
    for rule in current_app.url_map.iter_rules():
        if rule.rule in omit_options:
            continue
        idx = rule.rule.replace('<', '{').replace('>', '}')
        options[idx] = options.get(idx, {'args': [], 'methods': []})
        options[idx]['args'] = list(rule.arguments)
        options[idx]['methods'] = list(set(options[idx]['methods']
                                           + list(rule.methods)))

    return jsonify(options)
