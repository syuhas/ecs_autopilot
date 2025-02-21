from setuptools import setup, find_packages

setup(
    name='ecs-deployer',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'yaml=config_cli.generate_config_yaml:app'
        ]
    },
    install_requires=[
        'typer'
    ],
    extras_require={
        'dev': ['pytest', 'pytest-cov']
    }
)