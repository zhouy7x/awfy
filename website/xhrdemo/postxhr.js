function postxhr(addr, data) {
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            console.log(xmlhttp.responseText);
        }
    }

    var res = encodeURIComponent(data);

    xmlhttp.open("POST", addr, true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send("result=" + res);
}
