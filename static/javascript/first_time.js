function backToCopy() {
    console.log('hello');
    const buttonElement = document.querySelector('.copy-button');
    if (buttonElement.classList.contains('is-copied')) {
        buttonElement.innerHTML = 'Copy';
        buttonElement.classList.remove('is-copied');
    }
}

function copyOnClick() {
    const buttonElement = document.querySelector('.copy-button');
    console.log(buttonElement);
    if (buttonElement.innerText === 'Copy') {
        console.log(buttonElement.classList);
        const content = document.querySelector('.private-key-paragraph');
        navigator.clipboard.writeText(content.innerHTML);
        buttonElement.innerHTML = 'Copied!';
        buttonElement.classList.add('is-copied');
        console.log('okay fine');
        setTimeout(backToCopy, 3000);
    } else {
        buttonElement.innerHTML = 'Copy';
        buttonElement.classList.remove('is-copied');
    }
}