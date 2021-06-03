function select(dom) {
    const result = document.querySelector(dom);
    return result
}

function init() {
    let api = '/api';
    let path = window.location.pathname;
    let imgs;
    getDataById(api + path);
    return imgs
}

async function getDataById(url) {
    let res = await fetch(url);
    let jsonData = await res.json();
    render(jsonData);
    book();
}

function render(data) {
    // console.log(data)
    // <img>
    imgs = data.data.images;
    let image = select('img');
    image.src = imgs[0];
    imgDot(0);


    // id="name"
    let name = select('#name');
    name.textContent = data.data.name;

    // id="category-mrt"
    let categoryMrt = select('#category-mrt');
    if (data.data.mrt !== null) {
        categoryMrt.textContent = `${data.data.category} at ${data.data.mrt}`;
    } else {
        categoryMrt.textContent = `${data.data.category}`;
    }

    // id="infors"
    let infors = document.querySelectorAll('#infors>p');
    infors[0].textContent = data.data.description;
    infors[1].textContent = data.data.address;
    infors[2].textContent = data.data.transport;
}

function imgDot(now) {
    let total = select('#total-img');
    total.innerHTML = '';
    for (let i = 0; i < imgs.length; i++) {
        let dot = document.createElement('div');
        if (i === now) {
            dot.className = 'show';
        } else {
            dot.className = 'none';
        }
        total.appendChild(dot);
    }
}

function changeImage(id) {
    let image = select('img');
    let nowIdx = imgs.indexOf(image.src);
    if (id === 'next-img') {
        if (nowIdx + 1 == imgs.length) {
            nowIdx = -1;
        }
        image.src = imgs[nowIdx + 1];
        imgDot(nowIdx + 1);

    } else {
        if (nowIdx - 1 < 0) {
            nowIdx = imgs.length;
        }
        image.src = imgs[nowIdx - 1];
        imgDot(nowIdx - 1);
    }

}

function showAmount() {
    let label = document.querySelectorAll('label');
    for (let i = 0; i < label.length; i++) {
        let input = label[i].querySelector('input');
        input.addEventListener('click', () => {
            if (input.checked) {
                let amount = select('#amount');
                if (input.value === 'morning') {
                    amount.textContent = '新台幣2000元';
                } else {
                    amount.textContent = '新台幣2500元';
                }
            }
        })
    }
}

function clickChangeImg(domId) {
    domId.addEventListener('click', () => {
        changeImage(domId.id);
        // clearInterval(slideImg);
        // slideImg = setInterval(() => {
        //     let image = select('img');
        //     if (image.complete) {
        //         changeImage(nextImg.id);
        //     }
        // }, 2000);
    });
}

function book() {
    let bookingBtn = select('#booking-btn');
    let bookingForm = select('#booking-form');

    bookingForm.addEventListener('submit', function (event) {
        event.preventDefault();
        // check login
        fetch('/api/user').then(res => res.json())
            .then(data => {
                if (data.data === null) {
                    signinup.click();
                } else {
                    let input = document.querySelectorAll('#booking-form input');

                    // check if current date > input date
                    let bookingMessage = select('#booking-message');
                    bookingMessage.textContent = '';
                    let now = new Date(Date.now())
                    let inputDate = new Date(input[0].value)
                    // get current year, month, date
                    let currentDate = new Date(now.getFullYear(), now.getMonth(), now.getDate())
                    inputDate = new Date(inputDate.getFullYear(), inputDate.getMonth(), inputDate.getDate())

                    if (currentDate >= inputDate) {
                        bookingMessage.textContent = '請選擇大於今天的日期';
                        bookingMessage.style.color = 'red';
                    } else {
                        // post booking data
                        let time;
                        input.forEach(i => {
                            if (i.checked) {
                                time = i.value;
                            }
                        })

                        let postBookingData = {
                            attractionId: parseInt(window.location.pathname.split('/')[2], 10),
                            date: input[0].value,
                            time: time,
                            price: parseInt(select('#amount').textContent.slice(3, 7), 10)
                        };
                        fetch('/api/booking', {
                                body: JSON.stringify(postBookingData),
                                method: 'POST',
                                headers: {
                                    'content-type': 'application/json'
                                }
                            }).then(res => res.json())
                            .then(data => {
                                if (data.ok) {
                                    window.location = '/booking';
                                    // console.log(data)
                                }
                            })
                    }
                }
            })
    })
}
// load data
imgs = init();

// change image
let lastImg = select('#last-img');
let nextImg = select('#next-img');
clickChangeImg(lastImg);
clickChangeImg(nextImg);



// let slideImg = setInterval(() => {
//     let image = select('img');
//     if (image.complete) {
//         changeImage(nextImg.id);
//     }
// }, 2000);



// show amount
showAmount();