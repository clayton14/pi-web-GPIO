async function update_things(){
    return null;
}

async function create_thing(){
    return null;
}

async function remove_thing(){
    return null;
}

async function update_status(){
    return null;
}

async function get_things(endpoint){
    let response = await fetch(endpoint);
    let data = await response.json();
    return data;
}


function build_html(){
    

}

console.log(get_things("http://claypower.local:8000/"))