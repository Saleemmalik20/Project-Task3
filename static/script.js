const API = "http://127.0.0.1:5000/api/students";

const form = document.getElementById("studentForm");
const tableBody = document.getElementById("studentTableBody");

async function fetchStudents() {

    const res = await fetch(API);

    const students = await res.json();

    renderStudents(students);

    updateStats(students);
}

function renderStudents(students) {

    tableBody.innerHTML = "";

    students.forEach(student => {

        tableBody.innerHTML += `
            <tr>
                <td>${student.full_name}</td>
                <td>${student.email}</td>
                <td>${student.phone}</td>
                <td>${student.course}</td>
                <td>${student.enrolled_on}</td>
                <td class="actions">

                    <button onclick="editStudent(${student.id},
                    '${student.full_name}',
                    '${student.email}',
                    '${student.phone}',
                    '${student.course}')">
                    Edit
                    </button>

                    <button class="delete-btn"
                    onclick="deleteStudent(${student.id})">
                    Delete
                    </button>

                </td>
            </tr>
        `;
    });
}

function updateStats(students) {

    document.getElementById("totalStudents").textContent =
        students.length;

    const pythonStudents =
        students.filter(s => s.course.toLowerCase() === "python");

    const javaStudents =
        students.filter(s => s.course.toLowerCase() === "java");

    document.getElementById("pythonCount").textContent =
        pythonStudents.length;

    document.getElementById("javaCount").textContent =
        javaStudents.length;
}

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const id = document.getElementById("studentId").value;

    const student = {
        full_name: document.getElementById("full_name").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value,
        course: document.getElementById("course").value
    };

    let url = API;
    let method = "POST";

    if (id) {
        url = `${API}/${id}`;
        method = "PUT";
    }

    await fetch(url, {
        method,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(student)
    });

    form.reset();

    document.getElementById("studentId").value = "";

    fetchStudents();
});

function editStudent(id, name, email, phone, course) {

    document.getElementById("studentId").value = id;
    document.getElementById("full_name").value = name;
    document.getElementById("email").value = email;
    document.getElementById("phone").value = phone;
    document.getElementById("course").value = course;
}

async function deleteStudent(id) {

    const confirmDelete =
        confirm("Are you sure you want to delete this student?");

    if (!confirmDelete) return;

    await fetch(`${API}/${id}`, {
        method: "DELETE"
    });

    fetchStudents();
}

document.getElementById("searchInput")
.addEventListener("keyup", async (e) => {

    const query = e.target.value;

    const res = await fetch(
        `/api/students/search?q=${query}`
    );

    const students = await res.json();

    renderStudents(students);
});

fetchStudents();

