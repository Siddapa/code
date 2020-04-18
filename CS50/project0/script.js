const classNames = {
	TODO_ITEM: 'todo-container',
	TODO_CHECKBOX: 'todo-checkbox',
	TODO_TEXT: 'todo-text',
	TODO_DELETE: 'todo-delete',
}

const list = document.getElementById('todo-list')
const itemCountSpan = document.getElementById('item-count')
const uncheckedCountSpan = document.getElementById('unchecked-count')

let itemCountTimes = 0
let uncheckedCountTimes = 0

function newTodo() {
	todo = prompt("What's your TODO", "Empty TODO")

	itemCountTimes++
	uncheckedCountTimes++
	uncheckedCountSpan.innerHTML = uncheckedCountTimes
	itemCountSpan.innerHTML = itemCountTimes

	let newli = document.createElement("li")
	newli.appendChild(document.createTextNode(todo))
	list.appendChild(newli)
}
