export async function deleteUser(user) {

    const userId = user.id

    try {
        const response = await fetch("http://127.0.0.1:5000/admin/delete_user", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({id : userId})
        });
        
        const data = await response.json()

        console.log(data)

    } catch (Error) {
        console.log(`Front end error : ${Error}`)
    }

}