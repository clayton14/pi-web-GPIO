async function get_things(endpoint){
    let responce = await fetch(endpoint);
    let data = await responce.json();
    return data;
}

const body = document.body
body.append(get_things())


console.log(get_things("http://claypower.local:8000/"))