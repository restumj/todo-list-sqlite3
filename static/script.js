const inputField = document.getElementById('task-input');
const addButton = document.getElementById('add-btn');

async function loadTasks() {
    try {
        const response = await fetch('/api/tasks');
        const tasks = await response.json();
        const task_list = document.getElementById('task-list');
        task_list.innerHTML = '';

        tasks.forEach(task => {
            const task_item = document.createElement('div');
            const task_left = document.createElement('div');
            const task_right = document.createElement('div');
            const li = document.createElement('li');
            const task_status = document.createElement('div');
            const delete_btn = document.createElement('button');
            
            // task_left
            li.textContent = task.name;
            task_status.setAttribute('class','task-status');
            task_left.setAttribute('class','task-left');
            task_left.appendChild(task_status);
            task_left.appendChild(li);

            // task_right
            delete_btn.setAttribute('type','button');
            delete_btn.setAttribute('class','delete-btn');
            delete_btn.textContent = 'Delete';
            
            delete_btn.addEventListener('click', async () => {
                await deleteTask(task.id);
            });

            task_right.setAttribute('class','task-right');
            task_right.appendChild(delete_btn);


            // wrap up task_left & task_right
            task_item.setAttribute('class','task-item');
            task_item.dataset.id = task.id;
            task_item.appendChild(task_left);
            task_item.appendChild(task_right);

            // main
            task_list.appendChild(task_item);
        });
    } catch (error) {
        console.error('Failed load tasks: ', error);
    }
}
loadTasks();

addButton.addEventListener('click', async () => {
    if ((inputField.value).trim() == '') {
        alert('Task name can\'t be empty!');
    } else {
        const url = '/api/tasks';
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
            
            loadTasks();
        } catch (error) {
            console.error('Error create new task: ', error);
        }
    }
    inputField.value = '';
});

// delete task
async function deleteTask(taskId) {
    const url = `/api/tasks/${taskId}`;
    
    try {
        const response = await fetch(url, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`)
        }
        
        loadTasks();
    } catch (error) {
        console.error('Error delete task: ', error);
    }
}