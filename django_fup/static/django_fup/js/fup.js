/*jslint browser: true*/
/*global qq, csrfmiddlewaretoken, jQuery */

"use strict";

var FileUploads = {};

(function ($) {
    var Uploader;

    Uploader = function (selector, url, csrf, onUploadComplete, onUploadFail) {
            var uploader;
            $(selector).fineUploader({
                request: {
                    endpoint: url,
                    params: {
                        'csrfmiddlewaretoken' : csrf,
                    }
                }
            }).on('progress', function (event, id, name, bytesUploaded, bytesTotal) {
                var progress;
                progress = (bytesUploaded / bytesTotal * 100) + '%';
                $('.file-upload-progress').show();
                $('.file-upload-progress .bar').css('width', progress);
            }).on('error', function (event, id, name, reason) {
                $('.file-upload-progress').hide();
                $('.file-upload-progress .bar').css('width', 0);
                if (onUploadFail) {
                    onUploadFail(id, name, reason);
                }
            }).on('complete', function (event, id, name, responseJSON) {
                $('.file-upload-progress').hide();
                $('.file-upload-progress .bar').css('width', 0);
                onUploadComplete(id, name, responseJSON);
            });
    };

    FileUploads.Uploader = function (selector, csrf, onUploadComplete, onUploadFail) {
        var $this, url, target, uploader_selector, instructions, upload_url;
        url = $(selector).data('source');
        upload_url =  $(selector).data('upload');
        target = $(selector).data('target');
        uploader_selector = '#file-uploader';
        $this = $(selector);
        new Uploader(uploader_selector, upload_url, csrf, function (id, orig_filename, data) {
            if (data.success) {
		if (onUploadComplete) {
                    onUploadComplete($this, data);
		}
            } else {
		if (onUploadFailed) {
                    onUploadFail($this, data);
		}
            }
        });
    }

    $(document).on('fup-load', '', function (evt) {
	new FileUploads.Uploader(evt.target, csrf_token, function (clicked, data) {
	    // close the modal
	    console.log($($(clicked).data('target')))

	    $('a[href="#close"]', $($(clicked).data('target'))).click();
	    
	    // update the image on the form
	    $('img', $(clicked)).attr('src', data.thumb_url);
	    $(clicked).next().val(data.url);
	});
    });

}(jQuery));
