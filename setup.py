import setuptools

#with open("README.md", "r") as fh:

#    long_description = fh.read()


# uninstall all packages:
# python -m pip freeze | xargs pip uninstall -y

setuptools.setup(
 #   name='pi_stream',
   # version='1.0',
#    description='To stream from a raspberry pi 4b',
#    author='Gabriel Grünberg',
 #   long_description=long_description,
 #   long_description_content_type="text/markdown",    
#    packages=['pi_stream'],
    install_requires=[
        'google-auth>=2.15.0',
        'google-auth-oauthlib>=0.8.0',
        'google-auth-httplib2>=0.1.0',
        'google-api-python-client>=2.70.0',
        'tomlkit>=0.11.6',
        'ffmpeg-python>=0.2.0'
    ],
  #  classifiers=[
 #       "Programming Language :: Python :: 3",
   #     "License :: OSI Approved :: MIT License",
   #     "Operating System :: Raspian OS",
  #  ],
    python_requires='>=3.9',
)