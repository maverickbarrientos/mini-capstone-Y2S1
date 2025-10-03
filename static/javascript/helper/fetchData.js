import { update } from "./update.js"
import { formatDate } from "./formatHelper.js"
import { deleteUser } from '../admin/users/deleteUser.js'

export async function fetchUsers() {
    try {
        const response = await fetch("http://127.0.0.1:5000/admin/fetch_users")
        const data = await response.json()
        
        if (data.length != 0) {
            renderUsers(data)
        } else {
            console.log("No users yet!")
            // put here td with text "no users yet!"
        }

    } catch (Error) {
        console.trace(Error);
        console.log(`Error : ${Error}`);
    }
}

const renderUsers = (users) => {
    
    const tableBody = document.querySelector("tbody");
    tableBody.innerHTML = "";
    users.forEach((user) => {
        const row = `
            <tr>
                <td>${user.first_name} ${user.last_name}</td>
                <td>${formatDate(user.birthdate)}</td>
                <td>${user.email}</td>
                <td>${user.phone_number}</td>
                <td>
                    <button class="edit-btn" value="${user.id}">Edit</button>
                    <button class="delete-btn" value="${user.id}">Delete</button>
                </td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });

    const editButtons = document.querySelectorAll(".edit-btn");
    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach((button) => {

        button.addEventListener('click', () => {

            const userId = button.value;
            const user = users.find(u => u.id == userId)

            deleteUser(user)

        });

    });

    editButtons.forEach(button => {
        
        button.addEventListener('click', () => {

            const userId = button.value;
            console.log(userId)
            const user = users.find(u => u.id == userId)
            
            localStorage.setItem("storedUser", JSON.stringify(user))

            window.location.href = "/admin/edit"

        });
    });
}

