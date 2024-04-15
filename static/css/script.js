// function exibirPopup(id) {
//     var popup = document.getElementById("popup_" + id);
//     if (popup){
//     popup.style.display = "block";


    // }    
// }

function fecharPopup(id) {
    var popup = document.getElementById("popup_" + id);
    popup.style.display = "none";
}


document.querySelectorAll('.image-container img').forEach(function (img) {
    img.addEventListener('click', function () {
        var id = this.parentElement.dataset.id;
        exibirPopup(id);
    });
});
function exibirPopup(id) {
    var popup = document.getElementById("popup_" + id);

    
    if (popup.style.display === "block") {
        popup.style.display = "none";
    } else {
        popup.style.display = "block";
    }
}


document.getElementById('remember-checkbox').addEventListener('change', function() {
    if (this.checked) {
        var remember = confirm("Deseja lembrar suas informações de login?");
        if (remember) {
            // Enviar uma solicitação para a rota /remember_me no servidor
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/remember_me', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        var response = JSON.parse(xhr.responseText);
                        if (response.status === 'success') {
                            console.log('Informações de login lembradas:');
                            console.log('Usuário:', response.username);
                            console.log('Senha:', response.password1);
                        } else {
                            console.error('Erro ao lembrar informações de login:', response.message);
                        }
                    } else {
                        console.error('Erro ao lembrar informações de login.');
                    }
                }
            };
            xhr.send('remember=true');
        }
    }
});
