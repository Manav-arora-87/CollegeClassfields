console.log("hello world")

const socket = io('http://localhost:8000')

const username = document.getElementById('username').innerText
console.log(username)
const alertBox = document.getElementById('alert-box')
const messagesBox = document.getElementById('messages-box')
const messageInput = document.getElementById('message-input')
const sendBtn = document.getElementById('send-btn')


// socket.on('Welcome',msg=>{
//     console.log(msg)
// })

const handleAlerts = (msg,type) =>{
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
        ${msg}
        </div>
    `
    setTimeout(()=>{
        alertBox.innerHTML = ""
    },5000)
}

socket.on('Welcome2',msg=>{
    // console.log(msg)
    handleAlerts(msg,'primary')
})


socket.on('byebye',msg=>{
    console.log(msg)
    handleAlerts(msg,'danger')
})

sendBtn.addEventListener('click',()=>{
    var   message = username+`<br>`+messageInput.value
    messageInput.value = ""
    console.log(message)

    socket.emit('message',message)


    
})


socket.on('messageToClients',msg=>{
    console.log(msg.split('<br>'))
    temp=msg.split('<br>')[0]
    if(temp==username){
        messagesBox.innerHTML+=`
        <li class="clearfix">
            <div class="message other-message float-right">${msg}</div>
        </li> 
        
        `
    }
    else{
        messagesBox.innerHTML+=`
        <li class="clearfix">
            <div class="message other-message float-left">${msg}</div>
        </li> 
        
        `
    }
})