from distutils.core import setup

version = '0.1'

setup(name='django-uploadify-s3',
      version=version,
      description='A Django application for enabling browser-based uploads to Amazon S3 with the Uploadify uploader.',
      author='Sam Charrington',
      author_email='sbc@charrington.com',
      url='https://github.com/sbc/django-uploadify-s3',
      packages=['uploadify_s3', 'uploadify_s3.templatetags'],
      package_data = {'uploadify_s3': ['templates/*.html']},
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      )