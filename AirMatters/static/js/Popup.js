/**
 * Created by Administrator on 2017/5/28.
 */
function login(){
    //document.getElementById("LoginHref").onclick = showMinLogin;
    showMinLogin();
    document.getElementById("close_minilogin").onclick = closeLogin;
    document.getElementById("cancelLogin").onclick = closeLogin;
    /* 显示登录窗口 */
    function showMinLogin(){
        var mini_login = document.getElementsByClassName("mini_login")[0];
        var cover = document.getElementsByClassName("cover")[0];
        mini_login.style.display = "block";
        cover.style.display = "block";

        mini_login.style.left = (window.screen.availWidth- mini_login.scrollWidth) / 2 + "px";
        mini_login.style.top = (window.screen.availHeight-mini_login.scrollHeight) / 2 + "px";
        cover.style.position = "fixed";
    }

    /* 关闭登录窗口 */
    function closeLogin(){
        var mini_login = document.getElementsByClassName("mini_login")[0];
        var cover = document.getElementsByClassName("cover")[0];
        mini_login.style.display = "none";
        cover.style.display = "none";
    }

}

function register(){
    // document.getElementById("RegisterHref").onclick = showMinRegister;
    showMinRegister();
    document.getElementById("close_miniregister").onclick = closeRegister;
     document.getElementById("cancelRegister").onclick = closeRegister;
    /* 显示注册窗口 */
    function showMinRegister(){
        var mini_register= document.getElementsByClassName("mini_register")[0];
        var cover = document.getElementsByClassName("cover")[0];
        mini_register.style.display = "block";
        cover.style.display = "block";

        mini_register.style.left = (window.screen.availWidth - mini_register.scrollWidth) / 2 + "px";
        mini_register.style.top = (window.screen.availHeight - mini_register.scrollHeight) / 2 + "px";
        cover.style.position = "fixed";
    }

    /* 关闭注册窗口 */
    function closeRegister(){
        var mini_register = document.getElementsByClassName("mini_register")[0];
        var cover = document.getElementsByClassName("cover")[0];
        mini_register.style.display = "none";
        cover.style.display = "none";
    }

}