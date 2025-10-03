const newUserForm = document.querySelector("#new-user-form");

newUserForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const firstName = document.querySelector("#first-name-input").value;
    const lastName = document.querySelector("#last-name-input").value;
    const birthDate = document.querySelector("#birthdate-input").value;
    const email = document.querySelector("#email-input").value;
    const phoneNumber = document.querySelector("#phone-number-input").value;
    const password = document.querySelector("#password-input").value;

    const formData = new FormData();
    formData.append("first_name", firstName);
    formData.append("last_name", lastName);
    formData.append("birthdate", birthDate);
    formData.append("email", email);
    formData.append("phone_number", phoneNumber);
    formData.append("password", password);

    
    try {
        const response = await fetch("http://127.0.0.1:5000/admin/add_user", { 
            method: "POST",
            body: formData
        });

        const data = await response.json()
        
        console.log(data)

        window.location.href = "/admin/admin_dashboard"
    }

    catch (Error) {
        console.log(`Error : ${Error}`)
    }
}); 