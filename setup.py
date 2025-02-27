from setuptools import setup, find_packages

setup(
    name='ecs-autopilot',
    version='0.3.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'config_ui=config.generate_config_ui:main',
            'config=config.generate_config:app',
            'config_dsl=config.generate_dsl:app'
        ]
    },
    install_requires=[
        'typer',
        'pyyaml',
        'textual-dev',
        'loguru',
        'jinja2'
    ],
    extras_require={
        'dev': ['pytest', 'pytest-cov']
    }
)