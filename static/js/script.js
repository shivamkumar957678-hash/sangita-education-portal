// ==========================
// Sangita Education Portal
// script.js
// ==========================

// Welcome Message

window.onload = function () {

    console.log("Sangita Education Portal Loaded");

};


// Dark Mode Toggle

function toggleDarkMode() {

    document.body.classList.toggle("dark-mode");

}


// Registration Success Alert

function registrationSuccess() {

    alert("Registration Submitted Successfully!");

}


// Certificate Verify Alert

function verifyCertificate() {

    let certId = document.getElementById("certificate_id");

    if (certId && certId.value === "") {

        alert("Please Enter Certificate ID");

        return false;

    }

    return true;

}


// Contact Form Alert

function contactSuccess() {

    alert("Message Sent Successfully!");

}


// Search Student

function searchStudent() {

    let input = document.getElementById("searchInput");

    if (input) {

        let filter = input.value.toUpperCase();

        let table = document.getElementById("studentTable");

        let tr = table.getElementsByTagName("tr");

        for (let i = 0; i < tr.length; i++) {

            let td = tr[i].getElementsByTagName("td")[1];

            if (td) {

                let txtValue = td.textContent || td.innerText;

                tr[i].style.display =
                    txtValue.toUpperCase().indexOf(filter) > -1
                        ? ""
                        : "none";

            }

        }

    }

}


// Live Date

function showDate() {

    let today = new Date();

    let date =
        today.getDate() +
        "/" +
        (today.getMonth() + 1) +
        "/" +
        today.getFullYear();

    let element = document.getElementById("todayDate");

    if (element) {

        element.innerHTML = date;

    }

}

showDate();