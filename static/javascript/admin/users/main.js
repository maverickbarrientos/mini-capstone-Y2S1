import { fetchUsers } from "../../helper/fetchData.js";

document.addEventListener('DOMContentLoaded', () => {

    localStorage.clear()
    
    fetchUsers();

})