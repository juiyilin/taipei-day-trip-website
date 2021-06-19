let content = document.querySelector('.content');
init();

function init() {
    fetch('/api/user').then(res => res.json())
        .then(data => {
            // console.log(data.data)
            if (data.data === null) {
                window.location = '/';
            } else {
                let username = document.querySelector('#username');
                username.textContent = data.data.name;
                content.appendChild(document.createElement('br'));
                getOrders(data.data);
            }
        })
}

function getOrders(user) {
    fetch('/api/order').then(res => res.json())
        .then(data => {
            // console.log(data.data)
            if (data.data.length == 0) {
                //no order
                let noOrder = document.createElement('p')
                noOrder.textContent = '沒有訂購紀錄'
                content.appendChild(document.createElement('br'));
                content.appendChild(noOrder);
            } else {
                renderOrders(data.data);
            }
        })
}

function renderOrders(dataArray) {
    // console.log(dataArray)
    let table = document.createElement('div');
    table.id = 'table';
    content.appendChild(table);
    //head
    let tableHead = document.createElement('div');
    tableHead.id = 'table-head';
    table.appendChild(tableHead);
    let headArray = ['訂單號碼', '行程日期', '景點', '價格', '狀態']
    headArray.forEach(head => {
        let div = document.createElement('div');
        div.textContent = head;
        tableHead.appendChild(div);
    })

    //body
    dataArray.forEach(data => {
        let tableRow = document.createElement('div');
        tableRow.className = 'table-row'

        let number = document.createElement('div');
        // number.textContent = data.number;
        number.className = 'number';
        let link = document.createElement('a');
        link.href = '/order/' + data.number;
        link.textContent = data.number
        number.appendChild(link);

        let date = document.createElement('div');
        date.textContent = data.date;
        date.className = 'date';

        let name = document.createElement('div');
        name.textContent = data.trip;
        name.className = 'name';

        let price = document.createElement('div');
        price.textContent = data.price;
        price.className = 'price';

        let status = document.createElement('div');
        if (data.status == 0) {
            status.textContent = '已付款';
            status.style.color = 'green';
        } else {
            status.textContent = '未付款';
            status.style.color = 'red';
        }
        status.className = 'status';

        let columns = [number, date, name, price, status]
        columns.forEach(col => {
            tableRow.appendChild(col)
        })
        table.appendChild(tableRow)
    })

}