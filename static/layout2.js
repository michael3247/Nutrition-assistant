document.getElementsByClassName("caret")[0].addEventListener("click", open);
const tag = document.getElementsByClassName("links")[0];
const prop = document.getElementsByClassName("caret")[0];
function open(){
    if(tag.style.height == "0px"){
        tag.style.height = "auto";
        prop.style.transform = "rotateX(0deg)";
    }
    else{
        tag.style.height = "0px";
        prop.style.transform = "rotateX(180deg)";
    }
}
let element = document.getElementsByClassName("links")

const profile = document.querySelectorAll('[id^="profile"]');
    profile.forEach(element => {
        element.addEventListener("click", go);
        function go(){
            window.location.replace("/profile")
        }
    });

const logout = document.querySelectorAll('[id^="logout"]');
    logout.forEach(element => {
        element.addEventListener("click", go);
        function go(){
            window.location.replace("/logout")
        }
    });

const me = document.querySelectorAll('[id^="me"]');
    me.forEach(element => {
        element.addEventListener("click", go);
        function go(){
            window.location.replace("/me")
        }
    });


const del = document.querySelectorAll('[id^="delete"]');
    del.forEach(element => {
        element.addEventListener("click", go);
        function go(){
            if (window.confirm("Do you really want to delete your account")) {
                document.getElementById("postForm").submit();
            }
        }
    });



document.getElementById("tracker").addEventListener("click", track)
function track(){
    window.location.replace("/track")
}
document.getElementById("search").addEventListener("click", search)
function search(){
    window.location.replace("/search")
}
document.getElementById("meal").addEventListener("click", meal)
function meal(){
    window.location.replace("/meal")
}

