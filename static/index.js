const test_ip = "http://127.0.0.1:8000/things/"

    async function get_things(endpoint){
        const response = await fetch(endpoint, {
            method: "GET"
        })
        .then((res) => {
            if(res.ok){
                console.log(res)
                return JSON.stringify(res)
            }else{
                console.error("[ERROR] something is not working")
            }
        }).then((data) => {
            console.log(data)
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

        console.log(thing.map())
            document.getElementById("app").innerHTML = 
            `
            
            `
    }

  get_things(test_ip)
    
