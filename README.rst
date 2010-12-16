========================================================================
Django Uploadify-S3 (DUS3): Browser-Based Uploads to Amazon S3 Made Easy
========================================================================

Overview
--------

This application aims to make it easy for you to add browser-based 
uploads to Amazon S3 to your Django projects using the Uploadify
jQuery plugin.

DUS3 is configuration driven, meaning you don't need to add any 
Uploadify or S3-specific code to your project to use these tools. 


Requirements
------------

Download the Uploadify ZIP file and unzip it in your project. This
application assumes the files will be located in an ``uploadify`` 
directory within your MEDIA_URL directory.

Note that Uploadify requires jQuery, and django-uploadify-s3 does not
automatically include it. (To avoid conflicts.) You will need to 
include jQuery in your base template, or on the uploadify upload page.

Background
----------

A general understanding of Uploadify and submitting browser-based
uploads to Amazon S3 is helpful if not necessary:

- Uploadify:
  http://www.uploadify.com/

- Browser-Based Uploads to Amazon S3: 
  http://docs.amazonwebservices.com/AmazonS3/latest/dev/UsingHTTPPOST.html


Installation & Use
------------------

1. Add ``uploadify_s3`` to your ``INSTALLED_APPLICATIONS``.

2. Add any desired project-wide settings to your ``settings.py``
   or equivalent. See Settings below.

3. Create a view and a template for your file upload page.

4. Call::

     uploadify_s3.UploadifyS3().get_options_json() 

   to generate the Uploadify configuration options and make this context
   available to your template.
   
   ``UploadifyS3()`` takes three optional parameters:
   
   - ``uploadify_options``: A dictionary of Uploadify options.
   - ``post_data``: A dictionary of POST variables that is used to
     set the Uploadify scriptData option and eventually sent to AWS.
   - ``conditions``: See conditions, below.
      
   These parameters are optional because DUS3 can in many cases pull
   all of its configuration data from your settings.py. The parameters
   override any values found in your settings file.
   
5. Load the DUS3 template tags and insert them in your template.

   Add this above any of the other tags to load the tag set::
      {% load uploadify_tags %}

   Add this in your ``<head>`` to include the Uploadify jQuery, CSS and
   SWF files::
      {% uploadify_head %}
   
   Add this in your ``<body>`` to include the Uploadify file upload 
   widget. Initially this will appear as a "Select Files" button;
   when files are added the queue and progress bars will be 
   displayed. The ``uploadify_options`` parameter is the options 
   string you created in your view::
      {% uploadify_widget uploadify_options %}
      
   Add this to your ``<body>`` to insert an Upload link/button. It takes a
   string parameter that allows you to add custom CSS classes::
      {% uploadify_upload "extra css classes" %}


Settings
--------

DUS3 looks for an ``UPLOADIFY_DEFAULT_OPTIONS``, which is used to override
Uploadify default option values on a project-wide bases. 
``UPLOADIFY_DEFAULT_OPTIONS`` is a Python dictionary with keys corresponding 
to Uploadify options and native Python values, i.e. use Python boolean
False to set a boolean option false, as opposed to string value of "false". 
These values may be overridden by passing options to ``UploadifyS3()``
in your view.
        
In addition, DUS3 recognizes the following AWS S3 options:

===========================   ==================================================
``AWS_ACCESS_KEY_ID``         Required. Either set in settings or pass in.
``AWS_SECRET_ACCESS_KEY``     Required. Either set in settings or pass in.
``AWS_BUCKET_NAME``           Required. Either set in settings or pass in.
``AWS_S3_SECURE_URLS``        Set to False to force http instead of https.
``AWS_BUCKET_URL``            Shouldn't need. Default is calculated from bucket name.
``AWS_DEFAULT_ACL``           Default is ``private``.
``AWS_DEFAULT_KEY_PATTERN``   The S3 ``key`` param. Default is ``'${filename}'``.
``AWS_DEFAULT_FORM_LIFETIME`` Signed form expiration time in secs from now.
===========================   ==================================================

Conditions
----------

To allow web browsers to post files to your S3 bucket you create and 
a policy document that describes the conditions under which AWS should 
accept a POST request. That policy document, and a signed version of it, 
is then included in the POST data.

AWS first verifies the integrity of the policy document and then compares
the conditions specified in the policy document with the POST data received.

See: http://docs.amazonwebservices.com/AmazonS3/latest/dev/index.html?AccessPolicyLanguage_UseCases_s3_a.html

``UploadifyS3()`` expects to receive a dictionary of conditions mapping a 
field name to a value object. Conditions are described by using different
data types for the value object*:

===============     ======================================================
Value Data Type     Condition Applied
===============     ======================================================
``nil``             A starts-with test that will accept any value
``str``             An equality test using the given string
``list``            An equality test, against a value composed of all 
                    the array's items combined into a comma-delimited 
                    string
``dict``            An operation named by the ``op`` mapping, with a value 
                    given as the ``value`` mapping
``slice``           A range test, where the range must lie between the
                    start and stop values of the slice object provided
===============     ======================================================

*The semantics of the conditions array were very much inspired by 
James Murty's *Programming Amazon Web Services*.


Troubleshooting
---------------

1. In order for the browser to communicate to your S3 bucket, you must
   upload a ``crossdomain.xml`` file to the root of your bucket. This example
   allows any browsers to communicate with your S3 bucket::
   
       <?xml version="1.0"?>
       <!DOCTYPE cross-domain-policy SYSTEM "http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">
       <cross-domain-policy>
         <allow-access-from domain="*" secure="false" />
       </cross-domain-policy>
   
2. Because Uploadify uses a Adobe Flash component to perform the actual
   upload, browser-based HTTP debugging tools like Firebug cannot see 
   the traffic between the browser and S3. You can however use a network
   sniffer like Wireshark (http://www.wireshark.org) to view the traffic.