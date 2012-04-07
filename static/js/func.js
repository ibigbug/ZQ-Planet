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

    //toggle sidebar
    $('.sidebar-toggle').click(function(){
        $('body').toggleClass('expanded');
        $('.cell').toggle();
        window._st(resize,500);
    });

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
        var fh = $('#footer').height();
        var s = $('body').scrollTop();
        if ((s + wh + fh) > dh) {
            $('#footer').addClass('show');
        } else {
            $('#footer').removeClass('show');
        }
    });
    
    // init data
    href = window.location.href;
    if (href.indexOf('#')!=-1){
        hash = href.split('#')[1];
        $($('#feed-'+hash)).click();
    }
    else {
        $($('.feed')[0]).click();
    };

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
                    for (var j=0;j<data.count;j++){
                        //if(waterFlow._loadFinish) return;
                        //var index = waterFlow._index;
                        html += '<article id="index-'+j+'">';
                        html += '<h3><a href="'+data.data[j]['link']+'">'+data.data[j]['title']+'</a></h3>';
                        html += '<div class="meta"><time datetime="'+data.data[j].time+'">'+data.data[j].time+'</time> By '+data.data[j].author+'</div>'
                        html += '<div class=content>'+data.data[j]['content']+'</div>';
                        html += '</article>';
                        //waterFlow._isFirst = false;
                        //waterFlow._index++ ;
                        //if(waterFlow._index>=data.count) waterFlow._loadFinish = true;
                    }
                    $('.container').append(html);
                },
            });
        //}
        /*
        else{
            for (var j=0;j<5;j++){
                for(var i=0; i<waterFlow.columnNum;i++){
                    data = $('.container').data('data');
                    var index = waterFlow._index;
                    var html = '';
                    html += '<article id="index-'+index+'">';
                    html += '<h3><a href="/view/'+data.data[index]['id']+'">'+data.data[index]['title']+'</a></h3>';
                    html += '<div class="meta"><time datetime="'+data.data[index].time+'">'+data.data[index].time+'</time> By '+data.data[index].author+'</div>'
                    html += '<div class=content>'+subString(data.data[index]['content'],random(300))+'</content>';
                    html += '</aticle>';
                    html += '</div>';
                    waterFlow._index++ ;
                    $('#column-'+i).append(html);
                }
                if(waterFlow._index>=data.count) waterFlow._loadFinish = true;
            }
        }*/
        return this;
    },
    /*
    onscroll: function(){
        window.onscroll = function(){
            var st = $('body').scrollTop();
            if(!this._loadFinish){
                var columns = $('.column');
                var _sT = $('body').scrollTop();
                for(var i=0;i<columns.length;i++){
                    _eleTop = $(columns[i]).offset().top;
                    _eleHeight = $(columns[i]).height();
                    eleBottom = _eleTop + _eleHeight - _sT ;
                    if($(window).height()-eleBottom>0){
                        var html = waterFlow.buildHtml();
                        $('#column-'+i).append(html);
                        $('#index-'+waterFlow._index).hide().fadeIn(400);
                        waterFlow._index +=1;
                        if(waterFlow._index>=$('.container').data('data').count) waterFlow._loadFinish = true;
                    }
                }
            }
        }
        return this;
    },*/
}
