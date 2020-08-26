const api_url  = '/api/';

function setUserAndAuthToken(usrnm,token){
    localStorage.loggedin_user = usrnm;
    localStorage.auth_token = token;
}

function unsetUserAndAuthToken(){
    localStorage.removeItem('auth_token');
    localStorage.removeItem('loggedin_user');
}

function logout(){
    unsetUserAndAuthToken();
    window.location = '/login/';
}