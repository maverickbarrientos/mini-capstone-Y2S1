import { formatDate } from "./formatHelper.js";

export async function update(user) {
  const firstName = document.querySelector("#first-name-input");
  const lastName = document.querySelector("#last-name-input");
  const birthDate = document.querySelector("#birthdate-input");
  const email = document.querySelector("#email-input");
  const phoneNumber = document.querySelector("#phone-number-input");

  firstName.value = user.first_name;
  lastName.value = user.last_name;
  birthDate.value = formatDate(user.birthdate);
  email.value = user.email;
  phoneNumber.value = user.phone_number;

  const editUserForm = document.querySelector("#edit-user-form");

  editUserForm.onsubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData(editUserForm);
    formData.append("id", user.id)

    try {
      const response = await fetch("http://127.0.0.1:5000/admin/edit_user", {
        method: "PUT",
        body: formData
      });

      const data = await response.json();

      console.log(data)

    } catch (Error) {
      console.log(`Error: ${Error}`);
    }
  };
}
