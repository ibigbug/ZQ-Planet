//rewrite setTimeout

var _st = window.setTimeout;
window.setTimeout = function(func, delay){
    if(typeof func == 'function'){
        var args = Array.prototype.slice.call(arguments,2);
        var f = (function(){ func.apply(null,args) ;});
        return _st(f, delay);
    }
    return _st(func,delay);
}

$(document).ready(function(){
    // go top

    $('body').dblclick(function(){$(this).animate({'scrollTop':0});});

    //fetch feed
    $('.feed').click(function(){
        var id = $(this).attr('id').split('-')[1];
        //waterFlow._current = id;
        waterFlow.append(id);
    });

    // footer 
    $('#footer').addClass('show');
    $(window).scroll(function() {
        var wh = $(window).height();
        var dh = $(document).height();
        var fh = $('#footer').height(); var s = $('body').scrollTop();
        if ((s + wh + fh) > dh) {
            $('#footer,.elevator-container').addClass('show');
        } else {
            $('#footer,.elevator-container').removeClass('show');
        }
    });
    
    // init data
    $($('.feed')[0]).click();

});

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var waterFlow = {
    debug: function(e){
        console.log(e);
    },
    //_isFirst: true,
    //_width: 300,
    //_current: null,
    //_loadFinish: false,
    //_index: 0,
    append: function(id){
        //if(this._isFirst){
        $('.container').html('');
        $('.elevator').html('');
        req = $.ajax({
            type: 'POST',
            url: '/',
            data: { 
                    id:id,
                    _xsrf: getCookie('_xsrf'),
                },
            success: function(data){
                //$('.container').data('data',data);
                //waterFlow._index = 0;
                var html = '';
                var elevatorHtml = '';
                for (var j=0;j<data.count;j++){
                    //if(waterFlow._loadFinish) return;
                    //var index = waterFlow._index;
                    html += '<article class="articles" id="index-'+j+'">';
                    html += '<h3><a href="'+data.data[j]['link']+'">'+data.data[j]['title']+'</a></h3>';
                    html += '<div class="meta"><time datetime="'+data.data[j].time+'">'+data.data[j].time+'</time> By '+data.data[j].author+'</div>'
                    html += '<div class=content>'+data.data[j]['content']+'</div>';
                    html += '</article>';
                    elevatorHtml += '<li class="elevator" id="floor-'+j+'"><a href="#index-'+j+'">'+data.data[j]['title']+'</a></li>';
                    //waterFlow._isFirst = false;
                    //waterFlow._index++ ;
                    //if(waterFlow._index>=data.count) waterFlow._loadFinish = true;
                }
                $('.container').append(html);
                $('.elevator').append(elevatorHtml);
            },
        });
        return this;
    },
}
// detect current
window.onscroll = function(){
    var articles = $('.articles');
    var _current = 0;
    for (var j=0;j<articles.length;j++){
        var aT = $(articles[j]).offset().top;
        var wT = $(window).scrollTop();
        if (aT - wT <= -$(articles[j]).height()/2) {
            _current = j + 1;
        }
    }
    $('.elevator').removeClass('ele-current');
    $('#floor-'+_current).addClass('ele-current');
}
