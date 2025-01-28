function fs_timeout_async_result(result){
    var callback = undefined;
    var r = {
        onResult: function(cb){
            callback = cb;
        }
    };
    setTimeout(function(){
        callback(result)
    }, 1000);
    return r;
}


function fs_ajax_async_result(func, url, params){
    var r = {
        onResult: function(callback){
            r.callback = callback;
            return r;
        },
        onError: function(errorcallback){
            r.errorcallback = errorcallback;
            return r;
        }
    };
    func(url, params)
        .success(function(result){
            if (r.callback) {
                if(result){
                    try {
                        result = JSON.parse(result);
                    } catch(err){}
                }
                r.callback(result)
            }
        })
        .error(function(e){
            if (r.errorcallback) {
                r.errorcallback(e)
            }            
        });
    return r;
}

function get4Sponsors(issue){
    var empties = [];
    for(var i=0; i<4 - issue.four_sponsors.length; i++){
        empties.push({empty:true});
    }
    return empties.concat(issue.four_sponsors)
}

// TODO: Use this function to open close all edit forms on the page
// On first position
// objectOne : object to be opened
// objecTwo : the object to be closed
var editToggle = function (objectOne, objectTwo) {
    extendedEditToggle($(objectOne), $(objectTwo))
}
// If one of the objects has hidden attribute toggle between them with sildeup/down function
function extendedEditToggle (objectOne, objectTwo) {
    if (objectOne.css('display') == 'none') {
        objectOne.slideDown();
        objectTwo.slideUp();
    } else {
        objectOne.slideUp();
        objectTwo.slideDown();
    }
}
