function encrypt(passw, open_key, n){
    let message         = passw.split("");
    let encrypt_message = [];

    for (let char of message){
        encrypt_message.push((BigInt(char.charCodeAt(0)) ** BigInt(open_key)) % BigInt(n));
    }
    console.log(message, encrypt_message);
    return encrypt_message.join("O")
}

$(document).ready(function() {

});