from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='DashUI',
    version='0.1',
    author='Árvai Gábor',
    author_email='argabor@gmail.com',
    packages=['dashui'],
    scripts=['examples/test_app.py'],
    url='https://github.com/argabor/dash-desktop/',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    description='DashUI lets you create first class desktop applications in Python with Dash framework',
    long_description=open('README.md').read(),
    install_requires=required,
    python_requires='>=3.6',
)
