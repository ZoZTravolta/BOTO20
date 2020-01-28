


const sendMessageToServer = async (userMessage, type) => {
  const url = 'https://boto20.herokuapp.com/message/?message=';

  const url_local = '/message/?message=';
  const todoEndpoint = '/todo/?message=';

  document.getElementById('userInput').value = '';

  const sendMessage = async () => {
    console.log(type)
    try {
      if (type == "todo") {
        return await axios.get(todoEndpoint + userMessage)
      }
      else {
        return await axios.get(url_local + userMessage + '&type=' + type) //
      }


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

document.getElementById('userInput').addEventListener('keyup', (e) => {
  if (e.keyCode == 13) {
    const userMessage = document.getElementById('userInput').value;
    const type = document.getElementById('selectType').value
    sendMessageToServer(userMessage, type)
  }
})
