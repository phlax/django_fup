/*jslint browser: true*/
/*global qq, csrfmiddlewaretoken, jQuery */

"use strict";

var FileUploads = {};

(function ($) {
    var Uploader;

    Uploader = function (selector, url, csrf, onUploadComplete, onUploadFail) {
        return function () {
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
    };

    FileUploads.Uploader = function (selector, csrf, onUploadComplete, onUploadFail) {
        selector.live("click", function (event) {
            var $this, url, target, uploader_selector, instructions, upload_url;
            url = $(this).attr('data-source');
            upload_url =  $(this).attr('data-upload');
            target = $(this).attr('data-target');
            uploader_selector = '#file-uploader';
            $this = this;
            $(target)
                .load(url, new Uploader(uploader_selector, upload_url, csrf, function (id, orig_filename, data) {
                    if (data.success) {
                        onUploadComplete($this, data);
                    } else {
                        onUploadFail($this, data);
                    }
                }), function () {
                    if (onUploadFail !== 'undefined') {
                        onUploadFail($this);
                    }
                });
        });
    };

}(jQuery));
