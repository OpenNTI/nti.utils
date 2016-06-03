
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$

Adapted from collective.pdfpeek 2.0.0
https://pypi.python.org/pypi/collective.pdfpeek/2.0.0

either ghostscript or convert is required 

"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import shutil
import tempfile

from abc import ABCMeta

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

import subprocess

from PIL import Image

from PyPDF2 import PdfFileReader
from PyPDF2.utils import PdfReadError

from nti.common.property import Lazy

# constants
inch = 72.0
cm = inch / 2.54
mm = cm * 0.1

class AbstractPDFExtractor(object):

	__metaclass__ = ABCMeta

	img_thumb_format = 'PNG'
	img_thumb_quality = 60
	img_thumb_optimize = True
	img_thumb_progressive = False

	img_preview_format = 'PNG'
	img_preview_quality = 90
	img_preview_optimize = True
	img_preview_progressive = False

	page_limit = -1

	preview_width = 512
	preview_length = 512
	thumbnail_width = 128
	thumbnail_length = 128

	use_ghostscript = True
	
	def __init__(self, data):
		if hasattr(data, "read"):
			self._data = data.read()
		else:
			self._data = data

	def _fix_pdf(self, data):
		try:
			result = data + '\n%%EOF\n'
			return result
		except Exception:
			logger.error('Unable to fix pdf file.')
			return data

	@property
	def data(self):
		return self._data

	@Lazy
	def pdf(self):
		result = None
		try:
			result = PdfFileReader(StringIO(self.data))
		except Exception:
			logger.warn('Error opening pdf file, trying to fix it...')
			fixed_data = self._fix_pdf(self.data)

			# try to reopen the pdf file again
			try:
				result = PdfFileReader(StringIO(fixed_data))
			except Exception:
				logger.warn('This pdf file cannot be fixed.')
		return result

	@property
	def pages(self):
		if self.pdf:
			if self.page_limit <= 0:
				return self.pdf.getNumPages()
			return min(self.pdf.getNumPages(), self.page_limit)
		return 0

	@property
	def metadata(self):
		data = {}
		if self.pdf:
			try:
				data = dict(self.pdf.getDocumentInfo())
			except (TypeError, PdfReadError):
				logger.exception("Error getting PDF document info")
			data['width'] = float(self.pdf.getPage(0).mediaBox.getWidth())
			data['height'] = float(self.pdf.getPage(0).mediaBox.getHeight())
			data['pages'] = self.pdf.getNumPages()
		return data

	def get_thumbnails(self, page_start=0, pages=1):
		thumb_size = (self.thumbnail_width, self.thumbnail_length)
		preview_size = (self.preview_width, self.preview_length)

		# set up the images dict
		images = {}

		# Extracting self.pages pages
		logger.info('Extracting %s page screenshots', self.pages)

		for page in range(page_start, page_start + pages):
			# for each page in the pdf file,
			# set up a human readable page number counter starting at 1
			page_number = page + 1
			# set up the image object ids and titles
			image_id = '%d_preview' % page_number
			image_title = 'Page %d Preview' % page_number
			image_thumb_id = '%d_thumb' % page_number
			image_thumb_title = 'Page %d Thumbnail' % page_number

			# create a file object to store the thumbnail and preview in
			raw_image_thumb = StringIO()
			raw_image_preview = StringIO()

			# run ghostscript, convert pdf page into image
			if self.use_ghostscript:
				raw_image = self.ghostscript_transform(page_number)
			else:
				raw_image = self.convert_transform(page_number)

			if raw_image is None:
				continue
			# use PIL to generate thumbnail from image_result
			try:
				img_thumb = Image.open(StringIO(raw_image))
			except IOError:
				logger.error('This is not an image: %s', raw_image)
				break

			img_thumb.thumbnail(thumb_size, Image.ANTIALIAS)

			# save the resulting thumbnail in the file object
			img_thumb.save(raw_image_thumb,
						   format=self.img_thumb_format,
						   quality=self.img_thumb_quality,
						   optimize=self.img_thumb_optimize,
						   progressive=self.img_thumb_progressive)
			raw_image_thumb.seek(0)

			# use PIL to generate preview from image_result
			img_preview = Image.open(StringIO(raw_image))
			img_preview.thumbnail(preview_size, Image.ANTIALIAS)

			# save the resulting thumbnail in the file object
			img_preview.save(raw_image_preview,
							 format=self.img_preview_format,
							 quality=self.img_preview_quality,
							 optimize=self.img_preview_optimize,
							 progressive=self.img_preview_progressive)
			raw_image_preview.seek(0)

			# add the objects to the images dict
			images[image_id] = (image_id, image_title, raw_image_preview)
			images[image_thumb_id] = (image_thumb_id, image_thumb_title, raw_image_thumb)
			logger.info('Thumbnail generated.')

		return images

	def ghostscript_transform(self, page_num, data=None):
		"""
		run the ghostscript command on the pdf file, capture the output
		png file of the specified page number
		"""

		data = self.data if data is None else data
		first_page = '-dFirstPage=%s' % page_num
		last_page = '-dLastPage=%s' % page_num
		gs_cmd = [
			'gs',
			'-q',
			'-dSAFER',
			'-dBATCH',
			'-dNOPAUSE',
			'-sDEVICE=png16m',
			'-dGraphicsAlphaBits=4',
			'-dTextAlphaBits=4',
			first_page,
			last_page,
			'-r59x56',
			'-sOutputFile=%stdout',  # noqa
			'-',
		]

		bufsize = -1
		gs_process = subprocess.Popen(gs_cmd,
									  bufsize=bufsize,
									  stdout=subprocess.PIPE,
									  stdin=subprocess.PIPE)
		gs_process.stdin.write(data)
		image_result = gs_process.communicate()[0]
		gs_process.stdin.close()
		return_code = gs_process.returncode
		if return_code == 0:
			logger.info('Ghostscript processed one page of a pdf file.')
		else:
			logger.warn('Ghostscript process did not exit cleanly! '
						'Error Code: %s', return_code)
			image_result = None
		return image_result

	def convert_transform(self, page_num, data=None):
		"""
		run the imagemagick convert command on the pdf file, capture the output
		png file of the specified page number
		"""
		data = self.data if data is None else data
		try:
			tmp_dir = tempfile.mkdtemp(dir="/tmp")
			name = tempfile.mkstemp(dir=tmp_dir)[1]
			with open(name, "wb") as fp:
				fp.write(data)
			png_file = '%s.png' % name
			convert_cmd = [
				'convert',
				'-background white',
				'-alpha remove',
				'%s[%s]' % (name, page_num-1),
				'%s'  % png_file,
			]
			image_result = None
			return_code = os.system(' '.join(convert_cmd))
			if return_code == 0:
				logger.info('convert processed one page of a pdf file.')
				with open(png_file, "r") as fp:
					image_result = fp.read()
			else:
				logger.warn('convert process did not exit cleanly! '
							'Error Code: %s', return_code)
				image_result = None
			return image_result
		finally:
			shutil.rmtree(tmp_dir, True)

class FilePDFExtractor(AbstractPDFExtractor):

	def __init__(self, data):
		super(FilePDFExtractor, self).__init__(os.path.expanduser(data))

	@property
	def data(self):
		with open(self._data, "rb") as fp:
			result = fp.read()
		return result

	def save_thumbnails(self, page_start=0, pages=1, path=None):
		name = os.path.splitext(os.path.split(self._data)[1])[0]
		path = os.path.split(self._data)[0] if not path else path
		for image_id, value in self.get_thumbnails(page_start, pages).items():
			if not image_id.endswith('_thumb'):
				continue
			out_file = '%s_%s.png' % (name, image_id)
			out_file = os.path.join(path, out_file)
			with open(out_file, "wb") as fp:
				fp.write(value[2].read())