from conf_engine import config, options

opts = [
    options.BooleanOption('debug', default=False)
]

config.register_options(opts)

