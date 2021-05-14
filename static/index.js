async function getData(page, keyword) {
    const url = '/api/attractions';
    if (loading == false) {
        // console.log('get data')
        loading = true;
        if (keyword === '') {
            res = await fetch(`${url}?page=${page}`);
        } else {
            res = await fetch(`${url}?page=${page}&keyword=${keyword}`);
        }
        jsonData = await res.json();
        appendContent(jsonData);
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
            let hyperlink = document.createElement('a');
            hyperlink.href = `/attraction/${data.data[i].id}`;
            let imgsrc = document.createElement('img');
            imgsrc.src = data.data[i].images[0];
            hyperlink.appendChild(imgsrc);
            img.appendChild(hyperlink);

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
    nextPage = data.nextPage;
    loading = false;
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

let loading = false;
let nextPage = '0';
let keyword = '';

window.addEventListener('load', function () {
    getData(nextPage, keyword);
})


window.addEventListener('scroll', function () {
    // let cnt = document.getElementById('content');
    // let cntPosition = cnt.getBoundingClientRect();

    // console.log('cntPosition.bottom:', cntPosition.bottom)
    // console.log('window.innerHeight:', window.innerHeight)
    // if (cntPosition.bottom < window.innerHeight) {
    //     if (nextPage != null) {
    //         getData(nextPage, keyword);
    //     }
    // }
    let options = {
        root: null,
        rootMargin: '0px',
        threshold: 0.3
    }
    let callback = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                getData(nextPage, keyword);
            }
        })
    }
    let observer = new IntersectionObserver(callback, options);
    let footer = document.querySelector('footer');
    observer.observe(footer);
})

//click to search
let searchIcon = document.getElementById('search-icon');
searchIcon.addEventListener('click', function () {
    removeContent();
    nextPage = '0';
    keyword = document.getElementById('spot-name-search').value;
    // console.log(keyword);
    getData(nextPage, keyword);
})


//tab enter to search
let inpSearch = document.getElementById('spot-name-search');
inpSearch.addEventListener('keyup', function (event) {
    if (event.keyCode === 13) {
        searchIcon.click();
    }
})