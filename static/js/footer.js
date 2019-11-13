function footer() {
    var bodyheight = document.getElementById('bodyHeight').clientHeight;
    var inner = window.innerHeight;
    if (inner-250 > bodyheight) {
        document.getElementById('footer').style = "\
        position: absolute;\
        right: 0;\
        bottom: 0;\
        left: 0;\
        padding: 1rem;\
        border-top: 8px solid #003E6D;\
        background-color: #222;\
        text-align: center;\
        height: 10em";
    }

    else {
        document.getElementById('footer').style = "\
        border-top: 8px solid #003E6D;\
        background: #222;\
        height: 10rem;\
        position: relative;\
        width: 100%;\
        margin: 20px 0 0 0;\
        overflow: hidden;";
    }
}

setInterval(footer, 100)