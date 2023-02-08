let navBar = document.getElementById('nav');

const red = () => {
    navBar.removeAttribute('class');
    navBar.setAttribute('class', 'navbar navbar-expand-sm bg-danger navbar-dark')
}

const blue = () => {
    navBar.removeAttribute('class');
    navBar.setAttribute('class', 'navbar navbar-expand-sm bg-primary navbar-dark')
}

const yellow = () => {
    navBar.removeAttribute('class');
    navBar.setAttribute('class', 'navbar navbar-expand-sm bg-warning navbar-dark')
}

const cyan = () => {
    navBar.removeAttribute('class');
    navBar.setAttribute('class', 'navbar navbar-expand-sm bg-info navbar-dark')
}

const gray = () => {
    navBar.removeAttribute('class');
    navBar.setAttribute('class', 'navbar navbar-expand-sm bg-secondary navbar-dark')
}