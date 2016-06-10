var m = require('mithril');
var $osf = require('js/osfHelpers');
var waterbutler =  require('js/waterbutler');
var AddProject = require('js/addProjectPlugin');


require('css/dropzone-plugin.css');
require('css/quick-project-search-plugin.css');
require('loaders.css/loaders.min.css');
var Dropzone = require('dropzone');

// Don't show dropped content if user drags outside dropzone
window.ondragover = function(e) { e.preventDefault(); };
window.ondrop = function(e) { e.preventDefault(); };


var xhrconfig = function(xhr) {
    xhr.withCredentials = true;

};

var ShareWindowDropzone = {

  controller: function() {
    Dropzone.options.shareWindowDropzone = {
        // Dropzone is setup to upload multiple files in one request this configuration forces it to do upload file-by-
        //file, one request at a time.
        clickable: '#shareWindowDropzone',
        parallelUploads: 1,
        autoProcessQueue: false,
        withCredentials: true,
        method:'put',
        border: '2px dashed #ccc',
        maxFilesize: 1,

        accept: function(file, done) {
            this.options.url = waterbutler.buildUploadUrl(false,'osfstorage',window.contextVars['shareWindowId'], file,{});
            this.processFile(file);
        },
        sending: function(file, xhr) {
            //Hack to remove webkitheaders
            var _send = xhr.send;
            xhr.send = function() {
               _send.call(xhr, file);
           };
        },
        success: function(file, xhr) {
            this.processQueue();
            file.previewElement.classList.add("dz-success");
        },

        error: function(file, message) {
            file.previewElement.classList.add("dz-error");
        },
    };

    $('#shareWindowDropzone').dropzone({
        url:'placeholder',
        previewTemplate: '<div class="dz-preview dz-processing dz-file-preview"><div class="dz-details"><div class="dz-filename"><span data-dz-name></span></div>' +
        '<div class="dz-size" data-dz-size></div><img data-dz-thumbnail /></div><div class="dz-progress"><span class="dz-upload" data-dz-uploadprogress></span></div>' +
        '<div class="dz-success-mark"><span>✔</span></div><div class="dz-error-mark"><span>✘</span></div><div class="dz-error-message"><span data-dz-errormessage></span></div></div>',
    });



      $('#ShareButton').click(function(e) {
        $('#ShareButton').attr('disabled', 'disabled');
        document.getElementById("ShareButton").style.cursor = "pointer";



         setTimeout(enable, 300);
          $('#shareWindowDropzone').slideToggle();
          $('#LinkToShareFiles').slideToggle();
          $(this).toggleClass('btn-primary');
      });
    function enable () {
        $('#ShareButton').removeAttr('disabled');
    }

  },

  view: function(ctrl, args) {
              function headerTemplate() {
            return [ m('h2.col-xs-4', 'Dashboard'), m('m-b-lg.col-xs-8.pull-right.drop-zone-disp',
                //m('button.btn.btn-primary.m-t-md.f-w-xl.pull-right #ShareButton', {onclick: function() {}}, 'Upload Public Files'),
                m('.pull-right', m('button.btn.btn-primary.m-t-md.f-w-xl #ShareButton', {onclick: function() {}}, 'Upload Public Files'), m.component(AddProject, {
                buttonTemplate : m('button.btn.btn-success.btn-success-high-contrast.m-t-md.f-w-xl.pull-right[data-toggle="modal"][data-target="#addProjectFromHome"]',
                    {onclick: function() {
                    $osf.trackClick('quickSearch', 'add-project', 'open-add-project-modal');
                    }}, 'Create new project'),
                modalID : 'addProjectFromHome',
                stayCallback : function _stayCallback_inPanel() {
                                document.location.reload(true);
                },
                trackingCategory: 'quickSearch',
                trackingAction: 'add-project',
                templatesFetcher: ctrl.templateNodes
            })))];
        }
          return m('.row', m('.col-xs-12', headerTemplate()), m('div.p-v-xs.text-center.drop-zone-format.drop-zone-invis .pointer .panel #shareWindowDropzone',
              m('button.close[aria-label="Close"]',{ onclick : function() {
                  $('#ShareButton').toggleClass('btn-primary');
                  $('#shareWindowDropzone').hide();
                  $('#LinkToShareFiles').hide();
              }}, m('.drop-zone-close','x')),
              m('p#shareWindowDropzone', m('h1.drop-zone-head',  'Drop files to upload'), 'Having trouble? Click anywhere in this box to manually upload a file.')),
              m('.h4.text-center.drop-zone-invis #LinkToShareFiles', 'Or go to your ', m('a', {href: '/share_window/', onclick: function() {}}, 'Public Files Project')));
  }
};

module.exports = ShareWindowDropzone;
