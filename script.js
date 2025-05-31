let count = 0;
let arrwithIdandTop = [];
arrwithIdandTop[count] = [];

function cloneElement(originalElement, workspace) {
  const element = document.getElementById(originalElement);
  //Generation clone of elements
  const clonedElement = document.createElement(element.tagName);
  
  //adding attributes on cloned element (name, value, className, draggable, id, onclick)
  for (let attr of element.attributes) {
    clonedElement.setAttribute(attr.name, attr.value);
  }
  clonedElement.style.cssText = "top: 50px; left: 50px; position:absolute; color:black; font-weight:bold;";
  clonedElement.classList.add("clonedComponent");
  clonedElement.setAttribute("draggable", "true");
  clonedElement.onclick = null;
  
  
  clonedElement.innerHTML = element.innerHTML;
  const work = document.getElementById(workspace);
  let newElement = work.appendChild(clonedElement);

  //Generating new Id for new elements
  const ids = clonedElement.id;
  const newIds = ids + count;
  
  //creating delete button
  const deleteBtn = document.createElement("button");
  deleteBtn.classList.add("delete-btn");
  deleteBtn.innerHTML = `<div id=${newIds} class='material-symbols-outlined close' style='top:-100%; left:-100%;'>remove</div>`;
  deleteBtn.addEventListener("click", function () {
    clonedElement.remove();
  });
  clonedElement.appendChild(deleteBtn);

  console.log(newIds); // printing Ids of cloned element

  //making draggable the cloned element
  function makeDraggable(clonedElement) {
    clonedElement.addEventListener("mousedown", function (e) {
      const rect = clonedElement.getBoundingClientRect();
      const initialX = e.clientX - rect.left / 4;
      const initialY = e.clientY - rect.top / 4;

      const onMouseMove = (event) => {
        clonedElement.style.left = event.clientX - initialX + "px";
        clonedElement.style.top = event.clientY - initialY + "px";
      };

      const onMouseUp = (event) => {
        document.removeEventListener("mousemove", onMouseMove);
        document.removeEventListener("mouseup", onMouseUp);
        clonedElement.style.left = event.clientX;
        clonedElement.style.top = event.clientY;

        const top = parseFloat(clonedElement.style.top);
        const div = clonedElement.querySelector("div");
        const inputElement = clonedElement.querySelector("input");
        let realValue = inputElement ? inputElement.value : "None";
        if (!realValue) {
          realValue = null;
        }

        arrwithIdandTop[count] = [top, div.getAttribute("id"), realValue];
        // console.log(arrwithIdandTop[count]);
      };

      document.addEventListener("mousemove", onMouseMove);
      document.addEventListener("mouseup", onMouseUp);
    });
  }
  makeDraggable(newElement);
  count++;
}

function getSortedClonedElementsWithId(){
  //refined array (removing repeated ids)
  let tempArray = arrwithIdandTop;
  for (let i = arrwithIdandTop.length - 1; i >= 0; i--) {
    for (let j = i - 1; j >= 0; j--){
      if(tempArray[i][1] === undefined)
        tempArray.splice(i, 1)
      else if (tempArray[i][1] === tempArray[j][1]){
        tempArray.splice(j, 1);
        i--;
      }
    }
  }
  arrwithIdandTop = tempArray;//refined array is here

  //sorted array on basice of Top value
  arrwithIdandTop.sort((a, b)=> a[0] - b[0]);

  //removing integer part from Ids
  function removeTrailingDigits(str){
    return str.replace(/\d+$/, '')
  }
  // console.log("after sorting "+arrwithIdandTop)

  for (let i = 0; i < arrwithIdandTop.length; i++){
    if(arrwithIdandTop[i][1]=== undefined)
      continue
    let word = arrwithIdandTop[i][1]; 
    arrwithIdandTop[i][1] = removeTrailingDigits(word);
  }
  // console.log("after removing triling number "+arrwithIdandTop)

  let string;
  for (let i = 0; i < arrwithIdandTop.length; i++){
    string += arrwithIdandTop[i][1] + arrwithIdandTop[i][2];
  }

  // if(string.length >= 1){
  // const massage = document.createElement(div);
  // massage.style.cssText = "background-color:#fd1616; color:black; border:1px solid black; border-radius:10px 0 10px 10px; "
  // massage.innerText = "Code Generated SuccessFully"
  // }

  console.log(string)
  document.getElementById("string").innerText = string;
}