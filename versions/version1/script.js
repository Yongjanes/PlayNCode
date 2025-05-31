function cloneElement(originalElement, workspace) {
    const element = document.getElementById(originalElement);
    const clonedElement = document.createElement(element.tagName);

    for (let attr of element.attributes) {
        clonedElement.setAttribute(attr.name, attr.value, attr.style = "top: 50px; left: 50px; position:absolute;");
        clonedElement.setAttribute("draggable","true");
        clonedElement.onclick = null
    }

    clonedElement.innerHTML = element.innerHTML;
    const work = document.getElementById(workspace);
    let newElement = work.appendChild(clonedElement);

    const deleteBtn = document.createElement('button');
    deleteBtn.classList.add('delete-btn');
    deleteBtn.innerHTML = "<div id='close' class='material-symbols-outlined'>close</div>";
    deleteBtn.addEventListener('click', function () {
        clonedElement.remove();
    });
    clonedElement.appendChild(deleteBtn);
    // return clonedElement;


    function makeDraggable(clonedElement) {
        clonedElement.addEventListener('mousedown', function (e) {
            const rect = clonedElement.getBoundingClientRect();
            const offsetX = e.clientX - rect.left;
            const offsetY = e.clientY - rect.top;

            function onMouseMove(event) {
                clonedElement.style.left = event.pageX - offsetX + 'px';
                clonedElement.style.top = event.pageY - offsetY + 'px';
            }

            function onMouseUp() {
                document.removeEventListener('mousemove', onMouseMove);
                document.removeEventListener('mouseup', onMouseUp);
            }

            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
        });
    }
    makeDraggable(newElement);
}