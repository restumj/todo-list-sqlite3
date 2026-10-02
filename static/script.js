const inputField = document.getElementById('task-input');
const addButton = document.getElementById('add-button');

async function loadTasks() {
    try {
        const response = await fetch('/api/tasks');
        const tasks = await response.json();
        const taskList = document.getElementById('task-list');
        taskList.innerHTML = '';

        tasks.forEach(task => {
            const li = document.createElement('li');
            li.textContent = task.name;
            li.setAttribute('class','items');
            taskList.appendChild(li);
        });
    } catch (error) {
        console.error('Gagal mengambil tugas: ', error);
    }
}

loadTasks();

addButton.addEventListener('click', async function () {

});