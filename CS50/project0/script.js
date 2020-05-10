const classNames = {
	TODO_ITEM: 'todo-container',
	TODO_CHECKBOX: 'todo-checkbox',
	TODO_TEXT: 'todo-text',
	TODO_DELETE: 'todo-delete',
}

const list = document.getElementById('todo-list')
const itemCountSpan = document.getElementById('item-count')
const uncheckedCountSpan = document.getElementById('unchecked-count')

let todoId = 0

function newTodo() {
	todo = prompt("What's your TODO", "Empty TODO")

	const newLi = document.createElement("li")
	const newDelete = document.createElement("button")

	newLi.setAttribute("id", todoId)
	newLi.appendChild(document.createTextNode(todo))
	newDelete.appendChild(document.createTextNode("delete"))

	todoId++

	newLi.appendChild(newDelete)
	list.appendChild(newLi)
	newDelete.setAttribute("onClick", deleteTodo(todoId-1))
}

function deleteTodo(elementIndex) {
	console.log(elementIndex)
	console.log(list.childNodes[elementIndex])
	list.removeChild(list.childNodes[elementIndex])
}
