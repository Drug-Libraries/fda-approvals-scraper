from setuptools import setup, find_packages

setup(
    name="fda_approvals_scraper",
    version="1.0.0",
    author="R.Shibin","Upputoori Sree Vasthav"
    author_email="rshibinpharma17@gmail.com","sreevasthav.upputoori@gmail.com"
    description="A web scraper for FDA drug approvals using Selenium.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "chromedriver-autoinstaller"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
