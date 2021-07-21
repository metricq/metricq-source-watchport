from setuptools import setup

setup(
    name="metricq_source_watchport",
    version="0.1",
    author="TU Dresden",
    python_requires=">=3.5",
    packages=["metricq_source_watchport"],
    scripts=[],
    entry_points="""
      [console_scripts]
      metricq-source-watchport=metricq_source_watchport:source
      """,
    install_requires=[
        "click",
        "click-completion",
        "click_log",
        "colorama",
        "metricq~=3.0",
        "pyserial-asyncio",
    ],
)
