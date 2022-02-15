import setuptools

setuptools.setup(
    name="fibastvizualizer",
    version="1.0.5",
    author="Nikita Abramov",
    description="Python course homework. AST visualizer.",
    url="https://github.com/n8ron/python-hse-2022",
    packages=["fibastvizualizer"],
    python_requires=">=3.9",
    install_requires=["networkx==2.6.3", "pydot==1.4.2"],
)
