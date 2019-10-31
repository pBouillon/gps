from distutils.core import setup

setup(
    name='github-profile-summary',
    version='0.1dev',
    packages=['github_profile_summary', ],
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "requests>=2.22.0"
    ],
    package_dir={'github_profile_summary': 'src'},

)
