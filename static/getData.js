async function getData(page, keyword) {
    const url = '/api/attractions';
    if (load == false) {
        // console.log('get data')
        if (keyword === '') {
            res = await fetch(`${url}?page=${page}`);
        } else {
            res = await fetch(`${url}?page=${page}&keyword=${keyword}`);
        }
        jsonData = await res.json();
        appendContent(jsonData);
        nextPage = jsonData.nextPage;
    } else {
        return;
    }
}

function appendContent(data) {
    let content = document.getElementById('content');
    if (data.data.length === 0) {
        let noResultTag = document.createElement('p');
        let noResultText = document.createTextNode('查無此結果');
        noResultTag.appendChild(noResultText);
        content.appendChild(noResultTag);
    } else {
        for (let i = 0; i < data.data.length; i++) {
            // .card>{.img>img}+{.card-info>.card-name+mrt+category}
            let card = document.createElement('div');
            card.className = 'card';

            // .img>img
            let img = document.createElement('div');
            img.className = 'img';
            let imgsrc = document.createElement('img');
            imgsrc.src = data.data[i].images[0];
            img.appendChild(imgsrc);

            // .card-info>.card-name+mrt+category
            let cardInfo = document.createElement('div');
            cardInfo.className = 'card-info';

            let cardName = document.createElement('div');
            cardName.className = 'card-name';
            let name = document.createTextNode(data.data[i].name);
            cardName.appendChild(name);

            let cardMrt = document.createElement('div');
            cardMrt.className = 'mrt';
            if (data.data[i].mrt !== null) {
                mrt = document.createTextNode(data.data[i].mrt);
            } else {
                mrt = document.createTextNode('其他');

            }

            cardMrt.appendChild(mrt);

            let cardCategory = document.createElement('div');
            cardCategory.className = 'category';
            let category = document.createTextNode(data.data[i].category);
            cardCategory.append(category);

            cardInfo.appendChild(cardName);
            cardInfo.appendChild(cardMrt);
            cardInfo.appendChild(cardCategory);

            card.appendChild(img);
            card.appendChild(cardInfo);
            content.appendChild(card);
        }
    }
    setTimeout(() => {
        load = false;
        // console.log(load)
    }, 2000);
}

function removeContent() {
    let container = document.querySelectorAll('.container')[2]
    let content = document.getElementById('content');
    content.remove();
    let cnt = document.createElement('div');
    cnt.className = 'width';
    cnt.id = 'content';
    container.appendChild(cnt);
}

let load = false;
let nextPage = '0';
let keyword = '';
window.addEventListener('load', function () {
    getData(nextPage, keyword);
})


window.addEventListener('scroll', function () {
    let cnt = document.getElementById('content');
    let cntPosition = cnt.getBoundingClientRect();

    setTimeout(() => {
        if (cntPosition.bottom < window.innerHeight) {
            if (nextPage != null) {
                getData(nextPage, keyword);
            }
            load = true;
            // console.log(load)
        }
    }, 2000);
})

let searchIcon = document.getElementById('search-icon');
searchIcon.addEventListener('click', function () {
    removeContent();
    nextPage = '0';
    keyword = document.getElementById('spot-name-search').value;
    // console.log(keyword);
    getData(nextPage, keyword);
})

let inpSearch = document.getElementById('spot-name-search');
inpSearch.addEventListener('keyup', function (event) {
    if (event.keyCode === 13) {
        searchIcon.click();
    }
})