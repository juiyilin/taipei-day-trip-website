function select(dom) {
    const result = document.querySelector(dom);
    return result
}

function removeAllContent() {
    contents.forEach(content => content.parentElement.remove())
}

function createNoBookingContent() {
    let body = select('body');

    // .container
    let container = document.createElement('div');
    container.className = 'container';

    //.content
    let content = document.createElement('div');
    content.className = 'content';

    //h3 
    let h3 = document.createElement('h3');
    h3.textContent = `您好，${account.name}，待預定的行程如下： `;

    let noBooking = document.createElement('p');
    noBooking.textContent = '目前沒有任何待預定的行程';
    content.appendChild(h3);
    content.appendChild(document.createElement('br'));
    content.appendChild(noBooking);
    container.appendChild(content);
    body.insertBefore(container, select('#popup-background'));
}

function appendContents(bookData) {
    // console.log(bookData);
    //spot-img
    select('#spot-img').src = bookData.attraction.image;
    //name
    select('#name').textContent = bookData.attraction.name;
    //date
    select('#date').textContent = bookData.date;
    //time
    if (bookData.time === 'morning') {
        select('#time').textContent = '早上 9 點到下午 4 點';
    } else {
        select('#time').textContent = '下午 2 點到晚上 9 點';
    }
    //amount
    let amounts = document.querySelectorAll('.amount');
    amounts.forEach(amount => amount.textContent = bookData.price);
    //address
    select('#address').textContent = bookData.attraction.address;
    showContents();
    trashcan();
}

function showContents() {
    contents.forEach(content => {
        if (contents[3] === content) {
            content.style.display = 'flex';
        } else {
            content.style.display = 'block';
        }
    })
}

function trashcan() {
    let trashcan = select('#delete');
    trashcan.addEventListener('click', function () {
        fetch('api/booking', {
                method: 'DELETE',
            }).then(res => res.json())
            .then(data => {
                if (data.ok) {
                    // console.log(data)
                    window.location.reload();
                }
            })
    })

}





let contents = document.querySelectorAll('.content');
contents.forEach(content => content.style.display = 'none');
let account;
let bookdata;
fetch('api/user').then(res => res.json())
    .then(data => {
        if (data.data === null) {
            window.location = '/';
        } else {
            let username = select('#username');
            username.textContent = data.data.name;
            let contactName = select('#contact-name');
            contactName.value = data.data.name;
            let email = select('#email');
            email.value = data.data.email;
            account = {
                name: data.data.name,
                email: data.data.email
            };
            fetch('/api/booking').then(res => res.json())
                .then(data => {
                    if (data.data === null) {
                        removeAllContent();
                        createNoBookingContent();

                    } else {
                        appendContents(data.data);
                        bookdata = data.data
                    }

                })
        }
    })