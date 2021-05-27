//show popup
function showPopup() {
    popupBackground.style.display = 'block';
    // click background to close(addEventListener)
    closePopup(popupBackground);
    // click X to close(addEventListener)
    let closes = document.querySelectorAll('.close');
    closes.forEach(close => {
        closePopup(close);
    })
    loginBlock.style.display = 'flex';
}

//close popup
function closePopup(btn) {
    btn.addEventListener('click', function () {
        popupBackground.style.display = 'none';
        loginBlock.style.display = 'none';
        signupBlock.style.display = 'none';
        clearInputValue();
        removeMessage();
    })
}

//clear value in input when close popup
function clearInputValue() {
    let allInputValue = document.querySelectorAll('.popup input');
    allInputValue.forEach(inputValue => inputValue.value = '');
}

// remove alertMessage above signup btn or login btn
function removeMessage() {
    let idMessage = document.getElementById('message');
    if (idMessage) {
        idMessage.remove();
    }
}

// insert alertMessage above signup btn or login btn
function insertMessage(message, color, block) {
    let alertMessage = document.createElement('p');
    alertMessage.id = 'message';
    alertMessage.textContent = message;
    alertMessage.style.color = color;
    let firstP = block.querySelector('p');
    block.insertBefore(alertMessage, firstP);
}



let signinup = document.querySelector('#signinup');
let popupBackground = document.getElementById('popup-background');
let loginBlock = document.getElementById('login-block');
let signupBlock = document.querySelector('#signup-block');

signinup.addEventListener('click', showPopup);

//if no account, switch
let switchTexts = document.querySelectorAll('.switch');
switchTexts.forEach(switchText => {
    switchText.addEventListener('click', function () {
        if (switchText.innerHTML === '點此註冊') {
            loginBlock.style.display = 'none';
            signupBlock.style.display = 'flex';
        } else {
            loginBlock.style.display = 'flex';
            signupBlock.style.display = 'none';
        }
        clearInputValue();
        removeMessage();
    })
})


// check login status
let userApi = '/api/user';

// get
fetch(userApi)
    .then(jsdata => jsdata.json())
    .then(data => {
        if (data.data !== null) {
            signinup.textContent = '登出系統';
            signinup.removeEventListener('click', showPopup);
            signinup.id = 'logout';
            // delete
            let logout = document.getElementById('logout');
            logout.addEventListener('click', function () {
                fetch(userApi, {
                        method: 'DELETE'
                    }).then(jsdata => jsdata.json())
                    .then(data => {
                        if (data.ok) {
                            window.location.reload();
                        }
                    })
            })
        } else {
            signinup.textContent = '登入/註冊';
        }
    })

// post
let signupBtn = document.getElementById('signup-btn');
signupBtn.addEventListener('click', function () {
    let input = document.querySelectorAll('#signup-block>input');

    // check email
    if (!input[1].value.includes('@')) {
        removeMessage();
        insertMessage('電子郵件須包含@', 'red', signupBlock);
    } else {
        let postData = {
            name: input[0].value,
            email: input[1].value,
            password: input[2].value
        };
        fetch(userApi, {
                body: JSON.stringify(postData),
                method: 'POST',
                headers: {
                    'content-type': 'application/json'
                }
            }).then(res => res.json())
            .then(data => {
                removeMessage();
                if (data.ok) {
                    clearInputValue();
                    insertMessage('註冊成功，重新整理', 'green', signupBlock);
                    setTimeout(() => {
                        window.location.reload()
                    }, 1000);
                } else {
                    insertMessage(data.message, 'red', signupBlock);
                }
            })
    }
})

//patch
let loginBtn = document.getElementById('login-btn');
loginBtn.addEventListener('click', function () {
    let input = document.querySelectorAll('#login-block>input');
    let patchData = {
        email: input[0].value,
        password: input[1].value
    };
    fetch(userApi, {
            method: 'PATCH',
            body: JSON.stringify(patchData),
            headers: {
                'content-type': 'application/json'
            }
        }).then(res => res.json())
        .then(data => {
            removeMessage();
            if (data.ok) {
                insertMessage('登入成功', 'green', loginBlock);
                window.location.reload();

            } else {
                insertMessage(data.message, 'red', loginBlock);
            }
        })
})

// booking
let booking = document.getElementById('booking');
booking.addEventListener('click', function () {
    fetch(userApi).then(res => res.json())
        .then(data => {
            if (data.data === null) {
                //if not login click 登入登出
                signinup.click();
            } else {
                window.location = '/booking';
            }
        })
})