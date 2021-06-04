TPDirect.setupSDK(20393, 'app_2z7jr1mUqiV83zVnB0YGFIBD39oZqpzYaBTB5Gk8RMcJmn4X8JJF71Wyw7d9', 'sandbox');
TPDirect.card.setup({
    fields: {
        number: {
            // css selector
            element: select('#card-number'),
            placeholder: '**** **** **** ****'
        },
        expirationDate: {
            // DOM object
            element: select('#card-expiration-date'),
            placeholder: 'MM / YY'
        },
        ccv: {
            element: select('#card-ccv'),
            placeholder: 'ccv'
        }
    },
    styles: {
        // Style all elements
        'input': {
            'color': 'gray'
        },
        // Styling ccv field
        'input.ccv': {
            'font-size': '16px'
        },
        // Styling expiration-date field
        'input.expiration-date': {
            'font-size': '16px'
        },
        // Styling card-number field
        'input.card-number': {
            'font-size': '16px'
        },
        // style focus state
        ':focus': {
            'color': 'black'
        },
        // style valid state
        '.valid': {
            'color': 'green'
        },
        // style invalid state
        '.invalid': {
            'color': 'red'
        },
        // Media queries
        // Note that these apply to the iframe, not the root window.
        '@media screen and (max-width: 400px)': {
            'input': {
                'color': 'orange'
            }
        }
    }
})
const btn = document.querySelector('#btn');
btn.addEventListener('click', function () {
    // console.log(TPDirect.card.getTappayFieldsStatus())
    // 確認填寫狀況
    let phoneValue = document.getElementById('phone').value;
    if (TPDirect.card.getTappayFieldsStatus().canGetPrime && phoneValue.slice(0, 2) === '09' && phoneValue.length === 10) {
        TPDirect.card.getPrime((result) => {
            // console.log('result', result)
            if (result.status !== 0) {
                alert('get prime error ' + result.msg)
                return
            }

            // 將prime相關資料post到後端，讓後端與TapPay 的Pay by Prime API 進行交易
            let order = {
                "prime": result.card.prime,
                "order": {
                    "price": bookdata.price,
                    "trip": {
                        "attraction": {
                            "id": bookdata.attraction.id,
                            "name": bookdata.attraction.name,
                            "address": bookdata.attraction.address,
                            "image": bookdata.attraction.image
                        },
                        "date": bookdata.date,
                        "time": bookdata.time
                    },
                    "contact": {
                        "name": account.name,
                        "email": account.email,
                        "phone": phoneValue
                    }
                }
            };
            // console.log('order', order)
            fetch('/api/orders', {
                    method: 'POST',
                    body: JSON.stringify(order),
                    headers: {
                        'content-type': 'application/json'
                    }
                }).then(res => res.json())
                .then(data => {
                    // console.log(data)
                    if (data.data.payment.status === 0) {
                        window.location = `/thankyou?number=${data.data.number}`;
                    } else {
                        alert(`付款失敗\n錯誤代號：${data.data.payment.status}\n錯誤訊息：${data.data.payment.message}`);
                    }
                })
        })
    } else {
        alert('請確認每個欄位是否填寫正確');

    }

})