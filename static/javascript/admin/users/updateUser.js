import { update } from "../../helper/update.js";

document.addEventListener('DOMContentLoaded', () => {

    const storedUser = JSON.parse(localStorage.getItem("storedUser"));
    if (storedUser) {
        update(storedUser);
    }

});