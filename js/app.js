// Cache jQuery references
var $gallery = null;

var onDocumentReady = function() {
  // jQuery references
  $gallery = $('.gallery');

  // Initialize
  $gallery.flickity({
    "pageDots": false,
    "accessibility": true
  }).focus();
}

$(document).ready(onDocumentReady);
