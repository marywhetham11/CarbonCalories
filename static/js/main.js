function switchItem(switchTo) {
    if (switchTo == 'login') {
        document.getElementById('login').style.display = 'block';
        document.getElementById('register').style.display = 'none';
        document.getElementById('login-option').style.backgroundColor = '#E4DBD9';
        document.getElementById('register-option').style.backgroundColor = 'transparent';
    } else {
        document.getElementById('login').style.display = 'none';
        document.getElementById('register').style.display = 'block';
        document.getElementById('login-option').style.backgroundColor = 'transparent';
        document.getElementById('register-option').style.backgroundColor = '#E4DBD9';
    }
}