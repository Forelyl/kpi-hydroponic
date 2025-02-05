const html = document.querySelector('html');

window.addEventListener("load", (event) => {
    const body = document.querySelector('body');
    setTimeout(() => {
        body.style.visibility = 'visible';
    }, 200);

});

/*
const html = document.querySelector('html');

const loader = document.createElement('loader-screen');
html.appendChild(loader);
html.style.overflow = 'hidden';

window.addEventListener("load", (event) => {
    const body = document.querySelector('body');
    setTimeout(() => {
        body.style.visibility = 'visible';
        loader.remove();
        html.style.overflowX = 'none';
        html.style.overflowY = 'auto';
    }, 200);

});
*/