export async function fetchPlants() {

    try {
        const response = await fetch("http://127.0.0.1:5000/admin/fetch_plants");
        const data = await response.json();

        console.log(data)

    } catch (Error) {
        console.log(`Front end Error : ${Error}`)
    }

}

// const renderPlants = (plants) => {

//     plants.forEach((plant) => {

//         const row = `<tr>
//             <td>${plant.plant_code}</td>
//             <td>${plant.plant_name}</td>
//             <td>${plant.description}</td>
//             <td>${plant.soil_type}</td>
//             <td>${plant.optimal_water_amount}</td>
//             <td>${plant.soil_min_moisture} - ${plant.soil_max_moisture}</td>
//             <td>${plant.ideal_min_temp} - ${plant.ideal_max_temp}</td>
//         </tr>`

//     });

// }