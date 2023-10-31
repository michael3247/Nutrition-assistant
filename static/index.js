document.getElementById("close").addEventListener("click", close);
function close(){
    document.getElementsByClassName("drop-menu")[0].setAttribute("style","display:none;");
    document.getElementsByClassName("menu")[0].setAttribute("style","display:block;");
}

document.getElementById("menu").addEventListener("click", open);
function open(){
    document.getElementsByClassName("drop-menu")[0].setAttribute("style","display:block;");
    document.getElementsByClassName("menu")[0].setAttribute("style","display:none;");
}

/*intro animation */
const down = document.querySelectorAll('.intro');
const fall = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry);
        if (entry.isIntersecting) {
            // Find child elements of the intersected element and add the class to them
            const childElements = entry.target.querySelectorAll('.move');
            childElements.forEach(function (childElement) {
                childElement.classList.add('return');
            });
        } else {
            // Find child elements of the intersected element and remove the class from them
            const childElements = entry.target.querySelectorAll('.move');
            childElements.forEach(function (childElement) {
                childElement.classList.remove('return');
            });
        }
    });
},
{
    threshold: 0.2,
});

down.forEach(el => fall.observe(el));


window.addEventListener("resize", redo);
function redo(){
    if (window.innerWidth > 1089){
        document.getElementsByClassName("drop-menu")[0].setAttribute("style", "display:none;");
        document.getElementsByClassName("menu")[0].setAttribute("style", "display:none;");
    }
    if (window.innerWidth < 1089){
        document.getElementsByClassName("menu")[0].setAttribute("style", "display:block;");
    }


}




const back = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting) {
            entry.target.classList.add('return2');
        } else {
            entry.target.classList.remove('return2');
        }
    });
});
const slide = document.querySelectorAll('.about');
slide.forEach((el) => back.observe(el));

//animations for the features

const ani = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting) {
            entry.target.classList.add('reverse');
        } else {
            entry.target.classList.remove('reverse');
        }
    });
},
{
    threshold: 0,
});
const push = document.querySelectorAll('.cont-a1');
push.forEach((el) => ani.observe(el));


const ani2 = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting) {
            entry.target.classList.add('reverse2');
        } else {
            entry.target.classList.remove('reverse2');
        }
    });
},
{
    threshold: 0,
});
const push2 = document.querySelectorAll('.cont-a2');
push2.forEach((el) => ani2.observe(el));

const ani3 = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting) {
            entry.target.classList.add('reverse3');
        } else {
            entry.target.classList.remove('reverse3');
        }
    });
},
{
    threshold: 0,
});
const push3 = document.querySelectorAll('.cont-a3');
push3.forEach((el) => ani3.observe(el));


const elementsWithID = document.querySelectorAll('[id^="signup"]');
    elementsWithID.forEach(element => {
        element.addEventListener("click", go);
        function go(){
            window.location.replace("/signup")
        }
    });
document.getElementById("ab").addEventListener("click", ab);
function ab(){
    window.location.replace("/#about")
}
