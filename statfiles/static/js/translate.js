// Translation
$(function(){
    console.log('user_preferred_language', user_preferred_language)

    var translated_text = {};
    $('.translateToggle').click(function(){
        console.log(translated_text)
        var trans_class_arr = $(this).data('trans_class').split(',')

        var that = this;
        var status = $(that).data('status');
        console.log('translate status:', status)

        if(status == 'to_translate' || status == 'to_detect'){   //do translate
            updateLinkStatus(that, 'translating')

            translateMulty(trans_class_arr, function(res){
                //success
                $(that).data('original_lang_name', res.original_lang_name);

                if(res.original_lang_code == res.translate_lang){
                    updateLinkStatus(that, 'already_preferred_language')
                }else{
                    updateLinkStatus(that, 'translated_success')
                }
            }, function(original_lang_name){
                //failed
                updateLinkStatus(that, 'translated_failed')
            })
        }else if(status == 'translated_success' || status == 'translated_failed'){   //to show original
            for(var i in trans_class_arr){
                var class_str = trans_class_arr[i]
                $('.'+class_str).text(translated_text[ class_str ].original);
            }
            updateLinkStatus(that, 'to_translate')
        }
    })

    function translateMulty(trans_class_arr, cb_success, cb_failed){
        var success_num = 0;
        var failed_num = 0;
        for(var i in trans_class_arr){
            translate(trans_class_arr[i], function(res){
                if(res.if_success){
                    success_num++
                }else{
                    failed_num++
                }
                if(success_num + failed_num == trans_class_arr.length){
                    if(failed_num == 0){
                        cb_success(res)
                    }else{
                        cb_failed(res)
                    }
                }
            })
        }
    }

    // update the translate link by default
    $('.translateToggle').each(function(){
        var that = this;

        var trans_class_arr = $(this).data('trans_class').split(',')
        original_language = $('.'+trans_class_arr[0]).data('original_language')

        if(!original_language){    //if we don't about the original language
            updateLinkStatus(that, 'to_detect')
        }else{
            if(original_language != user_preferred_language){//if original language not equals the user preferred language
                updateLinkStatus(that, 'to_translate')
            }
        }
    })

    function updateLinkStatus(that, status){
        $(that).data('status', status);
        updateTranslateLinkInfo(that)
    }

    // status: to_detect, to_translate, translating, translated_success, translated_failed, already_preferred_language
    function updateTranslateLinkInfo(that){
        status = $(that).data('status');

        if(status == 'to_detect'){
            $(that).text('文A');
        }
        else if(status == 'to_translate'){
            $(that).text('Translate');
        }
        else if(status == 'translating'){
            $(that).text('Translating...');
        }
        else if(status == 'translated_success'){
            $(that).text('Show original in '+$(that).data('original_lang_name'));
        }
        else if(status == 'translated_failed'){
            $(that).text('Translate failed');
        }
        else if(status == 'already_preferred_language'){
            $(that).text('Already in your preferred language');
            $(that).attr('href', '/user/edit');
        }
        else{
            $(that).text('文A');
        }
    }
    // do translate
    function translate(content_class, cb){
        //if(translated_text[content_class]){
        //    $('.'+content_class).text(translated_text[content_class].translate)
        //    return;
        //}
        var data = {
            content : $('.'+content_class).text(),
            from : $('.'+content_class).data('from'),
            original_language : $('.'+content_class).data('original_language')
        }

        $.post('/core/json/translate', data, function(res){
            translated_text[content_class] = res
            console.log(res)
            $('.'+content_class).text(res.translate)

            cb(res)
        })
    }
})