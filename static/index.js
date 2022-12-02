let test_ip = "http://127.0.0.1:8000/things/"
    async function get_things(endpoint){
        let response = await fetch(endpoint, {
            method: "GET"
        })
        .then(res => {
            if(res.ok){
                return res.json()
            }else{
                console.error("[ERROR] something is not working")
            }
        })
        .then(json => {
            return json
        })
        
        // let data = await response.json();
        // return data;
    }


    async function update_things(endpoint, thing_name, new_pin){
        let response = await fetch(endpoint, {
            method: "PUT",
            body: JSON.stringify({
                
            })
        })
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

    

    function build_html(){
        let things = get_things(test_ip)
        console.log(typeof things)
        document.getElementById("app").innerHTML = 
        `
        <p>${things}</p>
        `

    }
    build_html()
    console.log(get_things(test_ip))
    
