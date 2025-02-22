from setuptools import setup, find_packages

setup(
    name='ecs-deployer',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'config_ui=config.generate_config:main',
            'config=config.generate_config_yaml:app'
        ]
    },
    install_requires=[
        'typer',
        'pyyaml',
        'textual-dev',
        'loguru'
    ],
    extras_require={
        'dev': ['pytest', 'pytest-cov']
    }
)