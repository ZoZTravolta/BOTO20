


const sendMessageToServer = async (userMessage, type) => {

  const sendMessage = async () => {
    try {
      return await axios.get('http://localhost:7000/message/?message=' + userMessage + '&type=' + type) // 
    } catch (error) {
      console.error(error)
    }
  }


  const request = await sendMessage()

  if (request.data.message) {
    document.getElementById('botoPic').setAttribute('src', './static/images/' + request.data.anim)
    var node = document.createElement("p");
    var textnode = document.createTextNode(request.data.message);
    node.appendChild(textnode);
    document.getElementById("responseText").prepend(node);
  }
}



document.getElementById('btnSubmit').addEventListener('click', () => {
  const userMessage = document.getElementById('userInput').value;
  const type = document.getElementById('selectType').value

  sendMessageToServer(userMessage, type)
})

