const inputField = document.getElementById('task-input');
const addButton = document.getElementById('add-button');

async function loadTasks() {
    try {
        const response = await fetch('/api/tasks');
        const tasks = await response.json();
        const taskList = document.getElementById('task-list');
        taskList.innerHTML = '';

        tasks.forEach(task => {
            const div = document.createElement('div');
            div.setAttribute('class','task-items');
            const li = document.createElement('li');
            li.textContent = task.name;
            const circle = document.createElement('div');
            circle.setAttribute('id','circle-status');
            div.appendChild(circle);
            div.appendChild(li);
            taskList.appendChild(div);
        });
    } catch (error) {
        console.error('Gagal mengambil tugas: ', error);
    }
}
loadTasks();

async function createNewTask() {
    const url = '/api/tasks'
    const data = {name: inputField.value};

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`)
        }
    } catch (error) {
        console.error('Error create new task: ', error);
    }
    
    loadTasks();
}

addButton.addEventListener('click', createNewTask);