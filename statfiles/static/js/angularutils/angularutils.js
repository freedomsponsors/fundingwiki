angular.module('angularutils', ['ngSanitize']);
angular.module('angularutils').value('editToggle', editToggle);
angular.module('angularutils').filter('markdownit', function() {
    return function(s) {
        s = s || '';
        var md = window.markdownit({
                  html: false, // Disabled for security issues, see documentation
                  linkify: true,
                  typographer: true
                })
        md.use(window.markdownitTaskLists)
        md.use(window.markdownitHashtag)
        md.use(window.markdownitUsername)
        md.use(window.markdownitSolution)
        md.use(window.markdownitProject)
        md.renderer.rules.table_open = function(tokens, idx) {
              return '<table class="table">';
        };
        return md.render(s);
    };
});
angular.module('angularutils').directive('mediaForm', function() {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            media:'=',
            issue:'=',
            csrf: '=',
            // notnew is used to modify the form to show only the parts that you can edit on a already created media
            notnew: '@'
        },
        templateUrl: '/static/js/angularutils/media-form-template.html',
        controller: function ($scope) {
          if ($scope.media === undefined) {
            $scope.media = {}
          }
        }
    }
});
angular.module('angularutils').directive('deleteButton', function() {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            action:'@',
        },
        template: '<a ng-click="execute(action)" style="color:red;" ><i class="fa fa-trash" aria-hidden="true"></i></a>',
        controller: function ($scope) {
            $scope.execute = function(url){
                $.ajax({
                    url: $scope.action,
                    type: 'DELETE',
                    success: function(result){
                        location.reload();
                    },
                    error: function(e){
                        alert("Error deleting")
                        console.log(e)
                    }
                });
            }
        }
    }
});
angular.module('angularutils').directive('markdownText', function(markdownitFilter) {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            text:'@',
        },
        template: '<span ng-bind-html-unsafe="text|markdownit"></span>'
    }
});
angular.module('angularutils').directive('textWithMarkdownPreview', function(markdownitFilter) {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            model:'=',
            nameid:'@',
            placeholder:'@',
            value: '@',
            required: '@',
            dirclass: '@',
            disable:'='
        },
        templateUrl: '/static/js/angularutils/textarea-and-markdownpreview.html',
        controller: function ($scope) {

            if ($scope.model !== undefined && $scope.model.disable) {
                $scope.disable = $scope.model.disable
            }

            if ($scope.required === undefined) {
                $scope.required = false;
            }

            if ($scope.value !== undefined) {
                $scope.model = $scope.value
            }
            $scope.markdown = function(s){
                if (s !== undefined ) {
                    var html = markdownitFilter(s)
                    return html;
                }
            }
        }
    }
});

angular.module('angularutils').directive('watchIssue', function() {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            watchLink: '@',
            issueId: '@',
            watching: '='
        },
        templateUrl: '/static/js/angularutils/watch-issue.html',
        controller: function ($scope) {
            $scope.action = function(){
                return $scope.watching ? 'unwatch' : 'watch';
            };

            $scope.toggle = function(){
                if($scope.watchLink){
                    return;
                }
                var url = '/core/' + $scope.action() + '/issue/'+$scope.issueId;
                $scope.loading = true;
                $.get(url).success(function(data){
                    if(data == 'WATCHING'){
                        $scope.watching = true;
                    } else if (data == 'NOT_WATCHING'){
                        $scope.watching = false;
                    } else {
                        alert('unrecognized watch response: '+data);
                    }
                    $scope.loading = false;
                    $scope.$digest();
                })
            };
        }
    }
});

angular.module('angularutils').directive('multilineEllipsis', function () {
    return {
        restrict: 'A',
        link: function (scope, element, attr) {
            var $container = $(element).find('.ellipsis');
            var divh = $(element).height();
            setTimeout(function(){
                while ($container.outerHeight() > divh) {
                    $container.text(function (index, text) {
                        if(text.length > 400){
                            text = text.substring(0, 400);
                        }
                        var result = text.replace(/\W*\s(\S)*$/, '...');
                        if (result == text){
                            result = text.substring(0, text.length - 4)+'...';
                        }
                        return result;
                    });
                }
            }, 0);

        }
    };
});

angular.module('angularutils').directive('sortHeader', function () {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            label: '@',
            property: '@'
        },
        templateUrl: '/static/js/angularutils/sortHeader.html',
        controller: function ($scope, SortHeaderModel) {
            $scope.m = SortHeaderModel;
            $scope.toggle = function(){
                SortHeaderModel.toggle($scope.property);
            };
        }
    };
});


angular.module('angularutils').factory('SortHeaderModel', function (){
    var self = {
        property: null,
        asc: true
    };
    self.toggle = function(property){
        if(self.property == property){
            self.asc = !self.asc;
        } else {
            self.property = property;
        }
        if(self.onchange){
            self.onchange(self.property, self.asc);
        }
    };
    self.init = function(property, asc){
        self.property = property;
        self.asc = asc;
    };
    return self;
});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
