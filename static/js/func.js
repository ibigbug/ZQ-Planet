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
    //toggle sidebar
    $('.sidebar-toggle').click(function(){
        $('body').toggleClass('expanded');
        $('.cell').toggle();
        window._st(resize,500);
    });

    //fetch feed
    $('.feed').click(function(){
        var id = $(this).attr('id').split('-')[1];
        waterFlow._current = id;
        waterFlow.init(id);
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
    $($('.feed')[0]).click();

});

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function resize(){
    $('.container').fadeOut(300).html('').fadeIn(400);
    waterFlow._loadFinish = false;
    waterFlow.detect().create().initAppend(waterFlow._current).onscroll();
}

var waterFlow = {
    debug: function(e){
        console.log(e);
    },
    _isFirst: true,
    _width: 300,
    _current: null,
    _loadFinish: false,
    _index: 0,
    reset: function(){
        $('.container').data('data','');
        this._isFirst = true;
        this._loadFinish = false;
        this._index = 0;
        return this;
    },
    detect: function(){
        this._index= 0,
        this._loadFinish = false;
        var containerWidth = $(window).width()-$('.container').offset().left;
        this.columnNum = parseInt(containerWidth/this._width);
        return this;
    },
    create: function(){
        $('.container').html('');
        var columnNum = this.columnNum;
        columnHtml = '';
        for(var i=0;i<columnNum;i++){
            columnHtml += '<div class="column" id="column-'+i+'"></div>';
        }
        $('.container').append(columnHtml);
        return this;
    },
    initAppend: function(id){
        if(this._isFirst){
            req = $.ajax({
                type: 'POST',
                url: '/',
                data: { 
                        id:id,
                        _xsrf: getCookie('_xsrf'),
                    },
                success: function(data){
                    $('.container').data('data',data);
                    for(var i=0; i<waterFlow.columnNum;i++){
                        for (var j=0;j<2;j++){
                            if(waterFlow._loadFinish) return;
                            var index = waterFlow._index;
                            var html = '';
                            html += '<article id="index-'+index+'">';
                            html += '<h3><a href="'+data.data[index]['link']+'">'+data.data[index]['title']+'</a></h3>';
                            html += '<div class="meta"><time datetime="'+data.data[index].time+'">'+data.data[index].time+'</time> By '+data.data[index].author+'</div>'
                            html += '<div class="content">'+data.data[index].content+'</div>'
                            html += '</aticle>';
                            html += '</div>';
                            $('#column-'+i).append(html);
                            waterFlow._isFirst = false;
                            waterFlow._index++ ;
                            if(waterFlow._index>=data.count) waterFlow._loadFinish = true;
                        }
                    }
                },
            });
        }
        else{
            for(var i=0; i<waterFlow.columnNum;i++){
                data = $('.container').data('data');
                var index = waterFlow._index;
                var html = '';
                html += '<article id="index-'+index+'">';
                html += '<h3><a href="'+data.data[i]['link']+'">'+data.data[i]['title']+'</a></h3>';
                html += '<div class="meta"><time datetime="'+data.data[i].time+'">'+data.data[i].time+'</time> By '+data.data[i].author+'</div>'
                html += '<div class="content">'+data.data[i].content+'</div>'
                html += '</aticle>';
                html += '</div>';
                $('#column-'+i).append(html);
                waterFlow._index++ ;
                if(waterFlow._index>=data.count) waterFlow._loadFinish = true;
            }
        }
        return this;
    },
    buildHtml: function(){
        if(!this._loadFinish&&!this._isFirst){
            var data = $('.container').data('data');
            var html = '';
            html += '<article id="index-'+this._index+'">';
            html += '<h3><a href="'+data.data[this._index]['link']+'">'+data.data[this._index]['title']+'</a></h3>';
            html += '<div class="meta"><time datetime="'+data.data[this._index].time+'">'+data.data[this._index].time+'</time> By '+data.data[this._index].author+'</div>'
            html += '<div class="content">'+data.data[this._index].content+'</div>'
            html += '</aticle>';
            html += '</div>';
            return html;
        }
        else return false;
    },
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
    },
    init: function(id){
        this.reset().detect().create().initAppend(id).onscroll();
    },
}
