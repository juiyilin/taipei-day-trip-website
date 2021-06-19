function select(dom) {
    const result = document.querySelector(dom);
    return result
}

function appendContents(data) {
    //spot-img
    select('#spot-img').src = data.trip.attraction.image;
    //number
    select('#number').textContent = data.number;
    //status
    if (data.status == 0) {
        select('#status').textContent = '已付款';
    } else {
        select('#status').textContent = '未付款';
    }
    //name
    select('#name').textContent = data.trip.attraction.name;
    //date
    select('#date').textContent = data.trip.date;
    //time
    if (data.time === 'morning') {
        select('#time').textContent = '早上 9 點到下午 4 點';
    } else {
        select('#time').textContent = '下午 2 點到晚上 9 點';
    }
    //amount
    let amounts = document.querySelectorAll('.amount');
    amounts.forEach(amount => amount.textContent = data.price);
    //address
    select('#address').textContent = data.trip.attraction.address;
    select('#info').href = `/attraction/${data.trip.attraction.id}`;
}

fetch('/api/user').then(res => res.json())
    .then(data => {
        if (data.data === null) {
            window.location = '/';
        } else {

            fetch('/api' + window.location.pathname).then(res => res.json())
                .then(data => {
                    // console.log(data.data)
                    appendContents(data.data);
                })
        }
    })